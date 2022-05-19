# Xclass-Project

# TABLE OF CONTENTS

#### [INTRODUCTION](#introduction)

#### [INSTALLATION](#installation)

#### [RUN](#run)

### INTRODUCTION
MAKE SURE THAT PYTHON IS INSTALLED ON YOUR COMPUTER
https://www.python.org/downloads/

Project X backend and webapp
main.py used to host web application from Raspberry Pi



### INSTALLATION

Our program uses a number of different imports. In order for this code to compile, make sure to install all required modules prior to running. Copy and paste each line into the terminal.


```pip install flask```
```pip install opencv-python```
```pip install mediapipe```
```pip install keyboard```
```pip install results```
```pip install RPi.GPIO```
```pip install python-crontab``` 

IF ```pip``` doesn't work try using ```pip3``` instead

IF encountering permission related or errors add ```--user``` in the commands above, this helps us run commands as administrator.

### RUN

Make sure you are running this code on Raspberry Pi. Imports such as RPi.GPIO and crontab will only work on Raspberry Pi.

The main function hosts our server.

```
python main.py
```

Use the local server to open the web app. It should be in an IP form address.


### NOTES


### AUTHORS AND ACKNOWLEDGEMENTS

GJ everyone!


MIT License

Copyright (c) [2022] [ChiClass]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.