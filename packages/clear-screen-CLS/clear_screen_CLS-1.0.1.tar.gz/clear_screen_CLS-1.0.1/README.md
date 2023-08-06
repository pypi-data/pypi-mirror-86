# CLear_Screen(cls)
Clear Screen for all OS's
**So you can use it in any script you want, it is very simple and practical for when you need to clean your terminal screen!
After you copy this file to a python path**
↓
↓
# *Example:*
#*Import script*

import cls

print("Hello world")


e = str(input("> "))

if e == 'clear':

   cls.cls()

# *Other Example:* 

#*Import script*

from cls import cls

print("Hello world")

e = str(input("> "))

if e == 'clear':

   cls()



