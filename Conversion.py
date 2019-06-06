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
directoryname = StringVar(fenetre)
entry = Entry(fenetre, textvariable=filename)
entry.pack()


# Fonction pour selectionner le fichier csv
def csv_fileSelect():
    filename.set(askopenfilename(filetypes=(("csv files", "*.csv"), ("all files", "*.*"))))


bouton_choisir_csv = Button(fenetre, text="Choisir le fichier csv", command=csv_fileSelect)
bouton_choisir_csv.pack()


# Fonction pour selectionner le fichier csv
def directorySelect():
    directoryname.set(askdirectory())


bouton_choisir_directory = Button(fenetre, text="Choisir le dossier où mettre le .top généré", command=directorySelect)
bouton_choisir_directory.pack()

bouton_lancer = Button(fenetre, text="Lancer", command=fenetre.quit)  # mettre la commande qui mènera au traitement
bouton_lancer.pack()

bouton_quitter = Button(fenetre, text="Quitter", command=fenetre.quit)
bouton_quitter.pack()

# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
fenetre.mainloop()
