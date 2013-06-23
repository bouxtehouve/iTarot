# Le joueur random a l'IA la plus simple possible : il joue une carte au hasard dans l'ensemble des cartes possibles

from cartes import carte
from joueur import joueur
import random

class joueur_random(joueur):
  def __init__(self,nom):
		joueur.__init__(self,nom)
		self.type="joueur_random"
		
	def __str__(self):
		return self.nom

	# IA basique : aleatoire

	def joue_une_carte(self,cartes_pli):
		cj=self.cartes_jouables(cartes_pli)
		#A suppr
		'''if len(cj)==0:
			print "Mon PENIS est sale"
		else:
			print "Mon PENIS est nettoye"
		print self.couleur_demandee(cartes_pli)
		print len(self.main)'''
		#Fin suppr
		a=cj[random.randint(0,len(cj)-1)]
		cartes_pli.append(a)
		self.main.remove(a)
		#print "Le joueur " +  self.nom + " joue : " + str(a) + "\n"
			
	def appel_roi(self): # Ameliorable
		couleurs=["trefle","pique","carreau","coeur"]
		a=random.randint(0,3)
		if carte(couleurs[a],"roi") not in self.main:
			self.roi_appele=couleurs[a]
		else:
			for i in xrange(0,3):
				if carte(couleurs[(a+i)%4],"roi") not in self.main:
					self.roi_appele=couleurs[(a+i)%4]
				else:
					self.roi_appele="trefle"
		#print "Le joueur " +  self.nom + " appelle le roi de " + self.roi_appele
		
	def fait_son_chien(self): # On choisit aleatoirement le chien, sachant qu'on n'a pas le droit de mettre de bouts
		i=0
		while i < 3:
			a=random.randint(0,len(self.main)-1)
			if not(carte.est_un_bout(self.main[a])):
				self.tas.append(self.main[a])
				self.main.remove(self.main[a])
				i+=1
		#print "Le joueur " +  self.nom + " a fait son chien. La partie commence ! \n"
		
	def annonce(self):
		annonces=["passe","petite","garde","garde sans","garde contre"]
		n=random.randint(0,4)
		#print "Le joueur " +  self.nom + "fait l'annonce : " + annonces[n]
		self.etat_annonce=annonces[n]
		
		
