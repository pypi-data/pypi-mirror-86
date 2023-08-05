# relative imports from an entry point are cumbersome
# 
# the issue is that the __package__ attribute is used
# to determine what '.' means in a relative import
# 
# BUT
# 
# understandably __package__ is None in an entry point
# 
# so to use relative imports in an entry point like here
# you need to define __package__ manually
# which, well, is not too nice
# 
# but just to illustrate the mechanism:

# override only if not already set
__package__ = __package__ or 'bidule'

from .machine import Machine

instance = Machine("Hello World")
instance.main()
