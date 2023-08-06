# autotyper

A simple command line tool to write the contents of a file to the cursor after a delay of few seconds. It uses
the `pyautogui` package to simulate the keystrokes to write out the file where the cursor is placed.


## Installation

Make sure you have Python3 installed on your system. 

```
pip install autotyper
```

You will have the `autotyper` command available to go on your system.

## Usage

```
Write file/clipboard content on cursor

optional arguments:
  -h, --help   show this help message and exit

clipboard:
  --clipboard  copy from clipboard flag

file:
  -f FILE      input file path, not required for clipboard mode
  -d DELAY     delay in sec before writing to the cursor
```

```
$ autotyper -f bubblesort.c -d 10
Writing file content to cursor in 10 sec...
```

In this time, position your cursor to where you want to type out the text, when the delay ends, 
the content of the file will be written to the cursor. Can be used in online exams
to write the content of a file, where copy paste is not allowed in the text box.

```
$ autotyper --clipboard -d 10
Writing clipboard content to cursor in 10 sec...
```


The content of your clipboard will be pasted on the cursor after the specified delay

## License

Copyright (c) **Junaid H. Rahim**. All rights reserved. Licensed under the MIT License

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
