"""******************************************************************
Extra Pivot
date        17/07/2026
how_to      create()
author      Domenica Montesdeoca <https://www.linkedin.com/in/maydo3d/>
*******************************************************************"""

import os
from maya import mel
from maya import cmds

class ExtraPivot: 
    def __init__(self):
        self.ui_title = 'extra_pivot_ui'
        self.extra_pivot_ui() 
    
    def extra_pivot_ui(self):
        #Close if already exists
        if cmds.window(self.ui_title, exists=True):
            print('Duplicate window closed')
            cmds.deleteUI(self.ui_title)

        self.window = cmds.window(self.ui_title, title='Extra_Pivot', width=400)
        cmds.columnLayout(adjustableColumn=True)

        # ******************** Instructions Create Pivot ****************
        cmds.text(label ='Select the control that you wish to add a pivot to',
                  align ='center',
                  font  ='smallPlainLabelFont',
                  height=25)
        cmds.setParent('..')

        # Create / Delete Pivot *******************************************
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=1)
        cmds.button(label     ='Create Pivot',
                    annotation='Select the control that you wish to add a pivot to',
                    width     =300, 
                    command   =self.create_pivot)
        cmds.button(label     ='Delete Pivot',
                    annotation='Deletes the last created pivot',
                    width     =100, 
                    command   =lambda *_: self.delete_confirm(' pivot'))
        cmds.setParent('..') 

        #*********************************************************************
        cmds.showWindow(self.window)

    def create_pivot_ctrls(self, size, *args):
        selected_ctrl  = cmds.ls(selection=True)[0]
        self.base_ctrl  = selected_ctrl
        self.pivot_ctrl = str(self.base_ctrl) + '_pivot'

        crv_x  = cmds.circle(name=self.pivot_ctrl, normal=(1, 0, 0), radius=size)
        crv_z  = cmds.circle(name=self.pivot_ctrl+'02',normal=(0, 0, 1), radius=size)
        crv_x2 = cmds.circle(name=self.pivot_ctrl+'03',normal=(1, 0, 0), radius=size*0.75)
        crv_z2 = cmds.circle(name=self.pivot_ctrl+'04',normal=(0, 0, 1), radius=size*0.75)

        crvs_list = [crv_x[0], crv_z[0], crv_x2[0], crv_z2[0]]
        shape_list = []

        for crv in crvs_list[1:]:
            shape = str(crv) + 'Shape'
            shape_list.append(shape)

        cmds.select(shape_list)
        cmds.select(self.pivot_ctrl, add=True)
        mel.eval('parent -r -s')
        cmds.delete(self.pivot_ctrl, constructionHistory=True)

        for crv in crvs_list[1:]:
            cmds.delete(crv)

        # Create locator as ctrl offset
        self.off_pivot   = 'off_' + str(self.base_ctrl) + '_pivot'
        create_off_pivot = cmds.spaceLocator(name=self.off_pivot)

        cmds.setAttr(self.off_pivot + '.localScale', size*1.60, size*1.60, size*1.60)

        cmds.parent(self.pivot_ctrl, self.off_pivot)
        cmds.setAttr(self.off_pivot + '.overrideEnabled', 1)
        cmds.setAttr(self.off_pivot + '.overrideColor', 17)

        cmds.setAttr(self.pivot_ctrl + '.overrideEnabled', 1)
        cmds.setAttr(self.pivot_ctrl + '.overrideColor', 14)

        cmds.matchTransform(self.off_pivot, self.base_ctrl)

    def create_pivot(self, *args):
        self.create_pivot_ctrls(size=1)

        parent_ctrl = cmds.listRelatives(self.base_ctrl, parent=True, type='transform')

        print('Selected control: ' + str(self.base_ctrl))
        print('Parent control: ' + str(parent_ctrl))

        mult_matrix_off = cmds.createNode("multMatrix", name="mltMatrix_Offset")
        mult_matrix_ctrl = cmds.createNode("multMatrix", name="mltMatrix_Control")

        cmds.connectAttr(self.off_pivot + ".worldInverseMatrix", mult_matrix_off + ".matrixIn[0]")
        cmds.connectAttr(self.pivot_ctrl + ".xformMatrix", mult_matrix_off + ".matrixIn[1]")
        cmds.connectAttr(self.off_pivot + ".worldMatrix", mult_matrix_off + ".matrixIn[2]")

        if parent_ctrl != None:
            parent_ctrl = parent_ctrl[0]
            print('Parent controlAgain: ' + str(parent_ctrl))
            cmds.connectAttr(parent_ctrl + ".worldMatrix", mult_matrix_ctrl + ".matrixIn[0]")
            cmds.connectAttr(mult_matrix_off + ".matrixSum", mult_matrix_ctrl + ".matrixIn[1]")
            cmds.connectAttr(parent_ctrl + ".worldInverseMatrix", mult_matrix_ctrl + ".matrixIn[2]")
            
            cmds.connectAttr(mult_matrix_ctrl + ".matrixSum", self.base_ctrl + ".offsetParentMatrix", f=True)
        else:
            cmds.connectAttr(mult_matrix_off + ".matrixSum", self.base_ctrl + ".offsetParentMatrix", f=True)

    def delete_pivot(self, *args):
        pass

    def delete_confirm(self, *args):
        result = cmds.confirmDialog(title='DELETE',
                                    message='Delete last pivot?',
                                    messageAlign='center',
                                    button=['Yes', 'No'],
                                    defaultButton='Yes',
                                    cancelButton='No')
        if result == 'Yes':
                self.delete_pivot()
                print('Pivot deleted')

def start():
    global main_widget
    main_widget = ExtraPivot()
start()