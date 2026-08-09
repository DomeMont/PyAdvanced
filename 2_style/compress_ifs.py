"""
content = assignment
course  = Python Advanced
 
date    = 14.11.2025
email   = contact@alexanderrichtertd.com

modified by = Domenica Montesdeoca
date = 16/07/2026 
"""

from maya import cmds

# Replaced ifs statements with for loops
def set_color(ctrlList=None, color=None):
    colors = [4, 13, 25, 17, 17, 15, 6, 16]

    for ctrl in ctrlList:
        print(ctrl)
        cmds.setAttr(ctrl + 'Shape.overrideEnabled', 1)

        for nr in range(len(colors)):
            color = color - 1
            if color == nr:
                cmds.setAttr(ctrl + 'Shape.overrideColor', colors[nr])

# EXAMPLE
# set_color(['circle','circle1'], 8)

# I left the same colors (numbers) that were in the original script,
# even though there was a repeated number 