import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

#le but est de simuler à quoi pourait resembler la coupe résultante du pliage de plusieurs matériaux
def pliage(couleurs,nb_pliages,mode='normal'):
    #couleurs est la liste des couleurs en hexcode des materiaux, de bas en haut
    #nb_pliages pliages sont effectué, le résultat est affiché
    couches = [[couleurs[0],1]]#liste de couple couleur,hauteur
    if(mode=='normal'):
        for i in range(1,len(couleurs)):
            if(couleurs[i]==couches[-1][0]):
                couches[-1][1]+=1
            else:
                couches.append([couleurs[i],1])
        h_tot = len(couleurs)
    elif(mode.startswith("ajout")):
        X = int(mode[5:])
        for i in range(1,len(couleurs)-X):
            if(couleurs[i]==couches[-1][0]):
                couches[-1][1]+=1
            else:
                couches.append([couleurs[i],1])
        h_tot = len(couleurs)-X
    for i in range(nb_pliages):
        #mode normal : simples plis
        if(mode=='normal'):
            n=len(couches)
            couches[-1][1]=2*couches[-1][1]
            for j in range(n-2,0,-1):
                couches.append(couches[j].copy())
            couches.append(couches[0])
            h_tot=2*h_tot
        #mode ajoutX : à chaque pli on ajoute les X dernières couches avant de plier
        elif(mode.startswith('ajout')):
            for j in range(len(couleurs)-X,len(couleurs)):
                couches.append([couleurs[j],h_tot/(2*X)])
            n=len(couches)
            couches[-1][1]=2*couches[-1][1]
            for j in range(n-2,0,-1):
                couches.append(couches[j].copy())
            couches.append(couches[0])
            h_tot=3*h_tot
    #affichage
    fig = plt.figure()
    ax = fig.add_subplot()
    #Rectangle : coin bas à gauche,largeur,hauteur
    y=0
    for barre in couches:
        ax.add_patch(Rectangle((0,y), h_tot, barre[1], color=barre[0]))
        y+=barre[1]
    #print(couches)
    plt.axis('equal')
    plt.axis('off')
    plt.show()

pliage(['#000','#CECEAA','#00f','#0f0','#f00'],4,mode='ajout1')
pliage(['#000','#CECEAA','#00f','#0f0','#f00'],4,mode='ajout2')

#epaiseur de la plaque rajouté au n-ème plit : (2*k/k-1)^n*e/k
#base k, e l’épaisseur de la première plaque possée (métal rare)