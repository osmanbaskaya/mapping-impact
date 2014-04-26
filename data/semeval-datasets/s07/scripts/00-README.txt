Scripts used in Semeval 2007 task#2 "Evaluating Word Sense Induction and
Discrimination Systems"

* unsup_eval.pl

This script performs the unsupervised evaluation. It needs two keyfiles: the
system keyfile (train+test) and the gold standard keyfile (test)

  Usage: unsup_eval.pl [-m (fscore|purity|entropy)] [-v] [-p all|n|v] clust_solution.key gold_standard_test.key
      -m which measure to compute (fscore|purity|entropy). Default is fscore
      -v verbose. Print results per word
      -p filter by part of speech. 'n' takes only nouns into account, 'v' only
      verbs. 'all' doesn't filter anything. Default is 'all'


* create_supervised_keyfile.pl

The script creates a (test) supervised keyfile given the system keyfile
(train+test) and the gold standard keyfile (train). The created keyfile is
the system's test part, where the cluster tags are replaced by a sense tag
according to a mapping matrix created over the train part.

  Usage: create_supervised_keyfile.pl [-p all|n|v] [-O map_out_dir] clust_solution.key gold_standard_train.key
      -p filter by part of speech. 'n' takes only nouns into account, 'v' only
         verbs. 'all' doesn't filter anything. Default is 'all'
      -O Temporal directory for leaving the mapping matrix. If option is
         present, the program creates a file per word (extension .c2s) with
         the mapping matrix which maps clusters to senses

* fill_unanswered_instances.pl

The script creates artificial clusters for unanswered instances of the
system. It needs a (incomplete) system keyfile (train+test) and the gold
standard (train+test). All the unanswered instances per word are clustered
to a newly generated dummy cluster.

  usage: fill_unanswered_instances clust_solution.key gold_standard_train_test.key
         Creates artificial clusters for unanswered instances

* sup_eval.sh

Shell script for performing the supervised evaluation.

  Usage: sup_eval.sh system.key outDir [train.key]

First parameter is the system keyfile (train+test) and a directory to let
the generated supervised keyfile. Then the scorer2 program is executed over
the newly generated supervised keyfile.

* scorer2.c

The official lexical sample scorer. Compile it with "gcc -o scorer2 scorer2.c"

* create_mfs_key.pl

Tag all instances of test with most frequent sense of train.

  Usage: create_mfs_key.pl [-p all|n|v] train.key test.key


* csolution_random.pl

Script for generating a randomly produced clustering solution. 

  Usage: csolution_random.pl [-k num_of_clusters ] [-m 1,2,3] key_file1 key_file2 ...
       -k number of induced clusters. If not present, number generated randomly (max. 10 clusters)
       -m instance assign method:
          1 assign one cluster randomly
          2 assign j (j<=k) clusters randomly
          3 assign j (j<=k) clusters randomly with a random possitive weight
       If only one cluster is induced, assign method is always 1
