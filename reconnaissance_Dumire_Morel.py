from image import Image

def lecture_modeles(chemin_dossier):
    fichiers= ['_0.png','_1.png','_2.png','_3.png','_4.png','_5.png','_6.png', 
            '_7.png','_8.png','_9.png']
    liste_modeles = []
    for fichier in fichiers:
        model = Image()
        model.load(chemin_dossier + fichier)
        liste_modeles.append(model)
    return liste_modeles


def reconnaissance_chiffre(image, liste_modeles, S):
    #Binarisation de l'image de base
    image_bin = image.binarisation(S)
    
    #Recadrement de l'image binarisée
    image_loc = image_bin.localisation()
    
    #Initialisation des variables similitude_max et chiffre_final
    similitude_max = 0
    chiffre_final = None
    
    #Redimensionnement de l'image recadrée en fonction de tous les modèles
    for i in range(0,len(liste_modeles),1):
        image_res = image_loc.resize(liste_modeles[i].H,liste_modeles[i].W)
        
        #Recherche de la similitude la plus élevée parmis tous les modèles
        if (similitude_max < image_res.similitude(liste_modeles[i])):
            similitude_max = image_res.similitude(liste_modeles[i])
            chiffre_final = i
        
    #Renvoie du chiffre dont la similitude est la plus élevée
    return chiffre_final
            
    

