
Semeval 2007 4th International Workshop on Semantic Evaluations

Task #2: Evaluating Word Sense Induction and Discrimination Systems

Release of final data
March 12, 2006

[Data files in final data release]

The data set distributed for this task includes:

* English_sense_induction.xml: A file for 100 target words. There are 65
  verbs and 35 nouns.

  Each input file consists of several instances of the target words, and
  each instance is a context in which a particular target word
  appears. Contexts are sequences of words and punctuation marks. Note that,
  unlike in the trial release, this file is actually a valid XML file, the
  DTD of which is also included (sense-induction.dtd).

* Random.key: A sample output of a dummy sense induction system.

  A dummy clustering solution for all the target words. In this
  solution the induced word senses and their associated weights have
  been randomly produced.

Files:

  00-README.txt	                 This file
  English_sense_induction.xml    Input file
  sense-induction.dtd            DTD file
  Random.key	   	         Example of output file
  words.txt			 The target words. There are 65 verbs and 35
				 nouns.

--
Authors: Eneko agirre <e.agirre@ehu.es>
	 Aitor Soroa <a.soroa@ehu.es>

Semeval site: http://nlp.cs.swarthmore.edu/semeval/
Task website: http://ixa2.si.ehu.es/semeval-senseinduction/
Join the discussion group: http://groups.google.com/group/senseinduction
