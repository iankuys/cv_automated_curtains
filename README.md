# cv_automated_curtains (remotely controlled automated curtains)

# TABLE OF CONTENTS

#### [INTRODUCTION](#introduction)

#### [INSTALLATION](#installation)

#### [RUN](#run)

#### [FUNCTION DOCUMENTATION](#documentation)

#### [ENDPOINTS](#endpoints)


## INTRODUCTION

MAKE SURE THAT PYTHON IS INSTALLED ON YOUR COMPUTER
https://www.python.org/downloads/

Project X backend and webapp
main.py used to host web application from Raspberry Pi

### Coding Guidelines
| Language   | Guideline | Tools |
|------------|-----------|-------|
| Python     |[Python Guideline](https://peps.python.org/pep-0008/)           | [Flask](https://flask.palletsprojects.com/en/2.1.x/ )     |
| JavaScript |[JavaScript Guideline](https://developer.mozilla.org/en-US/docs/MDN/Guidelines/Code_guidelines/JavaScript#general_javascript_guidelines)|       |
| CSS        |[CSS Guideline](https://developer.mozilla.org/en-US/docs/MDN/Guidelines/Code_guidelines/CSS)      |       |
| HTML       |[HTML Guideline](https://developer.mozilla.org/en-US/docs/MDN/Guidelines/Code_guidelines/HTML)      |       |



## INSTALLATION

Our program uses a number of different imports. In order for this code to compile, make sure to install all required modules prior to running. Copy and paste each line into the terminal.


```pip install .```

IF ```pip``` doesn't work try using ```pip3``` instead

IF encountering permission related or errors add ```--user``` in the commands above, this helps us run commands as administrator.




## RUN

Make sure you are running this code on Raspberry Pi. Imports such as RPi.GPIO and crontab will only work on Raspberry Pi.

The main function hosts our server.

```
python main.py
```

Use the local server to open the web app. It should be in an IP form address.

## DOCUMENTATION

### main.py
This module contains functions and a class that controls the Caring Curtain's movement and gesture control component.

```fingerPosition(image, handNo=0)```
Defines finger position as well as setting up for hand gestures.

>**Parameters:**
image: static picture passed with camera
handNo: int

>**Returns:**
List with finger position; each item is a 3-tuple withan id and the x and y coordinates

```cronConfig(x,y,z)```
Configures CronTab in Pi OS. Depending on the z parameter, this function will set a command regarding opening or closing the curtain.

>**Parameters:**
x: hours
y: minutes
z: 'open' or 'close'

```ChiCurtain.openCurtain()```
Opens curtain.

```ChiCurtain.closeCurtain()```
Closes curtain.

```ChiCurtain.stopCurtain()```
Stops curtain.

```index()```
Generates output from a template file(index.html) for root URL.

>**Returns:**
render_template function from the flask.templating package that renders template file

```openTimer()```
Gets data from time form for advanced scheduling.

>**Returns:**
Redirects to a /timerCheck/x/y/z with data from form, with 'open' as the z parameter.

```closeTimer()```
Gets data from time form for advanced scheduling.

>**Returns:**
Redirects to a /timerCheck/x/y/z with data from form, with 'close' as the z parameter.

```timerCheck(x,y,z)```
    Calls cronConfig(x,y,z) to create a             scheduled job.
>**Parameters:**
    x: hours
    y: minutes
    z: action ('open' or 'close')
    
>**Returns:**
    'success' - used for testing purposes


```home()```
    Opens our chiCurtain instance. Prints 'hello from open' for testing purposes.
>**Returns:**
'hi' - used for testing purposes

```close_manual()```
    Closes our chiCurtain instance. Prints 'hello from close' for testing purposes.
>**Returns:**
'hi' - used for testing purposes

```capture_gesture()```
    Captures gesture by using multiple static images. Adds amount of fingers held up based on data returned from fingerPosition(). According to amount of fingers, this function will open or close our chiCurtain instance.



# ENDPOINTS

## Open Timer
This endpoint sends user-inputted data to add/update the scheduled time for opening the curtain.

### Path

```http 
POST /openTimer
```

### Response
```
HTTP/1.1 201 Created
Status: 201 Created

{
    name: 'client'
    time: '00:00'
}
```
Note: time is in military time and varies based on user input

## Close Timer
This endpoint sends user-inputted data to add/update the scheduled time for closing the curtain.

### Path

```http 
POST /closeTimer
```

### Response
```
HTTP/1.1 201 Created
Status: 201 Created

{
    name: 'client'
    time: '00:00'
}
```

Note: time is in military time and varies based on user input

## Timer Check
This endpoint accepts time as a path parameter.

### Path

```http 
GET /timerCheck/<x>/<y>/<z>
```

### Response
```
HTTP/1.1 200 OK
Status: 200 OK

{
    name: 'client'
    x: <x>
    y: <y>
    z: <z>
}
```

## Open
This endpoint sets time to *now* to open curtain manually.

### Path

```http 
POST /open
```

### Response
```
HTTP/1.1 200 OK
Status: 200 OK

{
    name: 'client'
    time: 'now'
}
```

## Close
This endpoint sets time to *now* to close curtain manually.

### Path

```http 
POST /close
```

### Response
```
HTTP/1.1 200 OK
Status: 200 OK

{
    name: 'client'
    time: 'now'
}
```


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
