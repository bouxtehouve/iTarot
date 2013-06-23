# Cette classe contient les infos indispensables qui permettent a un joueur de jouer toujours selon les regles.
# Les differentes IA et le joueur humain utilisent cette classe pour jouer.

class joueur:
  def __init__(self,nom):
		self.nom=str(nom)
		self.main=[]
		self.tas=[]
		self.chien=[] #inutile ?
		self.role=""
		self.etat_annonce=None
		self.attaquant=None
		
	def __str__(self):
		return self.nom

	def ai_je_couleur(self,couleur): # permet de savoir si la main du joueur contient la couleur voulue
		i=0
		while i<len(self.main):
			if self.main[i].couleur ==couleur:
				return True
			else:
				i +=1
		if ((i == len(self.main)) and (self.main[i-1].couleur != couleur)): #2eme partie inutile ?
			return False
			
	def ai_je_carte(self,card):
		col=card.couleur
		ran=card.rang
		Trouve=False
		for i in self.main:
			if (i.couleur==col) and (i.rang==ran):
				Trouve=True
		return Trouve
	
	def ai_je_plushaut(self,couleur,hauteur):
		i=0
		while i<len(self.main):
			if (self.main[i].couleur==couleur and self.main[i].hauteur > hauteur):
				return True
				break
			else:
				i +=1
		if i==len(self.main):
			return False
		else:
			return True
	
	def plushaut_el(self,ens_cartes,couleur): # permet de connaitre la plus haute valeur d'une couleur pour un ensemble de cartes
		maximum=-1
		for carte_i in ens_cartes:
			if (carte_i.couleur==couleur and carte_i.hauteur > maximum):
				maximum = carte_i.hauteur
		return maximum
		
	def couleur_demandee(self,cartes_pli): # cette fonction determine la couleur du pli avec les discussions sur l'excuse en 1ere carte jouee
		if len(cartes_pli)==0 or (len(cartes_pli)==1 and cartes_pli[0].couleur=="excuse"): #Cas pas de couleur demandee
			return "choix"
		else:
			if cartes_pli[0].couleur !="excuse": #Cas couleur demandee
				return cartes_pli[0].couleur
			else:
				return cartes_pli[1].couleur
	
	def est_jouable(self,cette_carte,cartes_pli):
		if cette_carte.couleur == "excuse" or self.couleur_demandee(cartes_pli) == "choix":
			return True # on peut toujours jouer l'excuse OU on est le premier a jouer ou on suit l'excuse
		else:
			col = self.couleur_demandee(cartes_pli)
			if cette_carte.couleur == col: # on joue la couleur demandee
				if col != "atout":
					return True # on joue la couleur demandee qui n'est pas atout
				else:
					if cette_carte.hauteur > self.plushaut_el(cartes_pli,"atout"):
						return True # on joue un atout plus haut que le plus haut atout joue
					else:
						if self.ai_je_plushaut("atout",self.plushaut_el(cartes_pli,"atout")) == True:
							return False # on joue un atout moins haut que... en ayant plus haut que ...
						else:
							return True # on n'a pas d'atout plus haut
			else:
				if col == "atout": # atout demande
					return not self.ai_je_couleur("atout")
				else: # couleur demandee
					if self.ai_je_couleur(col) == True:
						return False # on joue autre chose en ayant la couleur demandee
					else:
						if self.ai_je_couleur("atout") == False:
							return True # on n'a ni atout ni couleur demandee, tout est permis
						else:
							if cette_carte.couleur!="atout":
								return False # on a de l'atout et pas la couleur, on doit jouer atout
							else:
								if cette_carte.hauteur > self.plushaut_el(cartes_pli,"atout"):
									return True # on joue plus haut que le plus haut atout
								else: # meme distinction que plus haut sur le fait que si on a un plus haut atout, on doit le jouer
									if self.ai_je_plushaut("atout",self.plushaut_el(cartes_pli,"atout")):
										return False
									else:
										return True
	
	def cartes_jouables(self,cartes_pli): # renvoie la liste des cartes jouables etant donne l'etat du pli et la main du joueur "nb"
		liste_cartes_jouables=[]
		for telle_carte in self.main:
			if self.est_jouable(telle_carte,cartes_pli)==True :
				liste_cartes_jouables.append(telle_carte)
		return liste_cartes_jouables
	
	def tri_main(self):
		liste_trefle=[]
		liste_carreau=[]
		liste_pique=[]
		liste_coeur=[]
		liste_atout=[]
		liste_excuse=[]
		for c in self.main:
			if c.couleur=="trefle":
				liste_trefle.append(c)
			if c.couleur=="carreau":
				liste_carreau.append(c)
			if c.couleur=="pique":
				liste_pique.append(c)
			if c.couleur=="coeur":
				liste_coeur.append(c)
			if c.couleur=="atout":
				liste_atout.append(c)
			if c.couleur=="excuse":
				liste_excuse=[c]
		liste_trefle.sort()
		liste_carreau.sort()
		liste_pique.sort()
		liste_coeur.sort()
		liste_atout.sort()
		self.main=liste_trefle+liste_carreau+liste_pique+liste_coeur+liste_atout+liste_excuse
		return self.main
