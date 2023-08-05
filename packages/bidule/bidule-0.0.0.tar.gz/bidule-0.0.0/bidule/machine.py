# from a regular code module,
# when importing another module in the same
# package, it is generally nicer to use relative imports

from .helpers import helper

# of course you can always use complete import like in
# from bidule.helpers import helper

class Machine:

    def __init__(self, x):
        self.x = x

    def main(self):
        helper(f"object Machine({repr(self.x)})")
        return 0
