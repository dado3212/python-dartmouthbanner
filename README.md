# python-dartmouthbanner
Python API for interacting with Dartmouth Banner.

This utilizes the requests library and some cookie setting to simplify programmatically interacting with Banner.

## How To Install

You can install python-dartmouthbanner using **pip**

    pip install python-dartmouthbanner
   
or via sources:

    python setup.py install

## Features

* Login/logout to Dartmouth Banner
* Get your GPA
* Get your DBA amount
* Add a course given course ID
* Drop a course given course ID

## Examples

### Login

    from dartmouthbanner import BannerConnection
    
    connection = BannerConnection()
    connection.login("<username>", "<password>")
    
### Try and get into a class
    from dartmouthbanner import BannerConnection
    from time import sleep
    
    connection = BannerConnection()
    connection.login("<username>", "<password>")
    
    n = 0
    while n != 1:
        n = connection.addCourse(95799)
        sleep(5)
    
    connection.logout()