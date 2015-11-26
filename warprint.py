#!/usr/bin/env python

from sys import argv, stdin
from weave import Dump
from utils import hexdump


do_hexdump = "-h" in argv
if do_hexdump:
	argv.remove("-h")

if len(argv) > 1:
	try:
		input_stream = open(argv[1], "rb")
	except Exception as e:
		print("Couldn't open %r for input: %s" % (argv[1], str(e)))
else:
	input_stream = stdin

for msg in Dump(input_stream):
	print(msg)
	if do_hexdump:
		print(hexdump(msg.data))
