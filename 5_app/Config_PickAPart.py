"""******************************************************************
Pick A-Part Configuration
content     Writes a .json config file

date        06/08/2026
dependency  Maya, Pick A-Part module
how_to      with open

author      Domenica Montesdeoca <https://www.linkedin.com/in/maydo3d/>
*******************************************************************"""

import json

json_path = r"F:\TDA_Python_Adv\MontesdeocaApp\5_app\config.json"

user_data = {
    'parts': {
        'Arm'   : ['Clavicle', 'Shoulder', 'Elbow', 'Wrist', 'HandEnd'], 
        'Leg'   : ['Hip', 'Knee', 'Ankle', 'FootEnd'],
        'Spine' : ['COG', 'Spine01', 'Spine02', 'Spine03', 'Spine04', 'Chest', 'Chest_End'],
        'Neck'  : ['Neck01', 'Neck02', 'Neck03', 'Head', 'Head_End'], 
        'Hand'  : {
            'Pinky'  : ['PinkyBase', 'Pinky01', 'Pinky02', 'Pinky03', 'PinkyEnd'],
            'Ring'   : ['RingBase', 'Ring01', 'Ring02', 'Ring03', 'RingEnd'],
            'Middle' : ['MiddleBase', 'Middle01', 'Middle02', 'Middle03', 'MiddleEnd'],
            'Index'  : ['IndexBase', 'Index01', 'Index02', 'Index03', 'IndexEnd'],
            'Thumb'  : ['ThumbBase', 'Thumb01', 'Thumb02', 'Thumb03', 'ThumbEnd']},
        'Foot' : {
            'Base'      : ['Foot'],
            'PinkyToe'  : ['PinkyToeBase', 'PinkyToe01', 'PinkyToe02', 'PinkyToe03', 'PinkyToeEnd'],
            'RingToe'   : ['RingToeBase', 'RingToe01', 'RingToe02', 'RingToe03', 'RingToeEnd'],
            'MiddleToe' : ['MiddleToeBase', 'MiddleToe01', 'MiddleToe02', 'MiddleToe03', 'MiddleToeEnd'],
            'IndexToe'  : ['IndexToeBase', 'IndexToe01', 'IndexToe02', 'IndexToe03', 'IndexToeEnd'],
            'ThumbToe'  : ['ThumbToeBase', 'ThumbToe01', 'ThumbToe02', 'ThumbToe03', 'ThumbToeEnd']} 
    },
    'prefix': {
        'joint'   : 'jnt_',
        'control' : 'ctl_',
        'auto'    : 'auto_',
        'group'   : 'grp_',
        'offset'  : 'off_'

    },
    'suffix': {
        'right'  : '_R',
        'left'   : '_L',
        'center' : '_C'
    }
}

with open(json_path, 'w') as outfile:
    json.dump(user_data, outfile, indent=4)


# read json file
# with open(json_path) as json_file:
#     data = json.load(json_file)