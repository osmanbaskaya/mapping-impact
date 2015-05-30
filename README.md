mapping-impact
==============

Measuring the impact of sense mapping for WSI methods


    make create-s13-system-ans-dir
    make create-chunk-keys-for-semeval-systems-s13
    for f in `ls -d semeval-systems/s13/*-ans | sed -e "s|-ans||g" -e "s|semeval-systems/s13/||g"`; do make $f-chunk-semeval-exp SEM=s13; done
    ls -d semeval-systems/s13/*-ans | sed -e "s|-ans||g" -e "s|semeval-systems/s13/||g" | xargs -i make evaluate-{}-s13
    make all-system-evaluate-s13 | tee individual-s13.tsv
