""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------
Body bone definitions 

"""

import mhx_rig
from mhx_rig import *

BodyJoints = [
    ('root-tail',      'o', ('spine3', [0,-1,0])),
    ('hips-tail',      'o', ('pelvis', [0,-1,0])),
    ('mid-uplegs',     'l', ((0.5, 'l-upper-leg'), (0.5, 'r-upper-leg'))),
    #('spine0',        'l', ((0.5, 'spine1'), (0.5, 'neck'))),
    ('spine-pt',       'o', ('spine2', [0,0,-10])),

    ('r-breast',       'vl', ((0.4, 3559), (0.6, 2944))),
    ('r-tit',          'v', 3718),
    ('l-breast',       'vl', ((0.4, 10233), (0.6, 10776))),
    ('l-tit',          'v', 10115),

    ('mid-rib-top',    'v', 7273),
    ('mid-rib-bot',    'v', 6908),

    ('neck2',          'vl', ((0.5, 6531), (0.5, 8253))),
    ('abdomen-front',  'v', 7359),
    ('abdomen-back',   'v', 7186),
    ('stomach-top',    'v', 7336),
    ('stomach-bot',    'v', 7297),
    ('stomach-front',  'v', 7313),
    ('stomach-back',   'v', 7472),

    ('penis-tip',      'v', 7415),
    ('penis-root',     'vl', ((0.5, 2792), (0.5, 7448))),
    ('scrotum-tip',    'v', 7444),
    ('scrotum-root',   'vl', ((0.5, 2807), (0.5, 7425))),

    ('r-toe-1-1',      'j', 'r-toe-1-1'),
    ('l-toe-1-1',      'j', 'l-toe-1-1'),
    ('mid-feet',       'l', ((0.5, 'l-toe-1-1'), (0.5, 'r-toe-1-1'))),
    ('floor',          'o', ('mid-feet', [0,-0.3,0])),
]

BodyHeadsTails = [
    ('MasterFloor',    'floor', ('floor', zunit)),

    ('Root',           'root-tail', 'spine3'),
    ('Shoulders',      'neck', ('neck', [0,-1,0])),
    ('BendRoot',       'spine3', ('spine3', yunit)),

    # Up spine
    ('Hips',           'spine3', 'root-tail'),
    ('Spine1',         'spine3', 'spine2'),
    ('Spine2',         'spine2', 'spine1'),
    ('Spine3',         'spine1', 'neck'),
    ('Neck',           'neck', 'neck2'),
    ('Head',           'neck2', 'head-end'),

    ('SpinePT',        'spine-pt', ('spine-pt', yunit)),
    ('SpineLinkPT',    'spine2', 'spine-pt'),

    # Down spine    
    ('DownHips',       'spine3', 'root-tail'),
    ('DownSpine1',     'spine2', 'spine3'),
    ('DownSpine2',     'spine1', 'spine2'),
    ('DownSpine3',     'neck', 'spine1'),
    ('DownNeck',       'neck', 'neck2'),
    
    ('DownPT1',        ('spine3', [0,0,-1]), ('spine3', [0,0.5,-1])),
    ('DownPT2',        ('spine2', [0,0,-1]), ('spine2', [0,0.5,-1])),
    ('DownPT3',        ('spine1', [0,0,-1]), ('spine1', [0,0.5,-1])),

    # Deform spine
    ('DfmRoot',        'root-tail', 'spine3'),
    ('DfmHips',        'spine3', 'root-tail'),
    ('DfmSpine1',      'spine3', 'spine2'),
    ('DfmSpine2',      'spine2', 'spine1'),
    ('DfmSpine3',      'spine1', 'neck'),
    ('DfmNeck',        'neck', 'neck2'),
    ('DfmHead',        'neck2', 'head-end'),

    # Deform torso
    ('DfmRib',         'mid-rib-top', 'mid-rib-bot'),
    #('RibTarget',      'spine2', 'mid-rib-bot'),
    ('DfmStomach',     'stomach-bot', 'mid-rib-bot'),
    #('HipBone',        'root-tail', 'stomach-bot'),
    ('Breathe',        'mid-rib-bot', ('mid-rib-bot', zunit)),
    ('Breast_L',       'r-breast', 'r-tit'),
    ('Breast_R',       'l-breast', 'l-tit'),

    ('Penis',          'penis-root', 'penis-tip'),
    ('Scrotum',        'scrotum-root', 'scrotum-tip'),
]

L_UPSPN = L_UPSPNFK+L_UPSPNIK
L_DNSPN = L_DNSPNFK+L_DNSPNIK

BodyArmature = [
    ('MasterFloor',        0, None, F_WIR, L_MAIN, NoBB),

    ('Root',               0, Master, F_WIR, L_UPSPN+L_DNSPNIK, NoBB),
    ('Shoulders',          0, Master, F_WIR, L_UPSPNIK+L_DNSPN, NoBB),
    ('BendRoot',           0, 'Root', 0, L_HELP, NoBB),

    # Up spine
    ('Hips',               0, 'Root', F_WIR, L_UPSPN, NoBB),
    ('Spine1',             0, 'Root', F_WIR, L_UPSPNFK, NoBB),
    ('Spine2',             0, 'Spine1', F_WIR, L_UPSPNFK, NoBB),
    ('Spine3',             0, 'Spine2', F_WIR, L_UPSPNFK, NoBB),
    ('Neck',               0, 'Spine3', F_WIR, L_UPSPN, NoBB),

    ('SpinePT'   ,         0, 'Shoulders', F_WIR, L_UPSPNIK, NoBB),
    ('SpineLinkPT',        0, 'Spine2', F_RES, L_UPSPNIK, NoBB),

    # Down spine
    ('DownNeck',           0, 'Shoulders', F_WIR, L_DNSPN, NoBB),
    ('DownSpine3',         0, 'Shoulders', F_WIR, L_DNSPNFK, NoBB),
    ('DownSpine2',         0, 'DownSpine3', F_WIR, L_DNSPNFK, NoBB),
    ('DownSpine1',         0, 'DownSpine2', F_WIR, L_DNSPNFK, NoBB),
    ('DownHips',           0, 'DownSpine1', F_WIR, L_DNSPN, NoBB),
    
    ('DownPT1',            0, 'DownSpine1', 0, L_HELP, NoBB),
    ('DownPT2',            0, 'DownSpine2', 0, L_HELP, NoBB),
    ('DownPT3',            0, 'DownSpine3', 0, L_HELP, NoBB),

    #('DownSpinePT'   ,     0, 'Root', F_WIR, L_DNSPNIK, NoBB),
    #('DownSpineLinkPT',    0, 'DownSpine2', F_RES, L_DNSPNIK, NoBB),

    # Deform spine    
    ('DfmRoot',            0, Master, F_NOSCALE, L_DMAIN, NoBB),
    ('DfmHips',            0, 'DfmRoot', F_DEF+F_NOSCALE, L_DMAIN, NoBB),
    ('DfmSpine1',          0, 'DfmRoot', F_DEF+F_CON+F_NOSCALE, L_DMAIN, (1,1,3) ),
    ('DfmSpine2',          0, 'DfmSpine1', F_DEF+F_CON+F_NOSCALE, L_DMAIN, (1,1,3) ),
    ('DfmSpine3',          0, 'DfmSpine2', F_DEF+F_CON+F_NOSCALE, L_DMAIN, (1,1,3) ),
    ('DfmNeck',            0, 'DfmSpine3', F_DEF+F_CON+F_NOSCALE, L_DMAIN, (1,1,3) ),

    # Head
    ('Head',               0, 'DfmNeck', F_WIR, L_UPSPN+L_DNSPN+L_HEAD, NoBB),
    ('DfmHead',            0, 'DfmNeck', F_DEF+F_CON, L_DMAIN, NoBB),

    # Deform torso
    ('DfmRib',             0, 'DfmSpine3', F_DEF, L_DMAIN, NoBB),
    #('RibTarget',          0, 'DfmSpine2', 0, L_HELP, NoBB),
    ('DfmStomach',         0, 'DfmHips', F_DEF, L_DMAIN, NoBB),
    #('HipBone',            0, 'DfmHips', 0, L_HELP, NoBB),

    ('Breathe',            0, 'DfmRib', F_WIR, L_TORSO, NoBB),

    ('Penis',              0, 'DfmHips', F_DEF, L_TORSO, (1,5,1) ),
    ('Scrotum',            0, 'DfmHips', F_DEF, L_TORSO, NoBB),
]

BreastArmature = [
    ('Breast_L',           -45*D, 'DfmRib', F_DEF+F_WIR, L_DEF+L_TORSO, NoBB),
    ('Breast_R',           45*D, 'DfmRib', F_DEF+F_WIR, L_DEF+L_TORSO, NoBB),
]

#
#    BodyControlPoses(fp):
#

limHips = (-50*D,40*D, -45*D,45*D, -16*D,16*D)
limSpine1 = (-60*D,90*D, -60*D,60*D, -60*D,60*D)
limSpine2 = (-90*D,70*D, -20*D,20*D, -50*D,50*D)
limSpine3 = (-20*D,20*D, 0,0, -20*D,20*D)
limNeck = (-60*D,40*D, -45*D,45*D, -60*D,60*D)

def BodyControlPoses(fp):
    addPoseBone(fp,  'MasterFloor', 'GZM_Root', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp,  'Root', 'MHCrown', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
        mhx_rig.rootChildOfConstraints +
        [('LimitRot', C_OW_LOCAL, 0, ['LimitRot', (0,0, -45*D,45*D, 0,0), (1,1,1)]) ])

    addPoseBone(fp,  'Shoulders', 'MHCrown', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (0,0, -45*D,45*D, 0,0), (1,1,1)]),
         ('LimitDist', 0, 1, ['LimitDist', 'Root', 'LIMITDIST_INSIDE'])
        ])

    # Up spine

    addPoseBone(fp,  'Hips', 'GZM_CircleHips', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHips, (1,1,1)])])

    addPoseBone(fp,  'Spine1', 'GZM_CircleSpine', 'Spine', (1,1,1), (0,0,0), (1,1,1), 
        ((1,1,1), (0.2,0.2,0.2), 0.05, None), 0, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine1, (1,1,1)])])

    addPoseBone(fp,  'Spine2', 'GZM_CircleSpine', 'Spine', (1,1,1), (0,0,0), (1,1,1), 
        ((1,1,1), (0.2,0.2,0.2), 0.05, None), 0,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine2, (1,1,1)])])

    addPoseBone(fp,  'Spine3', 'GZM_CircleChest', 'Spine', (1,1,1), (0,0,0), (1,1,1), 
        ((1,1,1), (0.96,0.96,0.96), 0.01, None), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine3, (1,1,1)]),
          ('IK', 0, 0, ['IK', 'Shoulders', 3, (-90*D, 'SpinePT'), (1,0,1)]),
         ])
         
    addPoseBone(fp,  'Neck', 'MHNeck', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limNeck, (1,1,1)])])
         
    # Spine IK
    addPoseBone(fp, 'SpinePT', 'MHCube025', 'Spine', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, 'SpineLinkPT', None, 'Spine', (1,1,1), (1,1,1), (1,1,1), (1,1,1), P_STRETCH,
        [('StretchTo', 0, 1, ['Stretch', 'SpinePT', 0])])

    # Down spine

    addPoseBone(fp,  'DownHips', 'GZM_CircleHips', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHips, (1,1,1)])])

    addPoseBone(fp,  'DownSpine1', 'GZM_CircleSpine', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine1, (1,1,1)])])

    addPoseBone(fp,  'DownSpine2', 'GZM_CircleSpine', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine2, (1,1,1)])])

    addPoseBone(fp,  'DownSpine3', 'GZM_CircleChest', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine3, (1,1,1)]),
        ])
         
    addPoseBone(fp,  'DownNeck', 'MHNeck', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limNeck, (1,1,1)])])
    
   
    # Deform spine    
    addDeformSpine(fp, 'DfmRoot', 'Root', 'DownHips', None, None, False, True, [])
    
    addDeformSpine(fp, 'DfmHips', 'Hips', 'DownHips', None, None, False, True, [])
    
    addDeformSpine(fp, 'DfmSpine1', 'Spine1', 'DownSpine1', 'DownSpine1', 'DownPT1', True, True,
        [('StretchTo', 0, 1, ['Stretch', 'Spine2', 0]) ])
            
    addDeformSpine(fp, 'DfmSpine2', 'Spine2', 'DownSpine2', 'DownSpine2', 'DownPT2', True, False,
        [('StretchTo', 0, 1, ['Stretch', 'Spine3', 0]) ])

    addDeformSpine(fp, 'DfmSpine3', 'Spine3', 'DownSpine3', 'DownSpine3', 'DownPT3', True, False, [])
    
    addDeformSpine(fp, 'DfmNeck', 'Neck', 'DownNeck', None, None, False, True, [])

#
#   BodyPropDrivers
#   (Bone, Name, Props, Expr)
#

    copyDeform(fp, 'DfmHead', 'Head', 0, U_ROT, None, [])
 
    # Head
    addPoseBone(fp,  'Head', 'MHHead', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-60*D,40*D, -60*D,60*D, -45*D,45*D), (1,1,1)])])

    # Torso
    addPoseBone(fp,  'DfmStomach',None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', C_STRVOL, 1, ['Stretch', 'DfmRib', 1]),
        ])

    #addPoseBone(fp, 'RibTarget', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])
    #addPoseBone(fp, 'HipBone', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, [])
    addPoseBone(fp,  'Breathe', 'MHCube01', None, (1,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp,  'Penis', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, [])

    addPoseBone(fp,  'Scrotum', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, [])

    return

#
#   addDeformSpine(fp, dbone, uptrg, downtrg, downik, downpt, invert, cpyloc, cnss):
#

def addDeformSpine(fp, dbone, uptrg, downtrg, downik, downpt, invert, cpyloc, cnss):
    if cpyloc:
        cnss.append( ('CopyLoc', 0, 1, ['UpLoc', uptrg, (1,1,1), (0,0,0), False, False]) )
    cnss.append( ('CopyRot', 0, 0, ['UpRot', uptrg, (1,1,1), (0,0,0), False]) )        
    cnss.append( ('CopyLoc', 0, 0, ['DownLoc', downtrg, (1,1,1), (0,0,0), invert, False]) )
    if downik:
        cnss.append( ('IK', 0, 0, ['DownIK', downik, 1, (-90*D, downpt), (True, False,True)]) )
    else:        
        cnss.append( ('CopyRot', 0, 0, ['DownRot', downtrg, (1,1,1), (0,0,0), False]) )        
    addPoseBone(fp, dbone, None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, cnss)
    return 

#
#   BodyPropDrivers
#   (Bone, Name, Props, Expr)
#

BodyPropDrivers = [
    ('DfmRoot', 'UpRot', ['InvertSpine'], '1-x1'),
    ('DfmRoot', 'UpLoc', ['InvertSpine'], '1-x1'),
    ('DfmRoot', 'DownLoc', ['InvertSpine'], 'x1'),
    ('DfmRoot', 'DownRot', ['InvertSpine'], 'x1'),

    ('DfmHips', 'UpRot', ['InvertSpine'], '1-x1'),
    ('DfmHips', 'UpLoc', ['InvertSpine'], '1-x1'),
    ('DfmHips', 'DownLoc', ['InvertSpine'], 'x1'),
    ('DfmHips', 'DownRot', ['InvertSpine'], 'x1'),

    ('DfmSpine1', 'UpLoc', ['InvertSpine'], '1-x1'),
    ('DfmSpine1', 'UpRot', ['InvertSpine'], '1-x1'),
    ('DfmSpine1', 'DownLoc', ['InvertSpine'], 'x1'),
    ('DfmSpine1', 'DownIK', ['InvertSpine'], 'x1'),

    ('DfmSpine2', 'UpRot', ['InvertSpine'], '1-x1'),
    ('DfmSpine2', 'DownLoc', ['InvertSpine'], 'x1'),
    ('DfmSpine2', 'DownIK', ['InvertSpine'], 'x1'),

    ('DfmSpine3', 'UpRot', ['InvertSpine'], '1-x1'),
    ('DfmSpine3', 'DownLoc', ['InvertSpine'], 'x1'),
    ('DfmSpine3', 'DownIK', ['InvertSpine'], 'x1'),

    ('DfmNeck', 'UpLoc', ['InvertSpine'], '1-x1'),
    ('DfmNeck', 'UpRot', ['InvertSpine'], '1-x1'),
    ('DfmNeck', 'DownLoc', ['InvertSpine'], 'x1'),
    ('DfmNeck', 'DownRot', ['InvertSpine'], 'x1'),

    ('Root', 'LimitRot', ['InvertSpine'], 'x1'),
    ('Shoulders', 'LimitRot', ['InvertSpine'], '1-x1'),
    ('Shoulders', 'LimitDist', ['SpineStretch', 'InvertSpine'], '(1-x1)*(1-x2)'),
    
    ('Spine3', 'IK', ['SpineIk', 'InvertSpine'], 'x1*(1-x2)'),
]

#
#   BreastControlPoses(fp):
#

def BreastControlPoses(fp):
    limBreastRot = (-45*D,45*D, -10*D,10*D, -20*D,20*D)
    limBreastScale =  (0.5,1.5, 0.2,2.0, 0.5,1.5)

    addPoseBone(fp,  'Breast_L', 'MHEndCube01', None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, 
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limBreastRot, (1,1,1)]),
         #('LimitScale', C_OW_LOCAL, 1, ['Scale', limBreastScale, (1,1,1)])
         ])

    addPoseBone(fp,  'Breast_R', 'MHEndCube01', None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limBreastRot, (1,1,1)]),
         #('LimitScale', C_OW_LOCAL, 1, ['Scale', limBreastScale, (1,1,1)])
         ])
    return

#
#    BodyShapeDrivers
#    Shape : (driver, channel, coeff)
#

BodyShapeDrivers = {
    'BreatheIn' : ('Breathe', 'LOC_Z', ('0', '2.0')), 
}

#
#    BodyShapeKeyScale = {
#

BodyShapeKeyScale = {
    'BreatheIn'            : ('spine1', 'neck', 1.89623),
    'BicepFlex'            : ('r-uparm-front', 'r-uparm-back', 0.93219),
}

BodySpines = [
    ('Spine', ['Spine1IK', 'Spine2IK', 'Spine3IK', 'Spine4IK', 'Shoulders'])
]



