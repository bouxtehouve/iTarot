'''
Created on 23 avr. 2013

@author: Bouxtehouve
'''
# def d'un joueur : nom, main, etc

from cartes import carte
from joueur import joueur

class joueur_max(joueur):
    def __init__(self,nom):
        joueur.__init__(self,nom)
        self.type="joueur_max"
        
    def __str__(self):
        return self.nom

    def joue_une_carte(self,cartes_pli): # Joue la carte de plus haute valeur possible
        cj=joueur.cartes_jouables(self,cartes_pli)
        maxi1=-1
        maxi2=-1
        a=None
        b=None
        trouve=False
        for c in cj:
            if c.hauteur > maxi2 and (c.couleur=="atout"):
                maxi2=c.hauteur
                b=c
            if c.hauteur > maxi1 and not(c.couleur=="atout"):
                maxi1=c.hauteur
                a=c
                trouve=True
        if not trouve:
            cartes_pli.append(b)
            self.main.remove(b)
        else:
            cartes_pli.append(a)
            self.main.remove(a)
        #print "Le joueur " +  self.nom + " joue : " + str(a) + "\n"
            
    def appel_roi(self): # Annonce a la couleur ou il a la plus haute carte ( sauf le roi ), sinon, c'est qu'il a les 4 rois, il s'appelle tout seul
        self.tri_main()
        maximum=-1
        col=None
        for c in self.main:
            if c.couleur != "atout" and carte(c.couleur,"roi") not in self.main and c.hauteur > maximum:
                maximum=c.hauteur
                col=c.couleur
        if col == None:
            col="trefle"
        self.roi_appele=col
        #print "Le joueur " +  self.nom + " appelle le roi de " + self.roi_appele
        
    def fait_son_chien(self): # Fonction qui pourra etre reprise pour l'IA, avec tendance eventuelle a se faire des coupes franches
        # Le joueur met au chien les 3 plus "petites" cartes de son jeu
        for i in xrange(0,3):
            mini=42
            a=None
            modif=False
            for c in self.main:
                if c.hauteur < mini and c.couleur != "excuse" and c.couleur != "atout":
                    mini= c.hauteur
                    a=c
                    modif=True
            if modif:
                self.tas.append(a)
                self.main.remove(a)
        # La a moins que le type ait plus de 16 atouts ca va, je rajoute une clause qui le fait se defausser de ses plus petits atouts au cas ou
        if len(self.tas) < 3:
            self.tri_main()
            if self.main[0].hauteur==1: # On a le petit, on va quand meme pas le mettre au chien
                for i in xrange(0,3-len(self.tas)):
                    self.tas.append(self.main[i+1])
                    self.main.remove(self.main[i+1])
            else: # On n'a pas le petit
                for i in xrange(0,3-len(self.tas)):
                    self.tas.append(self.main[i])
                    self.main.remove(self.main[i]) 
        #print "Le joueur " +  self.nom + " a fait son chien. La partie commence ! \n"

    def annonce(self): # Embryon d'intelligence qui regarde simplement le nomre d'atouts et de bouts
        compte_bouts=0
        compte_atouts=0
        for c in self.main:
            if c.est_un_bout()==True:
                compte_bouts +=1
            if c.couleur=="atout":
                compte_atouts+=1
        if compte_bouts ==3:
            self.etat_annonce="garde contre"
            #print "Le joueur " +  self.nom + "fait l'annonce : " + self.etat_annonce
        if compte_bouts ==2:
            self.etat_annonce="garde sans"
            #print "Le joueur " +  self.nom + "fait l'annonce : " + self.etat_annonce
        if compte_bouts ==1:
            self.etat_annonce="garde"
            #print "Le joueur " +  self.nom + "fait l'annonce : " + self.etat_annonce
        else:
            if compte_atouts >=5:
                self.etat_annonce="petite"
                #print "Le joueur " +  self.nom + "fait l'annonce : " + self.etat_annonce
            else:
                self.etat_annonce="passe"
                #print "Le joueur " +  self.nom + "fait l'annonce : " + self.etat_annonce    
            
            
            
#a=joueur_max("Bob")       
            
            
#print a   
     
            
            
            
            
            
