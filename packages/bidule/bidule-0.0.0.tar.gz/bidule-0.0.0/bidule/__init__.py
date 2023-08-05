# without this file, everything works just fine
# however an application that needs to use our
# Machine class would need to do
# 
# from bidule.machine import Machine
# 
# so what if we want to break our code into 
# more modules and the class ends up in
# ./subpackage/machine.py or elsewhere ?
# 
# the point is, user apps whould not need to know
# about our internal choices, so it's safer if 
# one can simply do instead
#
# from bidule import Machine
# 

# and we achieve this with this simple line
# 
from .machine import Machine

# like always this will define is the current module
# - i.e. the bidule package - the global variable Machine
