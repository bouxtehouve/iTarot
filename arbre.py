class arbre:
    def __init__(self,truc):
        self.racine=truc
        self.enfants=[]
        self.parent=None
    
    def ajoute_enfants(self,enfants): # enfants est une liste d'objets
        for t in enfants:
            fils=arbre(t)
            self.enfants.append(fils)
            fils.parent=self
    
    '''Les fonctions suivantes ne servent pas durant le jeu mais ont servi lors du debugage, on ne les a pas supprimees pour les remercier'''
    def est_racine(self):
        return self.parent == None
        
    def est_feuille(self):
        return self.enfants == []
    
    def profondeur(self):
        if self.parent==None:
            return 0
        else:
            return 1+self.profondeur(self.parent)
        
    def parcours(self,fonction):
        fonction(self.racine)
        for t in self.enfants:
            self.parcours(t)
            
if __name__=="__main__":
    a=(arbre(1))
    a.ajoute_enfants([2])
    b=a.enfants[0]
