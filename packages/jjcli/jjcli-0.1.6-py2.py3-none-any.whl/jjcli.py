"""
python module for command-line filter

 python3 -m jjcli          ## for manual
 python3 -m jjcli skel     ## for a initial filter skeleton


 from jjcli import *       ## re.* functions also imported
 c=clfilter(opt="do:")     ## options in c.opt;
                           ##    autostrip  (def=True)
                           ##    inplace    (def=False) 

 for line in c.input():    ## process one rstriped line at the time
    ## process line

 for txt in c.slurp():     ## process one stripied text at the time
    ## process txt

 for par in c.paragraph(): ## process one stripied paragraph at the time
    ## process par

 c.lineno()                ## line number
 c.filelineno()
 c.parno()                 ## paragraph number
 c.fileparno()
 c.filename()
 c.filename()
 c.nextfile()
 c.isfirstline()

 ## subprocesses
 a=qx( "ls" )
 for x in qxlines("find | grep '\.jpg$'"): 
   ...
 qxsystem("vi aaa")

 imports all functions from re.*

"""

import subprocess 
from re import *    ## all re functions are imported!
import fileinput as F, getopt, sys
import csv

## execute external comands
def qx(*x)      : return subprocess.getoutput(x)
def qxlines(*x) : return subprocess.getoutput(x).splitlines()
def qxsystem(*x): subprocess.call(x,shell=True)

## Command line filters
class clfilter:
   '''csfilter - Class for command line filters'''
   
   def __init__(self,opt=None,rs="\n",autostrip=True,inplace=False):
       opcs=[]
       if opt:
           opts, args = getopt.getopt(sys.argv[1:],opt)
       else:
           opts = []
           args = []
       self.opt=dict(opts)
       self.args=args
       self.rs=rs
       self.autostrip=autostrip
       self.inplace=inplace
 
   def input(self,files=None): 
       files = files or self.args
       if self.autostrip:
           return map(lambda x:str(x).rstrip(),F.input(files=files,inplace=self.inplace))
       else:
           return F.input(files=files,inplace=self.inplace)

   def row(self,files=None):
       files = files or self.args
       return csv.reader(F.input(files=files))

   def paragraph(self,files=None):
       files = files or self.args or [None]
       self.parno_=0
       for f in files:
           t=""
           state=None
           self.fileparno_=0
           fs = [] if f == None else [f]
           for l in F.input(files=fs,inplace=self.inplace):
               if search(r'\S', l) and state == "inside delim":
                   self.parno_+= 1
                   self.fileparno_+= 1
                   if self.autostrip:
                       yield self.cleanpar(t)
                   else:
                       yield t
                   state ="inside par"
                   t=l
               elif search(r'\S', l) and state != "inside delim":
                   t += l
                   state ="inside par"
               else:
                   state ="inside delim"
                   t += l
           if search(r'\S',t):             ## last paragraph
               self.parno_+= 1
               self.fileparno_+= 1
               if self.autostrip:
                   yield self.cleanpar(t)
               else:
                   yield t

   def slurp(self,files=None):
       files = files or self.args or [None]
       for f in files:
           t=""
           fs = [] if f == None else [f]
           for l in F.input(files=fs,inplace=self.inplace):
               t += l
           if self.autostrip:
               yield self.clean(t)
           else:
               yield t

   def clean(self,s):              # clean: normalise end-of-line spaces and termination
       return sub(r'[ \r\t]*\n','\n',s)

   def cleanpar(self,s):           # clean: normalise end-of-line spaces and termination
       return sub(r'\s+$','\n' ,sub(r'[ \r\t]*\n','\n',s))

   filename    = lambda s : F.filename()      # inherited from fileinput
   filelineno  = lambda s : F.filelineno()
   lineno      = lambda s : F.lineno()
   fileparno   = lambda s : s.fileparno_
   parno       = lambda s : s.parno_
   nextfile    = lambda s : F.nextfile()
   isfirstline = lambda s : F.isfirstline()
   close       = lambda s : F.close()


__version__ = "0.1.6"

def main():
   if   len(sys.argv)==1: 
      print(__doc__)
   elif sys.argv[1] == "skel":
      print(
"""#!/usr/bin/python3.7
from jjcli import * 
c=clfilter(opt="do:")     ## options c.opt  in dictionary

for line in c.input():    ## process one line at the time
    ## process line

for txt in c.slurp():     ## process one file at the time
    ## process text
""")

if __name__ == "__main__": main()
