"""******************************************************************
Pick-A-Part UI
content     Qt Designer UI

date        17/08/2026
dependency  Maya
how_to      start()

author      Domenica Montesdeoca <https://www.linkedin.com/in/maydo3d/>
*******************************************************************"""

import os 
import sys 
import importlib
import webbrowser 

CURRENT_PATH = os.path.dirname(__file__)
sys.path.append(CURRENT_PATH)

from Qt import QtWidgets, QtGui, QtCore, QtCompat  

import PickAPart as pick
importlib.reload(pick) 

# Variables **********************************************************************************************************************
TITLE = os.path.splitext(os.path.basename(__file__))
CURRENT_PATH = os.path.dirname(__file__) 

# QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(
#     QtCore.Qt.HighDpiScaleFactorRoundingPolicy.Round)

# Class **************************************************************************************************************************
class PickAPart:
    def __init__(self):
        UI_PATH = "/".join([CURRENT_PATH, "ui", 'PickAPart' + ".ui"])
        self.wgPick = QtCompat.loadUi(UI_PATH)
        self.wgPick.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # SIGNALS ****************************************************************************************************************
        self.wgPick.btnAddPart.clicked.connect(self.add_part)     # Add Part
        self.model_tree = QtGui.QStandardItemModel()
        # self.model_tree.setHorizontalHeaderLabels(['Parts'])    # Add more items for more columns
        self.wgPick.treeView.setModel(self.model_tree)            # Make the tree view read the info from model_tree
        self.main_part = QtGui.QStandardItem('Main')
        self.model_tree.appendRow(self.main_part)

        self.wgPick.btnDeletePart.clicked.connect(lambda *_: self.delete_confirm('part'))   # Delete Part
        self.wgPick.btnCreateGuides.clicked.connect(lambda *_: pick.create_guides())        # Create Guides
        self.wgPick.btnCreateRig.clicked.connect(lambda *_: pick.create_rig())              # Create Rig

        self.wgPick.show()

# FUNCTIONALITIES
    def add_part(self):
        MAIN_NAME = self.wgPick.lneMainInput.text()
        current_part = self.wgPick.cbParts.currentText()
        hierarchy = None

        version = 0
        while self.model_tree.findItems(f"{current_part}{version:02d}", QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive):
            version += 1

        # Add .00 to the added parts
        current_part = f"{current_part}{version:02d}"
        print(current_part)
        part = QtGui.QStandardItem(current_part)
        self.main_part.appendRow(part)   

        print('Lista de Partes')
        print(self.get_items_hierarchy(self.model_tree.invisibleRootItem()))

    def delete_part(self):
        selected_part = self.wgPick.treeView.selectionModel().selectedRows()[0]

        item = self.model_tree.itemFromIndex(selected_part)

        if item == self.main_part:
            return

        self.model_tree.removeRow(selected_part.row(), selected_part.parent())

    # TODO  Create a pop up to ask before deleting parts, guides and rig

    def delete_confirm(self, step):
        """Delete pop up for different steps of the process

        Args:
            step (str): Stage of the system creation (part, guide, rig)
        """
        btn_confirm = QtWidgets.QMessageBox.question(self.wgPick, 'DELETE', f'Delete last {step}?')

        if btn_confirm == QtWidgets.QMessageBox.Yes:
            if step=='part':
                self.delete_part()
            elif step=='guides':
                pick.delete_guides()
            elif step=='rig':
                pick.delete_rig()
    
    # TODO get items in container as a list to create parts ESTO EN EL OTRO ARCHIVO
    # TODO PASAR ESTA PARTE AL OTRO ARCHIVO YA FUNCIONA AQUI

    # def get_items_hierarchy(self, parent):
    #     all_parts = [] 
    #     for row in range(parent.rowCount()):
    #         part = parent.child(row)
    #         all_parts.append(part.text())

    #         if part.hasChildren():
    #             all_parts.extend(self.get_items_hierarchy(part))
        
    #     return all_parts


# Start UI ***********************************************************************************************************************
def load():
    global main_widget
    main_widget = PickAPart()
load()

# START
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     classVar = PickAPart()
#     app.exec_()