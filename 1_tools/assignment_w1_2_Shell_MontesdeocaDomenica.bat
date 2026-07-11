:: *****************************************************************
:: author: Domenica Montesdeoca
:: date: 07/07/2026
:: *****************************************************************

:: Create directory "shell_test"
mkdir F:\TDA_Python_Adv\shell_test
:: Create file "test_print.py" with a simple print into the directory
echo print("testing a print") >F:\TDA_Python_Adv\shell_test\test_print.py
:: Rename the file to "new_test_print.py"
ren F:\TDA_Python_Adv\shell_test\test_print.py new_test_print.py
:: List what is in the directory "shell_test" including their file permissions
dir F:\TDA_Python_Adv\shell_test
icacls F:\TDA_Python_Adv\shell_test
:: Execute the Python file and call the simple print
python F:\TDA_Python_Adv\shell_test\new_test_print.py
:: Remove the directory "shell_test" with its content
rmdir F:\TDA_Python_Adv\shell_test