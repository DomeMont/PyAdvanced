"""******************************************************************
Pick-A-Part UI
content     Qt Designer UI

date        04/09/2026
dependency  Maya
how_to      load()

author      Domenica Montesdeoca <https://www.linkedin.com/in/maydo3d/>
*******************************************************************"""

import os 
import sys 
import json
import importlib
import webbrowser

CURRENT_PATH = os.path.dirname(__file__)
TITLE = os.path.splitext(os.path.basename(__file__))

sys.path.append(CURRENT_PATH)
json_path = f'{CURRENT_PATH}\config.json'

from Qt import QtWidgets, QtGui, QtCore, QtCompat  
from maya import cmds

import PickAPart as pick
importlib.reload(pick) 


# READ CONFIG FILE  *****************************************************************
with open(json_path) as json_file:
    data = json.load(json_file)


# Variables **********************************************************************************************************************
prefix_grp = data['prefix']['group']
prefix_ctl  = data['prefix']['control']
prefix_off  = data['prefix']['offset']


# Class **************************************************************************************************************************
class UI():
    def __init__(self):
        UI_PATH = "/".join([CURRENT_PATH, "ui", 'PickAPart' + ".ui"])
        self.wgPick = QtCompat.loadUi(UI_PATH)

        self.ui_title = self.wgPick.windowTitle()
        
        # Close if already exists
        if cmds.window(self.ui_title, exists=True):
            cmds.deleteUI(self.ui_title)

        self.wgPick.setObjectName(self.ui_title)
        self.wgPick.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) 

        # SIGNALS ****************************************************************************************************************
        self.wgPick.btnAddPart.clicked.connect(self.btn_add_part)     # Add Part
        self.model_tree = QtGui.QStandardItemModel()              # Create a container for the tree view
        # self.model_tree.setHorizontalHeaderLabels(['Parts'])    # Add more items for more columns
        self.wgPick.treeView.setModel(self.model_tree)            # Make the tree view read the info from model_tree
        self.main_part = QtGui.QStandardItem('Main')              
        self.model_tree.appendRow(self.main_part)                 # Set 'Main' as a item in the hierarchy
        self.wgPick.treeView.expandAll()                          # Make all items visible from the start

        self.wgPick.btnParentPart.clicked.connect(self.btn_parent_part)                         # Parent Part
        self.wgPick.btnDeletePart.clicked.connect(lambda *_: self.delete_confirm('part'))       # Delete Part

        self.wgPick.btnCreateGuides.clicked.connect(self.btn_create_guides)                     # Create Guides
        self.wgPick.btnDeleteGuides.clicked.connect(lambda *_: self.delete_confirm('guides'))   # Delete Guides

        self.wgPick.btnCreateRig.clicked.connect(self.btn_create_rig)                           # Create Rig
        self.wgPick.btnDeleteRig.clicked.connect(lambda *_: self.delete_confirm('rig'))         # Delete Rig
        self.wgPick.btnAboutMe.clicked.connect(lambda *_: self.open_websites('about'))
        self.wgPick.btnHelp.clicked.connect(lambda *_: self.open_websites('help'))

        # SHOW UI 
        self.wgPick.show()

    # FUNCTIONALITIES ************************************************************************************************************
    def btn_add_part(self):
        self.MAIN_NAME = self.wgPick.lneMainInput.text()
        current_part = self.wgPick.cbParts.currentText()
        hierarchy = None

        if not self.MAIN_NAME: 
            self.MAIN_NAME = 'Main'

        # Look if a name + version exist so no names are repeated
        version = 0
        while self.model_tree.findItems(f"{current_part}{version:02d}", QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive):
            version += 1

        # Add .00 to the added parts
        current_part = f"{current_part}{version:02d}"
        part = QtGui.QStandardItem(current_part)

        # parent to selected part
        selected_part = self.wgPick.treeView.selectionModel().selectedRows() 
        if selected_part:
            parent = self.model_tree.itemFromIndex(selected_part[0])
            parent.appendRow(part)
        else:        
            self.main_part.appendRow(part)

    def btn_parent_part(self):
        selected_parts = self.wgPick.treeView.selectionModel().selectedRows() 

        if len(selected_parts) < 2:
            print('Select at least 2 items')
            return

        new_parent = self.model_tree.itemFromIndex(selected_parts[-1])

        for nr in range(len(selected_parts[:-1])):
            part = self.model_tree.itemFromIndex(selected_parts[nr])
            old_parent = part.parent()
            row = old_parent.takeRow(part.row())
            new_parent.appendRow(row)

        self.all_parts = self.get_items_hierarchy(self.model_tree.invisibleRootItem())

        parts_hierarchy =  {}
        for nr, part in enumerate(self.all_parts[1:]):
            part = self.model_tree.findItems(part, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)[0]
            parent = part.parent()

            parts_hierarchy[f'Part: {part.text()}'] = f'Parent: {parent.text()}'
        print(parts_hierarchy)

    def btn_delete_part(self):
        selected_part = self.wgPick.treeView.selectionModel().selectedRows()[0]
        item = self.model_tree.itemFromIndex(selected_part)

        if item == self.main_part:
            return

        self.model_tree.removeRow(selected_part.row(), selected_part.parent())

    def delete_confirm(self, step):
        """Delete pop up for different steps of the process

        Args:
            step (str): Stage of the system creation (part, guide, rig)
        """
        btn_confirm = QtWidgets.QMessageBox.question(self.wgPick, 'DELETE', f'Delete last {step}?')

        if btn_confirm == QtWidgets.QMessageBox.Yes:
            if step=='part':
                self.btn_delete_part()
            elif step=='guides':
                pick.delete_guides(self.GUIDES)
            elif step=='rig':
                pick.delete_rig(self.GRP_ALL)
    
    def get_items_hierarchy(self, parent):
        """Gets all the items currently in the view tree by row

        Args:
            parent (variable): The item whose children are we looking for

        Returns:
            list: A list of strings of all the items in the view tree
        """
        all_parts = [] 
        for row in range(parent.rowCount()):
            part = parent.child(row)
            all_parts.append(part.text())

            if part.hasChildren():
                all_parts.extend(self.get_items_hierarchy(part))

        return all_parts
    
    def btn_create_guides(self):
        self.GUIDES = f'{prefix_grp}GUIDES_{self.MAIN_NAME}'

        self.all_parts = self.get_items_hierarchy(self.model_tree.invisibleRootItem())
        pick.create_guides(self.MAIN_NAME, self.GUIDES, self.all_parts)

    def btn_create_rig(self):
        self.GRP_ALL = prefix_grp + self.MAIN_NAME
        CTRL_GLOBAL  = f'{prefix_ctl}Global{self.MAIN_NAME}_C'
        CTRL_MAIN    = f'{prefix_ctl}Main{self.MAIN_NAME}_C'
        GRP_SKELETON = f'{prefix_grp}Skeleton{self.MAIN_NAME}'
        GRP_RIG = f'{prefix_grp}Rig{self.MAIN_NAME}'
        CTRL_SIZE = self.wgPick.slControlSize.value()

        self.all_parts = self.get_items_hierarchy(self.model_tree.invisibleRootItem())
        pick.create_rig(self.GUIDES, self.MAIN_NAME, self.GRP_ALL, CTRL_GLOBAL, CTRL_MAIN, GRP_SKELETON, 
                        GRP_RIG, self.all_parts, CTRL_SIZE)

    def open_websites(self, site):
        if site == 'about':
            webbrowser.open('https://www.linkedin.com/in/maydo3d/')
        if site == 'help':
            webbrowser.open(f'https://github.com/DomeMont/PyAdvanced/wiki/How-to-use-Pick%E2%80%90A%E2%80%90Part')


# Start UI ***********************************************************************************************************************
def load():
    global main_widget
    main_widget = UI()
load()

# START
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     classVar = UI()
#     app.exec_()