SHELL := /bin/bash
### PATH
SRILM_PATH=/opt/srilm/bin/i686-m64
export PATH := .:${PATH}:/scratch/1/obaskaya/tools/bin/:${SRILM_PATH}
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

TEST=$(shell find ../data/pos-filtering/ -name "*.raw.gz" | sort)
TWITTER_EXISTED_PW_LIST='existed-twitter-pseudoword-list.txt'
# If dev data is changed, you should change the gold standard file
DEVDATA=activeness brahms bathroom al ashur
#ls *.key | sed 's|.key||g' > ../../../run/existed-twitter-pseudoword-list.txt

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

twitter-inst-list.gz: ../data/twitter/keys/
	cat ../data/twitter/keys/*.instances | sort -t$$'\t' -k2,2 -k3,3n \
	| uniq | gzip > $@

# test-inst-list.gz should be sorted
# test-inst-list does not have instance column like twitter-inst-list so
# it should not work properly. instance files in keys/ should have instance ids column.
# See new_key target
test.context.gz: test-inst-list.gz
	zcat $< | extract-context.py ../data/pos-filtering/ | gzip > $@

../data/keys2:
	mkdir $@
	for i in `ls *\.key | sed 's|.key||g'`; do paste <(cat $i.key | cut -d ' ' -f2) \
		<(cat $i.instances) > ../keys/$i.instances; done

# twitter-inst-list.gz should be sorted
twitter.context.gz: twitter-inst-list.gz
	zcat $< | extract-context.py ../data/twitter/pos-filtering/ | gzip > $@

# test-inst-list.gz should be sorted
test.sentence.gz: test-inst-list.gz
	zcat $< | extract-sentence.py ../data/pos-filtering/ | gzip > $@

# twitter-inst-list.gz should be sorted
twitter.sentence.gz: twitter-inst-list.gz
	zcat $< | extract-sentence.py ../data/twitter/pos-filtering/ | gzip > $@

random.context.gz: train.context.gz
	zcat $< | ./sample-contexts.py 2500  | gzip > $@

missing.context.gz: train.context.gz sub-missing-words.txt
	zcat $< | ./sample-missing-contexts.py 2500 sub-missing-words.txt | gzip > $@

random.sentence.gz: train.sentence.gz
	zcat $< | ./sample-contexts.py 2500  | gzip > $@

test-comp-sep: sentence/test test.sentence.gz
	separate-comps.py $^

train-comp-sep: sentence/train random.sentence.gz 
	separate-comps.py $^

twitter-test-comp-sep: twitter-sentence/test twitter.sentence.gz
	separate-comps.py $^

twitter-train-comp-sep: twitter-sentence/train random.sentence.gz test.sentence.gz
	separate-comps.py $^

sub-comp-sep: sub/ target.sub.gz
	separate-comps.py $^

twitter-sub-comp-sep: twitter/sub/ twitter.sub.gz
	separate-comps.py $^

FS_NSUB=100 # go until you have this many substitutes
FS_PSUB=1.0 # or this much cumulative probability
FS_OPTIONS=-n ${FS_NSUB} -p ${FS_PSUB}
# all.sub.gz: train.lm.gz train.context.gz trial.context.gz test.context.gz
# 	zcat train.context.gz trial.context.gz test.context.gz |\
# 	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > $@
#
missing.sub.1.gz missing.sub.2.gz missing.sub.3.gz: missing.context.gz train.lm.gz
	zcat $< | tail -n +000001 | head -115000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > missing.sub.1.gz &\
	zcat $< | tail -n +115001 | head -115000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > missing.sub.2.gz &\
	zcat $< | tail -n +230001 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > missing.sub.3.gz &\
	wait

all.sub.1.gz all.sub.2.gz all.sub.3.gz all.sub.4.gz all.sub.5.gz: random.context.gz train.lm.gz
	zcat $< | tail -n +000001 | head -325000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > all.sub.1.gz &\
	zcat $< | tail -n +325001 | head -325000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > all.sub.2.gz &\
	zcat $< | tail -n +650001 | head -325000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > all.sub.3.gz &\
	zcat $< | tail -n +975001 | head -325000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > all.sub.4.gz &\
	zcat $< | tail -n +1300001 |\
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
	zcat $< | tail -n +750001 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > test.sub.6.gz &\
	wait

twitter.all.sub.1.gz twitter.all.sub.2.gz twitter.all.sub.3.gz twitter.all.sub.4.gz: twitter.context.gz train.lm.gz
	zcat $< | tail -n +00001 | head -45000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > twitter.sub.1.gz &\
	zcat $< | tail -n +45001 | head -45000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > twitter.sub.2.gz &\
	zcat $< | tail -n +90001 | head -45000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > twitter.sub.3.gz &\
	zcat $< | tail -n +135001 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > twitter.sub.4.gz &\
	wait

test.sub.gz: test.sub.1.gz test.sub.2.gz test.sub.3.gz test.sub.4.gz test.sub.5.gz test.sub.6.gz
	zcat $^ | gzip > $@

missing.sub.gz: missing.sub.1.gz missing.sub.2.gz missing.sub.3.gz
	zcat $^ | gzip > $@

twitter.sub.gz: twitter.all.sub.1.gz twitter.all.sub.2.gz twitter.all.sub.3.gz twitter.all.sub.4.gz 
	zcat $^ | grep -P '^<\w+\.\w+' | gzip > $@

#2199795 442158795 4402274133
target.sub.gz: test.sub.gz all.sub.1.gz all.sub.2.gz all.sub.3.gz all.sub.4.gz all.sub.5.gz
	zcat $^ | grep -P '^<\w+\.\w+' | gzip > $@

pairs.100.gz: target.sub.gz
	perl -le 'print "$<" for 1..100' | xargs zcat | wordsub -s ${SEED} | gzip > $@

SC_OPTIONS=-a -r 1 -d 25 -z 0.166 -p 50 -u 0.2 -s ${SEED} -v
# example: add.v.scode.gz
# caution: no instance enrichment will be made ({1,3})
%.scode.gz: pairs.100.gz
	 zcat $< | grep -P '^<$*\.\d{1,3}>' | scode ${SC_OPTIONS} | gzip > scode_vec/$@

create-input-for-hdp: ${PSEUDO_W_FILE}
	rm -rf hdp-wsi/wsi_input/example/all/*.lemma
	create-hdp-input.py $<

# some pseudowords that have missing component(s) should be deleted
twitter-hdp-input-cleaner: hdp-wsi/wsi_input/example/num_test_instances.all.txt
	twitter-hdp-cleaner.py

create-input-for-wordsub: ${PSEUDO_W_FILE}
	create-wordsub-input.py $< sub/ wordsub/

twitter-create-input-for-wordsub: ${PSEUDO_W_FILE}
	create-wordsub-input.py $< twitter/sub/ twitter/wordsub/ ${TWITTER_EXISTED_PW_LIST}

%.pairs.gz:
	perl -le 'print "wordsub/$*.gz" for 1..100' | xargs zcat | wordsub -s ${SEED} \
	| gzip > pairs/$@
	#perl -le 'print "twitter/wordsub/$*.gz" for 1..100' | xargs zcat | wordsub -s ${SEED} \
	#| gzip > twitter/pairs/$@

SUBS=$(shell find wordsub/  -name "*" | sed 's|wordsub/||g' | sort)
create-input-for-pairs: wordsub/
	echo ${SUBS} | sed 's|.gz|.pairs.gz|g' | xargs -n1 -P 50 make

TSUBS=$(shell find twitter/wordsub/  -name "*" | sed 's|twitter/wordsub/||g' | sort)
twitter-create-input-for-pairs: twitter/wordsub/
	echo ${TSUBS} | sed 's|.gz|.pairs.gz|g' | xargs -n1 -P 50 make 

eval/hdp.ans:
	rm -rf hdp-wsi/topicmodelling/topicmodel_output/*
	cd hdp-wsi/; ./run_wsi.sh; wait
	cp hdp-wsi/wsi_output/tm_wsi $@

NUM_CLUST=10
ans/%.ans:
	y-cluster.py $* ${SEED} ${NUM_CLUST} #| gzip > $@

twitter/ans/%.ans:
	y-twitter-cluster.py $* ${SEED} ${NUM_CLUST} #| gzip > $@

PAIRS=$(shell find pairs/ -name "*") 
aiku-run:
	echo ${PAIRS} | sed -e 's/pairs.gz/ans/g' -e 's/pairs/ans/g' | xargs -n 1 -P 60 make
#./key-mapper.py ans/actor.ans ../data/keys/actor.key

twitter-aiku-run: 
	cat ${TWITTER_EXISTED_PW_LIST} | sed -e 's|$$|.ans|g' -e 's|^|twitter/ans/|g' | \
		xargs -n 1 -P 60 make

AIKU_ANS=$(shell find ans/ -name "*.ans" | sed -e 's|\.ans||g' -e 's|ans/||g') 
eval/aiku.ans:
	for f in ${AIKU_ANS}; do aiku-key-mapper.py ans/$$f.ans ../data/keys/$$f.key; done
	cat ans2/*.ans > $@

hdp-ans/%.ans:
	paste <(cat ../data/keys/$*.key2 | cut -d' ' -f1,2) <(cat eval/hdp.ans | grep -P "^$*.n " | cut -d ' ' -f3-) > $@
	# to run it with all data: for i in `ls ../data/keys/*.key2 | sed -e 's|../data/keys/||g' -e 's|.key2||g'`; 
	# do make hdp-ans/$i.ans; done

twitter-exclude-list%.txt: ../data/cleaned-tweets/
	for i in `ls $<*.tsv`; do echo `cat $$i | wc -l | awk \
	'{if ($$1<$*) print $$1}'` $$i | sed 's/.tsv//g'; done  | grep -P "\d+" > $@

twitter-pseudoword-samples-more-than-%.txt: twitter-exclude-list%.txt create-pwlist.py
	create-pwlist.py ${PSEUDO_W_FILE} $< > $@
	wc -l $@

%-pw-list.txt: %-ans
	ls $</* | sed -re 's|$</||g' -e 's|\.ans||g' | sort > $@
	wc $@

gigaword-pw-list.txt: aiku-pw-list.txt cw-pw-list.txt hdp-pw-list.txt squat-pw-list.txt
	comm -12 hdp-pw-list.txt $< | sort > intersect.tmp
	comm -12 squat-pw-list.txt cw-pw-list.txt | sort > intersect2.tmp
	comm -12 intersect.tmp intersect2.tmp > $@
	rm intersect.tmp intersect2.tmp

gigaword-p%-pw-list.txt: ${PSEUDO_W_FILE} gigaword-pw-list.txt 
	cat $< | awk '{print $$1"\t"NF-1}' | sed "s|[<>]||g" #| grep -P "\t$*" | cut -f1 \
	#| sort > list.tmp
	#comm -12 list.tmp gigaword-pw-list.txt | sort > $@
	#wc $@

twitter-pw-list.txt: aiku-twitter-pw-list.txt cw-twitter-pw-list.txt hdp-twitter-pw-list.txt squat-twitter-pw-list.txt
	comm -12 hdp-twitter-pw-list.txt $< | sort > intersect.tmp
	comm -12 squat-twitter-pw-list.txt cw-twitter-pw-list.txt | sort > intersect2.tmp
	comm -12 intersect.tmp intersect2.tmp > $@
	rm intersect.tmp intersect2.tmp

# mapping needs to be done first!(eval/aiku.ans) then use prepare-chunk-experiment-%
GIGA_CHUNKS="../data/chunks/"
gigaword-%-chunk-exp: %-ans/ %-chunk-keys gigaword-pw-list.txt gold/gigaword
	chunk-exp.py $^ ${GIGA_CHUNKS} 1   0 150  ${DEVDATA} & \
	chunk-exp.py $^ ${GIGA_CHUNKS} 2 150 300  ${DEVDATA} & \
	chunk-exp.py $^ ${GIGA_CHUNKS} 3 300 450  ${DEVDATA} & \
	chunk-exp.py $^ ${GIGA_CHUNKS} 4 450 600  ${DEVDATA} & \
	chunk-exp.py $^ ${GIGA_CHUNKS} 5 600 750  ${DEVDATA} & \
	chunk-exp.py $^ ${GIGA_CHUNKS} 6 750 850  ${DEVDATA} & \
	chunk-exp.py $^ ${GIGA_CHUNKS} 7 850 1000 ${DEVDATA} & \
	wait

TW_CHUNKS="../data/twitter/chunks/"
twitter-%-chunk-exp: %-twitter-ans/ %-twitter-chunk-keys twitter-pw-list.txt gold/twitter
	chunk-exp.py $^ ${TW_CHUNKS} 1   0  90  ${DEVDATA} & \
	chunk-exp.py $^ ${TW_CHUNKS} 2  90 180  ${DEVDATA} & \
	chunk-exp.py $^ ${TW_CHUNKS} 3 180 270  ${DEVDATA} & \
	chunk-exp.py $^ ${TW_CHUNKS} 4 270 360  ${DEVDATA} & \
	chunk-exp.py $^ ${TW_CHUNKS} 5 360 450  ${DEVDATA} & \
	chunk-exp.py $^ ${TW_CHUNKS} 6 450 540  ${DEVDATA} & \
	chunk-exp.py $^ ${TW_CHUNKS} 7 540 1000 ${DEVDATA} & \
	wait

GIGA_CHUNKS="../data/chunks/"

ims%-pw-list.txt: gigaword-pw-list.txt ims-testing-output/has-%-instances/semcor.chunk.0
	cd ims-testing-output/has-$*-instances/semcor.chunk.0; \
	ls *.result | sed 's|\.n\.result||g' | sort > intersect.tmp; 
	mv ims-testing-output/has-$*-instances/semcor.chunk.0/intersect.tmp .
	comm -12 intersect.tmp $< > $@
	rm intersect.tmp
	wc $@

gigaword-%-chunk-imsbased-exp: %-ans/ %-ims-chunk-keys ims${NUM_INST}-pw-list.txt gold/gigaword
	-mkdir $*-ims-chunk-keys/${NUM_INST}
	chunk-exp-ims-based.py $^ ${GIGA_CHUNKS} ${NUM_INST} 1    0 130  ${DEVDATA} #& \
	#chunk-exp-ims-based.py $^ ${GIGA_CHUNKS} ${NUM_INST} 2  130 260  ${DEVDATA} &\
	#chunk-exp-ims-based.py $^ ${GIGA_CHUNKS} ${NUM_INST} 3  260 390  ${DEVDATA} &\
	#chunk-exp-ims-based.py $^ ${GIGA_CHUNKS} ${NUM_INST} 4  390 520  ${DEVDATA} & \
	#chunk-exp-ims-based.py $^ ${GIGA_CHUNKS} ${NUM_INST} 5  520 650  ${DEVDATA} &\
	#chunk-exp-ims-based.py $^ ${GIGA_CHUNKS} ${NUM_INST} 6  650 780  ${DEVDATA} &\
	#chunk-exp-ims-based.py $^ ${GIGA_CHUNKS} ${NUM_INST} 7  780 990  ${DEVDATA} &\
	#wait

gigaword-%-default-chunk-merge: %-chunk-keys
	chunk-merger.py $* default gigaword

twitter-%-default-chunk-merge: %-chunk-keys
	chunk-merger.py $* default twitter

gigaword-%-tuned-chunk-merge: %-chunk-keys
	chunk-merger.py $* tuned gigaword

twitter-%-tuned-chunk-merge: %-chunk-keys
	chunk-merger.py $* tuned twitter

ims-%-default-chunk-merge: %-ims-chunk-keys
	ims-chunk-merger.py $* default ims ${INST_NUM}

chunk-scores/%-mapped-gigaword-p6OrMore-default.scores: ../keys/gold/gigaword-p6OrMore.semcor.key ../keys/gold/gigaword-p6OrMore.uniform.key
	./classifiers-scorer.py $* mapped gigaword default $^ > $@

pw-p%.scores: gigaword-p%-pw-list.txt
	pw-score.py $< $* ${DEVDATA} > $@

chunk-scores/%-mapped-gigaword-tuned.scores: ../keys/gold/gigaword.semcor.key ../keys/gold/gigaword.uniform.key 
	./classifiers-scorer.py $* mapped gigaword tuned $^ > $@

chunk-scores/%-mapped-gigaword-default.scores: ../keys/gold/gigaword.semcor.key ../keys/gold/gigaword.uniform.key
	./classifiers-scorer.py $* mapped gigaword default $^ > $@

chunk-scores/%-mapped-twitter-tuned.scores: ../keys/gold/twitter.semcor.key ../keys/gold/twitter.uniform.key
	./classifiers-scorer.py $* mapped twitter tuned $^ > $@

chunk-scores/%-mapped-twitter-default.scores: ../keys/gold/twitter.semcor.key ../keys/gold/twitter.uniform.key
	./classifiers-scorer.py $* mapped twitter default $^ > $@

chunk-scores/ims/aiku-mapped-ims%-default.scores: ../keys/gold/ims%.semcor.key ../keys/gold/ims%.uniform.key ../keys/aiku/mapped/ims/default/%/*
	ims-classifiers-scorer.py aiku $* mapped ims default > $@

chunk-scores/ims/cw-mapped-ims%-default.scores: ../keys/gold/ims%.semcor.key ../keys/gold/ims%.uniform.key ../keys/cw/mapped/ims/default/%/*
	ims-classifiers-scorer.py cw $* mapped ims default > $@

chunk-scores/ims/squat-mapped-ims%-default.scores: ../keys/gold/ims%.semcor.key ../keys/gold/ims%.uniform.key ../keys/squat/mapped/ims/default/%/*
	ims-classifiers-scorer.py squat $* mapped ims default > $@

chunk-scores/ims/ensemble-mapped-ims%-default.scores: ../keys/gold/ims%.semcor.key ../keys/gold/ims%.uniform.key ../keys/ensemble/mapped/ims/default/%/*
	ims-classifiers-scorer.py ensemble $* mapped ims default > $@

chunk-scores/ims/hdp-mapped-ims%-default.scores: ../keys/gold/ims%.semcor.key ../keys/gold/ims%.uniform.key ../keys/hdp/mapped/ims/default/%/*
	ims-classifiers-scorer.py hdp $* mapped ims default > $@

clear-data: 
	rm -rf ../data/components ../data/monosemous-words ../data/pos-filtering

prepare-chunk-experiment-%: % # for aiku and hdp experiment
	-for i in pack ford; do rm $*/$$i.ans; done
	cat $*/adams_apple.ans | sed "s|adams_apple|adam\'s_apple|g" > $*/adam\'s_apple.ans
	-rm -rf adams_apple.ans

excel-%.tab: chunk-scores
	score-excel-format.py $* $</*p2*.scores > $@

ims-excel-%.tab: chunk-scores/ims chunk-scores/ims/*
	score-ims-excel-format.py $* $</*.scores > $@

cw-twitter-key-copy: ../keys/cw/cw-wsd-twitter
	for i in `ls $</*graded*`; do cp $$i cw-twitter-ans/; done
	cd cw-twitter-ans; ls | sed -e "p;s|cw.graded-sense.key|ans|" | xargs -n2 mv

squat-gigaword-key-copy: ../keys/squat/squat-wsd-gigaword
	for i in `ls $</*graded*`; do cp $$i squat-ans/; done
	cd squat-ans; ls | sed -e "p;s|squat.graded-sense.key|ans|" | xargs -n2 mv

squat-twitter-key-copy: ../keys/squat/squat-wsd-twitter
	for i in `ls $</*graded*`; do cp $$i squat-twitter-ans/; done
	cd squat-twitter-ans; ls | sed -e "p;s|squat.graded-sense.key|ans|" | xargs -n2 mv

gold-%-split: ../keys/gold/dev/%.dev.key gold/% # does not work for gigaword, format prob.
	gold-key-splitter.py $^ ${DEVDATA}

../keys/gold/gigaword-p%.semcor.key: ../data/chunks/ gigaword-p%-pw-list.txt
	gold-standard-creator.py $^ semcor ${DEVDATA} | sort | uniq > $@
	wc $@

../keys/gold/gigaword-p%.uniform.key: ../data/chunks/ gigaword-p%-pw-list.txt
	gold-standard-creator.py $^ uniform ${DEVDATA} | sort | uniq > $@
	wc $@

../keys/gold/gigaword.%.key: ../data/chunks/ gigaword-pw-list.txt
	gold-standard-creator.py $^ $* ${DEVDATA} | sort | uniq > $@

../keys/gold/twitter.%.key: ../data/twitter/chunks/ twitter-pw-list.txt
	gold-standard-creator.py $^ $* ${DEVDATA} | sort | uniq > $@

../keys/gold/ims%.semcor.key: ../data/chunks/ ims%-pw-list.txt
	gold-standard-creator.py $^ semcor ${DEVDATA} | sort | uniq > $@

../keys/gold/ims%.uniform.key: ../data/chunks/ ims%-pw-list.txt
	gold-standard-creator.py $^ uniform ${DEVDATA} | sort | uniq > $@

%-gigaword-uniform-gradedsense.key: %-ans ../keys/gold/gigaword.uniform.key
	cat $</*ans | system-key-creator.py ../keys/gold/gigaword.uniform.key | sort > $@ 

%-gigaword-semcor-gradedsense.key: %-ans ../keys/gold/gigaword.semcor.key
	cat $</*ans | system-key-creator.py ../keys/gold/gigaword.semcor.key | sort > $@ 

%-gigaword-uniform-singlesense.key: %-gigaword-uniform-gradedsense.key
	cat $< | graded2single.py > $@

%-gigaword-semcor-singlesense.key: %-gigaword-semcor-gradedsense.key
	cat $< | graded2single.py > $@

## make ensemble-gigaword-uniform-singlesense.key
gigaword-ensemble-%.key:
	ensemble-key-creator.py misc/*gigaword-$*.key | sort > $@

ensemble-ans-create: gigaword-pw-list.txt ensemble-ans
	ensemble-ans-creator.py $^ aiku-ans hdp-ans cw-ans squat-ans

perp-exp-%: ../keys/gold/gigaword.%.key chunk-scores/pw-scores/
	for f in `ls ../keys/*/mapped/ims/default/750/*$*.ans.gz`; do \
		pw-score-perp-calc.py $$f $^; \
	done

chunk-scores/pw-scores/ims-pw-%: ims-pw-scores/has-750-instances-%.scores ../keys/gold/ims750.%.key
	ims-score-perp-calc.py $^ $* > $@

### Tests on real datasets [ Semeval 07, 10, 13 ] ###
# Semeval 13
SEM13=../data/semeval-datasets/s13/key-splits/single-sense-instances
create-s13-chunks:
	for i in `seq 0 4`; do \
		dataset-splitter.py ${SEM13}/split-$$i.train.key ${SEM13}/split-$$i.eval.key \
		../data/chunks-s13 $$i; \
	done

# Semeval 10
SEM10=../data/semeval-datasets/s10/evaluation/sup_eval/80_20/all
create-s10-chunks:
	for i in `seq 1 5`; do \
		dataset-splitter.py ${SEM10}/mapping.$$i.key ${SEM10}/test.$$i.key \
		../data/chunks-s10 `expr $$i - 1`; \
	done

# Semeval 07
SEM07=../data/semeval-datasets/s07/keys/random_split/82_18
create-s07-chunks:
	dataset-splitter.py ${SEM07}/senseinduction.random82train.key \
	${SEM07}/senseinduction.random82test.key ../data/chunks-s07 0

create-%-system-ans-dir: ../data/semeval-system-ans/%
	for s in `ls $</`; do \
		system-key-splitter.py $</$$s semeval-systems/$*/$$s; done

# TEST ET
%-ensemble-ans-create: %-tw-list.txt ../keys/gold/%.key
	-rm -rf semeval-systems/$*/ensemble-ans
	-mkdir semeval-systems/ensemble-ans
	ensemble-ans-creator.py $^ semeval-systems/ensemble-ans `ls -d semeval-systems/$*/*ans/`
	mv semeval-systems/ensemble-ans semeval-systems/$*/

%-tw-list.txt: ../data/chunks-% 
	cat $</*.key | cut -f1 -d' ' | sort | uniq > $@
	wc $@

#${SEM} can be semeval07, semeval10, semeval13
%-chunk-semeval-exp: semeval-systems/${SEM}/%-ans/ semeval-systems/${SEM}/%-chunk-keys \
		${SEM}-tw-list.txt gold/${SEM}
	python chunk-exp-semeval-based.py $^ ../data/chunks-${SEM} ${SEM}

../keys/gold/%.key: ../data/chunks-%
	cat $</*chunk0*.key | sort | uniq > $@
	wc $@

evaluate-%-s13:
	for i in `seq 0 4`; do python ../keys/scorer.py semeval-systems/s13/$*-chunk-keys/SVM_Linear/SVM_Linear-semeval-semeval-1-$$i ../keys/gold/s13.test.$$i.key; done
	for i in `seq 0 4`; do python ../keys/scorer.py semeval-systems/s13/$*-chunk-keys/SVM_Linear/SVM_Linear-semeval-semeval-1-$$i ../keys/gold/s13.test.$$i.key; done | grep Precision | awk '{sum+=$$3}END{print sum/NR}'

evaluate-%-s07:
	python ../keys/scorer.py semeval-systems/s07/$*-chunk-keys/SVM_Linear/SVM_Linear-semeval-semeval-1-0 ../keys/gold/s07.test.0.key

evaluate-%-s10:
	for i in `seq 0 4`; do python ../keys/scorer.py semeval-systems/s10/$*-chunk-keys/SVM_Linear/SVM_Linear-semeval-semeval-1-$$i ../keys/gold/s10.test.$$i.key; done
	for i in `seq 0 4`; do python ../keys/scorer.py semeval-systems/s10/$*-chunk-keys/SVM_Linear/SVM_Linear-semeval-semeval-1-$$i ../keys/gold/s10.test.$$i.key; done | grep Precision | awk '{sum+=$$3}END{print sum/NR}'

# SEMEVAL INDIVIDUAL SYSTEM EXPERIMENT (Experiment #3 in the paper)

create-chunk-keys-for-semeval-systems-%: semeval-systems/%  # create-chunk-keys-...-s13
	-ls -d $</*-ans | sed 's|-ans||g'  | xargs -i mkdir '{}-chunk-keys'

%-all-system-chunk-exp: semeval-systems/%/  # call s13-all-system-chunk-exp
	for f in `ls -d $<*-ans | sed -e "s|-ans||g" -e "s|$<||g"`;do make $$f-chunk-semeval-exp SEM=$*; done

all-system-evaluate-%: semeval-systems/%/ # all-system-evaluate-s13
	for f in `ls -d $<*-ans | sed -e "s|-ans||g" -e "s|$<||g"`;do echo -e $$f '\t' `make evaluate-$$f-$* | tail -2 | grep -v Leaving`; done

.SECONDARY:
#small.tok.gz small.pos.gz small.lem.gz small.raw.gz
#tok.mono.gz pos.mono.gz lem.mono.gz raw.mono.gz

#../keys/gold/gigaword/gigaword.%.key: ../keys/gold/gigaword/%
	#cd $<; ls *.key | grep -Pv "^((activeness)|(brahms)|(bathroom)|(ashur)|(al))\." |\
	#xargs -0 -d'\n' cat > ../key.tmp
	#mv $</../key.tmp $@
	#wc $@

#../keys/gold/twitter/twitter.%.key: ../data/twitter/chunks
	#cd $<; ls *.$*.key |\
	#grep -Pv "^((activeness)|(brahms)|(bathroom)|(ashur)|(al))\." | xargs -n 1 cat \
	#> ../key.tmp
	#mv $</../key.tmp $@
	#wc $@
