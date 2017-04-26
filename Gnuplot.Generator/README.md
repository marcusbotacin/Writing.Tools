# Gnuplot.Generator

A tool to help graph creating using gnuplot.

## Usage

```
Usage: python gplotgen.py
--input <.dat file>
--output <.eps/.png file>
--script <.gnu file>
--eps/--png (graph type)
--histo
--title <title>
--yrange <range> --ytics <tics> --yformat <format>
--columns (a:b:c:d:e)
-h/--help
```

## Example

```
python gplotgen.py --input tests/inputs/histo.dat --output tests/test.eps --histo --eps --script tests/scripts/histo.gnu --title "My Title" --columns 2:1:3:4:5 --yrange [0:65] --ytics 10 --yformat "%2.0f%%"
```
