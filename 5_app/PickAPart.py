"""******************************************************************
Pick A-Part
content     creates rigging systems based on the added 
            parts under the same hierarchy

date        22/07/2026
dependency  Maya, Mel
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
        cmds.columnLayout(adjustableColumn=True, columnAttach=('both', 10), rowSpacing=5)

        # ************************* SEPARATOR *********************************
        cmds.columnLayout(adjustableColumn=True)
        cmds.separator(height=5, style='none') 
        cmds.setParent('..')

        # ************************* SELECT MAIN GROUP NAME *********************
        self.main_grp_name = cmds.text(label ='SELECT MAIN GROUP NAME',
                                       font  ='boldLabelFont',
                                       align ='center',
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
        cmds.text(label ='ADD PARTS',
                  font  ='boldLabelFont',
                  align ='center',
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

        cmds.button(label     ='Add Part',
                    annotation='Adds the selected part to the rig',
                    width     =200, 
                    command   =self.add_part)
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
        cmds.button(label     ='Delete Part',
                    annotation='Deletes the selected part in the hierarchy',
                    width     =300, 
                    command   =lambda *_: self.delete_confirm(' part'))
        cmds.setParent('..') 

        # Create / Delete Guides *******************************************
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=1)
        cmds.button(label     ='Create Guides',
                    annotation='Creates all the needed guides',
                    width     =300, 
                    command   =self.create_guides)

        cmds.button(label     ='Delete Guides',
                    annotation='Deletes all guides',
                    width     =100, 
                    command   =lambda *_: self.delete_confirm(' guides'))
        cmds.setParent('..') 

        # Create / Delete Rig *******************************************
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=1)
        cmds.button(label     ='Create Rig',
                    annotation='Creates the rig for all parts',
                    width     =300, 
                    command   =self.create_rig)

        cmds.button(label     ='Delete Rig',
                    annotation='Deletes the rig',
                    width     =100, 
                    command   =lambda *_: self.delete_confirm(' rig'))
        cmds.setParent('..') 

        #*********************************************************************
        cmds.showWindow(self.window)

    # PARTS HIERARCHY ******************************************************************
    def add_part(self, *args):
        # Gets the part in the drop down menu
        current_part   = cmds.optionMenuGrp(self.part_select, q=True, value=True)
        self.MAIN_NAME = cmds.textField(self.grp_name_text, q=True, text=True)

        print('Added: ' + str(current_part))

        if not self.MAIN_NAME:
            self.MAIN_NAME = 'Main'

        print('Main name: ' + str(self.MAIN_NAME))

        self.add_to_hierarchy(part=current_part)

    def add_to_hierarchy(self, part, *args):
        main_exists = cmds.treeView(self.hierarchy, q=True, itemExists=self.MAIN_NAME)

        if main_exists == 0:
            cmds.treeView(self.hierarchy, edit=True, addItem=(self.MAIN_NAME, ''))

        cmds.treeView(self.hierarchy, edit=True, addItem=(part, self.MAIN_NAME))

    def get_items_hierarchy(self, *args):
        parts = cmds.treeView(self.hierarchy, q=True, children='')    
        self.all_parts = []

        for part in parts: self.all_parts.append(part)
               
        print('Parts: ' + str(self.all_parts))

    def delete_part_hierarchy(self, *args):
        self.get_items_hierarchy()

        selected_parts = [part for part in self.all_parts if cmds.treeView(self.hierarchy, q=True, itemSelected=part)]
        
        for part in selected_parts: cmds.treeView(self.hierarchy, edit=True, removeItem=part)
   
    # GUIDES CREATION ******************************************************
    def create_guides(self, *args):
        print('**Create guides**')
        self.get_items_hierarchy()
        self.grp_guides_list = []

        for part in self.all_parts:
            if 'Arm' in part:
                print('creating an arm guide')
                custom_name = part.replace('Arm', '')
                self.create_limb_guide(part, nr_guides=4) 
            elif 'Leg' in part:
                print('creating a leg guide')
                custom_name = part.replace('Leg', '')
                self.create_limb_guide(part, nr_guides=4, tr=(0, -10, 0)) 
        
        self.grp_guides = cmds.group( empty=True, name='grp_GUIDES' )
        cmds.parent(self.grp_guides_list, self.grp_guides)
 
    def create_limb_guide(self, part, nr_guides, tr=(10,0,0),*args):
        """
        Args:
            part (str): The selected part (Arm, Leg)
            nr_guides (int): The number of guides that are created
            tr (int): Direction in which the guides will be created. Defaults to (10,0,0).
        """
        previous_loc = None

        for nr in range(nr_guides):
            loc_name = 'guide_' + str(part) + str(nr+1) + '_L'
            current_loc = cmds.spaceLocator(name=loc_name)[0]
            cmds.setAttr(str(loc_name) + 'Shape'+ '.localScale', 5.0, 5.0, 5.0)
                            
            if previous_loc:
                cmds.parent(current_loc, previous_loc)
                cmds.setAttr(str(current_loc) + '.translate', tr[0], tr[1] ,tr[2])
            else:
                guide_grp_name = 'grp_Guides_' + part + '_L'
                cmds.group(current_loc, name=guide_grp_name, absolute=False)
                self.grp_guides_list.append(guide_grp_name)

            previous_loc = current_loc
        
        # Create a guide for a Pole Vector
        loc_poleV = 'guide_PoleVector_' + str(part) + '_L'
        cmds.spaceLocator(name=loc_poleV)[0]
        cmds.setAttr(str(loc_poleV) + 'Shape'+ '.localScale', 5.0, 5.0, 5.0)

        cmds.parent(loc_poleV, guide_grp_name)

        print('grp guides: ' + str(self.grp_guides_list))
                  
    def delete_guides(self, *args):
        print('**Delete guides**')
        cmds.delete(self.grp_guides)

    # PARTS CREATION / RIG CREATION *****************************************************
    def create_main_part(self, *args):
        """Creates the main group and controls for the rig
        """
        self.GRP_ALL   = 'grp_' + self.MAIN_NAME
        CTRL_GLOBAL    = 'ctl_Global_C'
        self.CTRL_MAIN = 'ctl_Main_C'
                
        main_ctrls  = [CTRL_GLOBAL, self.CTRL_MAIN]
        grp_main_ctrls = []
        size = 100 # cm

        cmds.circle(name=CTRL_GLOBAL, normal=(0, 1, 0), radius=size*0.75)
        cmds.circle(name=self.CTRL_MAIN, normal=(0, 1, 0), radius=size*0.65)

        for main_ctrl in main_ctrls: cmds.setAttr(main_ctrl + 'Shape' + '.overrideEnabled', 1)
        
        cmds.setAttr(CTRL_GLOBAL + 'Shape' + '.overrideColor', 17)
        cmds.setAttr(self.CTRL_MAIN + 'Shape' + '.overrideColor', 18)
            
        for main_ctrl in main_ctrls:
            cmds.delete(main_ctrl, constructionHistory=True)
            grp_main_ctrl = main_ctrl.replace('ctl_', 'grp_')
            cmds.group(main_ctrl, name=grp_main_ctrl)
            grp_main_ctrls.append(grp_main_ctrl)
        
        cmds.parent(grp_main_ctrls[1], CTRL_GLOBAL)
        cmds.group(grp_main_ctrls[0], name = self.GRP_ALL)

        cmds.addAttr(CTRL_GLOBAL, longName='Global_Scale', attributeType='float', defaultValue=1, 
                                  minValue=1, maxValue=100, keyable=True)

    def create_skeleton(self, or_j, sec_axis, *args):
        """
        Args:
            or_j (str): Joint orientation
            sec_axis (str): Secondary axis orientation
        """
        cmds.select(deselect=True)
        self.joint_list = []

        for guide in self.guide_list[::-1]:
            guide_position = cmds.xform(guide, q=True, worldSpace=True, translation=True)
            jnt = cmds.joint(position=(guide_position[0], guide_position[1], guide_position[2]))
            self.joint_list.append(jnt)

        cmds.joint(self.joint_list,e=True, orientJoint=or_j, secondaryAxisOrient=sec_axis)
        cmds.joint(self.joint_list[-1], e=True, orientJoint='none')

    def create_parts(self, *args):
        self.get_items_hierarchy()

        for part in self.all_parts:
            if 'Arm' in part:
                print('Creating an arm')
                custom_name = part.replace('Arm', '')
                self.create_limb(custom_name, part)
            elif 'Leg' in part:
                print('Creating a leg')
                custom_name = part.replace('Leg', '')
                self.create_limb(custom_name, part) 

    def create_rig(self, *args):
        print('Create rig')
        self.create_main_part()
        self.create_parts()

    def delete_rig(self, *args):
        print('Delete rig')
      
    def create_limb(self, custom_name, part, *args):
        """Creates the rigging system for limbs

        Args:
            custom_name (str): The added str in case the name part was edited
            part (str): The selected part (Arm, Leg)
        """
        self.limb_sys = ['','FK_', 'IK_']
        self.limb_sections = [] 
        self.prefix_jnts = 'jnt_'
        self.side = '_L'
        
        if 'Arm' in part:
            self.limb_sections = ['Shoulder', 'Elbow', 'Wrist', 'EndHand']
            or_j     = 'xyz'
            sec_axis = 'yup'

        elif 'Leg' in part:
            self.limb_sections = ['Hip', 'Knee', 'Ankle', 'EndFoot']
            or_j     = 'xyz' 
            sec_axis = 'zup'
         
        grp_guide  = 'grp_Guides_' + str(part) + str(self.side)
        grp_joints = 'grp_Joints_' + str(part) + str(self.side)

        self.guide_list = cmds.listRelatives(grp_guide, allDescendents=True, type="transform")
        self.guide_poleV = self.guide_list[-1]
        self.guide_list.pop(-1)
        cmds.group(empty=True, name=grp_joints)

        # Create skeleton for main, FK and IK systems
        for nr_sys in range(len(self.limb_sys)):
            self.jnt_listIK = []
            self.create_skeleton(or_j, sec_axis)
            cmds.parent(self.joint_list[0], grp_joints)
            
            for nr in range(len(self.limb_sections)):
                new_jnt_name = self.prefix_jnts + self.limb_sys[nr_sys] + self.limb_sections[nr] + custom_name + self.side
                cmds.rename(self.joint_list[nr], new_jnt_name)
                print('Original joint: ' + str(self.joint_list[nr]))
                print('New joint: ' + new_jnt_name)
                self.jnt_listIK.append(new_jnt_name)

        cmds.parent(grp_joints, self.GRP_ALL)

        self.create_limb_fk(custom_name, part)
        self.create_limb_ik(custom_name, part)
        self.fkik_blend(custom_name, part)
    
    def create_limb_fk(self, custom_name, part, *args):
        """
        Args:
            custom_name (str): The added str in case the name part was edited
            part (str): The selected part (Arm, Leg)
        """
        self.grp_controlsFK = 'grp_controls_FK_' + str(part)
        grp_controls = cmds.group(empty=True, name=self.grp_controlsFK)
        root_FK = 'jnt_FK_' + self.limb_sections[0] + custom_name + self.side

        # Get the list of joints for FK
        sys_jointsFK = cmds.listRelatives(root_FK,allDescendents=True)
        sys_jointsFK.append(root_FK)
        sys_jointsFK.pop(0)
        print(sys_jointsFK)

        fk_offsets = []

        for nr_j in range(len(sys_jointsFK)):
            # Create FK controls
            ctl_name = sys_jointsFK[nr_j].replace('jnt_', 'ctl_')
            self.create_custom_controls('circle', ctl_name, 4)
 
            off_name = ctl_name.replace('ctl_', 'off_')

            # Position and parent constraint FK controls
            cmds.matchTransform(off_name, sys_jointsFK[nr_j])
            cmds.parentConstraint(ctl_name, sys_jointsFK[nr_j], maintainOffset=True)
            
            cmds.parent(cmds.ls(sl=True), self.grp_controlsFK)
            fk_offsets.append(off_name)

        # Create hierarchy FK controls
        for nr_off in range(len(fk_offsets[:-1])):
            fk_control = fk_offsets[nr_off+1].replace('off', 'ctl')
            cmds.parent(fk_offsets[nr_off], fk_control)

        cmds.parent(self.grp_controlsFK, self.CTRL_MAIN)

        # STRETCH FK
        off_midFK = 'off_FK_' + self.limb_sections[1] + custom_name + self.side
        off_endFK = 'off_FK_' + self.limb_sections[2] + custom_name + self.side
        offs_FK = [str(off_midFK), str(off_endFK)]

        for off_FK in offs_FK:
            ctrl_stretchFK = cmds.listRelatives(off_FK, parent=True, type='transform')[0]
            
            # Create Stretch attribute
            cmds.addAttr(ctrl_stretchFK, longName='Stretch', attributeType='float', defaultValue=1, 
                                         minValue=1, maxValue=100, keyable=True)

            # Connections Stretch attribute (Nodes)
            base_stretch = cmds.getAttr(str(off_FK) + '.translateX')

            mlt_UpperArmStretch_FK = "mlt_" + str(ctrl_stretchFK) + "Stretch"
            cmds.createNode("multiplyDivide", n=mlt_UpperArmStretch_FK)

            cmds.connectAttr(str(ctrl_stretchFK) + '.Stretch', str(mlt_UpperArmStretch_FK) + '.input1X')
            cmds.setAttr(str(mlt_UpperArmStretch_FK) + '.input2X', base_stretch)
            cmds.connectAttr(str(mlt_UpperArmStretch_FK) + '.outputX', str(off_FK) + '.translateX')

    def create_limb_ik(self, custom_name, part, *args):
        """
        Args:
            custom_name (str): The added str in case the name part was edited
            part (str): The selected part (Arm, Leg)
        """
        self.grp_controlsIK = 'grp_controls_IK_' + str(part)
        grp_controls = cmds.group(empty=True, name=self.grp_controlsIK)
        
        # IK Controls names
        ctrl_baseIK = 'ctl_IK' + self.limb_sections[0] + custom_name + 'Base' + self.side
        ctrl_poleIK = 'ctl_' + part + 'PoleVector' + self.side
        ctrl_endIK  = 'ctl_IK' + self.limb_sections[2] + custom_name + self.side
        ctrl_rotIK  = 'ctl_IKRot' + self.limb_sections[2] + custom_name + self.side
        ctrls_limbIK = [ctrl_baseIK, ctrl_poleIK, ctrl_endIK, ctrl_rotIK]  
        offs_limbIK  = []

        # Get controls offset groups 
        for nr in range(len(ctrls_limbIK)):
            offs = ctrls_limbIK[nr].replace('ctl_', 'off_')
            offs_limbIK.append(offs)

        off_baseIK, off_poleIK, off_endIK, off_rotIK = offs_limbIK

        print('IK Joints: ' + str(self.jnt_listIK))

        # Create controls 
        self.create_custom_controls('lever', ctrl_baseIK, 4)
        self.create_custom_controls('cone', ctrl_poleIK, 4)
        self.create_custom_controls('cube', ctrl_endIK, 4)
        self.create_custom_controls('sphere', ctrl_rotIK, 4)
        

        for nr in range(len(ctrls_limbIK)):
            cmds.matchTransform(offs_limbIK[nr], self.jnt_listIK[nr])
        
        if 'Leg' in part: cmds.setAttr(str(off_endIK) + '.rotate', 0, 0, 0) # Makes IK Leg orient to world
        cmds.matchTransform(off_rotIK, self.jnt_listIK[2])
        cmds.matchTransform(off_poleIK, self.guide_poleV)

        cmds.parent(off_poleIK, ctrl_endIK)
        cmds.parent(off_baseIK, off_endIK, self.grp_controlsIK)
        cmds.parent(self.grp_controlsIK, self.CTRL_MAIN)

        # Create IK
        IK_name      = part + custom_name + str("IK")
        IK_handle    =  str('ikH_') + IK_name + self.side
        ctl_ikH_name = ctrl_endIK

        IK_start_jnt = self.jnt_listIK[0]
        IK_end_jnt   =self.jnt_listIK[2]

        cmds.ikHandle(name=IK_handle, startJoint=IK_start_jnt, endEffector=IK_end_jnt, solver='ikRPsolver')
        effector = cmds.ikHandle(IK_handle, q=True,  endEffector=True)
        eff_name = str('eff_') + IK_name + self.side
        cmds.rename(effector, eff_name)
        cmds.poleVectorConstraint(ctrl_poleIK, IK_handle)

        cmds.parent(IK_handle, ctrl_rotIK)
        cmds.parent(off_rotIK, ctrl_endIK)

        cmds.parentConstraint(ctrl_baseIK, IK_start_jnt) 
        cmds.orientConstraint(ctrl_rotIK, IK_end_jnt)

        # TODO Create Soft IK

    def fkik_blend(self, custom_name, part, *args):
        """Creates the FK / IK  switch

        Args:
            custom_name (str): The added str in case the name part was edited
            part (str): The selected part (Arm, Leg)
        """
        self.jnt_listFK = []
        self.jnt_list   = []

        # Create list with joints for different systems
        for nr in range(len(self.jnt_listIK)):
            jnt_FK= self.jnt_listIK[nr].replace('IK_', 'FK_')
            self.jnt_listFK.append(jnt_FK)

            jnt= self.jnt_listIK[nr].replace('IK_', '')
            self.jnt_list.append(jnt)

        print('skeleton main:' + str(self.jnt_list))
        print('skeleton FK:' + str(self.jnt_listFK))
        print('skeleton IK:' + str(self.jnt_listIK))

        # Create names for FK /IK switch control and system
        name = part + custom_name
        ctl_switch_name = 'ctl_IKFK_' + name
        ctl_switch = self.create_custom_controls('cube', ctl_switch_name, 3)

        cmds.makeIdentity(ctl_switch_name, apply=True)
        cmds.addAttr(ctl_switch_name, longName= 'FK_IK', shortName='FK_IK', keyable=True, attributeType='float', 
                                      defaultValue=0.0, minValue=0.0, maxValue=1.0)

        self.off_switch_name = ctl_switch_name.replace('ctl_', 'off_')

        # Constraint switch under limb system and parent under main controls
        cmds.parentConstraint(self.jnt_list[0], self.off_switch_name, maintainOffset=False, skipRotate=['x', 'y', 'z'])
        cmds.parent(self.off_switch_name, self.CTRL_MAIN)

        # FK / IK switch via blend colors (Nodes)
        self.blc_rotation_list = []
        self.blc_translation_list = []
        for nr_j in range(len(self.jnt_list)):
            print(self.jnt_list[nr_j])
            blc_name = self.jnt_list[nr_j].split('_')[1:]
            blc_name = '_'.join(blc_name)
            
            blc_rotation = 'blc_Rotation' + blc_name
            cmds.createNode('blendColors', n=blc_rotation)
            cmds.connectAttr(self.jnt_listIK[nr_j] + '.rotate', blc_rotation + '.color1', f=True)
            cmds.connectAttr(self.jnt_listFK[nr_j] + '.rotate', blc_rotation + '.color2', f=True)
            cmds.connectAttr(blc_rotation + '.output', self.jnt_list[nr_j] + '.rotate', f=True)
            self.blc_rotation_list.append(blc_rotation)

            blc_translation = 'blc_Translation' + blc_name
            cmds.createNode('blendColors', n=blc_translation)
            cmds.connectAttr(self.jnt_listIK[nr_j] + '.translate', blc_translation + '.color1', f=True)
            cmds.connectAttr(self.jnt_listFK[nr_j] + '.translate', blc_translation + '.color2', f=True)
            cmds.connectAttr(blc_translation + '.output', self.jnt_list[nr_j] + '.translate', f=True)
            self.blc_translation_list.append(blc_translation)

        print('Blend color nodes created:')
        print(self.blc_rotation_list, self.blc_translation_list)

        cmds.connectAttr(ctl_switch_name + '.FK_IK', self.blc_rotation_list[0] + '.blender', f=True)
        cmds.connectAttr(ctl_switch_name + '.FK_IK', self.blc_translation_list[0] + '.blender', f=True)

        for nr in range(len(self.blc_rotation_list[:-1])):
            print(self.blc_rotation_list[nr])
            cmds.connectAttr(self.blc_rotation_list[nr] + '.blender', self.blc_rotation_list[nr+1] + '.blender', f=True)

        for nr in range(len(self.blc_translation_list[:-1])):
            print(self.blc_translation_list[nr])
            cmds.connectAttr(self.blc_translation_list[nr] + '.blender', self.blc_translation_list[nr+1] + '.blender', f=True)

        # Manage systems visibility
        switch_visibility = 'rev_IKFKSwitch' + name
        cmds.createNode('reverse', n=switch_visibility)
        cmds.connectAttr(ctl_switch_name + '.FK_IK', switch_visibility + ".input.inputX", f=True)
        cmds.connectAttr(switch_visibility + ".outputX", self.grp_controlsFK + ".visibility", f=True)
        cmds.connectAttr(ctl_switch_name + '.FK_IK', self.grp_controlsIK + ".visibility", f=True)

        cmds.setAttr(self.jnt_listFK[0] + '.visibility', 0)
        cmds.setAttr(self.jnt_listIK[0] + '.visibility', 0)

    # CUSTOM CONTROLS *******************************************************************
    def create_custom_controls(self, shape, ctl_name, s=1.25, *args):
        """
        Args:
            shape (str): Shape to create
            ctl_name (str): Name of the control
            s (float, optional): Size of the control. Defaults to 1.25.
        """
        if shape == 'cube':
            points = [(s, s, -s), (-s, s, -s), (-s, s, s), (s, s, s), (s, s, -s),
                      (s, -s, -s), (-s, -s, -s), (-s, -s, s), (s, -s, s), (s, -s, -s),
                      (-s, -s, -s), (-s, s, -s),
                      (-s, s, s), (-s, -s, s), (s, -s, s), (s, s, s)]
            crv_curve = cmds.curve(point=points, degree=1, name=ctl_name)

        elif shape == 'cone':
            s = s*0.5
            points =[(-s, 0, s), (0, s*2, 0), (s, 0, s), (-s, 0, s),
                     (-s, 0, -s), (0, s*2, 0), (s, 0, -s), (-s, 0, -s),
                     (s, 0, -s), (s, 0, s)]
            crv_curve = cmds.curve(point=points, degree=1, name=ctl_name)
                    
        elif shape == 'lever':
            points =[(0, 0, 0), (0, s*4, 0)]
            stick = cmds.curve(point=points, degree=1, name=ctl_name)

            circle_x = cmds.circle(name=ctl_name, normal=(1, 0, 0), radius=s)
            circle_y = cmds.circle(name=ctl_name+'02',normal=(0, 1, 0), radius=s)
            circle_z = cmds.circle(name=ctl_name+'03',normal=(0, 0, 1), radius=s)
                
            circles_list = [stick, circle_x[0], circle_y[0], circle_z[0]]
            shape_list = []

            for circle in circles_list[1:]:
                cmds.move(0, s*4, 0, circle)
                cmds.makeIdentity(circle, apply=True)
                shape = str(circle) + 'Shape'
                shape_list.append(shape)

            cmds.select(shape_list)
            cmds.select(ctl_name, add=True)
            mel.eval('parent -r -s')
            
            cmds.delete(ctl_name, constructionHistory=True)

            for circle in circles_list[1:]:
                cmds.delete(circle)
        
        elif shape == 'sphere':
            circle_x = cmds.circle(name=ctl_name, normal=(1, 0, 0), radius=s)
            circle_y = cmds.circle(name=ctl_name+'02',normal=(0, 1, 0), radius=s)
            circle_z = cmds.circle(name=ctl_name+'03',normal=(0, 0, 1), radius=s)
                
            circles_list = [circle_x[0], circle_y[0], circle_z[0]]
            shape_list = []

            for circle in circles_list[1:]:
                cmds.makeIdentity(circle, apply=True)
                shape = str(circle) + 'Shape'
                shape_list.append(shape)

            cmds.select(shape_list)
            cmds.select(ctl_name, add=True)
            mel.eval('parent -r -s')
            cmds.delete(ctl_name, constructionHistory=True)
            
            for circle in circles_list[1:]:
                cmds.delete(circle)
        
        elif shape == 'circle':
            cmds.circle(name=ctl_name, normal=(1, 0, 0), radius=s)
            cmds.delete(ctl_name, constructionHistory=True)     
        
        # Pivot on world center
        cmds.move(0, 0, 0, str(ctl_name) + '.scalePivot', str(ctl_name) + '.rotatePivot', worldSpace=True)
        cmds.makeIdentity(ctl_name, apply=True )

        # Creates controls under different groups
        groups_layers = ['ctl_', 'auto_', 'grp_', 'off_' ]

        current = ctl_name
        for nr in range(len(groups_layers[:-1])):
            group_name = current.replace(groups_layers[nr], groups_layers[nr+1])
            group = cmds.group(current, name=group_name)
            current = group_name
            cmds.move(0, 0, 0, str(current) + '.scalePivot', str(current) + '.rotatePivot', worldSpace=True)

    # POP UP ****************************************************************************
    def delete_confirm(self, step, *args):
        """Delete pop up for different steps of the process

        Args:
            step (str): Stage of the system creation (part, guide, rig)
        """
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

    # SCRIPT END

# START ******************************************************************************
def start():
    global main_widget
    main_widget = PickAPart()
start()