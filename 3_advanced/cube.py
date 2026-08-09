"""
content = assignment
course  = Python Advanced
 
date    = 14.11.2025
email   = contact@alexanderrichtertd.com

modified by = Domenica Montesdeoca
date = 02/08/2026
"""

"""
CUBE CLASS

1. CREATE an abstract class "Cube" with the functions:
   translate(x, y, z), rotate(x, y, z), scale(x, y, z) and color(R, G, B)
   All functions store and print out the data in the cube (translate, rotate, scale and color).

2. ADD an __init__(name) and create 3 cube objects.

3. ADD the function print_status() which prints all the variables nicely formatted.

4. ADD the function update_transform(ttype, value).
   "ttype" can be "translate", "rotate" and "scale" while "value" is a list of 3 floats.
   This function should trigger either the translate, rotate or scale function.

   BONUS: Can you do it without using ifs?

5. CREATE a parent class "Object" which has a name, translate, rotate and scale.
   Use Object as the parent for your Cube class.
   Update the Cube class to not repeat the content of Object.

"""
class Object:
    def __init__(self):
        self.name      = ''
        self.translation = (0.0, 0.0, 0.0)
        self.rotation    = (0.0, 0.0, 0.0)
        self.scaling     = (1.0, 1.0, 1.0)
        self.coloring    = (0.5, 0.5, 0.5)   # Since all have color I left it in the Parent Class

class Cube(Object):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.translation = (10, 0.0, 2.5)     # I am not sure if I had to modify it here or afterwards
        self.rotation    = (45, 90, 45)
        self.scaling     = (20, 20, 20)
        self.coloring    = (1,1, 0.5)
        # self.print_status()

    def translate(self, x, y, z):
        self.translation = (x, y, z)
        print(self.translation)

    def rotate(self, x, y, z):
        self.rotation = (x, y, z)
        print(self.rotation)

    def scale(self, x, y, z):
        self.scaling = (x, y, z)
        print(self.scaling)

    def color(self, R, G, B):
        self.coloring= (R, G, B)
        print(self.coloring)

    def print_status(self):
        print(f"""
        Object name: "{self.name}"
        {self.name} translation: {self.translation}
        {self.name} rotation:    {self.rotation}
        {self.name} scale:       {self.scaling}
        {self.name} color:       {self.coloring}
        """)

    def update_transform(self, ttype: str, value: float):
        transform = {'translate':self.translate,
                     'rotate'   :self.rotate,
                     'scale'    :self.scale}
        transform[ttype](*value)

 # Create 3 cube objects  
dice = Cube('geo_Dice')
gift = Cube('geo_Gift')
box  = Cube('geo_Box')

# Modify dice
dice.update_transform('translate', (15.9, 52.0, 4.3))
dice.update_transform('rotate', (90.0, 42.5, 0.2))
dice.update_transform('scale', (2.5, 1.0, 2.5))
dice.coloring = (1.0, 0.7, 0.25)
dice.print_status()

# Modify gift
gift.update_transform('translate', (7.0, 3, 59.5))
gift.update_transform('rotate', (0.15, 92.0, 0.3))
gift.update_transform('scale', (1.0, 5.0, 1.0))
gift.coloring = (0.2, 0.5, 0.1)
gift.print_status()

# Modify box
box.update_transform('translate', (0.75, 19.5, 59.5))
box.update_transform('rotate', (75.0, 80.0, 15))
box.update_transform('scale', (50.5, 50.5, 35.0))
box.coloring = (0.9, 0.3, 1)
box.print_status()