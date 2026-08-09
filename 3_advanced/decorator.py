"""
content = assignment
course  = Python Advanced
 
date    = 14.11.2025
email   = contact@alexanderrichtertd.com

modified by = Domenica Montesdeoca
date = 03/08/2026
"""


"""
0. CONNECT the decorator "print_process" with all sleeping functions.
   Print START and END before and after.

   START *******
   main_function
   END *********


1. Print the processing time of all sleeping functions.
END - 00:00:00


2. PRINT the name of the sleeping function in the decorator.
   How can you get the information inside it?

START - long_sleeping

"""


import time



#*********************************************************************
# DECORATOR
def print_process(func):
    def wrapper(*args, **kwargs):
        print(f'START - {func.__name__}')
        func(*args)

        processing_time = time.process_time()
        hours   = int(processing_time // 3600)
        minutes = int((processing_time%3600) // 60)
        seconds = int(processing_time % 60)

        print(f'END - {hours:02d}:{minutes:02d}:{seconds:02d}\n')  
    return wrapper


#*********************************************************************
# FUNC
@print_process
def short_sleeping(name):
    time.sleep(.1)
    print(name)

@print_process
def mid_sleeping(name):
    time.sleep(2)
    print(name)

@print_process
def long_sleeping(name):
    time.sleep(4)
    print(name)

short_sleeping("So sleepy")
mid_sleeping("Time for a nap")
long_sleeping("Good Night")
