# ! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Using ALDialog Methods"""
import os
from tkinter import *
from tkinter import filedialog

# Création de la fenetre et titre
from tkinter.filedialog import askopenfilename, askdirectory

fenetre = Tk()
champ_label = Label(fenetre, text="Bienvenue!")
# On affiche le label dans la fenêtre
champ_label.pack()

filename = StringVar(fenetre)

entry = Entry(fenetre, textvariable=filename)
entry.pack()


# Fonction pour selectionner le fichier csv
def csv_fileSelect():
    filename.set(askopenfilename(filetypes=(("csv files", "*.csv"), ("all files", "*.*"))))


bouton_choisir = Button(fenetre, text="Choisir le fichier csv", command=csv_fileSelect)
bouton_choisir.pack()

var_texte_entree = StringVar()
ligne_entree = Entry(fenetre, textvariable=var_texte_entree, width=30)
ligne_entree.pack()



# Fonction pour selectionner le fichier csv
def directorySelect():
    filename.set(askdirectory)




champ_fichier_sortie = Label(fenetre, text="Entrez le lien de votre dossier de destination:")
# On affiche le label dans la fenêtre
champ_fichier_sortie.pack()

var_texte_sortie = StringVar()
ligne_sortie = Entry(fenetre, textvariable=var_texte_sortie, width=30)
ligne_sortie.pack()

bouton_lancer = Button(fenetre, text="Lancer", command=fenetre.quit)  # mettre la commande qui mènera au traitement
bouton_lancer.pack()

bouton_quitter = Button(fenetre, text="Quitter", command=fenetre.quit)
bouton_quitter.pack()


# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
fenetre.mainloop()
