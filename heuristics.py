# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 16:56:13 2020

@author: Anthony
"""

import random

import ordonnancement as o
import flowshop as f

# schedules jobs according to a sequence and returns the corresponding length
def evaluate(sequence, nb_machines) :
    ordo = o.Ordonnancement(nb_machines)
    ordo.ordonnancer_liste_job(sequence)
    return ordo.duree()

# creates a random scheduling and prints its information
def random_scheduling(F) :
    sequence = []
    while F.l_job != [] :
        sequence.append(F.l_job.pop(random.randint(0, len(F.l_job) - 1)))
    ordo = o.Ordonnancement(F.nb_machines)
    ordo.ordonnancer_liste_job(sequence)
    ordo.afficher()
    print("The length of this scheduling is {}".format(evaluate(sequence, F.nb_machines)))

# Simple test of the 'evaluate' and 'random_scheduling' functions
F = f.Flowshop()
F.definir_par("jeu2.txt")
random_scheduling(F)