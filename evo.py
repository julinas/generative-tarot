#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Peng Ding @ 2016-01-07 17:00:10

import random
import math
import operator
from PIL import Image, ImageDraw, ImageChops
from functools import reduce

from genetic import genetic, gene

# TARGET_IMG_NAME = 'test.jpg'  # target image file name
POP_SIZE = 25                 # population size
MUT_RATE = 0.05               # mutation rate
GENERATIONS = 100000          # number of generations
CHILDREN_PER_GEN = 5          # children generated in each generations
TRI_NUM = 100                 # number of triangles
BACKGROUND_COLOR = 'white'    # background color

img_width = 225
img_height = 300
baseimg = None
sectDims = None

# load target image and resize
TARGET = None
# TARGET = Image.open(TARGET_IMG_NAME).convert('RGB')
# TARGET = TARGET.resize((500, 500))


class individual(object):
    """
    The individual class, which is an image.

    Attributes:
        genes: all the genes(triangles).
        im: the actual image file.
        fitness: the fitness, the lower the better
    """
    def __init__(self, parent_1=None, parent_2=None):
        """
        Inits an individual.
        If it has parents, generate its genes via crossover operation.
        If not, generate its genes randomly.

        Args:
            parent_1: a parent.
            parent_2: another parent.
        """
        self.genes = []
        op = genetic()
        if parent_1 and parent_2:
            array = op.crossover3(parent_1, parent_2, TRI_NUM)
            self.generate_genes_from_array_with_mut(array, MUT_RATE)
        else:
            for i in range(TRI_NUM):
                self.genes.append(gene(img_width, img_height))
        # set actual image
        self.im = self.get_current_img()
        # calculate fitness
        self.fitness = self.get_fitness(TARGET)

    def get_current_img(self):
        """
        Get actual image file using the properties of the triangles.

        Important: set canvas to RGB, draw object to RGBA.

        Returns:
            im: the image file.
        """
        # im = Image.new('RGB', (img_width, img_height), BACKGROUND_COLOR)
        im = baseimg
        draw = ImageDraw.Draw(im, 'RGBA')
        for gene in self.genes:
            draw.polygon([gene.pos_1, gene.pos_2, gene.pos_3],
                         fill=(gene.color['r'], gene.color['g'],
                               gene.color['b'], gene.color['a']))
        del draw
        return im

    def save_current_img(self, f_name):
        """
        Save image to a file.

        Args:
            f_name: saved file name.
        """
        self.im.save(f_name, 'PNG')
		
    def return_current_img(self):
        """
		Returns image to calling function.
        """
        return self.im

    def get_fitness(self, target):
        """
        Get fitness of the individual.
        This was calculated by RMS distance of histograms.

        Args:
            target: target image.

        Returns:
            the fitness value.
        """
        cropped_target = target.crop(sectDims)
        cropped_im = self.im.crop(sectDims)
		
        h = ImageChops.difference(cropped_target, cropped_im).histogram()
        return math.sqrt(reduce(operator.add,
                         list(map(lambda h, i: h*(i**2),
                             h, list(range(256))*3))) /
                            (float(cropped_target.size[0]) * cropped_target.size[1]))

    def get_array(self):
        """
        Get array representation(DNA sequence) of the genes.

        Returns:
            array: DNA sequence.
        """
        array = []
        for g in self.genes:
            array.append(g.pos_1)
            array.append(g.pos_2)
            array.append(g.pos_3)
            array.append(g.color['r'])
            array.append(g.color['g'])
            array.append(g.color['b'])
        return array

    def generate_genes_from_array_with_mut(self, array, rate):
        """
        Transform DNA sequence into a list of genes,
        plus a mutation.

        Args:
            array: DNA sequence.
            rate: mutation rate.
        """
        new_array = zip(*[iter(array)]*6)
        self.genes = []
        for chunk in new_array:
            g = gene(img_width, img_height)
            if random.uniform(0, 1) > rate:
                g.pos_1 = chunk[0]
                g.pos_2 = chunk[1]
                g.pos_3 = chunk[2]
                g.color['r'] = chunk[3]
                g.color['g'] = chunk[4]
                g.color['b'] = chunk[5]
            self.genes.append(g)


def initialize(pop):
    """
    Inits population.

    Args:
        pop: population.

    Returns:
        pop: population.
    """
    for i in range(POP_SIZE*2):
        pop.append(individual())
    pop.sort(key=lambda x: x.fitness)
    pop = pop[:POP_SIZE]
    return pop


def evolve(pop):
    """
    Evolve population.

    Args:
        pop: population.

    Returns:
        pop: population.
    """
    for i in range(GENERATIONS):

        children = []
        # generate weighed choices according to fitness
        parent_choices = []
        w = 100
        for p in pop:
            parent_choices.append((p, w))
            if w > 0:
                w = w - 10
        pop_choices = [val for val, cnt in parent_choices for j in range(cnt)]
        # generate children
        for j in range(CHILDREN_PER_GEN):
            parent_1 = random.choice(pop_choices)
            parent_2 = random.choice(pop_choices)
            child = individual(parent_1, parent_2)
            children.append(child)
        # compare and save new individuals
        pop += children
        pop.sort(key=lambda x: x.fitness)
        pop = pop[:POP_SIZE]
        # print log info
        # if i % 10000 == 0 or i in [100, 200, 500, 1000, 5000]:
            # pop[0].save_current_img(str(i)+'_b.png')  # save intermediate imgs
        if i % 100 == 0:
            # print current best fitness and avg fitness
            avg = sum(list(map(lambda x: x.fitness, pop))) / 25
            print("Finish {} {} {}".format(str(i), pop[0].fitness, avg))
    return pop

def getApproxImg(img, baseImg, sectID, generations=100000, width=225, height=300):
	global TARGET, baseimg, GENERATIONS, img_width, img_height, sectDims
	TARGET = img
	baseimg = baseImg
	GENERATIONS = generations
	img_width = width
	img_height = height
	
	if sectID == 1:
		sectDims = (0, 0, width/2, height/2)
	elif sectID == 2:
		sectDims = (0, height/2, width/2, height)
	elif sectID == 3:
		sectDims = (width/2, 0, width, height/2)
	elif sectID == 4:
		sectDims = (width/2, height/2, width, height)
	elif sectID == 5:
		sectDims = (width/4, height/4, 3*width/4, 3*height/4)
	
	pop = []
	pop = initialize(pop)
	pop = evolve(pop)
	return pop[0].return_current_img()

if __name__ == '__main__':
    pop = []
    pop = initialize(pop)
    pop = evolve(pop)
    pop[0].save_current_img('best.png')
    print(pop[0].fitness)
