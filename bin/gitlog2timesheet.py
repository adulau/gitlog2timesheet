# -*- coding: utf-8 -*-
#
#    gitlog2timesheet - generate timesheet from git log
#
#    Copyright (C) 2009-2012 Alexandre Dulaunoy (a AT foo.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import subprocess
import os.path
import sys
import datetime
from optparse import OptionParser

def gitlog(location = None):
    if location is None or not os.path.exists(location):
        return None
    l = []
    cmd = ["git", "log", "--no-merges", "--simplify-merges", "--format=%an|%ae|%at|%s"]
    p = subprocess.Popen(cmd,cwd=location,stdout=subprocess.PIPE)
    output = p.stdout.read()
    for line in output.split("\n"):
        l.append(line)
    return l

def logmessage(name = None, email = None, when = None, message = None, repo = None, commitfactor = 4):
    logmessage = ""
    t=datetime.datetime.fromtimestamp(when)
    d=t-datetime.timedelta(hours=commitfactor)
   
    logmessage = "From "+d.ctime()+" to "+t.ctime() + "\n"
    logmessage += "   "+name+" ("+email+") worked on "+ repo +"\n"
    logmessage += "    and did the following: "+ message +"\n" 
    return logmessage

usage = "usage: %s path_to_git_repos" % sys.argv[0]
parser = OptionParser(usage)
parser.add_option("-d", "--debug", action="store_true" ,dest="debug", help="output debug messages", default=False)
parser.add_option("-w", "--commitfactor", dest="commitfactor", help="work time factor per commit, default is 4 hours",default=4, type="int")

(options, args) = parser.parse_args()

for repo in args:
    val = gitlog(location = repo)
    if options.debug:
        print val
    for line in val:
        try:
            (name, email, when, message) = line.split("|")
        except:
            continue 
        print logmessage(name=unicode(name), email=email, when=float(when), commitfactor = options.commitfactor, message=unicode(message), repo = os.path.basename(os.path.normpath(repo)))

        
