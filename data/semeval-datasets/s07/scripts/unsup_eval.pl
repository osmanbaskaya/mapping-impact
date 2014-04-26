#!/usr/bin/perl -w
#
# input: 
#        Clustering solution:
#         word instance cluster1[/weight1] cluster2[/weight2] ...
#        Gold Standard:
#         word instance sense1#sense2...
#
# output: given n*(n-1)/2 pairwise combinations of all examples
#         compute for each pair
#         - if the senses are equal and the hubs are equal => OK++
#         - if the senses are different and the hubs are different => OK++
#         - otherwise don't do anything
#         = OK / (n*(n-1)/2)
#

# issues: 1) if the instance has more that one gold standard sense, it
#            is taken as a new sense. That is, two instances in the gold 
#            standard are taken to have the same class if they agree in all senses.
#
#         2) if no clusters are assigned, we assume a NULL cluster
#
# ALDATZEKO:
#    input1: gold standard
#            word instance sense1 sense2 ...
#    input2: result file
#            word instance cluster1/weight1 cluster2/weight2 ...
#
#    pisu maximoa duen clusterra aukeratu
#    bi cluster badaude pisu berarekin: cluster berri bat sortuko dugu 


use strict;
use IO::File;
use File::Basename;
use Getopt::Std;
use Data::Dumper;

my %opts;

getopt('mp', \%opts);

my $opt_v = $opts{'v'} ? 1 : 0;
my $opt_f = $opts{'m'} ? $opts{'m'} : 'fscore' ;
my $opt_p = $opts{'p'} ? $opts{'p'} : 'all';

&usage("No input files.") unless (scalar (@ARGV) > 1);

my $csolution_key_file = shift(@ARGV);
my $gs_key_file = shift(@ARGV);

&usage("Can't open key file $csolution_key_file") unless (-f $csolution_key_file);
&usage("Can't open key file $gs_key_file") unless (-f $gs_key_file);
&usage("undefined $opt_f option ") unless ($opt_f =~ /^(pur|fsc|ent)/);
&usage("undefined $opt_p option ") unless ($opt_p =~ /^(all|n|v)/);

&main();

sub main {

  my %gs;   # Gold standard (test);  ( word => { sense => [exampleId,...] } )
  my %hub;  # Clustering solution    ( word => { cluster => [exampleId,...] } )
  my %hubR; # hub reverse            ( word => { exampleId => [cluster, ... ] } )

  &initialize($csolution_key_file, $gs_key_file, \%gs, \%hub, \%hubR);

  my %measures;

  my $str;

  $str = "FScore" if ($opt_f =~ /^fsc/);
  $str = "Purity" if ($opt_f =~ /^pur/);
  $str = "Entropy" if ($opt_f =~ /^ent/);

  foreach my $word (keys %gs) {
      if ($word eq "hope.v") {
	  my $deb = 0;
      }

    $measures{$word}->{classN} = scalar(keys %{$gs{$word}});   # Number of clases
    $measures{$word}->{clustN} = scalar(keys %{$hub{$word}});  # Numer of clusters
    $measures{$word}->{n} = scalar keys %{ $hubR{$word} };       # Number of instances
    my $n = $measures{$word}->{n};
    my $measure;
    if ($str eq "FScore") {
      $measure = &evaluatefscore($gs{$word},$hub{$word},$hubR{$word}, $n) ;
    } elsif ($str eq "Entropy") {
      $measure = &evaluateentropy($gs{$word},$hub{$word},$hubR{$word}, $n) ;
    } elsif ($str eq "Purity") {
      $measure = &evaluatepurity($gs{$word},$hub{$word},$hubR{$word}, $n) ;
    } else {
      die "$opt_f not implemented yet\n" ;
    }
    $measures{$word}->{res} = $measure; #[$measure, $n];
  }

  # Print output

  &print_figures(\%measures, $str);

}


sub print_figures {

  my ($h, $str) = @_;


  my $N = 0;
  my $tot_ok = 0;
  my $word_count = 0;
  my $clust_n;
  my $class_n;

  printf "%20s%9s%9s%5s%9s\n","word", "clustN", "classN", "N", $str if ($opt_v);
  foreach my $word (sort keys %{ $h }) {
    $word_count++;
    $clust_n += $h->{$word}->{clustN};
    $class_n += $h->{$word}->{classN};
    $tot_ok+= $h->{$word}->{res} * $h->{$word}->{n};
    printf "%20s%9d%9d%5d  %6.3f\n", $word, $h->{$word}->{clustN}, $h->{$word}->{classN}, $h->{$word}->{n}, $h->{$word}->{res} if ($opt_v);
    $N+=$h->{$word}->{n};
  }
  printf "%10s: %5.3f clust_average: %5.3f class_average: %5.3f\n", $str, $tot_ok/$N, $clust_n/$word_count, $class_n/$word_count;

}

sub initialize {

  my ($file_in, $gs_key_file, $gs, $hub, $hubR) = @_;


  my %CSolution;  # Clustering solution ( word => { inst => [cluster] } )
  my %CSol_gs;    # Clustering solution Gold Standard (test) ( word => { inst => [cluster, ... ] } )

  &read_cluster_solution($file_in, \%CSolution);
  &read_gold_standard($gs_key_file, \%CSol_gs);

  foreach my $word (keys %CSol_gs) {

    next if &discard_word($word, $opt_p);

    my %gs_word;
    my %hub_word;
    my %hubR_word;

    foreach my $inst (keys %{$CSol_gs{$word}}) { # Only test instances
      my $cluster = $CSolution{$word}->{$inst}->[0];
      my $sense = $CSol_gs{$word}->{$inst}->[0];

      if (! defined $gs_word{$sense}) {
	$gs_word{$sense} = [$inst];
      } else {
	push @{ $gs_word{$sense} }, $inst;
      }

      if (! defined $hub_word{$cluster}) {
	$hub_word{$cluster} = [$inst];
      } else {
	push @{ $hub_word{$cluster} }, $inst;
      }

      $hubR_word{$inst} = $cluster;
    }
    $gs->{$word} = \%gs_word;
    $hub->{$word} = \%hub_word;
    $hubR->{$word} = \%hubR_word;
  }
}


sub evaluatefscore {
  my ($gs,$hub,$hubR, $n) = @_;
  my $f = 0 ;

  # classes are in gs
  # clusters are in hub and hubR

  # fscore = sum{i=1..c} n_i / n * max_j f(i,j)
  # where:
  # f(class_i,cluster_j) = 2*pr(i,j)*recall(i,j) / (pr(i,j) + recall(i,j))
  # pr(i,j) = n_ij / n_j
  # re(i,j) = n_ij / n_i

  my $fscore = 0 ;
  foreach my $class (keys %$gs) {
    my $classN = scalar @{ $gs->{$class} } ;
    my $maxf = -1 ;
    foreach my $cluster (keys %$hub) {
      my $clusterN = scalar @{ $hub->{$cluster} } ;
      $f = &fmeasure($gs->{$class},$class, $classN, $cluster, $clusterN, $hubR) ;
      $maxf = $f if $f > $maxf ;
    }
    $fscore += ($classN / $n ) * $maxf ;
  }
  return $fscore;
}

sub fmeasure {
  my ($classSET,$classNAME, $classN, $clusterNAME,$clusterN,$clusterR) = @_;

  my $overlap = 0 ;

  foreach my $ex1 (@$classSET) {
    $overlap++ if $clusterR->{$ex1} eq $clusterNAME }
  my $pr = $overlap / $clusterN ;
  my $recall = $overlap / $classN ;
#  printf "\t\t\t\t-- $classNAME $clusterNAME %4.2f %4.2f\n", $pr, $recall  if ($opt_v);
  if ($pr+$recall) {
    return 2*$pr*$recall / ($pr+$recall) ;}
  else {
    return 0 }
}


sub evaluateentropy {
  my ($gs,$hub,$hubR, $n) = @_;
  my $f = 0 ;

  # classes are in gs: i = 1..q 
  # clusters are in hub and hubR: j = 1..r

  # entropy = sum{j=1..r} n_j / n * E (j)
  # where:
  # E(j) = - 1 / log q * sum{i=1..q} n_ij / n_j log ( n_ij / n_j )


  my $entropy = 0 ;
  foreach my $clusterNAME (keys %$hub) {
    my $clusterN = scalar @{ $hub->{$clusterNAME} } ;
    $entropy += ($clusterN / $n) * &entropy($clusterNAME, $clusterN, $gs,$hub, $hubR, $n) ;
  }
  return $entropy;
}

sub entropy {
  my ($clusterNAME, $clusterN, $gs,$hub, $hubR, $n) = @_;

  my $overlap ;
  my $entropy = 0 ;
  return 0 if scalar keys %$gs == 1;
  foreach my $class (keys %$gs) {
      $overlap = scalar ( grep { $hubR->{$_} eq $clusterNAME } @{$gs->{$class}} ) ;
      $entropy +=  ( $overlap / $clusterN ) * log ( $overlap / $clusterN ) if $overlap > 0 ;
  }
#  printf "\t\t\t\t-- $classNAME $clusterNAME %4.2f %4.2f\n", $pr, $recall  if ($opt_v);

  return ( -1 / log (scalar keys %$gs ) ) * $entropy ;
}

sub evaluatepurity {
  my ($gs,$hub,$hubR, $n) = @_;
  my $f = 0 ;

  # classes are in gs: i = 1..q 
  # clusters are in hub and hubR: j = 1..r

  # purity = sum{j=1..r} n_j / n * P (j)
  # where:
  # P(j) = 1 / n_j * max{i=1..q} n_ij 


  my $purity = 0 ;
  foreach my $clusterNAME (keys %$hub) {
    my $clusterN = scalar @{ $hub->{$clusterNAME} } ;
    $purity += ($clusterN / $n) * &purity($clusterNAME, $clusterN, $gs,$hub, $hubR, $n) ;
  }
  return $purity;
}

sub purity {
  my ($clusterNAME, $clusterN, $gs,$hub, $hubR, $n) = @_;

  my $overlap ;
  my $overlapmax = -1 ;
  foreach my $class (keys %$gs) {
      $overlap = scalar ( grep { $hubR->{$_} eq $clusterNAME } @{$gs->{$class}} ) ;
      $overlapmax = $overlap if $overlap > $overlapmax ;
  }
#  printf "\t\t\t\t-- $classNAME $clusterNAME %4.2f %4.2f\n", $pr, $recall  if ($opt_v);

  return ( 1 / $clusterN ) * $overlapmax ;
}


sub discard_word {
  my ($word, $pos) = @_;

  return 1 if $pos =~ /^n/ && $word !~ /\.n/;
  return 1 if $pos =~ /^v/ && $word !~ /\.v/;
  return 0;
}


# Return ( word => { inst => [cluster, ...] } )

sub read_gold_standard {

  my ($file, $CSolution) = @_;

  &read_key_file($file, $CSolution);

}

# Return ( word => { inst => [cluster, ...] } )

sub read_cluster_solution {

  my ($file, $CSolution) = @_;

  my %temp;

  &read_key_file($file, \%temp);
  while (my ($word, $instV) = each %temp) {
    my %word_inst;
    while (my ($inst, $cs) = each %{$instV}) {
      # Select cluster with maximum weight
      # if there is a tie, create a new cluster
      my @selected_clusters;
      my $max_weight = 0;
      foreach my $cw (@{$cs}) {
	my ($cluster, $weight) = split(/\//, $cw);
	$weight = 1 unless defined($weight); # default weigth
	if ($weight > $max_weight) {
	  @selected_clusters = ($cluster);
	  $max_weight = $weight;
	} elsif ($weight == $max_weight) {
	  push (@selected_clusters, $cluster);
	}
      }
      $word_inst{$inst} = [ join(".", @selected_clusters) ];
    }
    $CSolution->{$word} = \%word_inst;
  }
}

{

  my $line_number;

# Return ( word => { inst => [cluster/weight, ... ] } )

  sub read_key_file {

    my ($file, $CSolution) = @_;

    my $fh = IO::File->new($file);
    die "Can't open $file: $!\n" unless defined $fh;
    $line_number = 0;
    my $l;
    while ($l = &read_line_nospace($fh)) {
      chomp($l);
      my @C = split(/\s+/, $l);
      die "Input error in file $file,  line $line_number\nError: too few fields\n" if (scalar(@C) < 3);
      my $word = shift(@C);
      my $inst = shift(@C);
      &remove_comments(\@C);
      # @C now contains the clusters (or senses) assigned to this instance
      die "Input error in file $file,  line $line_number\nError: no labels\n" if (scalar(@C) == 0);
      if (!defined($CSolution->{$word})) {
	# first appearence of the word
	$CSolution->{$word} = {$inst => \@C};
      } else {
	$CSolution->{$word}->{$inst} = \@C;
      }
    }
  }

  sub remove_comments {

    my $v = shift;

    my $m = scalar(@{$v});
    my $i = 0;
    while ($i != $m) {
      if ($v->[$i] eq "!!") {
	splice(@{$v}, $i);
	last;
      }
      $i++;
    }
  }

  sub read_line_nospace {

    my $fh = shift;
    my $l;

    while($l = <$fh>) {
      $line_number++;
      last unless ($l =~ /^\s*$/o);
    }
    return $l;
  }
}

sub usage {
  my $str = shift;

  die <<"EOUSG"
  Error: $str\n
  Usage: unsup_eval.pl [-m (fscore|purity|entropy)] [-v] [-p all|n|v] clust_solution.key gold_standard_test.key
      -m which measure to compute (fscore|purity|entropy). Default is fscore
      -v verbose. Print results per word
      -p filter by part of speech. 'n' takes only nouns into account, 'v' only
         verbs. 'all' doesn't filter anything. Default is 'all'
EOUSG

}
