#!/usr/bin/env python

import re, os

def GetDisasmGroup(file, group, out):
	stack = []
	found = False
	with open(file,'r') as f:
		for line in f:
			if found:
				# Detect end of block
				end = re.search('^[\d[a-zA-Z]*\s{1}\<[^\>]*\>\:$', line)
				if end:
					break
				else:
					stack.append(line)

			# try to found start
			else:
				start = re.search('^[\d[a-zA-Z]*\s{1}\<' + group + '\>\:$', line)
				if start:
					found = True
					stack.append(line)

	# stack
	lines = [line.rstrip() for line in stack if not re.search('^\s*$', line)]
	with open(out, 'wb') as f:
		f.write(os.linesep.join(lines))