gilog2timesheet
===============

gitlog2timesheet is a tool to general timesheet from git repositories.

The hours spent per user per repository can be displayed. This can
be useful if you have to complete regular timesheet for european research
project or alike.

Usage
-----

        Usage: gitlog2timesheet.py path_to_git_repos path_to_git_repos...

        Options:
          -h, --help            show this help message and exit
          -d, --debug           output debug messages
          -w COMMITFACTOR, --commitfactor=COMMITFACTOR
                                work time factor per commit, default is 4 hours
          -t, --total           total hours worked for each user per
                                repository/project
          -f FORMAT, --outputformat=FORMAT
                                output format text, csv (default is text)
          -u USER, --user=USER  limit timesheet to the user specified
          -p, --previouslog     user previous date, or work time factor if less, 
                                for commit duration


Sample output
-------------


        gitlog2timesheet.py -t -w 4 /home/adulau/git/forban

        From Mon Apr  9 15:12:02 2012 to Mon Apr  9 16:12:02 2012
           Alexandre Dulaunoy (a@foo.be) worked on forban
            and did the following: Fixed #12 test if loot directory exists

        From Mon Apr  9 13:30:30 2012 to Mon Apr  9 14:30:30 2012
           Alexandre Dulaunoy (a@foo.be) worked on forban
            and did the following: Fixed #9 lootcleanup added

        From Mon Apr  9 12:41:42 2012 to Mon Apr  9 13:41:42 2012
           Alexandre Dulaunoy (a@foo.be) worked on forban
            and did the following: Fixed #10 The browsing is now naturally sorted.

        From Sun Apr  8 10:35:10 2012 to Sun Apr  8 11:35:10 2012
           Alexandre Dulaunoy (a@foo.be) worked on forban
            and did the following: Fixed #7 cleanup mode added
        ...
        Forban:Philippe Teuwen->12 hours.
        Forban:Alexandre Dulaunoy->964 hours.
        Forban:Olaf TNSB->4 hours.

Software required
-----------------

* Python 2.4 and up
* git

Note
----

Usually assuming that a commit has an amount of time spent on it is usually wrong.

But the tool is usually used for organizational structure requiring timesheet in a
strict format like who did what and when. You have been warned.

Similar tools
-------------

* http://wadobo.com/trac/dtt manage time dedication per task / project using distributed version control systems.

dtt is a real tracking system when you are doing development. gitlog2timesheet objective is to avoid the burden of creating
timesheets when you have already git repositories around.
