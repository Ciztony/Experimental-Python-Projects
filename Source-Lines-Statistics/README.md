# A lightweight line counter for various text-based files

### Supports many files like Python, C++, Text, and more

How to use:

- Click on the exe
- First question takes in the absolute or relative file path of your folder or file 
(if folder the code will recursively check for files)

- Type 'end' in the terminal if you want to end the session (any form is fine, 'end' is case-insensitive)

- Second question takes in the following syntax:

If you want the whole file to be counted, the syntax is as follows: file extension, another file extension
Example: json, txt

If you want to exclude comments, the syntax is as follows: file extension([opening delimiter | closing delimiter] ^ single comment type),
Example: cpp([/* | */] ^ //), py(#)

Notes:

- Multiline comments with code on the same line, excluding single comment types like #, may or may not be considered as a line
[The parser is complex and it was hard to parse it properly]
- Error handling is limited, so try to keep as close to the syntax as possible
- I may implement file and folder exclusion in the near future

_Crazy, the source Python file is under 10KB!!_

### Created by Ciztony 2025
