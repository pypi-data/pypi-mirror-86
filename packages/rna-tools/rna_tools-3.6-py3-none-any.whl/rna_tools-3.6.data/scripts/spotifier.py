#!python
"""
install to work on psd files: psd-tools3
"""
import argparse
from PIL import Image, ImageChops, Image, ImageDraw, ImageFont, ImageStat
import logging
import os


def trim(im):
    """
    https://stackoverflow.com/questions/10615901/trim-whitespace-using-pil
    """
    bg = Image.new(im.mode, im.size, im.getpixel((1,1)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 0.5, -100)  # 1.0
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else: return im

def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    #parser.add_argument('-', "--", help="", default="")

    parser.add_argument("-v", "--verbose",
                        action="store_true", help="be verbose")
    parser.add_argument("-d", "--debug",
                        action="store_true", help="be even more verbose")

    parser.add_argument("--dont-align",
                        action="store_true", help="don't align dots")
    parser.add_argument("-x", default=30, type=int)
    parser.add_argument("-y", default=30, type=int)
    parser.add_argument("--trim-rms", default=50, type=int)
    parser.add_argument("--size", default=110, type=int)
    parser.add_argument("-a", "--annotate", action="store_true")
    parser.add_argument("-t", "--title")
    parser.add_argument("map", help='map')
    parser.add_argument("file", help="pre-processed image(s)", nargs='+')
    return parser


def get_rms(im):
    stat = ImageStat.Stat(im)
    #r,g,b = stat.mean
    ## print('bg sum', stat.sum[0])
    ## print('bg mean', stat.mean[0])
    ## print('bg rms', stat.rms[0])
    return stat.rms[0]


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    if list != type(args.file):
        args.file = [args.file]
        
    outputs = []

    for file in args.file:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(message)s",
            handlers=[
                logging.FileHandler("spotifier.log"),
                logging.StreamHandler()
            ])
        logging.info('file: %s ' % (str(args)))

        args.trim = not args.dont_align
        if file.endswith('.psd'):
             try:
                 from psd_tools import PSDImage
             except:
                 print('pip install psd-tools3')

             psd = PSDImage.load(file)
             if 1 or args.verbose:
                 for l in psd.layers:
                     if l.name != 'Background':
                         i = l.as_PIL()
                         #i.save('tmp.png')
                     print(l)
             img = psd.as_PIL()
            ## from PIL import Image, ImageSequence
            ## im = Image.open(args.file)
            ## layers = [frame.copy() for frame in ImageSequence.Iterator(im)]
            ## print(layers)
            ## img = layers
        else:
            img = Image.open(file)

        # load map
        list_txt = '['
        names = []
        for l in open(args.map):
            if l.strip():

                name = ''
                if '#' in l:
                    l, name = l.split('#')
                names.append(name.strip())  # collect names

                list_txt += '[' + l + '],'
        list_txt += ']'
        figure = eval(list_txt)
        if args.verbose: print('Figure:', figure)

        # parameters
        xshift = 121
        yshift = 110
        size = args.size
        half = size / 2

        x0 = args.x
        y0 = args.y

        # format of the plate
        PLATE_FORMAT = [
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 0],
             ]

        pix = [
            # 1
            [390, 119], # 1
            [525, 117], # 2
            [661, 121], # 3
            [796, 117], # 4

            # 2
            [259, 234], # 5
            [389, 234], # 6
            [526, 234], # 7
            [661, 234], # 8
            [803, 234], # 9
            [942, 229], # 10

            # 3
            [134, 360], # 11
            [257, 352], # 12
            [393, 354], # 13
            [529, 354], # 14
            [665, 348], # 15
            [803, 349], # 16
            [944, 350], # 17
            [1049,350], # 18

            [125, 479], # 19
            [254, 474.00], # 20
            [389.00, 479], # 21
            [527.00, 479], # 22
            [668.00, 479], # 23
            [804.00, 479], # 24
            [941.00, 473.00], # 25
            [1060.00, 475.00], # 26

            [125, 597], # 27
            [254, 597], # 28
            [389.00, 597], # 29
            [527.00, 597], # 30
            [668.00, 597], # 31
            [804.00, 597], # 32
            [941.00, 597], # 33
            [1060.00, 597], # 34

            [125, 710], # 35
            [254, 719], # 36
            [389.00, 719], # 37
            [527.00, 719], # 38
            [668.00, 719], # 39
            [804.00, 719], # 40
            [941.00, 719], # 41
            [1060.00, 719], # 42

            [125, 846], # 43
            [254, 846], # 44
            [389, 846], # 45
            [527, 846], # 46
            [668, 846], # 47
            [804, 846], # 48
            [941, 846], # 49
            [1060, 846], # 50

            [254, 970], # 51
            [389, 970], # 52
            [527, 970], # 53
            [668, 970], # 54
            [804, 970], # 55
            [941, 970], # 56

            [395, 1085], # 57
            [530, 1085], # 58
            [665, 1085], # 59
            [794, 1085], # 60
            [940, 1085], # 61
            ]

        x_id = 0
        y_id = 0

        spots = []
        spot_id = 1
        for row in PLATE_FORMAT:
            for i in row:
                #x = x0 + (xshift * x_id)  # 150 * 3
                #y = y0 + (yshift * y_id) # 120 * 3
                #print(x, y)
                if i: #  and y_id == 1:
                    x, y = pix[spot_id - 1] # index for list

                    area = (x - half, y - half, x + half, y + half)
                    cropped_img = img.crop(area)
                    rms = get_rms(img)
                    if args.trim and rms > args.trim_rms:
                        cropped_img = trim(cropped_img)
                    if args.debug:
                        cropped_img.save('auto-' + str(y_id) + '-' + str(x_id) + '.png')
                    if args.verbose: print(spot_id, '----------------',)
                    spot_id += 1
                    spots.append(cropped_img)
                x_id += 1
            y_id += 1 # move row down
            x_id = 0

        extra = 0
        if args.annotate:
            extra = 600
        fig = Image.new('RGB', (len(figure[0]) * 100 + extra, len(figure) * 100))
        draw = ImageDraw.Draw(fig)
        x = 0; y = 0

        # LOAD FONT
        # font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
        # should work for OSX
        try:
            fnt = 'Helvetica.ttc'
            font = ImageFont.truetype(fnt, size=40)
        except OSError:
            font = ImageFont.load_default() # should work for everything else
        font_bar = ImageFont.truetype(fnt, size=100)
        #####################################################

        picked_wt = False

        for i, row in enumerate(figure):
            spots_text = ''
            row_fig = Image.new('RGB', (len(figure[0]) * 100, len(figure) * 100)) # for calculations, for each raw new one
            row_fig_y = 0
            for s in row:  # spot in row
                # for center something like this https://stackoverflow.com/questions/1970807/center-middle-align-text-with-pil
                fig.paste(spots[s - 1], (x, y)) # s - 1 # index from 0
                row_fig.paste(spots[s - 1], (x, row_fig_y))
                spots_text += ' ' + str(s)
                x += 100
            # run it for the whole row
            if not picked_wt:
                wt = get_rms(row_fig)
                picked_wt = True
            row_fig_rms = get_rms(row_fig)
            d = round(row_fig_rms - wt, 1)
            if args.verbose: print("%.2f %.2f ∆" % (round(wt, 2), row_fig_rms), d)
            #print(round(1, 2), )
            # str(x) + '-' + str(y)
            if args.annotate:
                draw.text((x, y), '|', font=font_bar, fill = 'darkgray')
                txt = '  ' + str(d).rjust(5) + ' #' + str(i + 1) + ' ' +  names[i] + ' ' + spots_text + '\n' + args.title
                draw.text((x + 20, y + 10), txt, font = font, fill ="white", align="center")#, , align ="right")
            y += 100
            x = 0

        fig.show()

        map_name = os.path.splitext(os.path.basename(args.map))[0]
        outfn = os.path.splitext(file)[0] + '_spots_' + map_name + '.png'
        fig.save(outfn)
        outputs.append(outfn)

    if len(outputs) > 1:
        # append files to make the final figure
        width = Image.open(outputs[0]).width
        img = Image.new('RGB', (width, 100 * len(outputs)))
        x = 0
        y = 0
        for output in outputs:
            out_img = Image.open(output)            
            img.paste(out_img, (x, y))              
            y += 100
        draw = ImageDraw.Draw(img)
        draw.line([(0, 0), (3, 3)], fill='orange', width=10)

        map_path = os.path.splitext(args.map)[0]
        img.save(map_path + '_all.png')
        img.show()
