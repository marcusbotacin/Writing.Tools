#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Marcus Botacin
# Generate Latex tables from specific inputs

import sys # receive args
import fileinput # read from multiple sources
from enum import Enum # define values

# error classes
class error_codes(Enum):
	format_error = 1 # format error
	other_errors = 2 # generic error
	# Future: more functionalities, more error codes

# display head when printing
head="[TTG]"

# usage information
def usage(bin_name):

	print("%s python %s -input <file> (default: stdin) --tex-options" % (head,bin_name))
	print("%s Tex Options: --title <title> (default: empty) "
		 "--format <columns> (required) "
		 "--position <position> (default: H) "
		 "--align <alignment> (default: l) "
		 "--title <title> (default:None) "
		 "--borders (default:No) "
		 % head)
	print("%s Type -h for help" % head)

# generate titles for the tables
def emit_title(columns,title,borders):
	# with or without borders
	# vertical bar
	if borders:
		pos = "|c|"
	else:
		pos = "c"

	# emit title itself
	print("\multicolumn{%d}{%s}{%s} \\\\" % (columns,pos,title))

	# with or without borders
	# horizontal bar
	if borders:
		print("\hline")

# generates table's begin
def emit_begin(columns,position,align,borders):
	
	# specified or default position value
	if position is None:
		position="H"
	print("\\begin{table}[%s]" % position)

	# specified or default alignment values
	if align is None:
		align="l"
	# print the bars (|) when having borders
	if borders:
		align=(("|"+align)*columns)+"|"
	else:
		align=align*columns

	# emit itself
	print("\\begin{tabular}{"+align+"}")

	# horizontal bar
	if borders:
		print("\hline")

# closing the table environment
def emit_end(borders):
	# last line print
	if borders:
		print("\\\\ \hline")

	# closing
	print("\\end{tabular}")
	print("\\end{table}")

# Main
def main(input,title,columns,position,align, borders):

	# begin table env
	emit_begin(columns,position,align,borders)

	# generate title when required
	if title is not None:
		emit_title(columns,title,borders)

	# iterate over data
	# stdin or file
	for i,line in enumerate(fileinput.input(input)):
		# at the end of each row
		if i % columns == 0 and i != 0:
			# new line
			print("\\\\")
			# horizontal bar
			if borders:
				print("\hline")
		# data itself, without next line
		print(line.strip()),
		# print separators
		if i % columns != columns-1:
			print(" & "),
	# at the end, next line
	print("")

	# close table env
	emit_end(borders)

# emit error messages
def raise_error(reason):
	# vector of error messages indexed by the error number
	error_messages=["Missing format or format error","Unknown Error"]
	
	# error message itself
	print("%s %s" % (head,error_messages[reason.value-1]))
	
	# as an error occurred, stop
	sys.exit(0)

# parser
def parse(args):
	bin_name=args[0] # script name
	input="-" # file_input stdin
	title=None # default: no title
	columns=None # default: error case
	position=None # default: H
	align=None # default: l(eft)
	borders=False # default: No borders

	# iterate over all args
	for i,arg in enumerate(args):
		#help
		if "-h" in arg:
			# display usage and dies
			usage(bin_name)
			sys.exit(0)
		# input, get file name
		if "-input" in arg:
			input=args[i+1]
		# title, get title
		if "--title" in arg:
			title=args[i+1]
		# format, get columns
		if "--format" in arg:
			columns=args[i+1]
		# positon, get value
		if "--position" in arg:
			position=args[i+1]
		# align, get value
		if "--align" in arg:
			align=args[i+1]
		# borders, set true
		if "--borders" in arg:
			borders=True
			
	# args parsed
	# case no column value supplied, raise an error and go away
	if columns is None:
		raise_error(error_codes.format_error)
		usage(bin_name)
		sys.exit(0)

	# parsed params
	return input,title,columns,position,align,borders

# Entry Point
if __name__ == "__main__":
	# parse args
	# errors will stop execution
	input,title,columns,position,align, borders = parse(sys.argv)
	# if ok, start
	main(input,title,int(columns),position,align,borders)
	
else:
	# module import case
	print("No module import support yet")
