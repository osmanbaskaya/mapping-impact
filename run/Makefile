SHELL := /bin/bash
### PATH
SRILM_PATH=/opt/srilm/bin/i686-m64
export PATH := .:${PATH}:/work/_upos_new/bin:.:${SRILM_PATH}
MATLAB_PATH=/mnt/opt/matlab/linux64/R2011a/bin/matlab -nojvm -nodisplay
SEED=1

CORP_FILES=$(shell find /data/ldc/gigaword_eng/ -name "*.gz" | sort)
RAW_FILES=$(shell find ../data/raw/ -name "out-*.gz" | sort)
TWITTER=$(shell find ../data/cleaned-tweets/ -name "*.tsv" | sort)
PSEUDO_W_FILE=pseudoword-samples/pseudowords.979-count.txt

TRAIN1=$(shell ls ../data/ukwac/UKWAC-* | sort -k 2 -t - -n | head -5 | tail -5)
TRAIN2=$(shell ls ../data/ukwac/UKWAC-* | sort -k 2 -t - -n | head -10 | tail -5)
TRAIN3=$(shell ls ../data/ukwac/UKWAC-* | sort -k 2 -t - -n | head -15 | tail -5)
TRAIN4=$(shell ls ../data/ukwac/UKWAC-* | sort -k 2 -t - -n | head -20 | tail -5)
TRAIN5=$(shell ls ../data/ukwac/UKWAC-* | sort -k 2 -t - -n | head -25 | tail -5)

TEST=$(shell find ../data/pos-filtering/  -name "*.raw.gz" | sort)

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

../data/twitter/monosemous-words: ${TWITTER}
	mkdir $@
	echo $^ | xargs -n 1 -P 60 twitter-tok-pos-lem.py 2>&1 | tee twitter-mono.err
	wait
	make twitter-raw-files

twitter-raw-files: ${TWITTER}
	twitter-raw-data-create.py $^ ../data/twitter/monosemous-words

twitter-clean: ../data/twitter/clean/ ../data/cleaned-tweets/ ../data/cleaner-tweets/
	remove-twitter-inst.py $^
	yes n | cp -i ../data/cleaned-tweets/* ../data/cleaner-tweets

../data/twitter/pos-filtering: ../data/twitter/monosemous-words ../data/twitter/clean/
	mkdir $@
	@echo $(shell find $< -name "*raw.gz" | sort) | sed 's/.raw.gz//g' \
	| xargs -n 1 -P 40 twitter-pos-filter.py

classifier-eval:
	classifier_eval.py -g dummy.key -k 10 -l Semeval2013 -i dummy.key 

### Base Corpus Creation ###
tok1.gz tok2.gz tok3.gz tok4.gz tok5.gz pos1.gz pos2.gz pos3.gz pos4.gz pos5.gz lemma1.gz lemma2.gz lemma3.gz lemma4.gz lemma5.gz: ${TRAIN1} ${TRAIN2} ${TRAIN3} ${TRAIN4} ${TRAIN5}
	zcat ${TRAIN1} | perl -pe 's/[^ -~\s]+/\<uni\>/g' | ./extract-train.py 1 &\
	zcat ${TRAIN2} | perl -pe 's/[^ -~\s]+/\<uni\>/g' | ./extract-train.py 2 &\
	zcat ${TRAIN3} | perl -pe 's/[^ -~\s]+/\<uni\>/g' | ./extract-train.py 3 &\
	zcat ${TRAIN4} | perl -pe 's/[^ -~\s]+/\<uni\>/g' | ./extract-train.py 4 &\
	zcat ${TRAIN5} | perl -pe 's/[^ -~\s]+/\<uni\>/g' | ./extract-train.py 5 &\
	wait

train.tok.gz train.pos.gz train.lemma.gz: tok1.gz tok2.gz tok3.gz tok4.gz tok5.gz pos1.gz pos2.gz pos3.gz pos4.gz pos5.gz lemma1.gz lemma2.gz lemma3.gz lemma4.gz lemma5.gz
	zcat tok*.gz | gzip > train.tok.gz
	zcat pos*.gz | gzip > train.pos.gz
	zcat lemma*.gz | gzip > train.lemma.gz

LM_NGRAM=4  # n-gram order
LM_VOCAB=400 # words seen less than this in GETTRAIN will be replaced with <unk>

train.vocab-all.gz: train.tok.gz
	zcat $< | awk 'length($$0) < 1001' | \
	ngram-count -write-order 1 -text - -write - | gzip > $@

train.vocab.gz: train.vocab-all.gz
	zcat $< | awk '{if ($$2 >= ${LM_VOCAB}) print $$1}' | gzip > $@
	zcat $@ | wc -l

train.lm.gz: train.tok.gz train.vocab.gz
	zcat $< | awk 'length($$0) < 1001' | \
	ngram-count -order ${LM_NGRAM} -kndiscount -interpolate -unk -vocab train.vocab.gz -text - -lm $@

train.context.gz: train.tok.gz train.pos.gz train.lemma.gz
	extract-train-context.py $^ ${TEST} | gzip > $@

train.sentence.gz: train.tok.gz train.pos.gz train.lemma.gz
	extract-train-sentence.py $^ ${TEST} | gzip > $@

test-inst-list.gz: ../data/keys/
	cat ../data/keys/*.instances | sort -t$$'\t' -k1,1 -k2,2n \
	| uniq | gzip > $@

test.context.gz: test-inst-list.gz
	zcat $< | extract-test-context.py | gzip > $@

test.sentence.gz: test-inst-list.gz
	zcat $< | extract-test-sentence.py | gzip > $@

random.context.gz: train.context.gz
	zcat $< | ./sample-contexts.py 2500  | gzip > $@

random.sentence.gz: train.sentence.gz
	zcat $< | ./sample-contexts.py 2500  | gzip > $@

test-comp-sep: sentence/test
	separate-comps.py test.sentence.gz $<

train-comp-sep: sentence/train
	separate-comps.py random.sentence.gz $<

sub-comp-sep: target.sub.gz sub/
	separate-comps.py $^

FS_NSUB=100 # go until you have this many substitutes
FS_PSUB=1.0 # or this much cumulative probability
FS_OPTIONS=-n ${FS_NSUB} -p ${FS_PSUB}
# all.sub.gz: train.lm.gz train.context.gz trial.context.gz test.context.gz
# 	zcat train.context.gz trial.context.gz test.context.gz |\
# 	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > $@

all.sub.1.gz all.sub.2.gz all.sub.3.gz all.sub.4.gz all.sub.5.gz: train.lm.gz random.context.gz
	zcat random.context.gz | tail -n +000001 | head -325000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > all.sub.1.gz &\
	zcat random.context.gz | tail -n +325001 | head -325000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > all.sub.2.gz &\
	zcat random.context.gz | tail -n +650001 | head -325000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > all.sub.3.gz &\
	zcat random.context.gz | tail -n +975001 | head -325000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > all.sub.4.gz &\
	zcat random.context.gz | tail -n +1300001 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > all.sub.5.gz &\
	wait

test.sub.1.gz test.sub.2.gz test.sub.3.gz test.sub.4.gz test.sub.5.gz test.sub.6.gz: test.context.gz train.lm.gz
	zcat $< | tail -n +000001 | head -150000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > test.sub.1.gz &\
	zcat $< | tail -n +150001 | head -150000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > test.sub.2.gz &\
	zcat $< | tail -n +300001 | head -150000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > test.sub.3.gz &\
	zcat $< | tail -n +450001 | head -150000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > test.sub.4.gz &\
	zcat $< | tail -n +600001 | head -150000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > test.sub.5.gz &\
	zcat $< | tail -n +750000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > test.sub.6.gz &\
	wait

test.sub.gz: test.sub.1.gz test.sub.2.gz test.sub.3.gz test.sub.4.gz test.sub.5.gz test.sub.6.gz
	zcat $^ | gzip > $@

#2199795 442158795 4402274133
target.sub.gz: test.sub.gz all.sub.1.gz all.sub.2.gz all.sub.3.gz all.sub.4.gz
	zcat $^ | grep -P '^<\w+\.\w+' | gzip > $@

pairs.100.gz: target.sub.gz
	perl -le 'print "$<" for 1..100' | xargs zcat | wordsub -s ${SEED} | gzip > $@

SC_OPTIONS=-a -r 1 -d 25 -z 0.166 -p 50 -u 0.2 -s ${SEED} -v
# example: add.v.scode.gz
# caution: no instance enrichment will be made ({1,3})
%.scode.gz: pairs.100.gz
	 zcat $< | grep -P '^<$*\.\d{1,3}>' | scode -i 50 ${SC_OPTIONS} | gzip > scode_vec/$@

create-input-for-hdp: ${PSEUDO_W_FILE}
	rm -rf hdp-wsi/wsi_input/example/all/*.lemma
	create-hdp-input.py $<

create-input-for-wordsub: ${PSEUDO_W_FILE}
	create-wordsub-input.py $<

%.pairs.gz:
	perl -le 'print "wordsub/$*.gz" for 1..100' | xargs zcat | wordsub -s ${SEED} | \
	gzip > pairs/$@

SUBS=$(shell find wordsub/  -name "*" | sed 's|wordsub/||g' | sort)
create-input-for-pairs: wordsub/
	echo ${SUBS} | sed 's|.gz|.pairs.gz|g' | xargs -n1 -P 50 make 

eval/hdp.ans:
	rm -rf hdp-wsi/topicmodelling/topicmodel_output/*
	cd hdp-wsi/; ./run_wsi.sh; wait
	cp hdp-wsi/wsi_output/tm_wsi $@

NUM_CLUST=10
ans/%.ans:
	y-cluster.py $* ${SEED} ${NUM_CLUST} #| gzip > $@

PAIRS=$(shell find pairs/ -name "*") 
aiku-run:
	echo ${PAIRS} | sed -e 's/pairs.gz/ans/g' -e 's/pairs/ans/g' | xargs -n 1 -P 60 make
#./key-mapper.py ans/actor.ans ../data/keys/actor.key
AIKU_ANS=$(shell find ans/ -name "*.ans" | sed -e 's|\.ans||g' -e 's|ans/||g') 
eval/aiku.ans:
	for f in ${AIKU_ANS}; do aiku-key-mapper.py ans/$$f.ans ../data/keys/$$f.key; done
	cat ans2/*.ans > $@

twitter-exclude-list%.txt: ../data/cleaned-tweets/
	for i in `ls $<*.tsv`; do echo `cat $$i | wc -l | awk \
	'{if ($$1<$*) print $$1}'` $$i | sed 's/.tsv//g'; done  | grep -P "\d+" > $@

twitter-pseudoword-samples-more-than-%.txt: twitter-exclude-list%.txt create-pwlist.py
	create-pwlist.py ${PSEUDO_W_FILE} $< > $@
	wc -l $@

PSEUDOWORDS=$(shell find ans3/ -name "*.ans" | sed -e 's|\.ans||g' -e 's|ans3/||g') 
chunk-evaluation:
	performance_eval.py ${PSEUDOWORDS}

clear-data: 
	rm -rf ../data/components ../data/monosemous-words ../data/pos-filtering

.SECONDARY:
#small.tok.gz small.pos.gz small.lem.gz small.raw.gz
#tok.mono.gz pos.mono.gz lem.mono.gz raw.mono.gz
