"""
content = assignment
course  = Python Advanced
 
date    = 14.11.2025
email   = contact@alexanderrichtertd.com

modified by = Domenica Montesdeoca
date = 16/07/2026 
"""

# original: logging.init.py

def findCaller(self):
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """
    # Currentframe() returns None if
    # IronPython isn't run with -X:Frames.
    current_fr = currentframe()

    if current_fr:
        current_fr = current_fr.fr_back
    
    while hasattr(current_fr, "fr_code"):
        code =  current_fr.fr_code
        file_name = os.path.normcase(code.co_filename)

        if file_name == _srcfile:
            current_fr = current_fr.fr_back
            continue
        
        return (code.co_filename, current_fr.fr_lineno, code.co_name)
        break
    return "(unknown file)", 0, "(unknown function)"

# How can we make this code better?
