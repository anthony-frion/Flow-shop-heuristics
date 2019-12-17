#!/usr/bin/env python

""" Classe Job """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

class Job():
    def __init__(self, numero, tab_durees=[]):
        # identificateur
        self.num = numero
        # nombre d'opérations
        self.nb_op = len(tab_durees)
        self.duree_op = [i for i in tab_durees]
        self.date_deb = [0 for i in tab_durees]
        # ajout exo 1
        self.duree_job = self.calculer_duree_job()
        
    def numero(self):
        return self.num

    def duree_operation(self, operation):
        return self.duree_op[operation]
    
    def date_debut(self, operation):
        return self.date_deb[operation]

    def duree(self):
        return self.duree_job

    def afficher(self):
        print("Job", self.numero(),"de durée totale", self.duree(), ":")
        for num in range(len(self.duree_op)):
            duree = self.duree_op[num]
            debut = self.date_deb[num]
            print("  opération", num, ": durée =", duree, "début =", debut)       

    # exo 1 :  A REMPLIR
    def calculer_duree_job(self):
        return sum(self.duree_op)

if __name__ == "__main__":
    pass