import drawSvg as draw 

def drawSvg(w, h, polygons, word):
    framemargin = 10
    margin = 25
    titlemargin = 25
    width = w + 2 * margin
    height = h + 2 * margin + titlemargin
    d = draw.Drawing(width, height, origin=(0, 0 - titlemargin))
    d.append(draw.Rectangle(margin-framemargin, margin-framemargin, \
        w + 2 * framemargin, h + 2* framemargin, \
        stroke='black', stroke_width=4, fill='white'))
        
    for polygon in polygons:
        color = polygon['color']
        hex = '#%02x%02x%02x' % (color[0], color[1], color[2])
        opacity = color[3]/255
        
        shape = polygon['shape']
        # hard-coded for 6-polygons
        p = draw.Lines(shape[0][0] + margin, shape[0][1] + margin,
            shape[1][0] + margin, shape[1][1] + margin, \
            shape[2][0] + margin, shape[2][1] + margin, \
            shape[3][0] + margin, shape[3][1] + margin, \
            shape[4][0] + margin, shape[4][1] + margin, \
            shape[5][0] + margin, shape[5][1] + margin, \
            stroke_width=0, close=True, fill=hex, fill_opacity=opacity)
        d.append(p)
    d.append(draw.Text(word.upper(), 20, width/2, -titlemargin/2, center=0.5, fill='black'))
    d.saveSvg('example.svg')
    