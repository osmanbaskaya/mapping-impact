SHELL := /bin/bash
### PATH
SRILM_PATH=/opt/srilm/bin/i686-m64
export PATH := .:${PATH}:/work/_upos_new/bin:.:${SRILM_PATH}
MATLAB_PATH=/mnt/opt/matlab/linux64/R2011a/bin/matlab -nojvm -nodisplay
SEED=1

CORP_FILES=$(shell find /data/ldc/gigaword_eng/ -name "*.gz" | sort)
RAW_FILES=$(shell find ../data/raw/ -name "out-*.gz" | sort)


### BIN SETUP
bin:
	cd ../bin; make

gigafetch.out:
	-rm ../data/out-*
	echo ${CORP_FILES} | xargs -n 1 -P 60 fetch-p.py >> $@

tokenize-lemmatize-postag.out:
	echo ${RAW_FILES} | xargs -n 1 -P 60 run-tok-pos-lem.py > $@
	
.SECONDARY:
