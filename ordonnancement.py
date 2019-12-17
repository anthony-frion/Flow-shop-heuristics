#!/usr/bin/env python

""" Classe Ordonnancement """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

#import Job
import job

class Ordonnancement():

    # constructeur pour un ordonnancement vide
    def __init__(self, nb_machines):
        # séquence des jobs
        self.seq = []            
        self.nb_machines = nb_machines
        # durée totale
        self.dur = 0
        # date à partir de laquelle la machine est libre
        self.date_dispo = [0 for i in range(self.nb_machines)]

    def duree(self):
        return self.dur
    
    def sequence(self):
        return self.seq
    
    def date_disponibilite(self, num_machine):
        return self.date_dispo[num_machine]
    
    def fixer_date_disponibilite(self, num_machine, date):
        self.date_dispo[num_machine] = date
        
    def date_debut_operation(self, job, operation):
        return job.date_deb[operation]

    def fixer_date_debut_operation(self, job, operation, date):
        job.date_deb[operation] = date
        


    def afficher(self):
        print("Ordre des jobs :", end='')
        for job in self.seq:
            print(" ",job.numero()," ", end='')
        print()
        for job in self.seq:
            print("Job", job.numero(), ":", end='')
            for mach in range(self.nb_machines):
                print(" op", mach, "à t =", self.date_debut_operation(job, mach),"|", end='')
            print()
        print("Cmax =", self.dur)

    # exo 2 A REMPLIR
    def ordonnancer_job(self, job):
        self.seq.append(job)
        for operation in range(job.nb_op):
            date1 = self.date_disponibilite(operation)
            date2 = job.date_deb[operation]
            nouvelle_date_debut = max(date1, date2)
            nouvelle_date_fin = nouvelle_date_debut + job.duree_operation(operation)
            self.fixer_date_disponibilite(operation, nouvelle_date_fin)
            self.fixer_date_debut_operation(job, operation, nouvelle_date_debut)
            if operation < job.nb_op - 1 :
                self.fixer_date_debut_operation(job, operation+1, nouvelle_date_fin)
            
            

    # exo 3 A REMPLIR
    def ordonnancer_liste_job(self, liste_jobs):
        for J in liste_jobs :
            self.ordonnancer_job(J)
        nv_liste_jobs = []
        for J in liste_jobs :
            NJ = job.Job(J.numero(), J.duree_op)
            nv_liste_jobs.append(NJ)
        self.dur = self.date_disponibilite(self.nb_machines-1)
        #return nv_liste_jobs
        
        


O = Ordonnancement(3)
    
if __name__ == "__main__":
    pass
'''
J1 = job.Job(1, [4,5,7])
J2 = job.Job(2, [9,3,4])
J3 = job.Job(3, [2,6,4])
O = Ordonnancement(3)
O.ordonnancer_liste_job([J1, J2, J3])
O.afficher()'''