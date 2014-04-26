#!/usr/bin/perl

use strict;
use IO::File;
use File::Basename;
use Getopt::Std;

my %opts;

getopt('p', \%opts);

my $opt_p = $opts{'p'} ? $opts{'p'} : 'all';

{

  &usage("No input files.") unless (scalar (@ARGV) == 2);
  &usage("undefined $opt_p option for -p switch.") unless ($opt_p =~ /^(all|n|v)/);

  my $train_key_file = shift @ARGV;
  my $test_key_file = shift @ARGV;

  &usage("Can't open key file $train_key_file") unless (-f $train_key_file);
  &usage("Can't open key file $test_key_file") unless (-f $test_key_file);

  &main($train_key_file, $test_key_file);
}

sub main {

  my ($train_key_file, $test_file, $map_out_dir) = @_;

  my %test;
  my %train;

  &read_cluster_solution($train_key_file, \%train);
  &read_cluster_solution($test_file, \%test);

  my %Sense_solution;

  foreach my $word (keys %train) {

    next if &discard_word($word, $opt_p);

    my @c2s;

    my %sense_freq = &get_gs_senses_freq($train{$word});    # { sense => frequency } (for mfs)

    my %H;
    &update_mfs(\%H, $test{$word}, \%sense_freq);
    $Sense_solution{$word} = \%H;
  }
  &write_sense_solution(\%Sense_solution);
}


sub update_mfs {

  my ($res, $src, $mfs) = @_;

  #get best sense
  my $best_sense;
  my $best_freq = 0;
  foreach my $s (keys %{$mfs}) {
    if ($mfs->{$s} > $best_freq) {
      $best_freq = $mfs->{$s};
      $best_sense = $s;
    }
  }

  foreach my $inst (keys %{$src}) {
    $res->{$inst} = $best_sense;
  }

}


sub get_gs_senses_freq {

  my $gs = shift;

  my %senses;
  my $N = 0;

  foreach my $inst (keys(%{$gs})) {
    my $delta = 1 / scalar(@{$gs->{$inst}});
    foreach my $s (@{$gs->{$inst}}) {
      $senses{$s}+= $delta;
    }
    $N++;
  }
  # Normalize
  foreach my $s (keys %senses) {
    $senses{$s}/= $N;
  }
  return %senses;
}

sub write_sense_solution {

  my ($ssol) = @_;

  my @Sol;

  foreach my $word (keys %{$ssol}) {
    foreach my $inst (keys %{$ssol->{$word}}) {
      push (@Sol, "$word $inst $ssol->{$word}->{$inst}");
    }
  }
  print join("\n", sort @Sol);
  print "\n";
}

sub discard_word {
  my ($word, $pos) = @_;

  return 1 if $pos =~ /^n/ && $word !~ /\.n/;
  return 1 if $pos =~ /^v/ && $word !~ /\.v/;
  return 0;
}

sub read_cluster_solution {

  my ($file, $CSolution) = @_;

  &read_key_file($file, $CSolution);

}

sub read_gold_standard {

  my ($file, $CSolution) = @_;

  &read_key_file($file, $CSolution);
}



{

  my $line_number;

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

    die "Error: $str\nUsage: create_mfs_key.pl [-p all|n|v] train.key test.key\n";
}
