from skimage import io
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np

class Image:
    def __init__(self):
        """Initialisation d'une image composee d'un tableau numpy 2D vide
        (pixels) et de 2 dimensions (H = height et W = width) mises a 0
        """
        self.pixels = None
        self.H = 0
        self.W = 0
    

    def set_pixels(self, tab_pixels):
        """ Remplissage du tableau pixels de l'image self avec un tableau 2D (tab_pixels)
        et affectation des dimensions de l'image self avec les dimensions 
        du tableau 2D (tab_pixels) 
        """
        self.pixels = tab_pixels
        self.H, self.W = self.pixels.shape


    def load(self, file_name):
        """ Lecture d'un image a partir d'un fichier de nom "file_name"""
        self.pixels = io.imread(file_name)
        self.H,self.W = self.pixels.shape 
        print("lecture image : " + file_name + " (" + str(self.H) + "x" + str(self.W) + ")")


    def display(self, window_name):
        """Affichage a l'ecran d'une image"""
        fig = plt.figure(window_name)
        if (not (self.pixels is None)):
            io.imshow(self.pixels)
            io.show()
        else:
            print("L'image est vide. Rien à afficher")


    #==============================================================================
    # Methode de binarisation
    # 2 parametres :
    #   self : l'image a binariser
    #   S : le seuil de binarisation
    #   on retourne une nouvelle image binarisee
    #==============================================================================
    def binarisation(self, S):
		# creation d'une image vide
        im_bin = Image()
        
        # affectation a l'image im_bin d'un tableau de pixels de meme taille
        # que self dont les intensites, de type uint8 (8bits non signes),
        # sont mises a 0
        im_bin.set_pixels(np.zeros((self.H, self.W), dtype=np.uint8))

        #parcout de chaque pixel de l'image à binariser par deux boucles for (une pour les 
        #lignes, puis une pour les colonnes), puis comparaison avec le seuil et
        #détermination de la valeur finale du pixel.
        for i in range(0,self.H,1):
            for j in range(0,self.W,1):
                if (self.pixels[i][j]<=S):
                    im_bin.pixels[i][j]=0
                else:
                    im_bin.pixels[i][j]=255
                    
        #renvoie de l'image binarisée
        return im_bin 

    #==============================================================================
    # Dans une image binaire contenant une forme noire sur un fond blanc
    # la methode 'localisation' permet de limiter l'image au rectangle englobant
    # la forme noire
    # 1 parametre :
    #   self : l'image binaire que l'on veut recadrer
    #   on retourne une nouvelle image recadree
    #==============================================================================
    def localisation(self):
        #Initialisation de deux tableaux : l'un contenant les positions des lignes des 
        #pixels noirs et l'autre les positions des colonnes des pixels noirs  
        position_pixels_l = []
        position_pixels_c = []
        
        #Remplissage des tableaux position_pixels
        for l in range(0,self.H,1):
            for c in range(0,self.W,1):
                if (self.pixels[l][c]==0):
                    position_pixels_l.append(l)
                    position_pixels_c.append(c)
        
        #Initialisation des variables si l'image ne comptient aucun pixel noir
        if (len(position_pixels_l)==0):
            l_min = None
            l_max = None
            c_min = None
            c_max = None
        
        #Initialisation des variables si l'image comptient au moins un pixel noir
        l_min = position_pixels_l[0]
        l_max = position_pixels_l[0]
        c_min = position_pixels_c[0]
        c_max = position_pixels_c[0]
        
        #Détermination de la valeur l_max (l_min est déjà trouvée)
        for i in position_pixels_l:
            if (i>l_max):l_max=i
        
        #Détermination des valeurs de c_min et c_max 
        for j in position_pixels_c:
            if (j<c_min):c_min=j
            if (j>c_max):c_max=j
        
        # creation d'une image vide et ajout du tableau recadré
        im_loc = Image()
        im_loc.set_pixels(self.pixels[l_min:l_max+1,c_min:c_max+1])
        
        #Renvoie de l'image recadrée
        return im_loc

    #==============================================================================
    # Methode de redimensionnement d'image
    #==============================================================================
    
    #Redimensionnement du tableau en fonction des dimensions passées en paramètres, 
    #passage du tableau de float en int puis ajout du tableau dans l'image 
    def resize(self, new_H, new_W):
        im_res = Image()
        tab_res = resize(self.pixels,(new_H,new_W),0)
        im_res.set_pixels(np.uint8(tab_res*255))
        return im_res

    #==============================================================================
    # Methode de mesure de similitude entre l'image self et un modele im
    #==============================================================================
    
    
    def similitude(self, im):
        #Initialisation d'un compteur
        cpt = 0
        
        #Vérification de l'intensité de chaque pixel de l'image à testée par rapport aux 
        #pixels de l'image modèle à la même position
        for l in range(0,self.H,1):
            for c in range(0,self.W,1):
                if (self.pixels[l][c]==im.pixels[l][c]):
                    cpt+=1
        return cpt/(self.H*self.W)