# import pysideuic

# UIfile = r"F:\TDA_Python_Adv\MontesdeocaApp\5_app\ui\PickAPart.ui"
# PythonFile = r"F:\TDA_Python_Adv\MontesdeocaApp\5_app\ui\UI_Python.py"

# with open(UIfile, 'w') as thePython:
#     pysideuic.compileUI(myUIFile, thePython)

import subprocess

ui_file = r"F:\TDA_Python_Adv\MontesdeocaApp\5_app\ui\PickAPart.ui"
py_file = r"F:\TDA_Python_Adv\MontesdeocaApp\5_app\ui\UI_Python.py"

result = subprocess.check_output([
    "pyside6-uic",
    ui_file
])

with open(py_file, "w", encoding="utf-8") as f:
    f.write(result.decode("utf-8"))

print("Done")