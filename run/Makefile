SHELL := /bin/bash
### PATH
SRILM_PATH=/opt/srilm/bin/i686-m64
export PATH := .:${PATH}:/work/_upos_new/bin:.:${SRILM_PATH}
MATLAB_PATH=/mnt/opt/matlab/linux64/R2011a/bin/matlab -nojvm -nodisplay
SEED=1

CORP_FILES=$(shell find /data/ldc/gigaword_eng/ -name "*.gz" | sort)
RAW_FILES=$(shell find ../data/raw/ -name "out-*.gz" | sort)
PSEUDO_WORDS_FILE=pseudoword-samples/pseudowords.1001-count.txt

### BIN SETUP
bin:
	cd ../bin; make

gigafetch.out:
	-rm ../data/raw/out-*
	echo ${CORP_FILES} | xargs -n 1 -P 60 fetch-p.py >> $@

tokenize-lemmatize-postag.out:
	echo ${RAW_FILES} | xargs -n 1 -P 60 run-tok-pos-lem.py > $@

tok.mono.gz pos.mono.gz raw.mono.gz lem.mono.gz: ${PSEUDO_WORDS_FILE}  #wc -l = 22632220
	echo ${RAW_FILES} | xargs -n 1 -P 60 monosemous-word-fetching.py $< &> mono-word-fetching.err
	wait
	cat ../data/word-components/lem* | gzip > lem.mono.gz
	cat ../data/word-components/raw* | gzip > raw.mono.gz
	cat ../data/word-components/tok* | gzip > tok.mono.gz
	cat ../data/word-components/pos* | gzip > pos.mono.gz
	#rm -rf ../data/word-components/*out*.gz

monosemous-creation: ${PSEUDO_WORDS_FILE} tok.mono.gz pos.mono.gz lem.mono.gz raw.mono.gz
	rm -rf ../data/monosemous-words/*.gz
	word-filtering.py $^

.SECONDARY:
