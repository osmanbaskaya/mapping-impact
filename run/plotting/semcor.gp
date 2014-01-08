#set term pngcairo
#set output "exp3-semcor.png"
set title "Performance on different training set sizes (SemCor)" font ",14"
set xlabel "Number of instances for the most frequent SemCor Sense" font ",14"
set ylabel "F1-Score" font ",14"
set xtics font ", 13"
set ytics font ", 13"
set xtics (10, 25, 50, 75, 100, 150, 200, 250, 500, 750)
set key right bottom font ", 13"
set xrange [0:800]
set ytics 0, 0.025, 1
set yrange [.5:1]
plot   "exp3-s.tab" u 1:2 w lp title "AIKU"  lw 2, \
"exp3-s.tab"  u 1:3 w lp title "HDP"   lw 2,  \
"exp3-s.tab" u 1:4 w lp title "Chinese Whispers"  lw 2, \
"exp3-s.tab" u 1:5 w lp title "SquaT" lw 2, \
"exp3-s.tab" u 1:6 w lp title "Ensemble" lw 2, \
"exp3-s.tab" u 1:8 w lp title "IMS" lw 2
