# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 16:56:13 2020

@author: Anthony
"""

import random

import ordonnancement as o
import flowshop as f

import numpy as np


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
"""F = f.Flowshop()
F.definir_par("jeu2.txt")
random_scheduling(F)"""

#####################################################"


# Useful auxilary functions

def fst(couple):
    a, b = couple
    return a


def snd(couple):
    a, b = couple
    return b





# schedules jobs according to a sequence and returns the corresponding length
def evaluate(sequence, nb_machines):
    ordo = o.Ordonnancement(nb_machines)
    ordo.ordonnancer_liste_job(sequence)
    time = ordo.duree()
    return time


# creates a random sequences from the jobs given in the flowshop F
def random_sequence(F):
    sequence = []
    jobs = [J for J in F.l_job]
    while jobs != []:
        sequence.append(jobs.pop(random.randint(0, len(jobs) - 1)))
    return sequence


# creates a random scheduling and prints its information
def random_scheduling(F):
    sequence = random_sequence(F)
    ordo = o.Ordonnancement(F.nb_machines)
    ordo.ordonnancer_liste_job(sequence)
    ordo.afficher()
    print("The length of this scheduling is {}".format(evaluate(sequence, F.nb_machines)))
    return sequence


# Swaps the two elements at the given indexes
def swap(sequence, index1, index2):
    copy = [J for J in sequence]
    copy[index1], copy[index2] = sequence[index2], sequence[index1]
    return copy


# Inserts the element index2 at the position index1
def insert(sequence, index1, index2):
    copy = [J for J in sequence]
    if index1 > index2:
        index1, index2 = index2, index1
    copy[index1] = sequence[index2]
    for k in range(index1 + 1, index2 + 1):
        copy[k] = sequence[k - 1]
    return copy


# Gets a random neighbour with the swap and insertion operators
def random_neighbour(sequence):
    index1, index2 = random.randint(0, len(sequence) - 1), random.randint(0, len(sequence) - 1)
    while index2 == index1:
        index2 = random.randint(0, len(sequence) - 1)
    if random.randint(0, 1) == 0:
        return swap(sequence, index1, index2)
    else:
        return insert(sequence, index1, index2)


# Computes the simulated annealing and returns a sequence of jobs and the associated time
# For each iteration the temperature is multiplied by the 'temperature_multiplier' parameter
# Once the temperature is under the 'final_temperature' parameter, the algorithm stops
def recuit(F, initial_temperature, temperature_multiplier, final_temperature):
    sequence = random_sequence(F)
    time = evaluate(sequence, F.nb_machines)
    temperature = initial_temperature
    while temperature >= final_temperature:
        nei_seq = random_neighbour(sequence)
        nei_time = evaluate(nei_seq, F.nb_machines)
        if nei_time <= time or np.exp(- (time - nei_time) / temperature) <= random.random():
            sequence = nei_seq
            time = nei_time
        temperature *= temperature_multiplier
    return sequence, time


# Auxilary function for the 'one cut point' reproduction
def auxReproduction1(seq1, seq2, cut_point, F):
    n = len(seq1)
    first_part = seq1[:cut_point]
    child_seq = first_part
    for k in range(cut_point, n):
        if seq2[k] not in first_part:
            child_seq.append(seq2[k])
    for i in range(cut_point):
        if seq2[i] not in child_seq:
            child_seq.append(seq2[i])
    time = evaluate(child_seq, F.nb_machines)
    return child_seq, time


# Random reproduction of two sequences with one cut point
def reproduction1(seq1, seq2, F):
    cut_point = random.randint(0, len(seq1) - 1)
    return auxReproduction1(seq1, seq2, cut_point, F)


# Best possible reproduction of two sequences with one cut point
def bestReproduction1(seq1, seq2, F):
    best_child = seq1
    best_time = 100000
    for cut_point in range(len(seq1)):
        child_seq, time = auxReproduction1(seq1, seq2, cut_point, F)
        if time < best_time:
            best_time = time
            best_child = child_seq
    return best_child, best_time


# Auxilary function for the 'two cut points' reproduction
def auxReproduction2(seq1, seq2, cut_point1, cut_point2, F):
    first_part = seq1[:cut_point1]
    last_part = seq1[cut_point2:]
    mid_part = []
    for J in seq2[cut_point1: cut_point2]:
        if J not in first_part and J not in last_part:
            mid_part.append(J)
    for J in seq1[cut_point1: cut_point2]:
        if J not in mid_part:
            mid_part.append(J)
    child_seq = first_part + mid_part + last_part
    time = evaluate(child_seq, F.nb_machines)
    return child_seq, time


# Random reproduction of two sequences with one cut point
def reproduction2(seq1, seq2, F):
    cut_point1, cut_point2 = 0, 0
    while cut_point1 >= cut_point2:
        cut_point1, cut_point2 = random.randint(0, len(seq1) - 1), random.randint(0, len(seq1) - 1)
    return auxReproduction2(seq1, seq2, cut_point1, cut_point2, F)


# Best possible reproduction of two sequences with one cut point
def bestReproduction2(seq1, seq2, F):
    best_child = seq1
    best_time = 100000
    for cut_point1 in range(1, len(seq1) - 1):
        for cut_point2 in range(cut_point1 + 1, len(seq1) - 1):
            child_seq, time = auxReproduction2(seq1, seq2, cut_point1, cut_point2, F)
            if time < best_time:
                best_time = time
                best_child = child_seq
    return best_child, best_time


# Generates an initial population of solutions with the simulated annealing,
# Then makes them reproduce themselves following a 'binary tree' structure :
# Each generation is half the size of the previous one
def binaryTreeReproductions(initialPopulation, reproductionAlgorithm):
    recuits = []
    for k in range(initialPopulation):
        sequence, time = recuit(F, 20, 0.99, 1)
        recuits.append((sequence, time))
    print([snd(x) for x in recuits], min([snd(x) for x in recuits]))
    population = recuits
    while len(population) > 1:
        new_population = []
        for k in range(len(population) // 2):
            new_population.append(reproductionAlgorithm(fst(population[2 * k]), fst(population[2 * k + 1]), F))
        population = new_population
    print(population[0])


# Creates an initial population through annealing, then reduces it to one solution
# At each step it seeks a good possible reproduction between the first element of the population and the others
# Then it kills the parents and adds the new found solution to the population
# The goal is to reduce the time, so it always looks for reproductions which the child is better than both the parents
def seekBestReproductions(initialPopulation, reproductionAlgorithm):
    recuits = []
    for k in range(initialPopulation):
        sequence, time = recuit(F, 20, 0.99, 1)
        recuits.append((sequence, time))
    print([snd(x) for x in recuits], min([snd(x) for x in recuits]))
    population = recuits
    while len(population) > 1:
        best_child, best_time = population[0]
        best_parent = 1
        for k in range(1, len(population)):
            child, time = reproductionAlgorithm(fst(population[0]), fst(population[k]), F)
            if time < best_time and time < snd(population[k]) and time < snd(population[0]):
                best_time = time
                best_child = child
                best_parent = k
        print("Obtaining time {} from parents of times {} and {}".format(best_time, snd(population[0]),
                                                                         snd(population[best_parent])))
        population.pop(0)
        if best_parent != 1:
            population.pop(best_parent - 1)
        else:
            to_remove = 0
            for k in range(len(population)):
                if snd(population[k]) > snd(population[to_remove]):
                    to_remove = k
            population.pop(to_remove)
        population.append((best_child, best_time))
    print(population[0])


# Tests
F = f.Flowshop()
F.definir_par("jeu3.txt")
seekBestReproductions(200, bestReproduction1)