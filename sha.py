#! /usr/bin/env python3

__author__        = "James Ng"
__copyright__     = "Copyright 2016 James Ng"
__license__       = "GPL"
__version__       = "1.0"
__maintainer__    = "James Ng"
__email__         = "jng@slt.net"
__status__        = ""

import hashlib
import argparse
import os
import sys

# --- options parsing and management
DEFAULT_BLOCK_SIZE = 8 * 1024 * 1024

pargs = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='return sha256 digest in hex for named files')
pargs.add_argument(dest='files', metavar='file', nargs='+', help='filename')
pargs.add_argument("-5", "--sha512", dest='sha512', action='count', help='generate sha2-512 digest')
pargs.add_argument("-b", "--block-size", dest='chunk', metavar="<size>",type=int, help='block size to read file, default 8192K', default=DEFAULT_BLOCK_SIZE)
#
args = pargs.parse_args();

# --- option validation
if args.chunk < 0:
	args.chunk = DEFAULT_BLOCK_SIZE

# --- check not needed, argparse ensures at least one file.
if len(args.files) == 0:
	exit(0)

# --- for throwing exceptions
class PathError(Exception):
	def __init__(self, path, message):
		self.path = path
		self.message = message

def sha256(p):
	# --- path validation, open() throws useful errmsg so these are really redundant
	if not os.path.exists(p):
		raise PathError(p, "File not found")
	if os.path.isdir(p):
		raise PathError(p, "Is a directory")
	if not os.path.isfile(p):
		raise PathError(p, "Not a file")

	if args.sha512:
		hasher = hashlib.sha512()
	else:
		hasher = hashlib.sha256()

	# --- read the file in chunks so we don't blow up memory
	with open(p, "rb") as f:
		buf = True
		while buf:
			buf = f.read(args.chunk)
			hasher.update(buf)
	return hasher.hexdigest()

for v in args.files:
	try:
		print("{} {}".format(sha256(v), v))
	except OSError as e:
		print("{}: {}".format(str(e.filename), e.strerror), file=sys.stderr)
	except PathError as e:
		print("{}: {}".format(e.path, e.message), file=sys.stderr)

