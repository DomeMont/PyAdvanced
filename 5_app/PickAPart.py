"""******************************************************************
Pick A-Part
content     Part based auto-rigger

date        05/09/2026
dependency  Maya, config.json

author      Domenica Montesdeoca <https://www.linkedin.com/in/maydo3d/>
*******************************************************************"""

import os 
import sys 
import json
from maya import mel
from maya import cmds

CURRENT_PATH = os.path.dirname(__file__)
sys.path.append(CURRENT_PATH)
json_path = f'{CURRENT_PATH}\config.json'


# READ CONFIG FILE  **************************************************************************************************************
with open(json_path) as json_file:
    data = json.load(json_file)
#   print(data['parts']['Arm'])     # Example
    """The configuration file will allow the user to decide the nomenclature used in the guide and rig.
    The names of each Part section can be modified (ex: Shoulder to ArmBase  or the name of you choosing)
    Prefix and suffix can be modified too if needed (ex: jnt_ to joint_, _L to _lft)
    In the case of the neck and spine, it is possible to reduce or increase the number of items by modifying the list
    """


# DECORATOR  *********************************************************************************************************************
def print_process(func):
    """Helps visualize completed processes in the script editor"""
    def wrapper(*args, **kwargs):
        print(f'*****START - {func.__name__}*****')
        func(*args)
        print(f'*****{func.__name__} - SUCCESSFUL*****\n')  
    return wrapper


# GUIDES CREATION ****************************************************************************************************************
class Guides:
    """Contains the base variables and function to create a chain of locators under a group that will be used as guides per Part."""

    def __init__(self):
        self.prefix_grp = data['prefix']['group']
        self.sections   = data['parts'][self.part]           
        translation = (0, 0, 0)

        self.guide_grp_name = f'{self.prefix_grp}Guides_{self.part}{self.name}'
        
    def guide_creation(self, color, translation, origin, mirror):
        """Creates the locators to be used as guides

        Args:
            color (int): Defines the color of the guides
            translation (int, int, int): Defines how much the guides will move compared to its parent
            origin (int, int, int): Sets the point of origin of the first guide
            mirror (bool): Defines if the Part mirror will be created

        Returns:
            list: All the created guides as a list
        """
        guide_list = []
        previous_guide = None
        loc_size = adjust_units_inverse(5)
        
        for nr, section in enumerate (self.sections):
            guide_name = f'guide_{section}_{self.name}'

            if cmds.objExists(guide_name):
                continue

            current_guide = cmds.spaceLocator(name=guide_name)[0] 
            cmds.setAttr(f'{guide_name}.translate', origin[0], origin[1], origin[2])   
            cmds.setAttr(f'{guide_name}Shape.localScale', loc_size, loc_size, loc_size)

            # Color
            cmds.setAttr(f'{guide_name}.overrideEnabled', 1)
            cmds.setAttr(f'{guide_name}.overrideColor', color)

            if previous_guide:
                cmds.parent(current_guide, previous_guide) 
                cmds.setAttr(f'{current_guide}.translate', translation[0], translation[1] , translation[2])
            else:
                cmds.addAttr(guide_name, longName='Mirror', attributeType='bool', defaultValue=mirror, 
                             hidden=False, keyable=False)
                cmds.setAttr(f'{guide_name}.Mirror', channelBox=True)

                cmds.group(empty=True, name=self.guide_grp_name, absolute=False)
                cmds.matchTransform(self.guide_grp_name, guide_name)
                cmds.parent(current_guide, self.guide_grp_name, absolute=False)

            guide_list.append(guide_name)     
            previous_guide = current_guide

        return guide_list

class LimbGuide(Guides):
    """Contains the information needed for the guides of limbs(arms and legs), and has an extra function for the pole vector

    Args:
        Guides (class): Creates a chain of locators and contains the base information
    """
    def __init__(self, part, name):
        self.part = part
        self.name = name 

        super().__init__()
        color = 13
        color_pv = 4
        mirror = 1      #True
        if part == 'Arm':
            self.bend = data['parts']['Arm'][2]    # Elbow
            origin = (5, 135, 0)
            trans_cm = adjust_units(20)
            translation = (trans_cm, 0, 0)
            self.bend_translate = -40
        else:
            self.bend = data['parts']['Leg'][1]    # Knee
            origin = (8, 90, 0)
            trans_cm = adjust_units(-40)
            translation = (0, trans_cm, 0)
            self.bend_translate = 40

        guide_list = self.guide_creation(color, translation, origin, mirror)
        self.pole_vector(color_pv)

        if part == 'Leg':  
            ankle = guide_list[-2]
            foot_end = guide_list[-1]
            
            cmds.setAttr(f'{ankle}.rotateX', -75)
            cmds.setAttr(f'{foot_end}.translateY', -15)

    def pole_vector(self, color_pv):
        # Create a guide for a Pole Vector
        guide_poleV = f'guide_PoleVector_{self.part}_{self.name}'

        if not cmds.objExists(guide_poleV):
            loc_size = adjust_units_inverse(5)

            guide_poleV = cmds.spaceLocator(name=guide_poleV)[0]
            cmds.setAttr(f'{guide_poleV}Shape.localScale', loc_size, loc_size, loc_size)

            # Color
            cmds.setAttr(f'{guide_poleV}.overrideEnabled', 1)
            cmds.setAttr(f'{guide_poleV}.overrideColor', color_pv)

            guide_bend = f'guide_{self.bend}_{self.name}'
            bend_position = cmds.xform(guide_bend, query=True, translation=True, worldSpace=True)
            cmds.xform(guide_poleV, worldSpace=True, translation=(bend_position[0], bend_position[1], self.bend_translate))

            cmds.parent(guide_poleV, self.guide_grp_name)

class SpineGuide(Guides):
    """Contains the information needed for the guides of a spine.

    Args:
        Guides (class): Creates a chain of locators and contains the base information
    """
    def __init__(self, part, name):
        self.part = part
        self.name = name 

        super().__init__()
        mirror = 0
        origin = (0, 90, 0)
        trans_cm = adjust_units(10)
        translation = (0, trans_cm, 0)  
        
        self.guide_creation(17, translation, origin, mirror)

class NeckGuide(Guides):
    def __init__(self, part, name):
        self.part = part
        self.name = name 

        super().__init__()
        mirror = 0
        origin = (0, 150, 0)
        trans_cm = adjust_units(5)
        translation = (0, trans_cm, 0)  
        self.guide_creation(14, translation, origin, mirror)

@print_process
def create_guides(MAIN_NAME, GUIDES, all_parts):
    """Creates the guides for each part in the view tree under their own group and adds them to a main guide group

    Args:
        MAIN_NAME (string): Name input by the user
        all_parts (list): List of all the Parts in the view tree
    """
    all_parts.pop(0)
    print(f'ALL PARTS: {all_parts}')

    # Creates main guide group if it does not exist
    if not cmds.objExists(GUIDES):
        grp_all_guides = cmds.group(empty=True, name=GUIDES)

    created_list = cmds.listRelatives(GUIDES, children=True) or []
    for nr, created in enumerate(created_list):
        created_list[nr] = created.split('_')[2]
    
    # Creates the guide for each part if id does not exist yet
    for part in all_parts:
        if part not in created_list:
            if 'Arm' in part:
                name = part.replace('Arm', '')
                arm  = LimbGuide('Arm', name)
                grp_guide = arm.guide_grp_name

            elif 'Leg' in part:
                name = part.replace('Leg', '')
                leg  = LimbGuide('Leg', name)
                grp_guide = leg.guide_grp_name
            
            elif 'Spine' in part:
                name  = part.replace('Spine', '')
                spine = SpineGuide('Spine', name)
                grp_guide = spine.guide_grp_name

            elif 'Neck' in part:
                name = part.replace('Neck', '')
                neck = NeckGuide('Neck', name)
                grp_guide = neck.guide_grp_name

            cmds.parent(grp_guide, GUIDES)
            print(f'Creating {part} guide')
                
def delete_guides(GUIDES):
    grp_guides = cmds.ls(GUIDES, type='transform')
    print('**Delete guides**')
    cmds.delete(grp_guides)


# PARTS CREATION / RIG CREATION **************************************************************************************************
class Skeleton:
    """Contains all the variables and functions to create a joint chain and duplicate
     it for the systems the rig needs (FK, IK, IK Spline)"""

    def __init__(self):
        self.prefix_jnt = data['prefix']['joint']
        self.prefix_grp = data['prefix']['group']

        self.orient_jnt     = 'xyz'
        self.secondary_axis = 'yup'

        self.joint_list = []
        self.systems  = ['FK_', 'IK_']
        self.sections = data['parts'][self.part]
        self.base     = data['parts'][self.part][0]
        self.guide_poleV = None

        self.grp_guide  = f'{self.prefix_grp}Guides_{self.part}{self.name}'
        self.guide_list = cmds.listRelatives(self.grp_guide, allDescendents=True, type="transform")     

        guide_position = cmds.xform(self.guide_list[0], q=True, worldSpace=True, translation=True)

        if guide_position[0] == 0:
            self.side = data['suffix']['center']
        elif guide_position[0] > 0:
            self.side = data['suffix']['left']
        elif guide_position[0] < 0:
            self.side = data['suffix']['right']

    def create_skeleton(self):
        cmds.select(deselect=True)
        print(f'Part guides: {self.grp_guide}')

        # Creates a joint based on the guide position
        for guide in self.guide_list[::-1]:
            guide_position = cmds.xform(guide, q=True, worldSpace=True, translation=True)
            jnt_name = guide.replace('guide', 'jnt')
            jnt_name = jnt_name + self.side

            jnt = cmds.joint(name=jnt_name, position=(guide_position[0], guide_position[1], guide_position[2]))
            self.joint_list.append(jnt)
            
        cmds.joint(self.joint_list,e=True, orientJoint=self.orient_jnt, secondaryAxisOrient=self.secondary_axis)
        cmds.joint(self.joint_list[-1], e=True, orientJoint='none')

        self.grp_joints_main = f'{self.prefix_grp}Skeleton_{self.part}{self.name}{self.side}'
        cmds.group(empty =True, name=self.grp_joints_main)
        cmds.matchTransform(self.grp_joints_main, self.guide_list[-1])
        cmds.parent(self.joint_list[0], self.grp_joints_main)

    def duplicate_skeleton(self):
        """Duplicates the skeleton starting from the designated base for each system (FK, IK, IK Spline)"""
        for sys in self.systems:
            self.joint_base = f'{self.prefix_jnt}{self.base}_{self.name}{self.side}'

            cmds.select(self.joint_base)
            cmds.duplicate(self.joint_base)

            new_jnt_base    = cmds.ls(selection=True)[0]
            new_joint_chain = cmds.listRelatives(new_jnt_base, allDescendents=True, type="joint", fullPath=True) 
            new_joint_chain.append(new_jnt_base)

            # Renames the joints according to the rigging system
            self.joints_main = []
            for joint in new_joint_chain:
                short_name = joint.split('|')[-1]

                if f'{self.side}1' in short_name:
                    short_name = short_name.replace(f'{self.side}1', self.side)

                jnt_rename = short_name.replace(self.prefix_jnt, f'{self.prefix_jnt}{sys}')
                cmds.rename(joint, jnt_rename)
                self.joints_main.append(short_name)
        
        # Reorganize the joints to start from the base and delete the unused one.
        self.joints_main.pop(0)
        self.joints_main.reverse()

class Rig(Skeleton):
    """Contains base variables and functions for the different systems: FK, IK and a switch between them or a IK Spline 
    with an FK hybrid system.

    Args:
        Skeleton (class): Creates the skeleton and its duplicates for each rigging system
    """
    def __init__(self):
        self.prefix_ctl = data['prefix']['control']
        self.prefix_off = data['prefix']['offset']
        self.prefix_grp = data['prefix']['group']

        super().__init__()
        self.grp_controls    = f'{self.prefix_grp}controls_{self.part}{self.name}{self.side}'
        self.grp_controlsFK  = f'{self.prefix_grp}controls_FK_{self.part}{self.name}{self.side}'
        self.grp_controlsIK  = f'{self.prefix_grp}controls_IK_{self.part}{self.name}{self.side}'
        self.grp_controlsIKS = f'{self.prefix_grp}controls_IKS_{self.part}{self.name}{self.side}'
        self.IKFK_pos = [0, 0, 0]

        self.grp_rig_main = f'{self.prefix_grp}Rig_{self.part}{self.name}{self.side}'

        cmds.group(empty=True, name=self.grp_controls)

    def create_fk(self, CTRL_SIZE_CM):
        self.root_fk = self.joint_base.replace(self.prefix_jnt, f'{self.prefix_jnt}{self.systems[0]}')
        cmds.group(empty=True, name=self.grp_controlsFK)
        cmds.matchTransform(self.grp_controlsFK, self.root_fk)

        self.joints_fk = cmds.listRelatives(self.root_fk, allDescendents=True)
        self.joints_fk.append(self.root_fk)
        self.joints_fk.pop(0)

        mid_fk = self.joints_fk[1]
        end_fk = self.joints_fk[2]
        offsets_fk = []

        cmds.select(deselect=True)

        for nr, joint in enumerate(self.joints_fk):
            # Create FK controls
            ctl_name = joint.replace(self.prefix_jnt, self.prefix_ctl)
            create_custom_controls('circle', ctl_name, CTRL_SIZE_CM*0.29, color=6)
            off_name = ctl_name.replace(self.prefix_ctl, self.prefix_off)

            # Position and parent constraint FK controls
            cmds.matchTransform(off_name, joint)
            cmds.parentConstraint(ctl_name, joint, maintainOffset=True)
            
            cmds.parent(cmds.ls(sl=True), self.grp_controlsFK)
            offsets_fk.append(off_name)

        # Create hierarchy FK controls
        for nr, offset in enumerate(offsets_fk[:-1]):
                control_fk = offsets_fk[nr+1].replace(self.prefix_off, self.prefix_ctl)
                cmds.parent(offset, control_fk)

        cmds.parent(self.grp_controlsFK, self.CTRL_MAIN)

         # STRETCH FK
        off_midFK = mid_fk.replace(self.prefix_jnt, self.prefix_off)
        off_endFK = end_fk.replace(self.prefix_jnt, self.prefix_off)
        offs_FK   = [str(off_midFK), str(off_endFK)]

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
        
        self.joints_fk.reverse()   # Makes the order the same as the other systems

    def create_ik(self, CTRL_SIZE_CM):
        grp_controls = cmds.group(empty=True, name=self.grp_controlsIK)
        self.root_ik = self.joint_base.replace(self.prefix_jnt, f'{self.prefix_jnt}{self.systems[1]}')
        cmds.matchTransform(self.grp_controlsIK, self.root_ik)

        self.joints_ik = cmds.listRelatives(self.root_ik,allDescendents=True)
        self.joints_ik.append(self.root_ik)
        self.joints_ik.pop(0)
        self.joints_ik.reverse()

        names_ik = []
        for joint in self.joints_ik:
            joint = joint.split('_')[2]
            names_ik.append(joint)
        
        if len(names_ik) > 3:
            name_root_ik = names_ik[0]
            name_midBottnon_ik = names_ik[1]
            name_end_ik  = names_ik[-1]
            name_end_ik  = names_ik[--2]
        else:
            name_root_ik, name_mid_ik, name_end_ik = names_ik

        # IK Controls names
        ctl_baseIK = f'{self.prefix_ctl}IK_{name_root_ik}Base_{self.name}{self.side}'
        ctl_poleIK = f'{self.prefix_ctl}IK_{self.part}PoleVector_{self.name}{self.side}'
        ctl_endIK  = f'{self.prefix_ctl}IK_{name_end_ik}Base_{self.name}{self.side}'
        ctl_rotIK  = f'{self.prefix_ctl}IKRot_{name_end_ik}Base_{self.name}{self.side}'
        controls_IK = [ctl_baseIK, ctl_poleIK, ctl_endIK, ctl_rotIK]  
        offsets_ik  = []

        # Get controls offset groups 
        for ctl in controls_IK:
            offs = ctl.replace(self.prefix_ctl, self.prefix_off)
            offsets_ik.append(offs)

        off_baseIK, off_poleIK, off_endIK, off_rotIK = offsets_ik

        # Create IK
        IK_name      = f'{self.part}{self.name}IK'
        IK_handle    =  f'ikH_{IK_name}{self.side}'
        ctl_ikH_name = ctl_endIK

        IK_start_jnt = self.joints_ik[0]
        IK_end_jnt   = self.joints_ik[-1]

        cmds.ikHandle(name=IK_handle, startJoint=IK_start_jnt, endEffector=IK_end_jnt, solver='ikSCsolver')
        effector = cmds.ikHandle(IK_handle, q=True,  endEffector=True)
        eff_name = f'eff_{IK_name}{self.side}'
        cmds.rename(effector, eff_name)

        # Create controls 
        create_custom_controls('lever', ctl_baseIK, CTRL_SIZE_CM*0.15, color=6)
        create_custom_controls('cube', ctl_endIK, CTRL_SIZE_CM*0.15, color=6)
        create_custom_controls('sphere', ctl_rotIK, CTRL_SIZE_CM*0.15, color=15)

        # Positions controls
        cmds.matchTransform(off_baseIK, IK_start_jnt)
        cmds.matchTransform(off_endIK, IK_end_jnt)
        cmds.matchTransform(off_rotIK, IK_end_jnt)

        if 'Leg' in self.part: 
            cmds.setAttr(f'{off_endIK}.rotate', 0, 0, 0)

        # Create the control hierarchy
        cmds.parent(IK_handle, ctl_rotIK)
        cmds.parent(off_rotIK, ctl_endIK)

        cmds.parentConstraint(ctl_baseIK, IK_start_jnt, maintainOffset=True) 
        cmds.orientConstraint(ctl_rotIK, IK_end_jnt, maintainOffset=True)

        # Changes the IK solver to a Rotate Plane solver if a Pole Vector guide is present
        if self.guide_poleV:
            create_custom_controls('cone', ctl_poleIK, CTRL_SIZE_CM*0.15, color=6)

            cmds.parent(off_poleIK, ctl_endIK) 
            cmds.matchTransform(off_poleIK, self.guide_poleV)
            cmds.ikHandle(IK_handle, edit=True, solver='ikRPsolver')
            cmds.poleVectorConstraint(ctl_poleIK, IK_handle)         

        cmds.parent(off_baseIK, off_endIK, self.grp_controlsIK)
        cmds.parent(self.grp_controlsIK, self.CTRL_MAIN)
    
    def fkik_blend(self, CTRL_SIZE_CM):
        print(f'Main joint chain: {self.joints_main}')
        print(f'FK joint chain: {self.joints_fk}')
        print(f'IK joint chain: {self.joints_ik}')

        # Create names for FK /IK switch control and system
        ctl_switch_name = f'{self.prefix_ctl}_IKFK_{self.part}{self.name}{self.side}'
        create_custom_controls('cube', ctl_switch_name, CTRL_SIZE_CM*0.05, color=15)

        cmds.addAttr(ctl_switch_name, longName= 'FK_IK', shortName='FK_IK', keyable=True, attributeType='float', 
                     defaultValue=0.0, minValue=0.0, maxValue=1.0)

        off_switch_name = ctl_switch_name.replace(self.prefix_ctl, self.prefix_off)
        cmds.matchTransform(off_switch_name, self.joints_main[0])
        cmds.move(self.IKFK_pos[0], self.IKFK_pos[1], self.IKFK_pos[2], ctl_switch_name, 
                  relative=True,  objectSpace=True)     # Positions according to part

        # Constraint switch under limb system and parent under main controls
        cmds.parentConstraint(self.joints_main[0], off_switch_name, maintainOffset=True, skipRotate=['x', 'y', 'z'])
        cmds.parent(off_switch_name, self.grp_controls)

        # FK / IK switch via blend colors (Nodes)
        blc_rotation_list = []
        blc_translation_list = []
        for nr, joint in enumerate (self.joints_main):
            blc_name = joint.split('_')[1:]
            blc_name = '_'.join(blc_name)
            
            blc_rotation = f'blc_Rotation{blc_name}'
            cmds.createNode('blendColors', n=blc_rotation)
            cmds.connectAttr(f'{self.joints_ik[nr]}.rotate', f'{blc_rotation}.color1', f=True)
            cmds.connectAttr(f'{self.joints_fk[nr]}.rotate', f'{blc_rotation}.color2', f=True)
            cmds.connectAttr(f'{blc_rotation}.output', f'{joint}.rotate', f=True)
            blc_rotation_list.append(blc_rotation)

            blc_translation = 'blc_Translation' + blc_name
            cmds.createNode('blendColors', n=blc_translation)
            cmds.connectAttr(self.joints_ik[nr] + '.translate', blc_translation + '.color1', f=True)
            cmds.connectAttr(self.joints_fk[nr] + '.translate', blc_translation + '.color2', f=True)
            cmds.connectAttr(blc_translation + '.output', joint + '.translate', f=True)
            blc_translation_list.append(blc_translation)

        cmds.connectAttr(ctl_switch_name + '.FK_IK', blc_rotation_list[0] + '.blender', f=True)
        cmds.connectAttr(ctl_switch_name + '.FK_IK', blc_translation_list[0] + '.blender', f=True)

        for nr, blc_rotation in enumerate (blc_rotation_list[:-1]):
            cmds.connectAttr(blc_rotation + '.blender', blc_rotation_list[nr+1] + '.blender', f=True)

        for nr, blc_translation in enumerate (blc_translation_list[:-1]):
            cmds.connectAttr(blc_translation + '.blender', blc_translation_list[nr+1] + '.blender', f=True)

        # Manage systems visibility
        switch_visibility = f'rev_IKFKSwitch_{self.part}{self.name}'
        cmds.createNode('reverse', n=switch_visibility)
        cmds.connectAttr(ctl_switch_name + '.FK_IK', switch_visibility + ".input.inputX", f=True)
        cmds.connectAttr(switch_visibility + ".outputX", self.grp_controlsFK + ".visibility", f=True)
        cmds.connectAttr(ctl_switch_name + '.FK_IK', self.grp_controlsIK + ".visibility", f=True)

        cmds.setAttr(self.joints_fk[0] + '.visibility', 0)
        cmds.setAttr(self.joints_ik[0] + '.visibility', 0)

    def create_ik_spline(self, CTRL_SIZE_CM):
        grp_controls = cmds.group(empty=True, name=self.grp_controlsIKS)
        self.root_iks = self.joint_base.replace(self.prefix_jnt, f'{self.prefix_jnt}IKS_')
        cmds.matchTransform(self.grp_controlsIKS, self.root_iks)

        joints_iks = cmds.listRelatives(self.root_iks, allDescendents=True)
        joints_iks.append(self.root_iks)
        joints_iks.pop(0)
        joints_iks.reverse()

        names_jnt_iks = []
        for joint in joints_iks:
            joint = joint.split('_')[2]
            names_jnt_iks.append(joint)
        
        if len(names_jnt_iks) > 3:
            name_root_iks     = names_jnt_iks[0]
            name_end_iks      = names_jnt_iks[-1]
        else:
            name_root_iks, name_mid_iks, name_end_iks = names_jnt_iks

        # Create IK Spline
        self.IKS_name = f'{self.part}{self.name}IKS'
        IKS_handle    = f'ikH_{self.IKS_name}{self.side}'
        IKS_effector  = f'eff_{self.IKS_name}{self.side}'
        IKS_curve     = f'crv_{self.IKS_name}{self.side}'

        IKS_start_jnt   = joints_iks[0]
        IKS_sec_jnt     = joints_iks[1]
        IKS_secLast_jnt = joints_iks[-2]
        IKS_end_jnt     = joints_iks[-1] 

        cmds.ikHandle(name=IKS_handle, startJoint=IKS_start_jnt, endEffector=IKS_end_jnt, solver='ikSplineSolver', 
                      rootOnCurve=True, parentCurve=True, createCurve=True, simplifyCurve=True, numSpans=2)

        effector = cmds.ikHandle(IKS_handle, q=True,  endEffector=True)
        cmds.rename(effector, IKS_effector)

        curveShape = (cmds.ikHandle(IKS_handle, q=True,  curve=True))
        curve = cmds.listRelatives(curveShape, parent=True)[0]
        cmds.rename(curve, IKS_curve)

        # Control names and creation
        ctl_base_iks = f'{self.prefix_ctl}IKS_Base{name_root_iks}_{self.name}{self.side}'
        ctl_mid_iks  = f'{self.prefix_ctl}IKS_Mid_{self.part}{self.name}{self.side}'
        ctl_top_iks  = f'{self.prefix_ctl}IKS_Top_{name_end_iks}_{self.name}{self.side}'

        ctl_baseSec_iks = f'{self.prefix_ctl}IKS_BaseSec{name_root_iks}_{self.name}{self.side}'
        ctl_topSec_iks  = f'{self.prefix_ctl}IKS_TopSec{name_end_iks}_{self.name}{self.side}'

        create_custom_controls('wide_cube', ctl_base_iks, CTRL_SIZE_CM*0.5, color=17)
        create_custom_controls('wide_cube', ctl_mid_iks, CTRL_SIZE_CM*0.5, color=17)
        create_custom_controls('wide_cube', ctl_top_iks , CTRL_SIZE_CM*0.5, color=17)

        create_custom_controls('double_circle', ctl_baseSec_iks, CTRL_SIZE_CM*0.2, color=14)
        create_custom_controls('double_circle', ctl_topSec_iks, CTRL_SIZE_CM*0.2, color=14)

        # Get control positions based on curve
        cvs = cmds.ls(f'{IKS_curve}.cv[:]', flatten=True)
        cv_positions = []

        for cv in cvs:
            position = cmds.xform(cv, q=True, worldSpace=True, translation=True)
            cv_positions.append(position)

        cv_basePos, cv_baseSecPos, cv_midPos, cv_topSecPos, cv_topSec = cv_positions
        controls_IKS = [ctl_base_iks, ctl_baseSec_iks, ctl_mid_iks, ctl_topSec_iks, ctl_top_iks]
        
        joints_IKS = []
        offsets_IKS = []
        for ctl in controls_IKS:
            joint = cmds.joint(name=ctl.replace(self.prefix_ctl, self.prefix_jnt))
            cmds.matchTransform(joint, ctl)
            cmds.parentConstraint(ctl, joint)
            cmds.setAttr(f'{joint}.visibility', False)
            
            joints_IKS.append(joint)
        
            offs = ctl.replace(self.prefix_ctl, self.prefix_off)
            offsets_IKS.append(offs)

        jnt_base_iks, jnt_baseSec_iks, jnt_mid_iks, jnt_topSec_iks, jnt_top_iks = joints_IKS    
        off_base_iks, off_baseSec_iks, off_mid_iks, off_topSec_iks, off_top_iks = offsets_IKS
        last_off = offsets_IKS[-1]

        if 'Spine' in self.part:
            for nr, offset in enumerate (offsets_IKS):
                if nr == 0:
                    crv_A = cv_positions[nr]
                    crv_B = cv_positions[nr+1]   
                elif offset == offsets_IKS[-1]:
                    crv_A = cv_positions[nr]
                    crv_B = cv_positions[nr-1]
                else:
                    cmds.xform(offset, translation=cv_positions[nr])
                    continue

                mid_position = [(crv_A[0] + crv_B[0])/2, (crv_A[1] + crv_B[1])/2, (crv_A[2] + crv_B[2])/2]
                cmds.xform(offset, translation=mid_position)

        elif 'Neck' in self.part:
            for nr, offset in enumerate (offsets_IKS):
                cmds.xform(offset, translation=cv_positions[nr])

        # Controls and Rig hierarchy
        grp_secJoints = f'{self.prefix_grp}SecJoints_{self.part}{self.name}{self.side}'
        grp_rigJoints = f'{self.prefix_grp}RigJoints_{self.part}{self.name}{self.side}'
        
        cmds.group(empty=True, name=grp_secJoints)
        cmds.group(empty=True, name=grp_rigJoints)
        cmds.group(empty=True, name=self.grp_rig_main)
        
        # Add an extra group for pivot in Spine for direct connections instead of parent
        root_jnt = cmds.listRelatives(self.joint_base, parent=True)[0]

        if root_jnt:
            self.grp_secJoints_extra = grp_secJoints.replace('SecJoints_', 'SecJointsExtra_')
            cmds.group(empty=True, name=self.grp_secJoints_extra)
            cmds.matchTransform(self.grp_secJoints_extra, root_jnt)
            cmds.parent(self.grp_secJoints_extra, grp_secJoints)
            cmds.parent(self.root_iks, IKS_handle, self.grp_secJoints_extra)
            
        else:            
            cmds.parent(grp_secJoints, grp_secJoints)
            cmds.parent(self.root_iks, IKS_handle, grp_secJoints)

        cmds.parent(grp_rigJoints, grp_secJoints, self.grp_rig_main)
        cmds.parent(joints_IKS, IKS_curve, grp_rigJoints)

        cmds.parent(offsets_IKS, self.grp_controlsIKS)
        cmds.parent(off_baseSec_iks, ctl_base_iks)
        cmds.parent(off_topSec_iks, ctl_top_iks)
        cmds.parent(self.grp_controlsIKS, self.CTRL_MAIN)

        if 'Neck' in self.part:
            cmds.delete(off_baseSec_iks, off_topSec_iks, jnt_baseSec_iks, jnt_topSec_iks)
            joints_IKS  = jnt_base_iks, jnt_mid_iks, jnt_top_iks    
            offsets_IKS = off_base_iks, off_mid_iks, off_top_iks

            cmds.orientConstraint(ctl_top_iks, IKS_end_jnt, maintainOffset=True)

        # Skin control joints to IK Spline Handle
        cmds.skinCluster(joints_IKS, IKS_curve, maximumInfluences=1)

        self.connect_skeletons(self.joints_main, joints_iks)
        self.create_twist(joints_iks, controls_IKS, IKS_handle)
        self.create_hybrid_system(joints_iks, offsets_IKS, CTRL_SIZE_CM)

        return ctl_base_iks

    def connect_skeletons(self, main_skeleton, sec_skeleton, axes=['X', 'Y', 'Z'], attrs=['translate', 'rotate']):
        """Creates a direct connection between two skeletons, only connects the input attributes and axes

        Args:
            main_skeleton (list): The principal skeleton that will be used for skinning
            sec_skeleton (list): The secondary skeleton mainly used for the rigging system
            axes (list, optional): Axes that will be connected. Defaults to ['X', 'Y', 'Z'].
            attrs (list, optional): Attributes that will be connected. Defaults to ['translate', 'rotate'].
        """

        for nr, joint in enumerate(main_skeleton):
            for axis in axes:
                for attr in attrs:
                    cmds.connectAttr(f'{sec_skeleton[nr]}.{attr}{axis}', f'{joint}.{attr}{axis}', force=True)

    def create_twist(self, joints_iks, controls_IKS, ikHandle):
        """Creates locators to be used as twist guides

        Args:
            joints_iks (list): The chain of joints that have the IK Spline
            controls_IKS (list): Controls for the IK Spline
            ikHandle (str): Name of the IK Handle from the IK Spline
        """
                
        IKS_start = f'loc_TwistStart_{self.IKS_name}{self.side}'
        IKS_end   = f'loc_TwistEnd_{self.IKS_name}{self.side}'

        twist_locators = [IKS_end, IKS_start]
        joints         = [joints_iks[-1], joints_iks[0]]
        controls       = [controls_IKS[-1], controls_IKS[0]]

        # Creates, positions the locators for the twist and hides them
        for nr, loc in enumerate(twist_locators):
            cmds.spaceLocator(name=loc)[0]
            cmds.matchTransform(loc, joints[nr])
            cmds.parent(loc, controls[nr])
            cmds.setAttr(f'{loc}.translate', self.twist_trans[0], self.twist_trans[1] ,self.twist_trans[2])
            cmds.hide(loc)

        # Sets the locators as the guides for the twist in the IK
        cmds.setAttr(f'{ikHandle}.dTwistControlEnable', 1)
        cmds.setAttr(f'{ikHandle}.dWorldUpType', 2)
        cmds.connectAttr(f'{IKS_start}.worldMatrix[0]', f'{ikHandle}.dWorldUpMatrix', force=True)
        cmds.connectAttr(f'{IKS_end}.worldMatrix[0]', f'{ikHandle}.dWorldUpMatrixEnd', force=True)
    
    def create_hybrid_system(self, joints_iks, offsets_IKS, CTRL_SIZE_CM):
        """Creates locators to be used as twist guides. For spine and neck

        Args:
            joints_iks (list): The chain of joints that have the IK Spline
            offsets_IKS (list): Offsets from the controls for the IK Spline
            CTRL_SIZE_CM (str): Defined size for all the controls

        Returns:
            str: Returns base control offset that contains the created Hybrid controls
        """

        # Control names and creation
        if 'Spine' in self.part:
            base = 'BaseFKH_'
            top = 'TopFKH_'
        else:
            base = 'MidFKH_'
            top = 'TopFKH_'

        ctl_base_hyb = f'{self.prefix_ctl}{base}{self.part}_{self.name}{self.side}'
        ctl_top_hyb  = f'{self.prefix_ctl}{top}{self.part}_{self.name}{self.side}'
        off_base_hyb = ctl_base_hyb.replace(self.prefix_ctl, self.prefix_off)
        off_top_hyb  = ctl_top_hyb.replace(self.prefix_ctl, self.prefix_off)

        ctl_head_ik = offsets_IKS[-1].replace(self.prefix_off, self.prefix_ctl)

        create_custom_controls('circle', ctl_base_hyb, CTRL_SIZE_CM*0.5, (1, 0, 0), color=23)
        create_custom_controls('circle', ctl_top_hyb, CTRL_SIZE_CM*0.5, (1, 0, 0), color=23)

        if 'Spine' in self.part:
            # Position controls
            cmds.matchTransform(off_base_hyb, joints_iks[1])
            cmds.matchTransform(off_top_hyb, joints_iks[-2])

            # Connections and hierarchy
            cmds.parent(off_top_hyb, offsets_IKS[2], ctl_base_hyb)
            cmds.parent(offsets_IKS[-1], ctl_top_hyb)
            cmds.parent(off_base_hyb, self.grp_controlsIKS)

        elif 'Neck' in self.part:
            # Create extra control
            ctl_neck_base_hyb = f'{self.prefix_ctl}BaseFKH_{self.part}_{self.name}{self.side}'
            off_neck_base_hyb = ctl_neck_base_hyb.replace(self.prefix_ctl, self.prefix_off)
            create_custom_controls('circle', ctl_neck_base_hyb, CTRL_SIZE_CM*0.5, (1, 0, 0), color=23)

            # Position controls
            cmds.parentConstraint(joints_iks[-2], joints_iks[1], off_base_hyb, maintainOffset=False)
            cmds.delete(f'{off_base_hyb}_parentConstraint1')
            cmds.matchTransform(off_top_hyb, joints_iks[-1])
            cmds.matchTransform(off_neck_base_hyb, joints_iks[0])

            # Connections and hierarchy
            cmds.parent(offsets_IKS[1], offsets_IKS[-1], ctl_base_hyb)
            cmds.parent(off_top_hyb, ctl_head_ik)
            cmds.parent(offsets_IKS[0], ctl_neck_base_hyb)
            cmds.parent(off_base_hyb, ctl_neck_base_hyb)
            cmds.parent(off_neck_base_hyb, self.grp_controlsIKS)

        return off_base_hyb

    def mirror_rig(self):
        """Duplicates the controls and skeleton with its connections and scales them in negative x 

        Returns:
            str: Returns the new skeleton to be integrated to the hierarchy
        """
        guide = cmds.listRelatives(self.grp_guide, type='transform', children=True)[0]
        status = cmds.getAttr(f'{guide}.Mirror')
        parent_controls = cmds.listRelatives(self.grp_controls, parent=True)
        parent_skeleton = cmds.listRelatives(self.grp_joints_main, parent=True)

        if status == 1:   # 1 = True
            left = data['suffix']['left']
            right = data['suffix']['right']
            side = self.grp_controls.split('_')[-1]
            
            if 'L' in side:
                mirror_side = right
            else:
                mirror_side = left

            controls_mirror = f'{self.prefix_grp}controls_{self.part}{self.name}{mirror_side}'
            skeleton_mirror = f'{self.prefix_grp}Skeleton_{self.part}{self.name}{mirror_side}'
            rig_mirror      = f'{self.prefix_grp}Rig_{self.part}{self.name}{mirror_side}'

            # Duplicate special 
            mirror_items = [self.grp_controls, self.grp_joints_main]
            duplicates = cmds.duplicate(mirror_items, upstreamNodes=True, returnRootsOnly=True)
           
            # Mirror the duplicate by scaling x to -1
            mirror_holder = f'{self.prefix_grp}Mirror_holder_{self.part}{self.name}'
            cmds.group(empty=True, name=mirror_holder)
            cmds.parent(duplicates, mirror_holder)
            cmds.setAttr(f'{mirror_holder}.scaleX', -1)

            # Rename the duplicates
            cmds.rename(duplicates[0], controls_mirror)
            cmds.rename(duplicates[1], skeleton_mirror)

            cmds.parent(skeleton_mirror, world=True)

            # Hierarchy and correct naming for all duplicate items
            cmds.parent(controls_mirror, parent_controls)
            cmds.delete(mirror_holder)

            cmds.select(controls_mirror, skeleton_mirror, replace=True)
            mel.eval(f'searchReplaceNames "_{side}" "{mirror_side}" "hierarchy";')

            if 'Leg' in {self.part}:
                mel.eval(f'searchReplaceNames "_{side}" "{mirror_side}" "hierarchy";')
                mel.eval(f'searchReplaceNames "_Reg" "_Leg" "hierarchy";')

            self.change_ctrl_color(controls_mirror)

            return skeleton_mirror

    def change_ctrl_color(self, group):
        """Changes the color of the controls inside the input group

        Args:
            group (list): Control containing the mirrored controls
        """

        controls = cmds.listRelatives(group, allDescendents=True, type='transform')

        for control in controls:
            enabled = cmds.getAttr(f'{control}.overrideEnabled')
            if enabled:
                current_color = cmds.getAttr(f'{control}.overrideColor')
                if current_color == 6:
                    cmds.setAttr(f'{control}.overrideColor', 13)
                elif current_color == 15:
                    cmds.setAttr(f'{control}.overrideColor', 12)

class LimbSkeleton(Rig):
    """Contains the information needed for the rigging system of limbs(arms and legs), saves the pole vector guide to 
    use its position but deletes it to be able to create the rigging systems.

    Args:
        Rig (class): Creates the required rigging systems
    """
    def __init__(self, part, name):
        self.part = part
        self.name = name  

        self.twist_trans = (0, 10, 0)

        super().__init__()
        self.guide_poleV = self.guide_list[-1]  
        self.guide_list.pop(-1)

        if part == 'Arm':
            self.bend     = data['parts']['Arm'][2]    # Elbow
            self.base     = data['parts']['Arm'][1]    # Shoulder
            self.IKFK_pos = [0, 15, 0]
            self.secondary_axis = 'yup'
        else:
            self.bend     = data['parts']['Leg'][1]  # Knee 
            self.IKFK_pos = [0, -15, 0]    
            self.secondary_axis = 'zup'    

        self.create_skeleton()
        self.duplicate_skeleton()
        self.create_fk(self.CTRL_SIZE_CM)
        self.create_ik(self.CTRL_SIZE_CM)
        self.fkik_blend(self.CTRL_SIZE_CM)

        # Creates the clavicle and parents all arm controls to it      
        if part == 'Arm':
            jnt_clavicle = cmds.listRelatives(self.joint_base, parent=True)[0]
            ctl_clavicle = jnt_clavicle.replace(self.prefix_jnt, self.prefix_ctl)
            off_clavicle = jnt_clavicle.replace(self.prefix_jnt, self.prefix_off)
            create_custom_controls('flat_lever', ctl_clavicle, self.CTRL_SIZE_CM*0.20, color=6)

            cmds.matchTransform(off_clavicle, jnt_clavicle)
            cmds.setAttr(f'{ctl_clavicle}.rotateX', 90)
            cmds.makeIdentity(ctl_clavicle, apply=True)
            cmds.parentConstraint(ctl_clavicle, jnt_clavicle, maintainOffset=True)
            cmds.parent(self.grp_controlsFK, ctl_clavicle)
            cmds.parent(self.grp_controlsIK, ctl_clavicle)

            cmds.matchTransform(self.grp_controls, off_clavicle)
            cmds.parent(off_clavicle, self.grp_controls)
        else:
            cmds.matchTransform(self.grp_controls, self.grp_controlsFK)
            cmds.parent(self.grp_controlsFK, self.grp_controlsIK, self.grp_controls)
        
        cmds.parent(self.grp_controls, self.CTRL_MAIN)

        self.skeleton_mirror = self.mirror_rig()
            
class SpineSkeleton(Rig):
    def __init__(self, part, name):
        self.part = part
        self.name = name
        self.twist_trans = (0, 0, -15)

        super().__init__()
        self.IKFK_pos = [0, 10, 10]
        self.orient_jnt     = 'xyz'
        self.secondary_axis = 'zdown'

        self.systems  = ['IKS_']
        self.base     = data['parts']['Spine'][1] 

        self.create_skeleton()
        cmds.joint(self.joint_list[0], e=True, orientJoint='none')      # Makes the hip joint be oriented to world

        self.duplicate_skeleton()
        ctl_base_iks = self.create_ik_spline(self.CTRL_SIZE_CM)

        # Names for COG Controls
        jnt_cog = cmds.listRelatives(self.joint_base, parent=True)[0]

        ctl_root_spine = f'{self.prefix_ctl}Root_{self.part}_{self.name}{self.side}'
        ctl_hip  = f'{self.prefix_ctl}Hip_{self.part}_{self.name}{self.side}'
        off_root_spine = ctl_root_spine.replace(self.prefix_ctl, self.prefix_off)
        off_hip  = ctl_hip.replace(self.prefix_ctl, self.prefix_off)

        # Control creation and hierarchy
        create_custom_controls('circle', ctl_root_spine, self.CTRL_SIZE_CM*0.71, (0, 1, 0), color=17)
        create_custom_controls('circle', ctl_hip, self.CTRL_SIZE_CM*0.51, (0, 1, 0), color=14)

        cmds.matchTransform(off_root_spine, off_hip, jnt_cog)

        cmds.parent(off_root_spine, self.CTRL_MAIN)
        cmds.parent(self.grp_controlsIKS, ctl_root_spine)
        cmds.parent(off_hip, ctl_base_iks)

        # Connect Root Joint to control
        cmds.parentConstraint(ctl_hip, jnt_cog, maintainOffset=True)

        # Connect extra group to pivot from root
        cmds.parentConstraint(ctl_hip, self.grp_secJoints_extra, maintainOffset=True)

        # Group under group Part  
        cmds.matchTransform(self.grp_controls, off_root_spine)    
        cmds.parent(off_root_spine, self.grp_controls)
        cmds.parent(self.grp_controls, self.CTRL_MAIN)
        self.skeleton_mirror = self.mirror_rig()

class NeckSkeleton(Rig):
    def __init__(self, part, name):
        self.part = part
        self.name = name
        self.twist_trans = (0, 0, -15)

        super().__init__()
        self.IKFK_pos =[ 0, 5, -10]
        self.secondary_axis = 'zdown'

        self.systems  = ['IKS_']
        self.base     = data['parts']['Neck'][0] 
        
        self.create_skeleton()
        self.duplicate_skeleton()
        self.create_ik_spline(self.CTRL_SIZE_CM*0.5)

        # Group under group Part
        cmds.matchTransform(self.grp_controls, self.grp_controlsIKS)  
        cmds.parent(self.grp_controlsIKS, self.grp_controls)
        cmds.parent(self.grp_controls, self.CTRL_MAIN)

        self.skeleton_mirror = self.mirror_rig()

@print_process
def create_rig(GUIDES, MAIN_NAME, GRP_ALL, CTRL_GLOBAL, CTRL_MAIN, GRP_SKELETON, GRP_RIG, all_parts, CTRL_SIZE):
    """Uses pre-established names. Defines the size of the controls, and executes the functions for the main controls, 
    and for each of the Parts rig.

    Args:
        MAIN_NAME (string):    Name input by the user. Default: 'Main'
        GRP_ALL (string):      Name of the group containing all elements of the rig
        CTRL_GLOBAL (string):  Name for the principal control
        CTRL_MAIN (string):    Name for the secondary control
        GRP_SKELETON (string): Name of the skeleton group
        all_parts (list):      List containing all parts from the view tree
        CTRL_SIZE (int):       Defines the size of all controls. Default 35(cm)
    """
    CTRL_SIZE_CM = adjust_units(CTRL_SIZE)
    create_main_part(MAIN_NAME, GRP_ALL, CTRL_GLOBAL, CTRL_MAIN, CTRL_SIZE_CM)
    create_parts(MAIN_NAME, GRP_ALL, CTRL_MAIN, GRP_SKELETON, GRP_RIG, all_parts, CTRL_SIZE_CM)
    
    cmds.hide(GUIDES)

def adjust_units(value):
    unit = cmds.currentUnit(q=True, linear=True)
    value = cmds.convertUnit(value, fromUnit = unit, toUnit = 'cm')
    value = float(value.replace('cm', ''))
    return value      

def adjust_units_inverse(value):
    unit = cmds.currentUnit(q=True, linear=True)
    if unit == 'cm':
        value = value
    elif unit == 'm':
        value = value / 100
    elif unit == 'mm':
        value = value *10
    return value

def create_main_part(MAIN_NAME, GRP_ALL, CTRL_GLOBAL, CTRL_MAIN, CTRL_SIZE_CM):
    """Creates the main group and controls for the rig"""
    prefix_grp  = data['prefix']['group']
    prefix_ctl  = data['prefix']['control']
    prefix_off  = data['prefix']['offset']
     
    main_ctrls     = [CTRL_GLOBAL, CTRL_MAIN]
    off_main_ctrls = [CTRL_GLOBAL.replace(prefix_ctl, prefix_off), CTRL_MAIN.replace(prefix_ctl, prefix_off)]

    # Creates 2 controls that will act as parents for all the rig
    create_custom_controls('circle', CTRL_GLOBAL, CTRL_SIZE_CM, (0, 1, 0), color=17)
    create_custom_controls('circle', CTRL_MAIN, CTRL_SIZE_CM*0.86, (0, 1, 0), color=18)

    cmds.parent(off_main_ctrls[1], CTRL_GLOBAL)
    cmds.group(off_main_ctrls[0], name = GRP_ALL)

    cmds.addAttr(CTRL_GLOBAL, longName='Global_Scale', attributeType='float', defaultValue=1, 
                 minValue=1, maxValue=100, keyable=True)

def create_parts(MAIN_NAME, GRP_ALL, CTRL_MAIN, GRP_SKELETON, GRP_RIG, all_parts, CTRL_SIZE_CM):

    cmds.group(empty=True, name=GRP_SKELETON)
    cmds.group(empty=True, name=GRP_RIG)
    cmds.parent(GRP_SKELETON, GRP_RIG, GRP_ALL)
    all_parts.pop(0)
    Skeleton.CTRL_MAIN = CTRL_MAIN
    Skeleton.CTRL_SIZE_CM = CTRL_SIZE_CM

    for part in all_parts:
        print(part)
        if 'Arm' in part:
            name = part.replace('Arm', '')
            arm = LimbSkeleton('Arm', name)
            grp_skeleton_chain = arm.grp_joints_main
            grp_skeleton_mirror = arm.skeleton_mirror
            grp_rig = arm.grp_rig_main
        
        elif 'Leg' in part:
            name = part.replace('Leg', '')
            leg = LimbSkeleton('Leg', name)
            grp_skeleton_chain = leg.grp_joints_main
            grp_skeleton_mirror = leg.skeleton_mirror
            grp_rig = leg.grp_rig_main

        elif 'Spine' in part:
            name = part.replace('Spine', '')
            spine = SpineSkeleton('Spine', name)
            grp_skeleton_chain = spine.grp_joints_main
            grp_skeleton_mirror = spine.skeleton_mirror
            grp_rig = spine.grp_rig_main

        elif 'Neck' in part:
            name = part.replace('Neck', '')
            neck = NeckSkeleton('Neck', name)
            grp_skeleton_chain = neck.grp_joints_main
            grp_skeleton_mirror = neck.skeleton_mirror
            grp_rig = neck.grp_rig_main

        if grp_skeleton_mirror:
            cmds.parent(grp_skeleton_mirror, GRP_SKELETON)

        cmds.parent(grp_skeleton_chain, GRP_SKELETON)

        if cmds.objExists(grp_rig):
            cmds.parent(grp_rig, GRP_RIG)
        print(f'Creating {part} rig system')   
        
def delete_rig(GRP_ALL):
    """Deletes the Main group containing all the rig items and deletes al bend color nodes by name"""
    if cmds.objExists(GRP_ALL):
        cmds.delete(GRP_ALL)

    if cmds.objExists('blc_*'):
        cmds.delete('blc_*')
    

# CUSTOM CONTROLS ****************************************************************************************************************
def create_custom_controls(shape, ctl_name, s=1.25, normal=(1, 0, 0), color=5):
    """Creates the controls required for the different systems, easy way to reuse shapes, define its name, size,
    direction and color.

    Args:
        shape (str): Shape to create
        ctl_name (str): Name of the control
        s (float, optional): Size of the control. Defaults to 1.25.
    """
    if 'cube' in shape:
        points = [(s, s, -s), (-s, s, -s), (-s, s, s), (s, s, s), (s, s, -s),
                    (s, -s, -s), (-s, -s, -s), (-s, -s, s), (s, -s, s), (s, -s, -s),
                    (-s, -s, -s), (-s, s, -s),
                    (-s, s, s), (-s, -s, s), (s, -s, s), (s, s, s)]
        crv_curve = cmds.curve(point=points, degree=1, name=ctl_name)

        if shape == 'wide_cube':
            cmds.scale(1, 0.10, 1, crv_curve)

    elif shape == 'cone':
        s = s*0.5
        points = [(-s, 0, s), (0, s*2, 0), (s, 0, s), (-s, 0, s),
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

    elif 'double_circle' in shape:
        circle_f = cmds.circle(name=ctl_name, normal=(0,0,1), radius=s)
        circle_b = cmds.circle(name=ctl_name + '02', normal=(0,0,1), radius=s)
        
        cmds.setAttr(f'{circle_f[0]}.translateZ', s)
        cmds.setAttr(f'{circle_b[0]}.translateZ', -s)
        cmds.delete(ctl_name, constructionHistory=True)

        circles_list = [f'{circle_f[0]}', f'{circle_b[0]}']
        shape_list = []

        for circle in circles_list:
            cmds.makeIdentity(circle, apply=True)
            shape = str(circle) + 'Shape'
            shape_list.append(shape)

        cmds.select(shape_list[1])
        cmds.select(ctl_name, add=True)
        mel.eval('parent -r -s')

        cmds.delete(ctl_name, constructionHistory=True)
        cmds.delete(circles_list[1])

    elif shape == 'flat_lever':
        points = [(0, 0, 0), (0, s, 0), (s/2, s*1.33, 0), (s/2, s*2, 0), (-s/2, s*2, 0), (-s/2, s*1.33, 0), (0, s, 0)]
        crv_curve = cmds.curve(point=points, degree=1, name=ctl_name)


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
        circle = cmds.circle(name=ctl_name, normal=normal, radius=s)
        cmds.delete(ctl_name, constructionHistory=True)

    # Color
    cmds.setAttr(f'{ctl_name}.overrideEnabled', 1)
    cmds.setAttr(f'{ctl_name}.overrideColor', color)
    
    # Pivot on world center
    cmds.move(0, 0, 0, f'{ctl_name}.scalePivot', f'{ctl_name}.rotatePivot', worldSpace=True)
    cmds.makeIdentity(ctl_name, apply=True )

    # Creates controls under different groups
    prefix_ctl  = data['prefix']['control']
    prefix_auto = data['prefix']['auto']
    prefix_grp  = data['prefix']['group']
    prefix_off  = data['prefix']['offset']
    groups_layers = [prefix_ctl, prefix_auto, prefix_grp, prefix_off]

    current = ctl_name
    for nr in range(len(groups_layers[:-1])):
        group_name = current.replace(groups_layers[nr], groups_layers[nr+1])
        group = cmds.group(current, name=group_name)
        current = group_name
        cmds.move(0, 0, 0, str(current) + '.scalePivot', str(current) + '.rotatePivot', worldSpace=True)

#     # SCRIPT END