set terminal postscript eps color colortext
set key outside
set encoding utf8
set auto x
set yrange [0:65]
set ytics 10
set format y '%2.0f%%'
set style data histogram
set style histogram cluster gap 1
set style fill solid border -1
set boxwidth 0.9
set output "tests/test.eps"
set grid
set title "My Title"
plot "tests/inputs/histo.dat" using 2:xtic(1) ti col, '' u 3 ti col, '' u 4 ti col, '' u 5 ti col
