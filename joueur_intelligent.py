from joueur import joueur
from cartes import carte
import copy
from arbre import arbre
import random

class joueur_intelligent(joueur):
    def __init__(self,nom):
        joueur.__init__(self,nom)
        self.type="joueur_intelligent"
        self.atouts_max=[21,21,21,21,21]
    
    '''En debut de partie l'IA cherche juste a gagner chaque tour, en fin de partie elle maximise ses chances de gagner. 
    En debut de partie elle ne va donc jamais anticiper sur le tour suivant'''
    
    
    def observe(self,n,game): 
        '''INUTILE POUR NOTRE PROGRAMME''' # Cette fonction vient completer la fonction homonyme de la classe jeu, on l'appelle ici car les infos qu'elle renvoie ne sont pas publiques
        #On regarde si un joueur vient de jouer un atout inferieur au plus haut atout joue, auquel cas on reajuste le majorant de ses atouts
        if n != self.numero(game):
            c=game.pli[len(game.pli)-1]
            col=c.couleur
            majorant=self.plushaut_el(game.pli,"atout")
            if col == "atout" and c.hauteur < majorant:
                self.atouts_max[n]=majorant
                i=1
                while carte("atout",str(majorant-i)) in self.main:
                    self.atouts_max[n]=carte("atout",str(majorant-i))
                    i+=1
     
    def numero(self,game):
        i=0
        while i<5:
            if game.joueurs[i].nom==self.nom:
                return i
            i+=1
    
    #===========================================================================
    # def maitre_a_coup_sur(self,game): #Regarde s'il y a moyen de gagner le pli a coup sur, au moment ou on doit jouer ( peu d'occurences en debut de partie lorsque non dernier a jouer )
    #     col=game.couleur_demandee(game.pli)
    #     if col =="choix":
    #         pass
    #     else:
    #         if game.appele_connu == True:
    #             pass
    #         else:
    #             pass
    #===========================================================================
                    
    def permutations(self,ensemble): #n est un multiple de 4  
        '''MARCHE MAIS TROP LONG LORSQUE N>16''' 
        n=len(ensemble)
        if n<=4:
            if n<=1:
                yield ensemble
            else:
                for p in self.permutations(ensemble[1:]):
                    for i in xrange(0,n):
                        yield p[:i]+ensemble[0:1]+p[i:n]
        else:
            for p1 in self.permutations(ensemble[0:4]):
                for p2 in self.permutations(ensemble[4:]):
                    yield p1[0:1]+p2[:(n/4)]+p1[1:2]+p2[(n/4):2*(n/4)]+p1[2:3]+p2[2*(n/4):3*(n/4)]+p1[3:4]+p2[3*(n/4):]
                    
    def permutationsn(self,ensemble): #l'ensemble est une liste d'objects
        n=len(ensemble)
        if n<=1:
            yield ensemble
        else:
            for p in self.permutationsn(ensemble[1:]):
                for i in xrange(0,n):
                    yield p[:i]+ensemble[0:1]+p[i:n]
                     
    def construire_permutations(self,g): #Retourne toutes les distributions possibles de cartes a un moment de la partie. On le fait au moment de jouer
        '''MARCHE MAIS BIEN TROP LONG EN DEBUT DE PARTIE'''      
        def ai_je_couleur(cartes,couleur): # permet de savoir si la main du joueur contient la couleur voulue
            i=0
            while i<len(cartes):
                if cartes[i].couleur ==couleur:
                    return True
                else:
                    i +=1
                    if ((i == len(cartes)) and (cartes[i-1].couleur != couleur)): #2eme partie inutile ?
                        return False
                        
        game=copy.deepcopy(g)
        distrib_possibles=[]
        distrib=[[],[],[],[],[]]
        if g.appelant==self.numero(g) and ( self.etat_annonce=="prise" or self.etat_annonce=="garde"): #Si on sait ce qu'il y a dans le chien
            for c in self.tas[0:3]: #On retire le chien des cartes restantes
                game.cartes_restantes.remove(c)
            for c in self.main: # On enleve ses propres cartes pour les rajouter dans touts les distributions
                game.cartes_restantes.remove(c)
                distrib[self.numero(game)].append(c)
            permut=list(self.permutations(game.cartes_restantes))
            q=len(permut[0])/4
            for i in xrange(0,len(permut)):
                for j in xrange(0,4):
                    distrib[(self.numero(game)+j)%5]=permut[i][j*q:(j+1)*q]
                for j in xrange(0,5-self.numero(game)):
                    distrib[(self.numero(game)+j)%5].append(permut[i][4*q+j])
                #Partie de verification sur les coupes
                bon_a_ajouter=True
                couleurs=["atout","trefle","pique","carreau","coeur"]
                for i in xrange(0,5):
                    if i != self.numero(game):
                        for col in couleurs:
                            if game.coupes[i][col]==True and ai_je_couleur(distrib[i],col):
                                bon_a_ajouter=False
                                break
                if bon_a_ajouter==True:
                    distrib_possibles.append(distrib)
        else: # Si on ne sait pas ce qu'il y a dans le chien
            for c in self.main: # On enleve ses propres cartes pour les rajouter dans touts les distributions futures
                game.cartes_restantes.remove(c)
                distrib[self.numero(game)].append(c)
            permut=list(self.permutationsn(game.cartes_restantes))
            q=len(permut[0])/4
            for i in xrange(0,len(permut)):
                for j in xrange(0,4):
                    distrib[(self.numero(game)+j)%5]=permut[i][j*q:(j+1)*q]
                for j in xrange(0,5-self.numero(game)):
                    distrib[(self.numero(game)+j)%5].append(permut[i][4*q+j])
                distrib.append(permut[i][len(permut[i])-3:len(permut[i])]) # Pour l'instant on rajoute le chien a la fin de la distrib
                #Partie de verification sur les coupes
                bon_a_ajouter=True
                couleurs=["atout","trefle","pique","carreau","coeur"]
                for i in xrange(0,5):
                    if i != self.numero(game):
                        for col in couleurs:
                            if game.coupes[i][col]==True and ai_je_couleur(distrib[i],col):
                                bon_a_ajouter=False
                                break
                if bon_a_ajouter==True:
                    distrib_possibles.append(distrib)
        return distrib_possibles

    def coup_par_coup(self,g): # On cherche a maximiser la probabilite de gagner le tour seulement, et non la partie
        def maitre_pli (pli): # renvoie le numero du joueur maitre ( on suppose le pli fini )
            def plushaut_el(ens_cartes,couleur): # permet de connaitre la plus haute valeur d'une couleur pour un ensemble de cartes
                maximum=-1
                for carte_i in ens_cartes:
                    if (carte_i.couleur==couleur and carte_i.hauteur > maximum):
                        maximum = carte_i.hauteur
                return maximum
            def couleur_demandee(cartes_pli): # cette fonction determine la couleur du pli avec les discussions sur l'excuse en 1ere carte jouee
                if len(cartes_pli)==0 or (len(cartes_pli)==1 and cartes_pli[0].couleur=="excuse"): #Cas pas de couleur demandee
                    return "choix"
                else:
                    if cartes_pli[0].couleur !="excuse": #Cas couleur demandee
                        return cartes_pli[0].couleur
                    else:
                        return cartes_pli[1].couleur
            col=couleur_demandee(pli)
            if  plushaut_el(pli, "atout") == -1: # pas d'atout joue, on regarde la plus grosse couleur jouee
                maximum=-1
                maitre = -1
                for i in xrange(0,5):
                    if (pli[i].couleur==col and pli[i].hauteur > maximum):
                        maximum = pli[i].hauteur
                        maitre = i
            else: # atout joue, on regarde le plus haut atout joue
                maximum=-1
                maitre = -1
                for i in xrange(0,5):
                    if (pli[i].couleur=="atout" and pli[i].hauteur > maximum):
                        maximum = pli[i].hauteur
                        maitre = i
            return maitre
        compte={}
        for c in self.cartes_jouables(g.pli):
            compte[c]=0
        #distrib_possibles=self.construire_permutations(g), ce qui serait marque en theorie si la fonction n'etait pas trop longue a executer
        for i in xrange(0,1): # d in distrib_possibles, ce qui serait marque en theorie si la fonction n'etait pas trop longue a executer
            jou=copy.deepcopy(g.joueurs)
            game=copy.deepcopy(g)
            game.joueurs=jou
            for i in xrange(0,5):
                game.joueurs[i].main=copy.deepcopy(g.joueurs[i].main)
            '''for i in xrange(0,5):
                game.joueurs[i].main=d[i]''' # ce qui serait marque en theorie si la fonction n'etait pas trop longue a executer
            def parcours_cpc(numero,tree,master,pli):
                pli.append(tree.racine) # On ajoute la carte qui vient d'etre jouee au pli
                temp=game.appele_connu
                if tree.racine==carte(game.roi_appele,"roi"):
                    game.appele_connu=True
                game.joueurs[numero].main.remove(tree.racine) # Et on la retire de la main du joueur qui vient de jouer
                if len(pli)<5: # Il reste des joueurs a jouer pour le tour
                    tree.ajoute_enfants(game.joueurs[(numero+1) % 5].cartes_jouables(pli))
                    for t in tree.enfants:
                        parcours_cpc((numero+1)%5,t,master,copy.deepcopy(pli))
                else: # Le tour est fini, on regarde si on a gagne
                    nouveau_maitre=(maitre_pli(pli) + master)%5
                    if nouveau_maitre ==self.numero(game) or ( game.appele_connu and game.joueurs[nouveau_maitre].attaquant==self.attaquant):
                        arb=copy.deepcopy(tree)
                        card=tree.racine
                        while arb.parent.racine != carte("debut","as"):
                            card=arb.parent.racine
                            arb=arb.parent
                        compte[card]+=1 # Si on a remporte le pli, on inscrit +1 au compte des plis remportes
                game.joueurs[numero].main.append(tree.racine) # On n'oublie pas de remettre la carte jouee dans le jeu du joueur a la fin du parcours des arbres en dessous
                game.appele_connu=temp
            arb=arbre(carte("debut","as"))
            arb.ajoute_enfants(self.cartes_jouables(g.pli))
            for t in arb.enfants:
                parcours_cpc(self.numero(game),t,game.maitre,copy.deepcopy(game.pli))
        return compte
            
    
    def joue_coup_par_coup(self,game): # Joue la carte de plus grande hauteur possible si on a une chance de gagner, la carte de plus petite hauteur sinon
        cj=self.cartes_jouables(game.pli)
        maxi=-1
        a=carte("debut","as")
        compte=self.coup_par_coup(game)
        for c in cj:
            if compte[c] > maxi: 
                maxi=compte[c]
        if maxi==0: # Quoi qu'on fasse, on perd le pli
            min=42
            for c in cj:
                if c.hauteur < min and compte[c]==0 and c != carte("atout","1"):
                    min=c.hauteur
                    a=c # Dans ce cas on lache le moins possible ( on "pisse" en jargon de joueur de tarot )
            if a.couleur=="debut":
                a=carte("atout","1")
        else: # Sinon, on fonce avec sa plus grosse carte de couleur, ou le plus petit atout
            max=-1
            min=42
            for c in cj:
                if c.hauteur > max and compte[c]==maxi and c.couleur!="atout":
                    max=c.hauteur
                    a=c
                if c.hauteur < min and compte[c]==maxi and c.couleur=="atout":
                    min=c.hauteur
                    a=c
        game.pli.append(a)
        self.main.remove(a)
        #print "Le joueur " +  self.nom + " joue : " + str(a) + "\n"
        
    def prevision_totale(self,g): # On cherche a maximiser la probabilite de gagner la partie sachant la carte jouee. A refaire a chaque tour
        def maitre_pli (pli): # renvoie le numero du joueur maitre ( on suppose le pli fini )
            def plushaut_el(ens_cartes,couleur): # permet de connaitre la plus haute valeur d'une couleur pour un ensemble de cartes
                maximum=-1
                for carte_i in ens_cartes:
                    if (carte_i.couleur==couleur and carte_i.hauteur > maximum):
                        maximum = carte_i.hauteur
                return maximum
            def couleur_demandee(cartes_pli): # cette fonction determine la couleur du pli avec les discussions sur l'excuse en 1ere carte jouee
                if len(cartes_pli)==0 or (len(cartes_pli)==1 and cartes_pli[0].couleur=="excuse"): #Cas pas de couleur demandee
                    return "choix"
                else:
                    if cartes_pli[0].couleur !="excuse": #Cas couleur demandee
                        return cartes_pli[0].couleur
                    else:
                        return cartes_pli[1].couleur
            col=couleur_demandee(pli)
            if  plushaut_el(pli, "atout") == -1: # pas d'atout joue, on regarde la plus grosse couleur jouee
                maximum=-1
                maitre = -1
                for i in xrange(0,5):
                    if (pli[i].couleur==col and pli[i].hauteur > maximum):
                        maximum = pli[i].hauteur
                        maitre = i
            else: # atout joue, on regarde le plus haut atout joue
                maximum=-1
                maitre = -1
                for i in xrange(0,5):
                    if (pli[i].couleur=="atout" and pli[i].hauteur > maximum):
                        maximum = pli[i].hauteur
                        maitre = i
            return maitre
        compte={}
        for c in self.cartes_jouables(g.pli):
            compte[c]=0
        #distrib_possibles=self.construire_permutations(g), ce qui serait marque en theorie si la fonction n'etait pas trop longue a executer
        for i in xrange(0,1): # d in distrib_possibles, ce qui serait marque en theorie si la fonction n'etait pas trop longue a executer
            jou=copy.deepcopy(g.joueurs)
            game=copy.deepcopy(g)
            game.joueurs=jou # On va redemarrer le jeu pour chaque distribution a partir de ce moment precis
            '''for i in xrange(0,5):
                game.joueurs[i].main=d[i] # On rajoute les mains correspondant a la distribution''' # ce qui serait marque en theorie si la fonction n'etait pas trop longue a executer
            def parcours_pt(numero,tree,master,pli):
                if game.tour <= 15: # Dernier tour pas fini
                    pli.append(tree.racine) # On ajoute la carte qui vient d'etre jouee au pli
                    temp=game.remplacant_excuse
                    if tree.racine.couleur=="excuse": # Traitement particulier de l'excuse, partie 1
                        game.joueurs[numero].tas.append(tree.racine)
                        mini=42
                        for c in game.joueurs[numero].tas:
                            if c.hauteur < mini and not c.est_un_bout():
                                mini=c.hauteur
                                game.remplacant_excuse=c
                    game.joueurs[numero].main.remove(tree.racine) # Et on la retire de la main du joueur qui vient de jouer
                    if len(pli)<5: # Il reste des joueurs a jouer pour le tour
                        tree.ajoute_enfants(game.joueurs[(numero+1) % 5].cartes_jouables(pli))
                        for t in tree.enfants:
                            parcours_pt((numero+1)%5,t,master,copy.deepcopy(pli))
                    else: # Le tour est fini, on regarde le gagnant et on augmente son tas comme dans le jeu ( si il est attaquant, car on ne compte que les points des attaquants a la fin du jeu )
                        nouveau_maitre=(maitre_pli(pli) + master)%5
                        if game.joueurs[nouveau_maitre].attaquant:
                            l=copy.deepcopy(pli)
                            if carte("excuse","") in l:
                                l.remove(carte("excuse",""))
                                if game.remplacant_excuse.couleur !="debut":
                                    l.append(game.remplacant_excuse) # Traitement particulier de l'excuse, partie 2
                            game.joueurs[nouveau_maitre].tas.extend(l)
                        pli=[]
                        game.tour+=1
                        if game.tour <=15:
                            tree.ajoute_enfants(game.joueurs[nouveau_maitre].cartes_jouables(pli)) # On redemarre un nouveau pli avec le joueur maitre
                            for t in tree.enfants:
                                parcours_pt(nouveau_maitre,t,nouveau_maitre,copy.deepcopy(pli))
                        else: # C'etait le dernier pli qui vient de se terminer, on relance la fonction et le premier test nous amene a la "fin de partie"
                            parcours_pt(nouveau_maitre,tree,nouveau_maitre,copy.deepcopy(pli))
                        if game.joueurs[nouveau_maitre].attaquant:
                            for c in l: # On doit retirer les cartes du pli remporte fait une fois qu'on a parcouru en dessous
                                game.joueurs[nouveau_maitre].tas.remove(c)
                        
                        if tree.racine.couleur=="excuse":
                            game.joueurs[numero].tas.remove(tree.racine)
                        game.tour+=-1
                    game.remplacant_excuse=temp
                    game.joueurs[numero].main.append(tree.racine) # On n'oublie pas de remettre la carte dans la main du joueur apres avoir parcouru les arbres fils
                else: # On est au dernier tour, on regarde si on a gagne
                    compt=0
                    bouts=0
                    #Partie de decompte des points, identique a celle du jeu et ininteressante ici
                    for k in game.joueurs[game.appelant].tas:
                        if k.est_un_bout()==True:
                            bouts+=1
                        compt += k.valeur()
                    if game.appelant != game.appele:
                        for k in game.joueurs[game.appele].tas:
                            if k.est_un_bout()==True:
                                bouts+=1
                            compt+=k.valeur()
                    if bouts==0:
                        if compt >= 56:
                            game.appelant_gagnant=True
                    if bouts==1:
                        if compt >= 51:
                            game.appelant_gagnant=True
                    if bouts==2:
                        if compt >= 41:
                            game.appelant_gagnant=True
                    if bouts==3:
                        if compt >= 36:
                            game.appelant_gagnant=True
                            
                    if game.appelant_gagnant==self.attaquant: # on regarde quelle carte on a jouee pour gagner la partie au moment du jeu ou on appelle la fonction
                        arb=copy.deepcopy(tree)
                        card=tree.racine
                        while arb.parent.racine != carte("debut","as"):
                            card=arb.parent.racine
                            arb=arb.parent
                        compte[card]+=1 # Si on a remporte la partie, on inscrit +1 au compte des victoires pour la carte jouee
                        arb=tree
                        game.appelant_gagnant=False
            arb=arbre(carte("debut","as"))
            arb.ajoute_enfants(self.cartes_jouables(g.pli))
            for t in arb.enfants:
                parcours_pt(self.numero(game),t,game.maitre,copy.deepcopy(game.pli))
        return compte
    
    def joue_prevision_totale(self,game): # Joue la carte de plus haute hauteur possible
        cj=self.cartes_jouables(game.pli)
        maxi=-1
        a=carte("excuse","")
        compte=self.prevision_totale(game)
        for c in cj:
            if compte[c] >= maxi and c.hauteur>=a.hauteur:
                maxi=compte[c]
                a=c
        game.pli.append(a)
        self.main.remove(a)
    
    def appel_roi(self): # Annonce a la couleur ou il a la plus haute carte ( sauf le roi ), sinon, c'est qu'il a les 4 rois, il s'appelle tout seul
        '''Fonction recopiee sur joueur_max, je n'appelle pas autrement en general'''
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
        
    def fait_son_chien(self): # Je me fais une simili-coupe franche si j'ai moins de 3 indiens a une couleur ( je retire tous les indiens a cette couleur ), joueur_max sinon
        compte_couleurs={"coeur":0,"trefle":0,"carreau":0,"pique":0}
        couleurs=["coeur","pique","carreau","pique"]
        for c in self.main:
            if c.couleur !="atout" and c.couleur!="excuse" and not c.est_une_tete():
                compte_couleurs[c.couleur]+=1
        mini=42
        deb=random.randint(0,3)
        col=None
        for i in xrange(0,4):
            if compte_couleurs[couleurs[(deb+i)%4]]<mini:
                mini=compte_couleurs[couleurs[(deb+i)%4]]
                col=couleurs[(deb+i)%4]
        if mini<=3:
            for c in self.main:
                if c.couleur==col and not c.est_une_tete():
                    self.tas.append(c)
                    self.main.remove(c)
            for i in xrange(0,3-mini): # Partie recopiee sur joueur_max, une fois ma simili-coupe franche faite je rajoute ( eventuellement ) des petites cartes au chien
                minimum=42
                a=None
                modif=False
                for c in self.main:
                    if c.hauteur < minimum and c.couleur != "excuse" and c.couleur != "atout":
                        minimum= c.hauteur
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
        else:
            for i in xrange(0,3): # Partie recopiee sur joueur_max, je mets mes plus petites cartes dans le chien
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

    def annonce(self): # Embryon d'intelligence qui regarde le nombre d'atouts, de bouts et de rois
        compte=0
        for c in self.main:
            if c.est_un_bout():
                compte+=3
            if c.couleur=="atout":
                compte+=1
            if c.rang=="roi":
                compte+=2
        if compte <8:
            self.etat_annonce="passe"
            #print "Le joueur " +  self.nom + "fait l'annonce : " + self.etat_annonce
        elif compte <12:
            self.etat_annonce="petite"
            #print "Le joueur " +  self.nom + "fait l'annonce : " + self.etat_annonce
        elif compte <16:
            self.etat_annonce="garde"
            #print "Le joueur " +  self.nom + "fait l'annonce : " + self.etat_annonce
        elif compte <20:
            self.etat_annonce="garde sans"
            #print "Le joueur " +  self.nom + "fait l'annonce : " + self.etat_annonce
        else:
            self.etat_annonce="garde contre"
            #print "Le joueur " +  self.nom + "fait l'annonce : " + self.etat_annonce 

        
if __name__ =="__main__":     
    j1=joueur_intelligent("Bob")
    l=[]
    for i in xrange(16):
        l.append(i+1)
    print l
    a=list(j1.permutations(l))
    print len(a)
            
            
                
                
            
        
        
        
    
