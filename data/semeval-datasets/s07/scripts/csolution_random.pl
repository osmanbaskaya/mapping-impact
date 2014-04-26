#!/usr/bin/perl

use strict;
use IO::File;
use File::Basename;
use Getopt::Std;

my %opts;

getopt('km', \%opts);

my %keys;

&usage("No input files.") unless scalar(@ARGV); 

my $opt_k = $opts{'k'} > 0 ? $opts{'k'} : 0;
my $opt_m = $opts{'m'} > 0 ? $opts{'m'} : 0;

foreach my $file (@ARGV) {
    &read_keyfile($file, \%keys);
}

my @ema;

foreach my $w (keys %keys) {
  &csolution_word($w, $keys{$w}, \@ema);
}

foreach my $ema (sort @ema) {
    print "$ema\n";
}

sub csolution_word {

  my ($word, $instV, $aRef) = @_;

  my @clusters = &generate_random_clusters($word);

  foreach my $inst (@$instV) {
    my $method = &rnumber(1,3);
    $method = $opt_m if $opt_m;
    $method = 1 if scalar @clusters == 1;
    my @C;
    if($method == 1) {
      @C = &cmethod1(\@clusters);
    } elsif ($method == 2) {
      @C = &cmethod2(\@clusters);
    } elsif ($method == 3) {
      @C = &cmethod3(\@clusters);
    }
    my $ema = sprintf "%s %s %s", $word, $inst, join(" ", @C);
    push (@$aRef, $ema);
  }
}

sub generate_random_clusters {
  my $word = shift;

  my $m = &rnumber(1,10); # max 10 hubs

  $m = $opt_k if $opt_k;

  return map { "$word.C$_" } (1..$m);

}


# Generate one cluster randomly:
#
# brother.n 00001 C2

sub cmethod1 {

  my $clusters = shift;

  return $clusters->[&rnumber(0, scalar(@$clusters)-1)];

}

# Generate j (j<=m) clusters randomly:
#
# brother.n 00002 C1 C3

sub cmethod2 {

  my $clusters = shift;

  my $m = scalar(@$clusters) - 1;
  my @v = map {$clusters->[$_]} (0..$m);
  shuffle(\@v);
  my $j = &rnumber(0, $m);
  return @v[0..$j];
}

# Generate j (j<=m) clusters randomly and assign a random possitive weight
# to each one:
#
# brother.n 00006 C0/0.5 C2/0.4 C1/0.1
# brother.n 00015 C4/914 C2/817

sub cmethod3 {

  my $clusters = shift;

  my $m = scalar(@$clusters) - 1;
  my @v = map {$clusters->[$_]} (0..$m);
  shuffle(\@v);
  my $j = &rnumber(0, $m);

  return map {"$_/".(&rnumber(1,10)/3)} @v[0..$j];
}


sub read_keyfile {

  my ($file, $keys) = @_;

  my $fh = IO::File->new($file);
  die "Cant open $file:$!\n" unless defined $fh;

  my $l;
  while ($l = read_line_nospace($fh)) {
    chomp($l);
    my ($w, $id, $senses) = split(/\s+/, $l);
    if (defined($keys->{$w})) {
      push(@{$keys->{$w}}, $id);
    } else {
      $keys->{$w} = [$id];
    }
  }
}

sub read_line_nospace {

  my $fh = shift;
  my $l;

  while($l = <$fh>) {
    last unless ($l =~ /^\s*$/o);
  }
  return $l;
}

sub rnumber {

  my ($min, $max) = @_;

  return int(rand($max-$min+1)) + $min;

}

sub shuffle {
  my $array = shift;
  my $i;
  for ($i = @$array; --$i; ) {
    my $j = int rand ($i+1);
    next if $i == $j;
    @$array[$i,$j] = @$array[$j,$i];
  }
}

sub usage {
  my $str = shift;

  die <<"EOUSG"
  Error: $str\n
  Usage: csolution_random.pl [-k num_of_clusters ] [-m 1,2,3] key_file1 key_file2 ...
       -k number of induced clusters. If not present, number generated randomly (max. 10 clusters)
       -m instance assign method:
          1 assign one cluster randomly
	  2 assign j (j<=k) clusters randomly
	  3 assign j (j<=k) clusters randomly with a random possitive weight
       If only one cluster is induced, assign method is always 1
EOUSG
}
