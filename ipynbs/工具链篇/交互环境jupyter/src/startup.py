
#coding:utf-8
from __future__ import print_function
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
from IPython.core.interactiveshell import InteractiveShell
from IPython.lib.pretty import pretty as _pretty
sh = InteractiveShell.instance()

def pretty(obj):
    import numpy as np
    if isinstance(obj, np.ndarray):
        return np.array2string(obj, separator=", ")
    else:
        return _pretty(obj)

# The class MUST call this class decorator at creation time
@magics_class
class MyMagics(Magics):

    @line_magic
    def goodlook_list(self, line):
        """
            %col number_of_column code
            """
        pos = line.find(" ")
        n = int(line[:pos])
        code = line[pos+1:]
        result = pretty(sh.ev(code)).split("\n")
        max_width = max(len(line) for line in result) + 3
        result = [line.ljust(max_width) for line in result]
        result = "\n".join(["".join(result[i:i+n]) for i in xrange(0, len(result), n)])
        print(result)
        
    @line_magic
    def exec_py2(self, line):
        """
        pass all the arguments to a new python2 process
        """
        import subprocess
        cmd = "python " + line
        subprocess.Popen(cmd, shell=True)

    @line_magic
    def exec_py3(self, line):
        """
        pass all the arguments to a new python3 process
        """
        import subprocess
        cmd = "python3 " + line
        subprocess.Popen(cmd, shell=True)
    @line_magic
    def exec_pypy(self, line):
        """
        pass all the arguments to a new pypy process
        """
        import subprocess
        cmd = "pypy " + line
        subprocess.Popen(cmd, shell=True)
        
ip = get_ipython()
# You can register the class itself without instantiating it.  IPython will
# call the default constructor on it.
ip.register_magics(MyMagics)
    