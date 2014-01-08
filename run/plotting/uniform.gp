#set term pngcairo
#set output "exp3-uniform.png"
set title "Performance on different training set sizes (Uniform)" font ",14"
set xlabel "Approximate number of instances for all training set" font ",14"
set ylabel "F1-Score" font ",14"
set xtics font ", 13"
set ytics font ", 13"
set xtics (10, 25, 50, 75, 100, 150, 200, 250, 500, 750)
set key right top font ", 13"
set xrange [0:900]
set ytics 0, 0.025, 1
set yrange [.45:0.875]
plot   "exp3-u.tab" u 1:2 w lp title "AIKU"  lw 2, \
       "exp3-u.tab" u 1:3 w lp title "HDP"   lw 2,  \
       "exp3-u.tab" u 1:4 w lp title "Chinese Whispers"  lw 2, \
       "exp3-u.tab" u 1:5 w lp title "SquaT" lw 2, \
       "exp3-u.tab" u 1:6 w lp title "Ensemble" lw 2, \
       "exp3-u.tab" u 1:8 w lp title "IMS" lw 2
