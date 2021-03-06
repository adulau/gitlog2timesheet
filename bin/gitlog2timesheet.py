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

def logmessage(name = None, email = None, when = None, message = None, repo = None, commitfactor = 4, format="text"):
    logmessage = ""
    t=datetime.datetime.fromtimestamp(when)
    nonecalculated = True 
    if options.previouslog:
        prevlogkey = name
        if prevlogkey in prevlogs:
            nonecalculated = False
            d=max(prevlogs[prevlogkey],t-datetime.timedelta(hours=commitfactor))
            #print unicode(prevlogs[prevlogkey])+"|"+unicode(t-datetime.timedelta(hours=commitfactor))+"|"+unicode(d)
            
    if nonecalculated:
        d=t-datetime.timedelta(hours=commitfactor)
        
    if options.total:
        if options.previouslog:
            timetoadd=((t-d).seconds/3600.0)
        else:
            timetoadd=commitfactor
            
        projectkey= repo+":"+name
        
        if projectkey in projecttime:
            projecttime[projectkey] += timetoadd
        else:
            projecttime[projectkey] = timetoadd
            
    if options.previouslog:
        prevlogkey= name
        prevlogs[prevlogkey]=t
        
    if format == "text":
        logmessage = "From "+d.ctime()+" to "+t.ctime() + "\n"
        logmessage += "   "+name+" ("+email+") worked on "+ repo +"\n"
        logmessage += "    and did the following: "+ message
    elif format == "csv":
        logmessage = d.ctime()+"|"+t.ctime()+"|"+unicode(round(timetoadd,2))+"|"+name+"|"+message
    return logmessage

usage = "usage: %s path_to_git_repos" % sys.argv[0]
parser = OptionParser(usage)
parser.add_option("-d", "--debug", action="store_true", dest="debug", help="output debug messages", default=False)
parser.add_option("-w", "--commitfactor", dest="commitfactor", help="work time factor per commit, default is 4 hours",default=4, type="int")
parser.add_option("-t", "--total", action="store_true", dest="total", help="total hours worked for each user per repository/project", default=False)
parser.add_option("-f", "--outputformat", dest="format", help="output format text, csv (default is text)", default="text", type="string")
parser.add_option("-u", "--user", dest="user", help="limit timesheet to the user specified", default=None, type="string")
parser.add_option("-p", "--previouslog", action="store_true", dest="previouslog", help="user previous date, or work time factor if less, for commit duration", default=False)

(options, args) = parser.parse_args()

if options.total:
    projecttime = {}
    
if options.previouslog:
    prevlogs={}
    
for repo in args:
    if not os.path.exists(repo):
        continue
    val = gitlog(location = repo)
    if options.debug:
        print val
    for line in reversed(val):
        try:
            (name, email, when, message) = line.split("|")
        except:
            continue
        if name == options.user or options.user is None:
            print logmessage(name=unicode(name), email=email, when=float(when), commitfactor = options.commitfactor, message=unicode(message), repo = os.path.basename(os.path.normpath(repo)), format=options.format)



if options.total:
    for x in projecttime:
        if options.format == "text":
            print x + "->" + unicode(int(round(projecttime[x],0)))+" hours."
        elif options.format == "csv":
            print x.split(":")[0]+"|"+x.split(":")[1]+"|"+unicode(int(round(projecttime[x],0)))
