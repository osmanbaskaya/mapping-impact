SHELL := /bin/bash
### PATH
SRILM_PATH=/opt/srilm/bin/i686-m64
export PATH := .:${PATH}:/work/_upos_new/bin:.:${SRILM_PATH}
MATLAB_PATH=/mnt/opt/matlab/linux64/R2011a/bin/matlab -nojvm -nodisplay
SEED=1

CORP_FILES=$(shell find /data/ldc/gigaword_eng/ -name "*.gz" | sort)
RAW_FILES=$(shell find ../data/raw/ -name "out-*.gz" | sort)
PSEUDO_W_FILE=pseudoword-samples/pseudowords.1001-count.txt

### BIN SETUP
bin:
	cd ../bin; make

gigafetch.out:
	-rm ../data/raw/out-*
	echo ${CORP_FILES} | xargs -n 1 -P 60 fetch-p.py >> $@

tokenize-lemmatize-postag.out:
	echo ${RAW_FILES} | xargs -n 1 -P 60 run-tok-pos-lem.py > $@

../data/components: ${PSEUDO_W_FILE}  #wc -l = 22632220
	mkdir $@
	echo ${RAW_FILES} | xargs -n 1 -P 60 fetch-w.py $< &> fetch-w.err

mono.%.gz: ../data/components
	cat $</$** | gzip > $@
	#echo `wc -l $@`

../data/monosemous-words: ${PSEUDO_W_FILE} mono.tok.gz mono.pos.gz mono.lem.gz mono.raw.gz
	mkdir $@
	mono-word-filtering.py $^ &> mono-word-filtering.err 

../data/pos-filtering: ../data/monosemous-words
	mkdir $@
	@echo $(shell find $< -name "*raw.gz" | sort) | sed 's/.raw.gz//g' \
	| xargs -n 1 -P 40 pos-filter.py

classifier-eval:
	classifier_eval.py -g dummy.key -k 10 -l Semeval2013 -i dummy.key 

corpus-creation-check:
	zcat ${CORP_FILES} | grep -iP 'wesleyan'

clear-data:
	rm -rf ../data/components ../data/monosemous-words ../data/pos-filtering


.SECONDARY:
#small.tok.gz small.pos.gz small.lem.gz small.raw.gz
#tok.mono.gz pos.mono.gz lem.mono.gz raw.mono.gz
