"""******************************************************************
Pick-A-Part UI
content     UI

date        03/08/2026
dependency  Maya
how_to      start()

author      Domenica Montesdeoca <https://www.linkedin.com/in/maydo3d/>
*******************************************************************"""

import sys
import json
import importlib

from maya import mel
from maya import cmds

PATH = r'F:\TDA_Python_Adv\MontesdeocaApp\5_app'
sys.path.append(PATH)

import PickAPart as pick
importlib.reload(pick) 
    
def pick_a_part_ui(*args):
    ui_title = 'pick_a_part_ui'
    # Close if already exists
    if cmds.window(ui_title, exists=True):
        print('Duplicate window closed')
        cmds.deleteUI(ui_title)

    window = cmds.window(ui_title, title='Pick-A-Part', width=400)
    cmds.columnLayout(adjustableColumn=True, columnAttach=('both', 10), rowSpacing=5)

    # SEPARATOR ***********************************************************
    cmds.columnLayout(adjustableColumn=True)
    cmds.separator(height=5, style='none') 
    cmds.setParent('..')

    # SELECT MAIN GROUP NAME **********************************************
    main_grp_name = cmds.text(label ='SELECT MAIN GROUP NAME',
                                    font  ='boldLabelFont',
                                    align ='center',
                                    height=15)
    cmds.setParent('..')

    # MAIN GROUP NAME *****************************************************
    cmds.rowLayout(numberOfColumns=1, adjustableColumn=True)
    name_text = cmds.textField(placeholderText='Main',
                                        width=250)
    cmds.setParent('..')

    # SEPARATOR ***********************************************************
    cmds.columnLayout(adjustableColumn=True)
    cmds.separator(height=25) 
    cmds.setParent('..')

    # ADD PARTS TITLE *****************************************************
    cmds.text(label    = 'ADD PARTS',
                font   = 'boldLabelFont',
                align  = 'center',
                height = 15)
    cmds.setParent('..')

    # ADD PARTS ***********************************************************
    cmds.rowLayout(numberOfColumns=2, adjustableColumn2=2)
    part_select = cmds.optionMenuGrp(label='Part', 
                                            columnWidth2=(50,150))
    cmds.menuItem(label='Arm')
    cmds.menuItem(label='Leg')
    cmds.menuItem(label='Spine')
    cmds.menuItem(label='Neck')

    hierarchy = None

    cmds.button(label      = 'Add Part',
                annotation = 'Adds the selected part to the rig',
                width      = 200, 
                command    = lambda *_: pick.add_part(part_select, name_text, hierarchy)
                )
    cmds.setParent('..')

    # SEPARATOR **********************************************************
    cmds.columnLayout(adjustableColumn=True)
    cmds.separator(height=5, style='none') 
    cmds.setParent('..')

    # EDIT HIERARCHY *****************************************************
    cmds.frameLayout(label="Hierarchy", collapsable=True)

    hierarchy = cmds.treeView('Hierarchy_tree',
                              numberOfButtons=0,
                              allowDragAndDrop=True, 
                              allowReparenting=True,
                              height=100)
    cmds.setParent("..")

    # DELETE PART ********************************************************
    cmds.rowLayout(numberOfColumns=1, adjustableColumn=1)
    cmds.button(label     ='Delete Part',
                annotation='Deletes the selected part in the hierarchy',
                width     =300, 
                command   =lambda *_: pick.delete_confirm(' part')
                )
    cmds.setParent('..') 

    # Create / Delete Guides *********************************************
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=1)
    cmds.button(label     ='Create Guides',
                annotation='Creates all the needed guides',
                width     =300, 
                command   =lambda *_: pick.create_guides()
                )

    cmds.button(label     ='Delete Guides',
                annotation='Deletes all guides',
                width     =100, 
                command   =lambda *_: pick.delete_confirm(' guides')
                )
    cmds.setParent('..') 

    # Create / Delete Rig ************************************************
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=1)
    cmds.button(label     ='Create Rig',
                annotation='Creates the rig for all parts',
                width     =300, 
                command   =lambda *_: pick.create_rig()
                )

    cmds.button(label     ='Delete Rig',
                annotation='Deletes the rig',
                width     =100, 
                command   =lambda *_: pick.delete_confirm(' rig')
                )
    cmds.setParent('..') 

    #*********************************************************************
    cmds.showWindow(window)

# START ******************************************************************
def start():
    global main_widget
    main_widget = pick_a_part_ui()
    
start()