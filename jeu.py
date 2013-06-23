
# deroulement du jeu
from paquet import paquet
from joueur_random import joueur_random
from joueur_humain import joueur_humain
from joueur_max import joueur_max
from cartes import carte
import random
from joueur_intelligent import joueur_intelligent

class jeu:
  
	def __init__(self):
		self.etat="Attente" #inspire d'iTarot, on devrait s'en inspirer et fractionner le jeu ? il a l'air de faire ca surtout pour le testing
		self.pli=[]
		self.annonce=None
		self.maitre=None
		self.appelant=None #Un entier
		self.appele=None    #Ici aussi
		self.roi_appele=None
		#Les attributs suivants servent aux joueurs qui y ont ou pas acces selon leur degre d'intelligence. Ces attributs sont publics, les joueurs en
		#particulier peuvent avoir plus d'infos
		self.tour=None #MODIFIE--------------------------------------------------------------
		self.atouts_restants=None
		self.cartes_restantes=None
		self.tetes_restantes=None
		self.excuse_restante=True
		self.remplacant_excuse=None
		self.coupes=[]
		self.tours_a=None
		self.appele_connu=False
		self.appelant_gagnant=False
		self.joueurs=[None,None,None,None,None]
		
	#def __init__(self, j):
	#	self.pli=copy.copy(j.pli)
	
	def commencer_partie(self,joueurs): # joueurs est une liste de joueurs, les noms des joueurs sont donnes dans l'ordre de leurs numeros	
		#On reinitialise tout:				
		dog=self.p0_reinitialisation(joueurs)
		
		#Debut de la partie annonces
		self.p1_annonces(joueurs)
		
		# Debut de la partie appel de roi et traitement du chien
		self.p2_appel_et_chien(joueurs,dog)
		
		# Jeu a proprement parler
		self.p3_jeu(joueurs)
		
		# Fin du jeu, decompte des points
		self.p4_decompte(joueurs)

	def p0_reinitialisation(self,joueurs):
		for i in xrange(0,5):
			joueurs[i].main=[]
			joueurs[i].tas=[]
			joueurs[i].chien=[]
			joueurs[i].role=""
			joueurs[i].etat_annonce=None
			joueurs[i].attaquant=False
			self.joueurs[i]=joueurs[i]
		pack=paquet()
		pack.distribution_paquet(joueurs)
		self.pli=[]
		self.annonce=None
		self.appelant=None
		self.appele=None
		self.roi_appele=None
		#MODIFIE A PARTIR D'ICI--------------------------------------------------------------
		self.tour=1
		self.cartes_restantes=pack.liste_cartes
		self.atouts_restants=pack.liste_cartes[1:22]
		self.excuse_restante=True
		self.remplacant_excuse=carte("debut","as")
		self.coupes=[]
		for i in xrange(0,5):
			self.coupes.append({"atout":False, "trefle":False,"pique":False,"carreau":False,"coeur":False})
		self.appele_connu=False
		self.tours_a= {"trefle":0,"pique":0,"carreau":0,"coeur":0,"atout":0}
		self.appelant_gagnant=False
		#FIN MODIF ----------------------------------------------------
		'''Fin de la reinitialisation'''
		return pack.chien

	def p1_annonces(self,joueurs):
		if self.maitre==None:
			self.offres(joueurs,random.randint(0,4))
		else:
			self.offres(joueurs,self.maitre)
		self.appelant=self.maitre
		self.annonce=(joueurs[self.appelant]).etat_annonce
		joueurs[self.appelant].attaquant=True

	def p2_appel_et_chien(self,joueurs,dog):
		joueurs[self.appelant].appel_roi()
		self.roi_appele=joueurs[self.appelant].roi_appele
		roi=self.roi_appele
		if (carte(roi,"roi") in dog) or (carte(roi,"roi") in joueurs[self.appelant].main):
			self.appele=self.appelant
		else:
			for i in xrange(1,5):
				if carte(roi,"roi") in joueurs[(self.appelant + i)%5].main:
					self.appele=(self.appelant + i)%5
					joueurs[self.appele].attaquant=True
		if self.annonce == "garde contre":
			i=0
			while i < 5 and (i != self.appelant) and ( i!=self.appele): # A TESTER : verifier que le booleen 0 != None marche comme on veut
				i+=1
			joueurs[i].tas.extend(dog) #on a trouve un joueur de l'equipe defenseurs
		else:
			if self.annonce=="garde sans":
				joueurs[self.appelant].tas.extend(dog)
			else:
				joueurs[self.appelant].main.extend(dog)
				joueurs[self.appelant].tri_main()
				joueurs[self.appelant].fait_son_chien()
			if (self.annonce=="garde" or self.annonce=="petite") and (carte(self.roi_appele,"roi") in dog):
				self.appele_connu=True
				
	def p3_jeu(self,joueurs):
		for i in xrange(0,15):
			#print " \n                         Le tour " + str(i+1) + " commence. \n"
			self.joue_un_tour(joueurs)
			#print "   Le pli est fini. Le voici :"
			for c in self.pli:
				#print c
				pass
			self.tour +=1
			
	def p4_decompte(self,joueurs):
		compte=0
		bouts=0
		for k in joueurs[self.appelant].tas:
			if k.est_un_bout()==True:
				bouts+=1
			compte += k.valeur()
		if self.appelant != self.appele:
			for k in joueurs[self.appele].tas:
				if k.est_un_bout()==True:
					bouts+=1
				compte+=k.valeur()
		if bouts==0:
			if compte >= 56:
				self.appelant_gagnant=True
				#print "\n       Le joueur %s remporte cette partie avec %s points de realises" %(joueurs[self.appelant].nom, str(compte))
			#else:
				#print "\n       Le joueur %s perd cette partie avec %s points de realises ( 56 requis )" %(joueurs[self.appelant].nom, str(compte))
		if bouts==1:
			if compte >= 51:
				self.appelant_gagnant=True
				#print "\n       Le joueur %s remporte cette partie avec %s points de realises" %(joueurs[self.appelant].nom, str(compte))
			#else:
				#print "\n       Le joueur %s perd cette partie avec %s points de realises ( 51 requis )" %(joueurs[self.appelant].nom, str(compte))
		if bouts==2:
			if compte >= 41:
				self.appelant_gagnant=True
				#print "\n       Le joueur %s remporte cette partie avec %s points de realises" %(joueurs[self.appelant].nom, str(compte))
			#else:
				#print "\n       Le joueur %s perd cette partie avec %s points de realises ( 41 requis )" %(joueurs[self.appelant].nom, str(compte))
		if bouts==3:
			if compte >= 36:
				self.appelant_gagnant=True
				#print "\n       Le joueur %s remporte cette partie avec %s points de realises" %(joueurs[self.appelant].nom, str(compte))
			#else:
				#print "\n       Le joueur %s perd cette partie avec %s points de realises ( 36 requis )" %(joueurs[self.appelant].nom, str(compte))
		'''Fin de partie ?'''

	def offres(self,joueurs,deb): #Le joueur deb commence a parler
		hauteur={"passe":0,"petite":1,"garde":2,"garde sans":3,"garde contre":4}
		maximum=-1
		joueur_max=-1
		for i in xrange(0,5):
			joueurs[(i+deb)%5].annonce()
			if hauteur[joueurs[(i+deb)%5].etat_annonce] > maximum:
				joueur_max=(i+deb)%5
				maximum=hauteur[joueurs[(i+deb)%5].etat_annonce]
		if maximum <=0:
			#print "Personne ne prend, bande de tarlouzes ! Je redistribue..."
			self.commencer_partie(joueurs)
		else:
			self.maitre=joueur_max
			#print "Le joueur " + joueurs[joueur_max].nom + " fait une " + joueurs[joueur_max].etat_annonce
	
	def couleur_demandee(self,cartes_pli): # cette fonction determine la couleur du pli avec les discussions sur l'excuse en 1ere carte jouee
		if len(cartes_pli)==0 or (len(cartes_pli)==1 and cartes_pli[0].couleur=="excuse"): #Cas pas de couleur demandee
			return "choix"
		else:
			if cartes_pli[0].couleur !="excuse": #Cas couleur demandee
				return cartes_pli[0].couleur
			else:
				return cartes_pli[1].couleur
							
	def maitre_pli (self): # renvoie le numero du joueur maitre ( on suppose le pli fini )
		def plushaut_el(ens_cartes,couleur): # permet de connaitre la plus haute valeur d'une couleur pour un ensemble de cartes
			maximum=-1
			for carte_i in ens_cartes:
				if (carte_i.couleur==couleur and carte_i.hauteur > maximum):
					maximum = carte_i.hauteur
			return maximum
		col=self.couleur_demandee(self.pli)
		if  plushaut_el(self.pli, "atout") == -1: # pas d'atout joue, on regarde la plus grosse couleur jouee
			maximum=-1
			maitre = -1
			for i in xrange(0,5):
				if (self.pli[i].couleur==col and self.pli[i].hauteur > maximum):
					maximum = self.pli[i].hauteur
					maitre = i
		else: # atout joue, on regarde le plus haut atout joue
			maximum=-1
			maitre = -1
			for i in xrange(0,5):
				if (self.pli[i].couleur=="atout" and self.pli[i].hauteur > maximum):
					maximum = self.pli[i].hauteur
					maitre = i
		return maitre
				
	def joue_un_tour(self,joueurs):
		self.pli=[]
		for i in xrange(0,5):
			j=(self.maitre+i)%5
			#if joueurs[j].type !="humain":
				#print "\n   Au joueur %s de choisir une carte. \n" %(joueurs[j].nom)
			if joueurs[j].type !="joueur_intelligent":
				joueurs[j].joue_une_carte(self.pli)
			else:
				if self.tour >=18: # <============================================ ICI POUR MODULER LE DECLENCHEMENT DE L'IA PREVISION_TOTALE, SI >=16 ON NE LA DECLENCHE PAS
					joueurs[j].joue_prevision_totale(self)
				else:
					joueurs[j].joue_coup_par_coup(self)
			self.observe(j)
			if self.pli[len(self.pli)-1].couleur=="excuse": # Traitement particulier de l'excuse, partie 1
				self.joueurs[j].tas.append(self.pli[len(self.pli)-1])
				mini=42
				for c in self.joueurs[j].tas:
					if c.hauteur < mini and not c.est_un_bout():
						mini=c.hauteur
						self.remplacant_excuse=c
			'''for k in xrange(1,5):
			if "k est un bot"
			joueurs[(self.maitre+i+k)%5].observe((self.maitre+i)%5)'''
		self.tours_a[self.couleur_demandee(self.pli)]+=1
		self.maitre=(self.maitre_pli()+self.maitre)%5
		if carte("excuse","") in self.pli: # Traitement particulier de l'excuse, partie 2
			self.pli.remove(carte("excuse",""))
			if self.remplacant_excuse.couleur !="debut":
				self.pli.append(self.remplacant_excuse)
		joueurs[self.maitre].tas.extend(self.pli)
		'''Manque le sort particulier reserve a l'excuse'''
		
	def observe(self,n): # Le joueur numero n vient de jouer. La fonction observe rend compte de ce que peut enregistrr un observateur exterieur qui ne voit
		#le jeu de personne, qui ne voit que le plateau de jeu
		
		#Deja on enregistre le fait que la carte c ait ete jouee
		c=self.pli[len(self.pli)-1]
		col=c.couleur
		if col=="excuse":
			self.excuse_restante=False
		if col=="atout":
			self.atouts_restants.remove(c)
		'''if c in self.tetes_restantes:
			self.tetes_restantes.remove(c)'''
		self.cartes_restantes.remove(c)
		#Puis on enregistre le fait que le joueur ait eventuellement coupe/pisse
		col=self.couleur_demandee(self.pli)
		if col != "choix" and c.couleur != col and c.couleur!="excuse":
			self.coupes[n][col]=True #Ameliorable, on le refait a chaque tour ou le mec coupe
			if col!="atout" and c.couleur!="atout":
				self.coupes[n]["atout"]=True # Le joueur n'a plus d'atouts
		#Puis on regarde si le roi appele a ete joue, ou si on sait avec certitude qui est le roi appele ( dans l'ordre )
		if self.appele_connu==False:
			if carte(self.roi_appele,"roi") in self.pli:
				self.appele_connu=True
			else:
				k=1
				while k<5 and self.coupes[((self.appele)+k)%5][self.roi_appele]==True:
					k+=1
				if k==5: #L'appelant s'est appele lui-meme, ou du moins le roi est dans le chien ou dans son jeu
					self.appele_connu=True
				
				
					
		
if __name__=="__main__":
	j=jeu()
	joueurs=[joueur_intelligent("Bob1"),joueur_random("Bob2"),joueur_random("Bob3"),joueur_random("Bob4"),joueur_random("Bob5")]
	compte_attaque=[0,0,0,0,0]
	compte_defense=[0,0,0,0,0]
	compt=0
	for i in xrange(0,1):  
		#print "La partie" + str(i) + "commence"
		dog=j.p0_reinitialisation(joueurs)
		
		#Debut de la partie annonces
		joueurs[0].etat_annonce="garde"
		j.appelant=0
		j.maitre=0
		j.annonce="garde"
		joueurs[0].attaquant=True
		
		# Debut de la partie appel de roi et traitement du chien
		j.p2_appel_et_chien(joueurs,dog)
		
		# Jeu a proprement parler
		j.p3_jeu(joueurs)
		
		# Fin du jeu, decompte des points
		j.p4_decompte(joueurs)
		#print "La partie" + str(i) + "s'acheve"
		'''if j.appelant_gagnant==True:
			compte_attaque[j.appelant] += 2
			if j.appelant != j.appele:
				compte_attaque[j.appele] += 1
			else:
			compte_defense[j.appelant] += -2
			if j.appelant != j.appele:
				compte_defense[j.appele] += -1'''
		if j.appelant_gagnant:
			#compte_attaque[0]+=1
			compt+=1
			#if j.appelant !=j.appele:
				#compte_attaque[j.appele]+=1
				#compt+=1
				
		#=======================================================================
		# joueurs=[joueur_max("Bob1"),joueur_random("Bob2"),joueur_random("Bob3"),joueur_random("Bob4"),joueur_random("Bob5")]
		# for i in xrange(0,10):  
		# 	#print "La partie" + str(i) + "commence"
		# 	dog=j.p0_reinitialisation(joueurs)
		# 	
		# 	#Debut de la partie annonces
		# 	joueurs[0].etat_annonce="garde"
		# 	j.appelant=0
		# 	j.maitre=0
		# 	j.annonce="garde"
		# 	joueurs[0].attaquant=True
		# 	
		# 	# Debut de la partie appel de roi et traitement du chien
		# 	j.p2_appel_et_chien(joueurs,dog)
		# 	
		# 	# Jeu a proprement parler
		# 	j.p3_jeu(joueurs)
		# 	
		# 	# Fin du jeu, decompte des points
		# 	j.p4_decompte(joueurs)
		# 	#print "La partie" + str(i) + "s'acheve"
		# 	'''if j.appelant_gagnant==True:
		# 		compte_attaque[j.appelant] += 2
		# 		if j.appelant != j.appele:
		# 			compte_attaque[j.appele] += 1
		# 		else:
		# 		compte_defense[j.appelant] += -2
		# 		if j.appelant != j.appele:
		# 			compte_defense[j.appele] += -1'''
		# 	if j.appelant_gagnant:
		# 		#compte_attaque[0]+=1
		# 		compt[1]+=1
		#=======================================================================
		'''else:
			compte_attaque[0]+=-1
			if j.appelant !=j.appele:
				compte_attaque[j.appele]+=-1'''
			
		#print compte_attaque
		#print compte_defense
	
	#===========================================================================
	# joueurs=[joueur_intelligent("Bob1","bourrin"),joueur_random("Bob2"),joueur_random("Bob3"),joueur_random("Bob4"),joueur_random("Bob5")]
	# 	
	# for i in xrange(0,100000):
	# 	#print "La partie" + str(i) + "commence"
	# 	dog=j.p0_reinitialisation(joueurs)
	# 	
	# 	#Debut de la partie annonces
	# 	joueurs[0].etat_annonce="garde"
	# 	j.appelant=0
	# 	j.maitre=0
	# 	j.annonce="garde"
	# 	joueurs[0].attaquant=True
	# 	
	# 	# Debut de la partie appel de roi et traitement du chien
	# 	j.p2_appel_et_chien(joueurs,dog)
	# 	
	# 	# Jeu a proprement parler
	# 	j.p3_jeu(joueurs)
	# 	
	# 	# Fin du jeu, decompte des points
	# 	j.p4_decompte(joueurs)
	# 	#print "La partie" + str(i) + "s'acheve"
	# 	'''if j.appelant_gagnant==True:
	# 		compte_attaque[j.appelant] += 2
	# 		if j.appelant != j.appele:
	# 			compte_attaque[j.appele] += 1
	# 		else:
	# 		compte_defense[j.appelant] += -2
	# 		if j.appelant != j.appele:
	# 			compte_defense[j.appele] += -1'''
	# 	if j.appelant_gagnant:
	# 		#compte_attaque[0]+=1
	# 		compt[1]+=1
	# 		#if j.appelant !=j.appele:
	# 			#compte_attaque[j.appele]+=1
	# 			#compt+=1
	# 	'''else:
	# 		compte_attaque[0]+=-1
	# 		if j.appelant !=j.appele:
	# 			compte_attaque[j.appele]+=-1'''
	# 		
	# 	#print compte_attaque
	# 	#print compte_defense
	#===========================================================================
		
	print compt
		
		
		
		# Le joueur_max ne gagne pas plus souvent que les autres. Plusieurs explications possibles :
		# - Le joueur_max se fait court-circuiter par l'appele
		# - Il ne suffit pas de jouer sa carte max pour gagner. D'ou besoin d'une meilleure IA
		# _ Par contre, il defend mieux que les joueurs random/ joueurs random

	
	
	
	
	
	
	
	
