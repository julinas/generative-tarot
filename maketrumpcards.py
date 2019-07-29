from makecard import drawSvg
import re
import retrieve_image

width = 225
height = 300

def maketrumpcard(i, keyword):
    polygons, foundimg = retrieve_image.getImage(keyword, desired_width=width, desired_height=height, return_found=True)
    path = 'cards/trumps/{}_{}.svg'.format(i, keyword)
    drawSvg(width, height, polygons, keyword, keyword, path)

    foundimg_path = 'found_imgs/trumps/{}_{}.jpg'.format(i, keyword)
    foundimg.save(foundimg_path)
    
def maketrumpcards():
    trumpspath = 'trumpstext'
    regex = r'\(\'([a-z]+)\', ([0-9]+)\)'

    with open('booklet.md', 'w') as ff:
        ff.write('# Description of Deck and Suggested Readings\n\n')
        ff.write('## Major Arcana\n\n')
        with open(trumpspath, 'r') as f:
            line = f.readline()
            foundall = re.findall(regex, line)
            for i, match in enumerate(foundall):
                print('processing {}'.format(match[0]))
                maketrumpcard(i, match[0])
                ff.write('**{} {}**\n\n'.format(i, match[0])) 
                
    
if __name__ == "__main__":
    maketrumpcards()