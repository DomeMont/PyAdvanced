"""******************************************************************
Pick A-Part
date        19/07/2026
how_to      start()
author      Domenica Montesdeoca <https://www.linkedin.com/in/maydo3d/>
*******************************************************************"""

import os
from maya import mel
from maya import cmds

class PickAPart: 
    def __init__(self):
        self.ui_title = 'pick_a_part_ui'
        self.pick_a_part_ui() 
    
    def pick_a_part_ui(self):
        #Close if already exists
        if cmds.window(self.ui_title, exists=True):
            print('Duplicate window closed')
            cmds.deleteUI(self.ui_title)

        self.window = cmds.window(self.ui_title, title='Pick-A-Part', width=400)
        # cmds.columnLayout(adjustableColumn=True)
        cmds.columnLayout(adjustableColumn=True, columnAttach=('both', 10), rowSpacing=5)

        # ************************* SEPARATOR *********************************
        cmds.columnLayout(adjustableColumn=True)
        cmds.separator(height=5, style='none') 
        cmds.setParent('..')

        # ************************* SELECT MAIN GROUP NAME *********************
        cmds.text(label='SELECT MAIN GROUP NAME',
                  font='boldLabelFont',
                  align='center',
                  height=15)
        cmds.setParent('..')

        # ************************* MAIN GROUP NAME ***************************
        cmds.rowLayout(numberOfColumns=1, adjustableColumn=True)
        self.grp_name_text = cmds.textField(placeholderText='Main',
                                            width=250)
        cmds.setParent('..')

        # ************************* SEPARATOR *********************************
        cmds.columnLayout(adjustableColumn=True)
        cmds.separator(height=25) 
        cmds.setParent('..')

        # ************************* ADD PARTS TITLE ***************************
        cmds.text(label='ADD PARTS',
                  font='boldLabelFont',
                  align='center',
                  height=15)
        cmds.setParent('..')

        # ************************* ADD PARTS *********************************
        cmds.rowLayout(numberOfColumns=2, adjustableColumn2=2)
        self.part_select = cmds.optionMenuGrp(label='Part', 
                                  columnWidth2=(50,150))
        cmds.menuItem(label='Arm')
        cmds.menuItem(label='Leg')
        cmds.menuItem(label='Spine')
        cmds.menuItem(label='Neck')

        cmds.button(label='Add Part',
                    annotation='Adds the selected part to the rig',
                    width=200, 
                    command=self.add_part)
        cmds.setParent('..')

        # ************************* SEPARATOR ********************************
        cmds.columnLayout(adjustableColumn=True)
        cmds.separator(height=5, style='none') 
        cmds.setParent('..')

        # ************************* EDIT HIERARCHY ***************************
        cmds.frameLayout(label="Hierarchy", collapsable=True)

        self.hierarchy = cmds.treeView(numberOfButtons=0,
                                       allowDragAndDrop=True, 
                                       allowReparenting=True,
                                       height=100)
        cmds.setParent("..")

        # ************************* DELETE PART ******************************
        cmds.rowLayout(numberOfColumns=1, adjustableColumn=1)
        cmds.button(label='Delete Part',
                    annotation='Deletes the selected part in the hierarchy',
                    width=300, 
                    command=lambda *_: self.delete_confirm(' part'))
        cmds.setParent('..') 

        # Create / Delete Guides *******************************************
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=1)
        cmds.button(label='Create Guides',
                    annotation='',
                    width=300, 
                    command=self.create_guides)
        cmds.button(label='Delete Guides',
                    annotation='Deletes all guides',
                    width=100, 
                    command=lambda *_: self.delete_confirm(' guides'))
        cmds.setParent('..') 

        # Create / Delete Rig *******************************************
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=1)
        cmds.button(label='Create Rig',
                    annotation='',
                    width=300, 
                    command=self.create_rig)
        cmds.button(label='Delete Rig',
                    annotation='Deletes the rig',
                    width=100, 
                    command=lambda *_: self.delete_confirm(' rig'))
        cmds.setParent('..') 

        #*********************************************************************
        cmds.showWindow(self.window)

    def add_part(self, *args):
        current_part = cmds.optionMenuGrp(self.part_select, q=True, value=True)
        print('Added: ' + str(current_part))
        self.main_name = cmds.textField(self.grp_name_text, q=True, text=True)

        if not self.main_name:
            self.main_name = 'Main'

        print(self.main_name)

        self.add_to_hierarchy(part=current_part)

    def add_to_hierarchy(self, part, *args):
        main_exists = cmds.treeView(self.hierarchy, q=True, itemExists=self.main_name)
        print(main_exists)

        if main_exists == 0:
            cmds.treeView(self.hierarchy, edit=True, addItem=(self.main_name, ''))

        cmds.treeView(self.hierarchy, edit=True, addItem=(part, self.main_name))

    def get_items_hierarchy(self, *args):
        parts = cmds.treeView(self.hierarchy, q=True, children='')    
        self.all_parts = []

        for part in parts:
            self.all_parts.append(part)
               
        print(self.all_parts)

    def delete_part_hierarchy(self, *args):
        self.get_items_hierarchy()

        selected_parts = [part for part in self.all_parts if cmds.treeView(self.hierarchy, q=True, itemSelected=part)]
        
        for part in selected_parts: cmds.treeView(self.hierarchy, edit=True, removeItem=part)

    def create_guides(self, *args):
        print('Create guides')
        self.create_limb_guide()

    
    def create_limb_guide(self, *args):
        nr_guides = 4
        previous_loc = None
        self.grp_guides_list = []

        self.get_items_hierarchy()

        for part in self.all_parts[1:]:
            part_name = part
            print(part_name)

            for nr in range(nr_guides):
                loc_name = 'guide_' + str(part_name) + str(nr+1) + '_L'
                current_loc = cmds.spaceLocator(name=loc_name)[0]
                cmds.setAttr(str(loc_name) + 'Shape'+ '.localScale', 5.0, 5.0, 5.0)
                                
                if previous_loc:
                    cmds.parent(current_loc, previous_loc)
                    cmds.setAttr(str(current_loc) + '.translateX', 10)
                else:
                    guide_grp_name = 'grp_Guides_' + part + '_L'
                    cmds.group(current_loc, name=guide_grp_name, absolute=False)
                    self.grp_guides_list.append(guide_grp_name)

                previous_loc = current_loc

            previous_loc = None

        print('grp guides: ' + str(self.grp_guides_list))
        self.grp_guides = cmds.group( empty=True, name='grp_GUIDES' )
        cmds.parent(self.grp_guides_list, self.grp_guides)
                  
    def delete_guides(self, *args):
        print('Delete guides')
        cmds.delete(self.grp_guides)

    def create_main_part(self, *args):
        ctrl_global = 'ctl_Global_C'
        ctrl_main   = 'ctl_Main_C'
        main_ctrls  = [ctrl_global, ctrl_main]
        grp_main_ctrls = []
        size = 100 # cm

        cmds.circle(name=ctrl_global, normal=(0, 1, 0), radius=size*0.75)
        cmds.circle(name=ctrl_main, normal=(0, 1, 0), radius=size*0.65)

        for main_ctrl in main_ctrls: cmds.setAttr(main_ctrl + 'Shape' + '.overrideEnabled', 1)
        
        cmds.setAttr(ctrl_global + 'Shape' + '.overrideColor', 17)
        cmds.setAttr(ctrl_main + 'Shape' + '.overrideColor', 18)
            
        for main_ctrl in main_ctrls:
            cmds.delete(main_ctrl, constructionHistory=True)
            grp_main_ctrl = main_ctrl.replace('ctl_', 'grp_')
            cmds.group(main_ctrl, name=grp_main_ctrl)
            grp_main_ctrls.append(grp_main_ctrl)
        
        cmds.parent(grp_main_ctrls[1], ctrl_global)

        cmds.addAttr(ctrl_global, longName='Global_Scale', attributeType='float', defaultValue=1, 
                     minValue=1, maxValue=100, keyable=True)

    def create_skeleton(self, *args):
        cmds.select(deselect=True)
        self.joint_list = []

        for guide in self.guide_list[::-1]:
            guide_position = cmds.xform(guide, q=True, worldSpace=True, translation=True)
            jnt = cmds.joint(position=(guide_position[0], guide_position[1], guide_position[2]))
            self.joint_list.append(jnt)
        cmds.joint(self.joint_list,e=True, orientJoint='xyz', secondaryAxisOrient='yup')
        # cmds.select(deselect=True)

    def create_arm(self, custom_name, part, *args):
        arm_sections = ['Shoulder', 'Elbow', 'Wrist', 'EndHand']
        arm_systems  = ['','FK_', 'IK_']
        prefix_jnts  = 'jnt_'
        side = '_L'
         
        grp_guide  = 'grp_Guides_' + str(part) + str(side)
        grp_joints = 'grp_Joints_' + str(part) + str(side)

        self.guide_list = cmds.listRelatives(grp_guide, allDescendents=True, type="transform")
        cmds.group(empty=True, name=grp_joints)

        for nr_sys in range(len(arm_systems)):
            self.create_skeleton()
            cmds.parent(self.joint_list[0], grp_joints)
            
            for nr in range(len(arm_sections)):
                new_jnt_name = prefix_jnts + arm_systems[nr_sys] + arm_sections[nr] + custom_name + side
                cmds.rename(self.joint_list[nr], new_jnt_name)

        self.create_arm_fk(custom_name, part)
    
    def create_arm_fk(self, custom_name, part, *args):
        self.grp_controlsFK = 'grp_controls_FK_' + str(part)
        grp_controls = cmds.group(empty=True, name=self.grp_controlsFK)
        root_FK = 'jnt_FK_Shoulder' + custom_name + '_L'

        sys_jointsFK = cmds.listRelatives(root_FK,allDescendents=True)
        sys_jointsFK.append(root_FK)
        sys_jointsFK.pop(0)
        # sys_jointsFK.reverse()
        print(sys_jointsFK)

        #Create a control under a group
        for nr_j in range(len(sys_jointsFK)):
            control_name = sys_jointsFK[nr_j].replace('jnt_', 'ctl_')
            control_creation = cmds.circle(name=control_name, normal=(1, 0, 0), radius=5)
            # cmds.delete(control_name, constructionHistory=True) 

            group_name = sys_jointsFK[nr_j].replace('jnt_', 'off_')
            cmds.group(control_name, name = group_name)

            cmds.matchTransform(group_name, sys_jointsFK[nr_j])
            cmds.parentConstraint(control_name, sys_jointsFK[nr_j], maintainOffset=True)
            
            cmds.parent(cmds.ls(sl=True), self.grp_controlsFK)
        # cmds.parent(self.grp_controlsFK, self.main_grp)
        fk_offsets = cmds.listRelatives(self.grp_controlsFK, children=True, type='transform')

        for nr_off in range(len(fk_offsets[:-1])):
            fk_control = cmds.listRelatives(fk_offsets[nr_off+1], children=True, type='transform')
            cmds.parent(fk_offsets[nr_off], fk_control)

        # STRETCH FK
        off_elbowFK = 'off_FK_Elbow' + custom_name + '_L'
        off_wristFK = 'off_FK_Wrist' + custom_name + '_L'
        offs_FK = [str(off_elbowFK), str(off_wristFK)]

        for off_FK in offs_FK:
            ctrl_stretchFK = cmds.listRelatives(off_FK, parent=True, type='transform')[0]
            cmds.addAttr(ctrl_stretchFK, longName='Stretch', attributeType='float', defaultValue=1, 
                         minValue=1, maxValue=100, keyable=True)

            base_stretch = cmds.getAttr(str(off_FK) + '.translateX')

            mlt_UpperArmStretch_FK = "mlt_" + str(ctrl_stretchFK) + "Stretch"
            cmds.createNode("multiplyDivide", n=mlt_UpperArmStretch_FK)

            cmds.connectAttr(str(ctrl_stretchFK) + '.Stretch', str(mlt_UpperArmStretch_FK) + '.input1X')
            cmds.setAttr(str(mlt_UpperArmStretch_FK) + '.input2X', base_stretch)
            cmds.connectAttr(str(mlt_UpperArmStretch_FK) + '.outputX', str(off_FK) + '.translateX')

    def create_part(self, *args):
        self.get_items_hierarchy()

        for part in self.all_parts:
            if 'Arm' in part:
                print('creating an arm')
                custom_name = part.replace('Arm', '')
                self.create_arm(custom_name, part)

    def create_rig(self, *args):
        print('Create rig')
        self.create_main_part()
        self.create_part()

    def delete_rig(self, *args):
        print('Delete rig')

    def delete_confirm(self, step, *args):
        result = cmds.confirmDialog(title='DELETE',
                                    message='Delete last' + step + '?',
                                    messageAlign='center',
                                    button=['Yes', 'No'],
                                    defaultButton='Yes',
                                    cancelButton='No')
        if result == 'Yes':
            if step==' part':
                self.delete_part_hierarchy()
            elif step==' guides':
                self.delete_guides()
            elif step==' rig':
                self.delete_rig()


def start():
    global main_widget
    main_widget = PickAPart()
start()