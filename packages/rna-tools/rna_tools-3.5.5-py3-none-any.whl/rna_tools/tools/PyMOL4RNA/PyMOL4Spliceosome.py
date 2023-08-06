"""
See the PyMOL Sessions processed with this code here <https://github.com/mmagnus/PyMOL4Spliceosome>
"""
from pymol import cmd
from rna_tools.tools.PyMOL4RNA import code_for_color_spl
from rna_tools.tools.PyMOL4RNA import code_for_spl

try:
    from pymol import cmd
except ImportError:
    print("PyMOL Python lib is missing")
    # sys.exit(0)



def spl(arg=''):
    """
    action='', name=''
    """
    if ' ' in arg:
        action, name = arg.split()
        name = name.lower()
    else:
        action = arg
        name = ''
    #import pandas as pd
    #df = pd.read_excel("/home/magnus/Desktop/pyMoL_colors-EMX.xlsx")
    if not action or action == 'help':
        spl_help()
    elif action == 'color' or arg=='c':
        code_for_color_spl.spl_color()
    elif arg == 'extract all' or arg == 'ea' or arg == 'e':
        code_for_spl.spl_extract()
    elif arg.startswith('hprp28'):
        cmd.do("color purple, PRP28_h* and resi 240-361") # RecA1
        cmd.do("color blue, PRP28_h* and resi 361-631") # RecA1
        cmd.do("color orange, PRP28_h* and resi 631-811")  # RecA2
    elif arg.startswith('hprp8'):
        print("RT, skyblue, 885-1251")
        print("Thumb/X, cyan, 1257-1375")
        cmd.do("color yellow, PRP8_h* and resi 1581-1752")  # rt
        cmd.do("color wheat, PRP8_h* and resi 1767-2020")   # rh
        cmd.do("color salmon, PRP8_h* and resi 2103-2234")  # jab
        cmd.do("color smudge, PRP8_h* and resi 1304-1577")  # linker
        cmd.do("color skyblue, PRP8_h* and resi 812-1303")  # rt
    elif arg.startswith('prp8'):
        print("RT, skyblue, 885-1251")
        print("Thumb/X, cyan, 1257-1375")
        
        cmd.do("color skyblue, PRP8_y* and resi 885-1251")  # rt
        cmd.do("color cyan, PRP8_y* and resi 1257-1375")    # thumb/x
        cmd.do("color smudge, PRP8_y* and resi 1376-1649")  # linker
        cmd.do("color wheat, PRP8_y* and resi  1840-2090")  # rh
        cmd.do("color salmon, PRP8_y* and resi 2150-2395")  # jab
        cmd.do("color yellow, PRP8_y* and resi 1650-1840")  # endo
    elif arg.startswith(''):
        if 'hjab' in arg.lower():
            cmd.select('PRP8_h* and resi 2103-2234')
        if 'hlinker' in arg.lower():
            cmd.select('PRP8_h* and resi 1304-1577')
        if 'hrt' in arg.lower():
            cmd.select('PRP8_h* and resi 812-1303')
        if 'hrh' in arg.lower():
            cmd.select('PRP8_h* and resi 1767-2020')
        if 'he' in arg.lower():
            cmd.select('PRP8_h* and resi 1581-1752')

    elif arg == 'align' or arg=='a':
        cmd.do("""
    align /5gm6//6, /5lj3//V;
    align /5mps//6, /5lj3//V;
    align /6exn//6, /5lj3//V;
    align /5y88//D, /5lj3//V;
    align /5ylz//D, /5lj3//V;
    """)
    else:
        spl_help()

cmd.extend('spl', spl)

def spl_help():
    print("""################ SPL #################
extract all (ea)  - show
colors            - list all colors
######################################
""")
spl_help()

def __spl_color():
    for m in mapping:
        protein = m[0]
        chain = m[1]
        color = m[2]
        print('\_' + ' '.join([protein, chain, color]))
        cmd.do('color ' + color + ', chain ' + chain)
        # cmd.do('color firebrick, chain V') # U6

def _spl_color():
    """Color spl RNAs (for only color spl RNA and use 4-color code for residues see `spl2`)
    """
    AllObj = cmd.get_names("all")
    for name in AllObj:
        if 'Exon' in name or 'exon' in name:
            cmd.color('yellow', name)
        if 'Intron' in name or 'intron' in name or '5splicing-site' in name:
            cmd.color('gray40', name)
        if '3exon-intron' in name.lower():
            cmd.color('gray20', name)
        if name.startswith("U2_snRNA"):
            cmd.color('forest', name)
        if name.startswith("U5_snRNA"):
            cmd.color('blue', name)
        if name.startswith("U4_snRNA"):
            cmd.color('orange', name)
        if name.startswith("U6_snRNA"):
            cmd.color('red', name)

    cmd.do('color gray')

    # trisnrp
    cmd.do('color orange, chain V') # conflict
    cmd.do('color red, chain W')
    cmd.do('color blue, chain U')
    #
    cmd.do('color blue, chain 5')
    cmd.do('color forest, chain 2')
    cmd.do('color red, chain 6')
    cmd.do('color orange, chain 4')
    cmd.do('color yellow, chain Y')
    # shi
    cmd.do('color blue, chain D') # u5
    cmd.do('color forest, chain L') # u2
    cmd.do('color red, chain E') # u6
    cmd.do('color yellow, chain M')
    cmd.do('color yellow, chain N')
    # afte branch
    cmd.do('color blue, chain U') # u5
    cmd.do('color forest, chain Z') # u2
    cmd.do('color red, chain V') # u6
    cmd.do('color yellow, chain E')
    cmd.do('color black, chain I')
    # 5WSG
    # Cryo-EM structure of the Catalytic Step II spliceosome (C* complex) at 4.0 angstrom resolution
    cmd.do('color blue, chain D') # u5
    #cmd.do('color forest, chain L') # u2
    cmd.do('color yellow, chain B')
    cmd.do('color yellow, chain b')
    cmd.do('color black, chain N')
    cmd.do('color black, chain M')

    cmd.do('color black, chain 3') # orange
    cmd.do('color black, chain E') # yellow
    cmd.do('color black, chain i')
    cmd.do('color black, chain e')

    cmd.do('color black, chain e')

    cmd.do('color dirtyviolet, chain L') # bud31
    cmd.do('color rasberry, chain L') # CERF1

    cmd.do('color skyblue, chain A') # PRP8
    cmd.do('color grey60, chain B') # BRR2
    cmd.do('color dirtyiolet, chain L') # BUD31
    cmd.do('color rasberry, chain O') # CEF1
    cmd.do('color rasberry, chain S') # CLF1
    cmd.do('color dirtyviolet, chain P') # CWC15
    cmd.do('color lightteal, chain D') # CWC16/YJU2
    cmd.do('color ruby, chain M') # CWC2
    cmd.do('color violetpurple, chain R') # CWC21
    cmd.do('color bluewhite, chain H') # CWC22
    cmd.do('color deepteal, chain F') # CWC25
    cmd.do('color black, chain I') # Intron
    cmd.do('color dirtyviolet, chain G') # ISY1
    cmd.do('color palegreen, chain W') # LEA1
    cmd.do('color palegreen, chain Y') # Msl1
    cmd.do('color lightpink, chain K') # PRP45
    cmd.do('color smudge, chain Q') # Prp16
    cmd.do('color grey70, chain t') # Prp19
    cmd.do('color lightblue, chain J') # PRP46
    cmd.do('color chocolate, chain N') # SLT11/ECM2
    cmd.do('color grey70, chain s') # Snt309
    cmd.do('color slate, chain C') # SNU114
    cmd.do('color brightorange, chain T') # SYF1
    cmd.do('color forest, chain Z') # U2
    cmd.do('color density, chain U') # U5
    cmd.do('color deepblue, chain b') # U5_Sm

    cmd.do('bg gray')
    # cmd.do('remove (polymer.protein)')

    cmd.set("cartoon_tube_radius", 1.0)
    ino()

def spl2():
    """Color spl RNAs and use 4-color code for residues (for only color spl RNA see `spl`)
    """

    AllObj = cmd.get_names("all")
    for name in AllObj:
        if 'Exon' in name or 'exon' in name:
            cmd.color('yellow', name)
        if 'Intron' in name or 'intron' in name or '5splicing-site' in name:
            cmd.color('gray40', name)
        if '3exon-intron' in name.lower():
            cmd.color('gray20', name)
        if name.startswith("U2_snRNA"):
            cmd.color('forest', name)
        if name.startswith("U5_snRNA"):
            cmd.color('blue', name)
        if name.startswith("U4_snRNA"):
            cmd.color('orange', name)
        if name.startswith("U6_snRNA"):
            cmd.color('red', name)

    cmd.do('color gray')

    # trisnrp
    cmd.do('color orange, chain V') # conflict
    cmd.do('color red, chain W')
    cmd.do('color blue, chain U')
    #
    cmd.do('color blue, chain 5')
    cmd.do('color forest, chain 2')
    cmd.do('color red, chain 6')
    cmd.do('color orange, chain 4')
    cmd.do('color yellow, chain Y')
    # shi
    cmd.do('color blue, chain D') # u5
    cmd.do('color forest, chain L') # u2
    cmd.do('color red, chain E') # u6
    cmd.do('color yellow, chain M')
    cmd.do('color yellow, chain N')
    # afte branch
    cmd.do('color blue, chain U') # u5
    cmd.do('color forest, chain Z') # u2
    cmd.do('color red, chain V') # u6
    cmd.do('color yellow, chain E')
    cmd.do('color black, chain I')
    # 5WSG
    # Cryo-EM structure of the Catalytic Step II spliceosome (C* complex) at 4.0 angstrom resolution
    cmd.do('color blue, chain D') # u5
    #cmd.do('color forest, chain L') # u2
    cmd.do('color yellow, chain B')
    cmd.do('color yellow, chain b')
    cmd.do('color black, chain N')
    cmd.do('color black, chain M')

    cmd.do('color black, chain 3') # orange
    cmd.do('color black, chain E') # yellow
    cmd.do('color black, chain i')
    cmd.do('color black, chain e')

    cmd.do('bg gray')
    cmd.do('remove (polymer.protein)')

    cmd.color("red",'resn rG+G and name n1+c6+o6+c5+c4+n7+c8+n9+n3+c2+n1+n2')
    cmd.color("forest",'resn rC+C and name n1+c2+o2+n3+c4+n4+c5+c6')
    cmd.color("orange",'resn rA+A and name n1+c6+n6+c5+n7+c8+n9+c4+n3+c2')
    cmd.color("blue",'resn rU+U and name n3+c4+o4+c5+c6+n1+c2+o2')
    cmd.set("cartoon_tube_radius", 1.0)
    ino()


def _spli():
    """
    # this trick is taken from Rhiju's Das code
    color red,resn rG+G and name n1+c6+o6+c5+c4+n7+c8+n9+n3+c2+n1+n2
    color forest,resn rC+C and name n1+c2+o2+n3+c4+n4+c5+c6
    color orange, resn rA+A and name n1+c6+n6+c5+n7+c8+n9+c4+n3+c2
    color blue, resn rU+U and name n3+c4+o4+c5+c6+n1+c2+o2

    #
    #cmd.color("yellow", "*intron*")
    #cmd.color("yellow", "*exon*")

    #cmd.show("spheres", "inorganic")
    #cmd.color("yellow", "inorganic")
    """
    cmd.color("orange", "U4_snRNA*")
    cmd.color("red", "U6_snRNA*")
    cmd.color("blue", "U5_snRNA*")
    cmd.color("green", "U2_snRNA*")
    cmd.color("red",'resn rG+G and name n1+c6+o6+c5+c4+n7+c8+n9+n3+c2+n1+n2')
    cmd.color("forest",'resn rC+C and name n1+c2+o2+n3+c4+n4+c5+c6')
    cmd.color("orange",'resn rA+A and name n1+c6+n6+c5+n7+c8+n9+c4+n3+c2')
    cmd.color("blue",'resn rU+U and name n3+c4+o4+c5+c6+n1+c2+o2')

try:
    from pymol import cmd
except ImportError:
    print("PyMOL Python lib is missing")
else:

    #cmd.extend("spl", spl)
    cmd.extend("spl2", spl2)

    # colors taken from https://github.com/maxewilkinson/Spliceosome-PyMOL-sessions
    cmd.set_color('lightgreen', [144, 238, 144])
    cmd.set_color('darkgreen', [0, 100, 0])
    cmd.set_color('darkseagreen', [143, 188, 143])
    cmd.set_color('greenyellow', [173, 255, 47])
    cmd.set_color('coral', [255, 127, 80])
    cmd.set_color('darkorange', [255, 140, 0])
    cmd.set_color('gold', [255, 215, 0])
    cmd.set_color('lemonchiffon', [255,250,205])
    cmd.set_color('moccasin', [255,228,181])
    cmd.set_color('skyblue', [135,206,235])
    cmd.set_color('lightyellow', [255,255,224])
    cmd.set_color('powderblue', [176,224,230])
    cmd.set_color('royalblue', [65,105,225])
    cmd.set_color('cornflowerblue', [100,149,237])
    cmd.set_color('steelblue', [70,130,180])
    cmd.set_color('lightsteelblue', [176,196,222])
    cmd.set_color('violetBlue', [40, 0, 120])
    cmd.set_color('mediumpurple', [147,112,219])
    

    print("""
PyMOL4Spliceosome
-----------------------
spl hprp8
spl prp8
""")
