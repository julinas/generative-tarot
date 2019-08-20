import drawSvg as draw 

def drawSvg(w, h, polygons, word, title, saveto_path):
    w = 183
    h = 309
    mult = 4
    bleed = 72
    
    framemargin = 10
    margin = framemargin + bleed
    titlemargin = 96
    width = w * mult + 2 * margin
    height = h * mult + 2 * margin + titlemargin
    d = draw.Drawing(width, height, origin=(0, 0 - titlemargin), style="font-size:70;font-family:Poor Richard, Times New Roman;stroke:black;stroke-width:1;fill:none")
    #d.append(draw.Rectangle(margin-framemargin, margin-framemargin, \
    #    w * mult + 2 * framemargin, h * mult + 2 * framemargin, \
    #    stroke='black', stroke_width=4, fill='none'))
    for polygon in polygons:
        color = polygon['color']
        hex = '#%02x%02x%02x' % (color[0], color[1], color[2])
        opacity = color[3]/255
        
        shape = polygon['shape']
        # hard-coded for 6-polygons
        p = draw.Lines(shape[0][0] * mult + margin, shape[0][1] * mult + margin,
            shape[1][0] * mult + margin, shape[1][1] * mult + margin, \
            shape[2][0] * mult + margin, shape[2][1] * mult + margin, \
            shape[3][0] * mult + margin, shape[3][1] * mult + margin, \
            shape[4][0] * mult + margin, shape[4][1] * mult + margin, \
            shape[5][0] * mult + margin, shape[5][1] * mult + margin, \
            stroke_width=0, close=True, fill=hex, fill_opacity=opacity)
        d.append(p)
    d.append(draw.Text(title.upper(), 70, width/2, 0, \
        center=0.5, fill='black'))
    d.saveSvg(saveto_path)
    