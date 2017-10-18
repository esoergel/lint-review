# Create unused imports
import os, re

# unused argument self
def thing(self):
    thing_two('arg1',
     'arg2'+'foo')  # wrong continued indentation
    print 'derp'

def thing_two(arg1, arg2):
    result=arg1*arg2  # bad whitespace
    if result <> arg1:
        print 'derp'
