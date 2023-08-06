========
patelier
========

A Japanese text-line analyzing package


Function
-----------------------------

This project is to analyze text lines written in Japanese.

| You can provide the text lines by selecting a text file.
| The text file needs to be encoded in **UTF-8** or **Shift-JIS**.
| Each control code (0x00-0x1f) in the text lines is changed to '▲'.
| For example, a tab code in the text lines is changed to '▲'.

The analysis result is displayed.


**This "patelier" is still under development.**

| *Maybe in the future,*
| *the patelier may be able to display more information*
| *by analyzing text lines.*

I hope the patelier helps you a little.


Development Status
-----------------------------

Pre-Alpha (experiment)


Necessary Environment
-----------------------------

* **Microsoft Windows 10** (Tested with 64 bit version)
* **Python Ver.3.7** (Tested with Ver. 3.7.9)
* **pip** (Installed with Python) (Tested with Ver. 20.2.4)


Preferred  Environment
-----------------------------

* **Google Chrome** or **Microsoft Edge**


Dependency
-----------------------------

* **eel** (Tested with Ver. 0.14.0)
* **mecab-python-windows** (MeCab) (Tested with Ver. 0.996.3)
* **natsort** (Tested with Ver. 6.0.0)
* **pyperclip** (Tested with Ver. 1.7.0)
* **python-docx** (Tested with Ver. 0.8.10)
* **pywin32** (win32com) (Tested with Ver. 224)
* **regex** (Tested with Ver. 2019.3.12)


Setup
-----------------------------

command::

    py -3.7 -m pip install patelier


Usage
-----------------------------

command::

    patelier


Auther
-----------------------------

K2UNIT


License
-----------------------------

This software is released under the MIT License, see LICENSE.txt.


Notes
-----------------------------

This "patelier" is supposed to be used in Japan.

| The patelier is still under development.
| So, the patelier may suddenly be unpublished,
| and the license terms may be changed
| in the future (eg to the Apache license 2.0, etc.).
