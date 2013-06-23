# Le joueur humain joue par inputs dans la console pour l'instant, a terme on remplacera les inputs par des clics ( partie graphique )

from joueur import joueur

class joueur_humain(joueur):
    def __init__(self,nom):
        joueur.__init__(self,nom)
        self.type="humain"
    
    def joue_une_carte(self,cartes_pli): 
        cj=self.cartes_jouables(cartes_pli)
        print "Les cartes jouables sont \n"
        for c in cj:
            print c
            print "\n"
        print "Veuillez choisir une des cartes ci-dessus \n"
        a=input()
        while a not in cj: #Bug mais sera remplace a terme dans la partie graphique ?
            print "Cette carte n'est pas jouable. Veuillez rectifier. \n"
            a=input()
        cartes_pli.append(a)
        self.main.remove(a)
        print "Le joueur " +  self.nom + " joue : " + str(a) + "\n"
        
    def annonce(self):
        annonces={"passe":0,"petite":1,"garde":2,"garde sans":3,"garde contre":4}
        print "%s , vos cartes sont : \n" %(self.nom)
        for l in self.main:
            print l
            print "\n"
        print "Faites votre annonce, %s !" %(self.nom)
        annonce=raw_input()
        while annonce not in annonces:
            print "Mauvaise annonce.Faites votre annonce, %s !" %(self.nom)
            annonce=raw_input()
        print "Le joueur " +  self.nom + "fait l'annonce : " + annonce
        self.etat_annonce=annonce
        
    def appel_roi(self,game): 
        couleurs=["trefle","pique","carreau","coeur"]
        print "%s , vos cartes sont : \n" %(self.nom)
        for l in self.main:
            print l
            print "\n"
        print "Quel roi appelez-vous, %s ?" %(self.nom)
        annonce=raw_input()
        while annonce not in couleurs:
            print "Mauvaise annonce. Quel roi appelez-vous, %s ?" %(self.nom)
            annonce=raw_input()
        print "Le joueur " +  self.nom + " appelle le roi de " + annonce
        game.roi_appele=annonce
        
    def fait_son_chien(self):
        for i in xrange(0,3):
            print "Choisissez une carte a mettre au chien : \n"
            for c in self.main:
                print c
                print "\n"
            a=input()
            while a not in self.main:
                print "Cette carte n'est pas dans votre main. Veuillez rectifier. \n"
                a=input()
            self.tas.append(a)
            self.main.remove(a)
