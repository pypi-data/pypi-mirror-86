__version__ = '0.1.0'

"""
usage: __init__.py [-h] [--clipboard] -f FILE -d DELAY

Write file/clipboard content on cursor

optional arguments:
  -h, --help   show this help message and exit

clipboard:
  --clipboard  copy from clipboard flag

file:
  -f FILE      input file path, not required for clipboard mode
  -d DELAY     delay in sec before writing to the cursor
"""

from argparse import ArgumentParser
import os.path
import pyautogui
import time
import sys
import pyperclip
import random


def is_valid_file(parser, arg):
	if not os.path.exists(arg):
		parser.error(f"The file {arg} does not exist!")
	else:
		return open(arg, 'r')  # return an open file handle


def main():

	parser = ArgumentParser(
		description="Write file/clipboard content on cursor")

	clipboard_grp = parser.add_argument_group("clipboard")
	file_grp = parser.add_argument_group("file")

	clipboard_grp.add_argument(
		"--clipboard", action="store_true", help="copy from clipboard flag")

	file_grp.add_argument("-f", dest="filename", required="--clipboard" not in sys.argv,
						  help="input file path, not required for clipboard mode", metavar="FILE",
						  type=lambda x: is_valid_file(parser, x))

	file_grp.add_argument("-d", dest="delay", required=True,
						  help="delay in sec before writing to the cursor", type=int)
	args = parser.parse_args()

	if args.clipboard:
		print(f"Writing clipboard content to cursor in {args.delay} sec...")
		time.sleep(args.delay)

		clip_content = pyperclip.paste()

		for c in clip_content:
			x = random.randint(1, 10)
			time.sleep(0.029*x)
			pyautogui.write(c)
	else:
		print(f"Writing file content to cursor in {args.delay} sec...")
		time.sleep(args.delay)

		file_content = args.filename.read()

		for c in file_content:
			x = random.randint(1, 10)
			time.sleep(0.029*x)
			pyautogui.write(c)


if __name__ == "__main__":
	main()
