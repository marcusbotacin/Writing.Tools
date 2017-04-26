#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Gnuplot histogram generator
# Marcus Botacin

import sys # get args

# display usage message
def usage(bin_name):
	print(	"Usage: python %s\n"
		"--input <.dat file>\n"
		"--output <.eps/.png file>\n"
		"--script <.gnu file>\n"
		"--eps/--png (graph type)\n"
		"--histo\n"
		"--title <title>\n"
		"--yrange <range> --ytics <tics> --yformat <format>\n"
		"--columns (a:b:c:d:e)\n"
		"-h/--help\n"
	 % bin_name)

# parse arguments
def parse(args):
	
	# set default values (empty)
	input=None
	output=None
	graph_type=None
	_usage=False
	out_type=None
	script = None
	title = None
	columns=None
	yrange=None
	ytics=None
	yformat=None

	# parse each arg
	for i,arg in enumerate(args):
		if "--yrange" in arg:
			yrange=args[i+1]
		if "--ytics" in arg:
			ytics=args[i+1]
		if "--yformat" in arg:
			yformat=args[i+1]
		if "--columns" in arg:
			columns=args[i+1]
		if "--title" in arg:
			title=args[i+1]
		if "--script" in arg:
			script=args[i+1]
		if "--input" in arg:
			input=args[i+1]
		if "--output" in arg:
			output=args[i+1]
		if "--histo" in arg:
			graph_type="histo"
		if "--eps" in arg:
			out_type="eps"
		if "--png" in arg:
			out_type="png"
		if arg in ["-h","--help"]:
			_usage=True

	# error cases
	if columns==None:
		print("No columns supplied")
		_usage=True
	if title==None:
		print("No title supplied")
		_usage=True	
	if input==None:
		print("No input file")
		_usage=True
	if output==None:
		print("No output file")
		_usage=True
	if graph_type==None:
		print("No graph type")
		_usage=True
	if out_type==None:
		print("No outfile type")
		_usage=True
	if script==None:
		print("No output script file")
		_usage=True
	if yrange==None:
		print("No yrange")
		_usage=True
	if ytics==None:
		print("No ytics")
		_usage=True
	if yformat==None:
		print("No yformat")
		_usage=True

	# display usage message ?
	# Yes for error cases or --help
	if _usage:
		usage(sys.argv[0])
		# case error, exit
		sys.exit(0)

	# return parsed values
	return script,input,output,graph_type,out_type,title,columns,yrange,ytics,yformat

# emit gnuplot header
def emit_header(f,out_type):
	if out_type == "eps":
		f.write("set terminal postscript eps color colortext\n")
	elif out_type == "png":
		f.write("set terminal png size 1200,800\n")
	else:
		print("outfile type error")
	
# emit general gnuplot config
def emit_general(f):
	f.write("set key outside\n"
		"set encoding utf8\n")

# emit gnuplot format specs
def emit_format(f,yrange,ytics,yformat):
	f.write("set auto x\n"
		"set yrange %s\n"
		"set ytics %s\n"
		"set format y '%s'\n" % (yrange,ytics,yformat))

# emit gnuplot info for histograms
def emit_histo(f):
	f.write("set style data histogram\n"
		"set style histogram cluster gap 1\n"
		"set style fill solid border -1\n"
		"set boxwidth 0.9\n")

# emit output file and settings
def emit_output(f,output):
	f.write("set output \"%s\"\n"
	"set grid\n" % output)

# emit graph title
def emit_title(f,title):
	f.write("set title \"%s\"\n" % title)

# emit plot command according the columns
def emit_columns(f,input,columns):
	c=columns.split(":")
	f.write("plot \"%s\" " % input)
	f.write("using %s:xtic(%s) ti col" % (c[0],c[1]))
	for i in c[2:]:
		f.write(", '' u %s ti col" % i)
	f.write("\n")

# main
def main(script,input,output,graph_type,out_type,title,columns,yrange,ytics,yformat):

	# open file
	f=open(script,"w")

	# emit settings
	emit_header(f,out_type)
	emit_general(f)
	emit_format(f,yrange,ytics,yformat)

	# case histo, emit hist
	if graph_type=="histo":
		emit_histo(f)

	# TODO: add other graph formats

	emit_output(f,output)
	emit_title(f,title)
	emit_columns(f,input,columns)

# entry import
# direct call
if __name__ == "__main__":
	# parse args
	script,input,output,graph_type,out_type,title,columns,yrange,ytics,yformat = parse(sys.argv)
	# if ok, call main
	main(script,input,output,graph_type,out_type,title,columns,yrange,ytics,yformat)
# indirect call, module import
else:
	# not supported yet
	print("No module import support Yet!")
