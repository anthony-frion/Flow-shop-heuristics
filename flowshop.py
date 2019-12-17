#!/usr/bin/env python

"""Résolution du flowshop de permutation : 

 - par algorithme NEH
 - par une méthode évaluation-séparation
 """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

import job
import ordonnancement as o
import sommet as s
import heapq

def comp(L1, L2) :
    result = []
    for x in L2 :
        if x not in L1 :
            result.append(x)
    return result

MAXINT = 10000

class Flowshop():
    def __init__(self, nb_jobs=0, nb_machines=0, l_job=[]):
        self.nb_jobs = nb_jobs
        self.nb_machines = nb_machines
        self.l_job = l_job

    def nombre_jobs(self):
        return self.nombre_jobs

    def nombre_machines(self):
        return self.nombre_machines

    def liste_jobs(self, num):
        return self.l_job[num]

    def definir_par(self, nom):
        """ crée un problème de flowshop à partir d'un fichier """
        # ouverture du fichier en mode lecture
        fdonnees = open(nom,"r")
        # lecture de la première ligne
        ligne = fdonnees.readline() 
        l = ligne.split() # on récupère les valeurs dans une liste
        self.nb_jobs = int(l[0])
        self.nb_machines = int(l[1])
       
        for i in range(self.nb_jobs):
            ligne = fdonnees.readline() 
            l = ligne.split()
            # on transforme les chaînes de caractères en entiers
            l = [int(i) for i in l]
            j = job.Job(i, l)
            self.l_job += [j]
        # fermeture du fichier
        fdonnees.close()
        
    
    # exo 4 A REMPLIR
    def creer_liste_NEH(self):
        nb_machines = self.nb_machines
        L = [J for J in sorted(self.l_job, key = lambda J: J.duree(), reverse=True)]
        O = []
        result = []
        for J in L :
            cand = 1000
            lcand = []
            for k in range(len(result) + 1) :
                copy = [job for job in result]
                copy.insert(k, J)
                O.append(o.Ordonnancement(nb_machines))
                O[0].ordonnancer_liste_job(copy)
                if O[0].dur < cand :
                    cand = O[0].dur
                    lcand = copy
                O.clear()
                for job in copy :
                    job.date_deb = [0 for d in job.date_deb]
            result = lcand        
            O.append(o.Ordonnancement(nb_machines))
        O.append(o.Ordonnancement(nb_machines))
        O[0].ordonnancer_liste_job(result)
        O[0].afficher()
        print("Durée NEH : " + str(O[0].dur))
        return result, O[0].dur
        

    # exo 5 A REMPLIR

    # calcul de r_kj tenant compte d'un ordo en cours
    def calculer_date_dispo(self, ordo, machine, job):
        nouvelle_date_fin = 0
        for operation in range(machine) :
            nouvelle_date_debut = max(nouvelle_date_fin, ordo.date_disponibilite(operation))
            nouvelle_date_fin = nouvelle_date_debut + job.duree_operation(operation)
        return nouvelle_date_fin - ordo.date_disponibilite(0)
            

    # calcul de q_kj tenant compte d'un ordo en cours
    def calculer_duree_latence(self, ordo, machine, job):
        if machine == ordo.nb_machines - 1 :
            return 0
        else :
            nouvelle_date_fin = 0
            for operation in range(machine + 1, job.nb_op) :
                nouvelle_date_debut = max(nouvelle_date_fin, ordo.date_disponibilite(operation))
                nouvelle_date_fin = nouvelle_date_debut + job.duree_operation(operation)
            return nouvelle_date_fin - ordo.date_disponibilite(machine+1)

    # calcul de la somme des durées des opérations d'une liste
    # exécutées sur une machine donnée
    def calculer_duree_jobs(self, machine, liste_jobs):
        return sum([job.duree_operation(machine) for job in liste_jobs])

    # calcul de la borne inférieure en tenant compte d'un ordonnancement en cours
    def calculer_borne_inf(self, ordo, liste_jobs):
        if liste_jobs == [] :
            return 0
        LBcand = 0
        for machine in range(ordo.nb_machines) :
            min_r = min([self.calculer_date_dispo(ordo, machine, job) for job in liste_jobs])
            min_q = min([self.calculer_duree_latence(ordo, machine, job) for job in liste_jobs])
            somme_durees = self.calculer_duree_jobs(machine, liste_jobs)
            LBmachine = min_r + min_q + somme_durees
            if LBmachine > LBcand:
                LBcand = LBmachine
                machinecand = machine
        return LBcand
            

    # exo 6 A REMPLIR
    # procédure par évaluation et séparation
    
    def evaluation_separation(self):
        O = o.Ordonnancement(self.nb_machines)
        compteur = 0
        meilleurOrdo, dureeMeilleurOrdo = self.creer_liste_NEH()
        print("Durée du meilleur ordo initial : " + str(dureeMeilleurOrdo))
        sommet = s.Sommet([], self.l_job, self.calculer_borne_inf(O, []), 0)
        heap = [sommet]
        while heap != [] :
            compteur += 1
            if compteur%2000 == 0 :
                print(str(compteur) + " noeuds parcourus")
            sommet = heapq.heappop(heap)
            O = o.Ordonnancement(self.nb_machines)
            for j in self.l_job :
                for operation in range(j.nb_op) :
                    O.fixer_date_debut_operation(j, operation, 0)
            if sommet.non_places == [] :
                non_places = comp(sommet.seq, self.l_job)
                O.ordonnancer_liste_job(sommet.seq)
                if O.dur <= dureeMeilleurOrdo :
                    meilleurOrdo = sommet.seq
                    dureeMeilleurOrdo = O.dur
                    print("Nouveau meilleur ordonnancement trouvé ! Durée : " + str(O.dur))
                    print([j.numero() for j in meilleurOrdo])
                    O.afficher()
            else :
                for J in sommet.jobs_non_places() :
                    nv_non_places = [j for j in sommet.jobs_non_places()]
                    nv_non_places.remove(J)
                    nv_seq = sommet.seq + [J]
                    O.ordonnancer_liste_job(nv_seq)
                    nv_val = self.calculer_borne_inf(O, nv_seq)
                    if nv_val <= dureeMeilleurOrdo :
                        nv_sommet = s.Sommet(nv_seq, nv_non_places, nv_val, 0)
                        heapq.heappush(heap, nv_sommet)
        print("Recherche terminée")
        print("La meilleure durée est " + str(dureeMeilleurOrdo))
        print("Un ordonnancement optimal est " + str([j.numero() for j in meilleurOrdo]))
        return meilleurOrdo, dureeMeilleurOrdo

F = Flowshop()
F.definir_par("jeu2.txt")
O = o.Ordonnancement(F.nb_machines)
#NEH, duree = F.creer_liste_NEH()
#O = o.Ordonnancement(F.nb_machines)
#print("La borne inf de l'ordonnancement NEH est " + str(F.calculer_borne_inf(O, NEH)))
F.evaluation_separation()

if __name__ == "__main__":
    pass

#Test Commit Juliette

