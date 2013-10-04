cat all-components.txt | awk '{print "https://dl.dropboxusercontent.com/u/3482709/research/mapping/pos-filtering/"$1}' | xargs -n 1 -P 10 wget
wait
echo "output should be = 82111500 3089750947 15270345138"
zcat *.gz  | wc
