"""******************************************************************
Pick A-Part
content     Part based auto-rigger

date        22/07/2026
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

""" ********************************************************************************
Look for the word 'PROBLEMS' for things I had trouble and could not figure out
Look for the word 'QUESTIONS' for questions in context
******************************************************************************** """

# READ CONFIG FILE  *****************************************************************
with open(json_path) as json_file:
    data = json.load(json_file)
#   print(data['parts']['Arm'])     # Example
    """The configuration file will allow the user to decide the nomenclature used in the guide and rig.
    The names of each Part section can be modified (ex: Shoulder to ArmBase  or the name of you choosing)
    Prefix and suffix can be modified too if needed (ex: jnt_ to joint_, _L to _lft)
    In the case of the neck and spine, it is possible to reduce or increase the number of items by modifying the list
    """


# DECORATOR  ************************************************************************
def print_process(func):
    """Helps visualize completed processes in the script editor
    """
    def wrapper(*args, **kwargs):
        print(f'*****START - {func.__name__}*****')
        func(*args)
        print(f'*****{func.__name__} - SUCCESSFUL*****\n')  
    return wrapper


# GUIDES CREATION ****************************************************************************************************************
class Guides:
    """Contains the base variables and function to create a chain of locators under a group that will be used as guides per Part."""

    def __init__(self):
        self.name = ''
        self.side = data['suffix']['left']
        self.prefix_grp = data['prefix']['group']

        self.sections    = data['parts'][self.part]           
        self.translation = (0, 0, 0)
        
    def guide_creation(self):
        previous_guide = None

        # for nr in range(len(self.sections)):
        for nr, section in enumerate (self.sections):
            guide_name = f'guide_{section}_{self.name}{self.side}'

            if cmds.objExists(guide_name):
                continue

            current_guide = cmds.spaceLocator(name=guide_name)[0]    
            cmds.setAttr(f'{guide_name}Shape.localScale', 5.0, 5.0, 5.0)

            if previous_guide:
                cmds.parent(current_guide, previous_guide) 
                cmds.setAttr(f'{current_guide}.translate', self.translation[0], self.translation[1] ,self.translation[2])
            else:
                self.guide_grp_name = f'{self.prefix_grp}Guides_{self.part}{self.name}{self.side}'
                cmds.group(current_guide, name=self.guide_grp_name, absolute=False)
                
            previous_guide = current_guide

class LimbGuide(Guides):
    """Contains the information needed for the guides of limbs(arms and legs), and has an extra function for the pole vector

    Args:
        Guides (class): Creates a chain of locators and contains the base information
    """
    def __init__(self, part, name):
        self.part = part

        super().__init__()
        self.name = name

        if part == 'Arm':
            self.bend = data['parts']['Arm'][2]    # Elbow
            self.translation = (12, 0, 0)
            self.bend_translate = -10
        else:
            self.bend = data['parts']['Leg'][1]    # Knee
            self.translation = (0, -12, 0)
            self.bend_translate = 10

        self.guide_creation()
        self.pole_vector()

    def pole_vector(self):
        # Create a guide for a Pole Vector
        guide_poleV = f'guide_PoleVector_{self.part}_{self.name}{self.side}'

        if not cmds.objExists(guide_poleV):

            guide_poleV = cmds.spaceLocator(name=guide_poleV)[0]
            cmds.setAttr(f'{guide_poleV}Shape.localScale', 5.0, 5.0, 5.0)

            guide_bend = f'guide_{self.bend}_{self.name}{self.side}'
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

        super().__init__()
        self.name = name  
        self.translation = (0, 10, 0)  

        self.guide_creation()
class NeckGuide(Guides):
    def __init__(self, part, name):
        self.part = part

        super().__init__()
        self.name = name  
        self.translation = (0, 5, 0)  

        self.guide_creation()

@print_process
def create_guides(MAIN_NAME, GUIDES, all_parts):
    """Creates the guides for each part in the view tree under their own group and adds them to a main guide group

    Args:
        MAIN_NAME (string): Name input by the user
        all_parts (list): List of all the Parts in the view tree
    """
    all_parts.pop(0)

    # Creates main guide group if it does not exist
    if not cmds.objExists(GUIDES):
        grp_all_guides = cmds.group(empty=True, name=GUIDES)
    
    # Creates the guide for each part if id does not exist yet
    for part in all_parts:
        if not cmds.objExists(f'*{part}*'):
            print(part)
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
        self.side = '_L'
        self.prefix_jnt = data['prefix']['joint']
        self.prefix_grp = data['prefix']['group']

        self.orient_jnt     = 'xyz'
        self.secondary_axis = 'yup'
        self.joint_list = []
        self.grp_joints_main = f'{self.prefix_grp}Skeleton_{self.part}{self.name}{self.side}'
        
        self.systems  = ['FK_', 'IK_']
        self.sections = data['parts'][self.part]
        self.base     = data['parts'][self.part][0]
        self.guide_poleV = None

        self.grp_guide  = f'{self.prefix_grp}Guides_{self.part}{self.name}{self.side}'
        self.guide_list = cmds.listRelatives(self.grp_guide, allDescendents=True, type="transform")            

    def create_skeleton(self):
        cmds.select(deselect=True)
        print(f'Part guides: {self.grp_guide}')

        # Creates a joint based on the guide position
        for guide in self.guide_list[::-1]:
            guide_position = cmds.xform(guide, q=True, worldSpace=True, translation=True)
            jnt_name = guide.replace('guide', 'jnt')
            jnt = cmds.joint(name=jnt_name, position=(guide_position[0], guide_position[1], guide_position[2]))
            self.joint_list.append(jnt)
            
        cmds.joint(self.joint_list,e=True, orientJoint=self.orient_jnt, secondaryAxisOrient=self.secondary_axis)
        cmds.joint(self.joint_list[-1], e=True, orientJoint='none')

        cmds.group(self.joint_list[0], name=self.grp_joints_main)

    def duplicate_skeleton(self):
        # Duplicates the skeleton starting from the designated base for each system (FK, IK, etc)
        for sys in self.systems:
            self.joint_base = f'{self.prefix_jnt}{self.base}_{self.name}{self.side}'
            cmds.select(self.joint_base)
            cmds.duplicate(self.joint_base)
            new_jnt_base = cmds.ls(selection=True)[0]
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
    """Contains base variables and functions for the different systems, at the moment 
    FK, IK and a switch between them.

    Args:
        Skeleton (class): Creates the skeleton and its duplicates for each rigging system
    """
    def __init__(self):
        self.prefix_ctl = data['prefix']['control']
        self.prefix_off = data['prefix']['offset']
        self.prefix_grp = data['prefix']['group']

        super().__init__()
        self.grp_controlsFK = f'{self.prefix_grp}controls_FK_{self.part}{self.name}{self.side}'
        self.grp_controlsIK = f'{self.prefix_grp}controls_IK_{self.part}{self.name}{self.side}'
        self.IKFK_pos = [0, 0, 0]

    def create_fk(self):
        # global self.CTRL_MAIN
        self.root_fk = self.joint_base.replace(self.prefix_jnt, f'{self.prefix_jnt}{self.systems[0]}')

        self.joints_fk = cmds.listRelatives(self.root_fk,allDescendents=True)
        self.joints_fk.append(self.root_fk)
        self.joints_fk.pop(0)

        mid_fk = self.joints_fk[1]
        end_fk = self.joints_fk[2]
        offsets_fk = []

        cmds.group(empty=True, name=self.grp_controlsFK)
        cmds.select(deselect=True)

        for nr, joint in enumerate(self.joints_fk):
            # Create FK controls
            ctl_name = joint.replace(self.prefix_jnt, self.prefix_ctl)
            create_custom_controls('circle', ctl_name, 4, color=6)
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
        
        self.joints_fk.reverse()   # Make the order the same as the other systems

    def create_ik(self):
        grp_controls = cmds.group(empty=True, name=self.grp_controlsIK)
        self.root_ik = self.joint_base.replace(self.prefix_jnt, f'{self.prefix_jnt}{self.systems[1]}')

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
            name_end_ik  = names_ik[-1]
        else:
            name_root_ik, name_mid_ik, name_end_ik = names_ik

        # IK Controls names
        ctl_baseIK = f'{self.prefix_ctl}IK_{name_root_ik}Base_{self.name}{self.side}'
        ctl_poleIK = f'{self.prefix_ctl}IK_{self.part}PoleVector_{self.name}{self.side}'
        ctl_endIK  = f'{self.prefix_ctl}IK_{name_end_ik}Base_{self.name}{self.side}'
        ctl_rotIK  = f'{self.prefix_ctl}IKRot_{name_end_ik}Base_{self.name}{self.side}'
        ctls_IK = [ctl_baseIK, ctl_poleIK, ctl_endIK, ctl_rotIK]  
        offsets_ik  = []

        # Get controls offset groups 
        for ctl in ctls_IK:
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
        create_custom_controls('lever', ctl_baseIK, 4, color=6)
        create_custom_controls('cube', ctl_endIK, 4, color=6)
        create_custom_controls('sphere', ctl_rotIK, 4, color=15)

        if 'Leg' in self.part: 
            cmds.setAttr(f'{off_endIK}.rotate', 0, 0, 0)

        # Positions controls
        cmds.matchTransform(off_baseIK, IK_start_jnt)
        cmds.matchTransform(off_endIK, IK_end_jnt)
        cmds.matchTransform(off_rotIK, IK_end_jnt)

        # Create the control hierarchy
        cmds.parent(IK_handle, ctl_rotIK)
        cmds.parent(off_rotIK, ctl_endIK)

        cmds.parentConstraint(ctl_baseIK, IK_start_jnt, maintainOffset=True) 
        cmds.orientConstraint(ctl_rotIK, IK_end_jnt, maintainOffset=True)

        # Changes the IK solver to a Rotate Plane solver if a Pole Vector guide is present
        if self.guide_poleV:
            create_custom_controls('cone', ctl_poleIK, 4, color=6)

            cmds.parent(off_poleIK, ctl_endIK) 
            cmds.matchTransform(off_poleIK, self.guide_poleV)
            cmds.ikHandle(IK_handle, edit=True, solver='ikRPsolver')
            cmds.poleVectorConstraint(ctl_poleIK, IK_handle)         

        cmds.parent(off_baseIK, off_endIK, self.grp_controlsIK)
        cmds.parent(self.grp_controlsIK, self.CTRL_MAIN)

        # TODO Create Soft IK
    
    def fkik_blend(self):
        print(f'Main joint chain: {self.joints_main}')
        print(f'FK joint chain: {self.joints_fk}')
        print(f'IK joint chain: {self.joints_ik}')

        # Create names for FK /IK switch control and system
        ctl_switch_name = f'{self.prefix_ctl}_IKFK_{self.part}{self.name}'
        create_custom_controls('cube', ctl_switch_name, 1, color=15)

        cmds.addAttr(ctl_switch_name, longName= 'FK_IK', shortName='FK_IK', keyable=True, attributeType='float', 
                     defaultValue=0.0, minValue=0.0, maxValue=1.0)

        self.off_switch_name = ctl_switch_name.replace(self.prefix_ctl, self.prefix_off)
        cmds.matchTransform(self.off_switch_name, self.joints_main[0])
        cmds.move(self.IKFK_pos[0], self.IKFK_pos[1], self.IKFK_pos[2], self.off_switch_name, relative=True)   # Positions according to part

        # Constraint switch under limb system and parent under main controls
        cmds.parentConstraint(self.joints_main[0], self.off_switch_name, maintainOffset=True, skipRotate=['x', 'y', 'z'])
        cmds.parent(self.off_switch_name, self.CTRL_MAIN)

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

class LimbSkeleton(Rig):
    """Contains the information needed for the rigging system of limbs(arms and legs), saves the pole vector guide to 
    use its position but deletes it to be able to create the rigging systems

    Args:
        Rig (class): Creates the required rigging systems
    """
    def __init__(self, part, name):
        self.part = part
        self.name = name  

        super().__init__()
        self.guide_poleV = self.guide_list[-1]  
        self.guide_list.pop(-1)

        if part == 'Arm':
            self.bend     = data['parts']['Arm'][2]    # Elbow
            self.base     = data['parts']['Arm'][1]    # Shoulder
            self.clavicle = data['parts']['Arm'][0] 
            self.IKFK_pos = [0, 10, 0]
            self.secondary_axis = 'yup'
        else:
            self.bend     = data['parts']['Leg'][1]  
            self.IKFK_pos = [10, 0, 0]  # Knee   
            self.secondary_axis = 'zup'    

        self.create_skeleton()
        self.duplicate_skeleton()
        self.create_fk()
        self.create_ik()
        self.fkik_blend()

        # Creates the clavicle and parents all arm controls to it
        if part == 'Arm':
            jnt_clavicle = f'{self.prefix_jnt}{self.clavicle}_{self.name}{self.side}'
            ctl_clavicle = jnt_clavicle.replace(self.prefix_jnt, self.prefix_ctl)
            off_clavicle = jnt_clavicle.replace(self.prefix_jnt, self.prefix_off)
            create_custom_controls('lever', ctl_clavicle, 4, color=6)

            cmds.matchTransform(off_clavicle, jnt_clavicle)
            cmds.setAttr(f'{off_clavicle}.rotateX', 90)
            cmds.parentConstraint(ctl_clavicle, jnt_clavicle, maintainOffset=True)
            cmds.parent(self.grp_controlsFK, ctl_clavicle)
            cmds.parent(self.grp_controlsIK, ctl_clavicle)

            cmds.parent(off_clavicle, self.CTRL_MAIN)
            
class SpineSkeleton(Rig):
    """why?
        -Custom position for Switch control
        -Different joint orientation
        -Hip or center of gravity (cog) joint is oriented to world 
    """
    def __init__(self, part, name):
        self.part = part
        self.name = name  

        super().__init__()
        self.IKFK_pos = [0, 10, 10]
        self.secondary_axis = 'zdown'

        self.create_skeleton()
        cmds.joint(self.joint_list[0], e=True, orientJoint='none')      # Makes the hip joint be oriented to world

        self.duplicate_skeleton()
        self.create_fk()
        self.create_ik()    # This will be replaced for an IK Spline
        self.fkik_blend()

class NeckSkeleton(Rig):
    """why?
        -Only needs to determine its skeleton secondary axis
    """
    def __init__(self, part, name):
        self.part = part
        self.name = name  

        super().__init__()
        self.IKFK_pos =[ 0, 5, -10]
        self.secondary_axis = 'zdown'
        
        self.create_skeleton()
        self.duplicate_skeleton()
        self.create_fk()
        self.create_ik()    # This will be replaced for an IK Spline
        self.fkik_blend()


@print_process
def create_rig(MAIN_NAME, GRP_ALL, CTRL_GLOBAL, CTRL_MAIN, GRP_SKELETON, all_parts):
    """Pre-established name nomenclature 

    Args:
        MAIN_NAME (string): Name input by the user. Default: 'Main'
        GRP_ALL (string): Name of the group containing all elements of the rig
        CTRL_GLOBAL (string): Name for the principal control
        CTRL_MAIN (string): Name for the secondary control
        GRP_SKELETON (string): Name of the skeleton group
        all_parts (list): List containing all parts from the view tree
    """
    create_main_part(MAIN_NAME, GRP_ALL, CTRL_GLOBAL, CTRL_MAIN)
    create_parts(MAIN_NAME, GRP_ALL, GRP_SKELETON, CTRL_MAIN, all_parts)

def create_main_part(MAIN_NAME, GRP_ALL, CTRL_GLOBAL, CTRL_MAIN):
    """Creates the main group and controls for the rig
    """
    prefix_grp  = data['prefix']['group']
    prefix_ctl  = data['prefix']['control']
    prefix_off  = data['prefix']['offset']

    size = 100 # cm
     
    main_ctrls     = [CTRL_GLOBAL, CTRL_MAIN]
    off_main_ctrls = [CTRL_GLOBAL.replace(prefix_ctl, prefix_off), CTRL_MAIN.replace(prefix_ctl, prefix_off)]

    # Creates 2 controls that will act as parents for all the rig
    create_custom_controls('circle', CTRL_GLOBAL, size*0.75, (0, 1, 0), color=17)
    create_custom_controls('circle', CTRL_MAIN, size*0.65, (0, 1, 0), color=18)

    # for ctrl in main_ctrls: 
    #     cmds.setAttr(f'{ctrl}Shape.overrideEnabled', 1)
    
    # cmds.setAttr(f'{CTRL_GLOBAL}Shape.overrideColor', 17)
    # cmds.setAttr(f'{CTRL_MAIN}Shape.overrideColor', 18)
        
    cmds.parent(off_main_ctrls[1], CTRL_GLOBAL)
    cmds.group(off_main_ctrls[0], name = GRP_ALL)

    cmds.addAttr(CTRL_GLOBAL, longName='Global_Scale', attributeType='float', defaultValue=1, 
                 minValue=1, maxValue=100, keyable=True)

def create_parts(MAIN_NAME, GRP_ALL, GRP_SKELETON, CTRL_MAIN, all_parts):
    cmds.group(empty=True, name=GRP_SKELETON)
    cmds.parent(GRP_SKELETON, GRP_ALL)
    all_parts.pop(0)
    Skeleton.CTRL_MAIN = CTRL_MAIN

    for part in all_parts:
        print(part)
        if 'Arm' in part:
            name = part.replace('Arm', '')
            arm = LimbSkeleton('Arm', name)
            grp_skeleton_chain = arm.grp_joints_main      
        
        elif 'Leg' in part:
            name = part.replace('Leg', '')
            leg = LimbSkeleton('Leg', name)
            grp_skeleton_chain = leg.grp_joints_main

        elif 'Spine' in part:
            name = part.replace('Spine', '')
            spine = SpineSkeleton('Spine', name)
            grp_skeleton_chain = spine.grp_joints_main

        elif 'Neck' in part:
            name = part.replace('Neck', '')
            neck = NeckSkeleton('Neck', name)
            grp_skeleton_chain = neck.grp_joints_main

        cmds.parent(grp_skeleton_chain, GRP_SKELETON) 
        print(f'Creating {part} rig system')   
        
def delete_rig(GRP_ALL):
    if cmds.objExists(GRP_ALL):
        cmds.delete(GRP_ALL)

    if cmds.objExists('blc_*'):
        cmds.delete('blc_*')
    

# CUSTOM CONTROLS ****************************************************************************************************************
def create_custom_controls(shape, ctl_name, s=1.25, normal=(1, 0, 0), color=5):
    """Creates controls based on custom shapes

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
        cmds.circle(name=ctl_name, normal=normal, radius=s)
        cmds.delete(ctl_name, constructionHistory=True)     

    # Color
    cmds.setAttr(f'{ctl_name}.overrideEnabled', 1)
    cmds.setAttr(f'{ctl_name}.overrideColor', color)
    
    # Pivot on world center
    cmds.move(0, 0, 0, str(ctl_name) + '.scalePivot', str(ctl_name) + '.rotatePivot', worldSpace=True)
    cmds.makeIdentity(ctl_name, apply=True )

    # Creates controls under different groups
    prefix_ctl = data['prefix']['control']
    prefix_auto = data['prefix']['auto']
    prefix_grp = data['prefix']['group']
    prefix_off = data['prefix']['offset']
    groups_layers = [prefix_ctl, prefix_auto, prefix_grp, prefix_off]

    current = ctl_name
    for nr in range(len(groups_layers[:-1])):
        group_name = current.replace(groups_layers[nr], groups_layers[nr+1])
        group = cmds.group(current, name=group_name)
        current = group_name
        cmds.move(0, 0, 0, str(current) + '.scalePivot', str(current) + '.rotatePivot', worldSpace=True)

#     # SCRIPT END
