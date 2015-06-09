# python-dartmouthbanner
Python API for interacting with Dartmouth Banner.

This utilizes the requests library and some cookie setting to mimic a browser so that you can log in.
Currently, the class allow you to log in, logout, get your GPA and DBA levels, and add/drop courses given
the course ID.  New features will be coming soon.

### Usage

    from dartmouthbanner import BannerConnection
    
    connection = BannerConnection()
    connection.login("<username>", "<password>")
    
    print connection.gpa()
    print connection.dba()
    connection.addCourse(95799)
    connection.dropCourse(96111)
    
    connection.logout()

### Installation

For now, just download the dartmouthbanner.py file.  I'll make it more easily accessible with a setup.py file in a bit.
