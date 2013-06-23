# gestion du paquet en terme de regles du jeu (et pas de donne)

import random,copy
# Cette classe permet de creer un paquet de cartes melangees aleatoirement et de distribuer les cartes aux joueurs.
from cartes import carte

class paquet: # faire ici la comparaison ?? car la creation des cartes se fait ici
  def __init__(self):
		self.liste_cartes=None
		self.creation_cartes()
		self.chien=None
	
	def creation_cartes(self):
		couleurs=["excuse","atout","trefle","pique","carreau","coeur"]
		rangs=["as","2","3","4","5","6","7","8","9","10","valet","cavalier","dame","roi"]
		liste_cartes=[]
		for i in couleurs:
			if i=="atout":
				for j in xrange(1,22):
					liste_cartes.append(carte(i,str(j)))
			else:
				if i=="excuse":
					liste_cartes.append(carte(i,""))
				else:
					for j in rangs:
						liste_cartes.append(carte(i,j))
		self.liste_cartes=liste_cartes
	
	def distribution_paquet(self,joueurs):	#Initialise les mains des joueurs, et le chien. A faire une fois qu'on a les joueurs.
		distrib=copy.copy(self.liste_cartes)
		random.shuffle(distrib)		# fonction python qui effectue une permutation aleatoire des cartes = melanger les cartes
		i_chien=random.randint(0,75)
		self.chien=distrib[i_chien:i_chien+3]	# pour plus de simplicite, on met 3 cartes des le debut de la distribution dans le chien
		distrib=distrib[0:i_chien] + distrib[i_chien+3:78]
	#le jeu moins le chien est distribue
		for i in xrange(0,5):
			joueurs[i].main.extend(distrib[15*i:15*i +15])
			joueurs[i].tri_main()

	
''''p=paquet()
def permutations(ensemble): #l'ensemble est une liste d'objects
            n=len(ensemble)
            if n<=1:
                yield ensemble
            else:
                for p in permutations(ensemble[1:]):
                    for i in xrange(0,n):
                        yield p[:i]+ensemble[0:1]+p[i:n]
lis=list(permutations(p.liste_cartes))
for i in xrange(0,10):
	print lis[i]
#print p.liste_cartes[21]


class noeud:
	def __init__(self):
		self.children = []
		self.parent = None
		
	def addChild(self, child)
		self.children.append(child)
		child.parent = self
		'''
