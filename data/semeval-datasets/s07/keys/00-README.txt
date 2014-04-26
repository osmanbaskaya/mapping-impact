Gold standard and several baselines used in Semeval 2007 task#2
"Evaluating Word Sense Induction and Discrimination Systems"

The key files of the gold standard and several baselines. The format
of all the files is:

name       instanceId   senseId

Files:

senseinduction.key                  The complete gold standard
senseinduction_train.key            The train part
senseinduction_test.key             The test part
senseinduction_test_nouns.key       The test part. Nouns.
senseinduction_test_verbs.key       The test part. Verbs.

baseline/                           Keyfiles for several baselines
baseline/1inst1cluster		    Evary instance is a different cluster
basline/1word1cluster		    All instances in an unique cluster

basline/mfs                         Tag test instances with most frequent 
                                    sense of train

baseline/random			    Induce the clusters and cluster instances
                                    randomly

random_split/                       Train/test random split
random_split/82_18/                 82% train, 18% test
random_split/50_50/                 50% train, 50% test
