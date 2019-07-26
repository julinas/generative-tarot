from copy import deepcopy as copy
import math
import numpy as np
from PIL import Image, ImageDraw, ImageChops
import random
from scipy.stats import truncnorm
import sys

import cv2

from maketrumpcards import drawSvg

DNA_TEST = None
DNA_BEST = None

NumShapes = 100
NumVertices = 6
width = 225
height = 300
BACKGROUND_COLOR = 'white'
CHANGED_SHAPE_INDEX = 0

NORM_COEF = width*height*3*255
FITNESS_MAX = sys.maxsize
FITNESS_TEST = FITNESS_MAX
FITNESS_BEST = FITNESS_MAX

CURR_FITNESS_SURPASSED = 0

def randint(maxnum): # random from normal distribution 
    num = math.floor(maxnum * truncnorm.rvs(0, 1, size=1))
    return num

class DNA:
    def __init__(self):
        self.polygons = []
        for i in range(NumShapes):
            # shape is color and points
            # points is randint () width and height
            shape = []
            for j in range(NumVertices):
                point = (randint(width), randint(height))
                shape.append(point)
            polygon = {
                'shape': shape,
                'color': (0, 0, 0, 128)
            }
            self.polygons.append(polygon)
            
    def drawImage(self):
        img = Image.new('RGB', (width, height), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img, 'RGBA')
        for i in range(NumShapes):
            polygon = self.polygons[i]
            draw.polygon(polygon['shape'], fill=polygon['color'])
        del draw
        return img

def mutateDNA(dna):
    global CHANGED_SHAPE_INDEX
    CHANGED_SHAPE_INDEX = randint(NumShapes)
    
    # cast to list, mutate, and cast back to tuple
    # tuple is used for ImageDraw but is immutable
    if True or random.random() < 0.5:
        # mutate color
        colorIndex = randint(4)
        color = list(dna.polygons[CHANGED_SHAPE_INDEX]['color'])
        color[colorIndex] = randint(256)
        dna.polygons[CHANGED_SHAPE_INDEX]['color'] = tuple(color)
    else:
        # mutate shape
        for point in dna.polygons[CHANGED_SHAPE_INDEX]['shape']:
            point = (randint(width), randint(height))

def compute_fitness(dna, target_img):
    curr_img = dna.drawImage()
    diff = ImageChops.difference(curr_img, target_img)
    return np.sum(np.absolute(np.array(diff)))

    
def pass_gene_mutation(dna_from, dna_to, gene_index):
    newcolor = dna_from.polygons[gene_index]['color']
    dna_to.polygons[gene_index]['color'] = (newcolor[0], newcolor[1], newcolor[2], newcolor[3])
    newshape = dna_from.polygons[gene_index]['shape']
    dna_to.polygons[gene_index]['shape'] = []
    for newpoint in newshape:
        point = (newpoint[0], newpoint[1])
        dna_to.polygons[gene_index]['shape'].append(point)

def evolve(target_img):
    global DNA_TEST, DNA_BEST, FITNESS_BEST, CURR_FITNESS_SURPASSED
    mutateDNA(DNA_TEST)
    FITNESS_TEST = compute_fitness(DNA_TEST, target_img)
    FITNESS_BEST_NORMALIZED = 100 * (1 - FITNESS_BEST/NORM_COEF)
    
    # we want fitness/error to be lower
    if (FITNESS_TEST <= FITNESS_BEST):
        pass_gene_mutation(DNA_TEST, DNA_BEST, CHANGED_SHAPE_INDEX)
        
        FITNESS_BEST = FITNESS_TEST

        # img = DNA_BEST.drawImage()
        # cvimg = np.array(img)
        # cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        
        # cv2.imshow('image', cvimg)
        # cv2.waitKey(1)
        FITNESS_BEST_NORMALIZED = 100 * (1 - FITNESS_BEST/NORM_COEF)
        if (FITNESS_BEST_NORMALIZED > CURR_FITNESS_SURPASSED):
            print("Fitness reached {}".format(CURR_FITNESS_SURPASSED))
            CURR_FITNESS_SURPASSED += .1

        if (FITNESS_BEST_NORMALIZED > 85):
            # img = DNA_BEST.drawImage()
            # cvimg = np.array(img)
            # cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
            
            # cv2.imshow('image', cvimg)
            # cv2.waitKey(1)
            return True
    else:
        pass_gene_mutation(DNA_BEST, DNA_TEST, CHANGED_SHAPE_INDEX)
        
def init():
    global DNA_TEST, DNA_BEST, width, height, CHANGED_SHAPE_INDEX, NORM_COEF, FITNESS_TEST, FITNESS_BEST, CURR_FITNESS_SURPASSED
    DNA_TEST = None
    DNA_BEST = None

    width = 225
    height = 300

    CHANGED_SHAPE_INDEX = 0

    NORM_COEF = width*height*3*255
    FITNESS_TEST = FITNESS_MAX
    FITNESS_BEST = FITNESS_MAX

    CURR_FITNESS_SURPASSED = 0
    
def run_evolve(target_img, desired_width, desired_height):
    global DNA_TEST, DNA_BEST, width, height, NORM_COEF
    
    init()
    
    width = desired_width
    height = desired_height
    NORM_COEF = width*height*4*255

    DNA_TEST = DNA()
    DNA_BEST = copy(DNA_TEST)
    
    target_img = target_img.transpose(Image.FLIP_TOP_BOTTOM)
    
    reachedRequiredFitness = False
    while not reachedRequiredFitness:
        reachedRequiredFitness = evolve(target_img)
        
    for i in range(5000):
        evolve(target_img)
        
    polygons = DNA_BEST.polygons
    return polygons
