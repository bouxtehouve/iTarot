class carte:
  def __init__(self, couleur, rang): #couleur et rang sont des chaines de caracteres, hauteur un entier
		#couleurs=["excuse","atout","trefle","pique","carreau","coeur"]
		#rangs=["as","2","3","4","5","6","7","8","9","10","valet","cavalier","dame","roi"]
		hauteurs={"as":1, "2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"valet":11,"cavalier":12,"dame":13,"roi":14}
		self.couleur=couleur
		self.rang=rang
		if couleur=="excuse":
			self.rang=""
			self.hauteur=0
		else:
			if couleur=="atout":
				self.hauteur=int(self.rang)
			else:
				self.hauteur=hauteurs[self.rang]
		
	def __str__(self):
		if self.couleur=="atout":
			return str(self.rang)  + " d'atout"
		if self.couleur=="excuse":
			return "excuse"
		return str(self.rang)  + " de " + self.couleur
		
	def valeur(self):
		valeurs={"as":0.5, "2":0.5,"3":0.5,"4":0.5,"5":0.5,"6":0.5,"7":0.5,"8":0.5,"9":0.5,"10":0.5,"valet":1.5,"cavalier":2.5,"dame":3.5,"roi":4.5}
		if self.couleur=="excuse":
			return 4.5
		else:
			if self.couleur=="atout":
				if self.est_un_bout()==True:
					return 4.5
				else:
					return 0.5
			else:
				return valeurs[self.rang]
		
	def estrouge(self):
		return self.couleur =="carreau" or self.couleur=="coeur"
		
	def estnoire(self):
		return self.couleur=="trefle" or self.couleur=="pique"
		
	def compare(self,c): # renvoie la carte la plus forte entre self et une autre carte "c", self est plus forte si les deux coueleurs (hors atout et excuse) sont differentes
		if self.couleur=="excuse":
			return c
		if c.couleur=="excuse":
			return self
		else:
			if self.couleur!=c.couleur:	# couleurs des deux cartes differentes
				if c.couleur!="atout":
					return self
				else:
					return c
			else:		# meme couleur
				if self.hauteur>c.hauteur: # comparaison valeur
					return self
				else:
					return c
					
	def est_un_bout(self):
		if (self.couleur=="excuse") or (self.couleur=="atout" and (self.hauteur==1 or self.hauteur==21)):
			return True
		else:
			return False
	
	def est_une_tete(self):
		r=self.rang
		return (r=="cavalier")or(r=="valet")or(r=="dame")or(r=="roi")
	
	'''def __cmp__(self, c):
		resultat = self.compare(c)
		if resultat == None: # sompare ne renvoie jamais "None" : pb !
			return 0
		if resultat == self:
			return -1
		if resultat == c:
			return 1'''


	def __eq__(self, c):
		return self.couleur == c.couleur and self.hauteur == c.hauteur
	
	def __ne__(self, c): # Quand on definit __eq__ on doit toujours definir __ne__ pour etre sur que les booleens fonctionnent bien
		return self.couleur != c.couleur or  self.hauteur != c.hauteur
	
	def __gt__(self,c):
		if self.couleur=="excuse":
			return False
		if c.couleur=="excuse":
			return True
		if self.couleur!=c.couleur:	# couleurs des deux cartes differentes
			if self.couleur=="atout":
				return True
		if self.couleur==c.couleur:
			return self.hauteur>c.hauteur
	
	def __ge__(self,c):
		if self.couleur=="excuse":
			return False
		if c.couleur=="excuse":
			return True
		if self.couleur!=c.couleur:	# couleurs des deux cartes differentes
			if self.couleur=="atout":
				return True
			return False
		if self.couleur==c.couleur:
			return self.hauteur>=c.hauteur
		
	'''def est_dans_ensemble(self,ens):
		trouve=False
		for c in ens:
			if self==c:
				trouve=True
		return trouve'''
	
	def __hash__(self):
		couleurs={"excuse":0,"atout":1,"trefle":2,"pique":3,"carreau":4,"coeur":5}
		return 100*couleurs[self.couleur]+self.hauteur


'''if __name__== "__main__":
	def test(resultat):
		if not resultat:
			raise "Error"'''
	
''''a = carte("pique", "roi")

	
b = carte("trefle", "dame")
	
print a.__hash__()'''
