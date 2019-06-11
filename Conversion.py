# ! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Using ALDialog Methods"""
import os
from tkinter import *
import csv
import qi
import argparse
import sys

# Création de la fenetre et titre
from tkinter.filedialog import askopenfilename, askdirectory

fenetre = Tk()
fenetre.geometry("500x200")
champ_label = Label(fenetre, text="Bienvenue!")
# On affiche le label dans la fenêtre
champ_label.pack()


# Fonction pour selectionner le fichier csv
def csv_fileSelect():
    filename.set(askopenfilename(filetypes=(("csv files", "*.csv"), ("all files", "*.*"))))


bouton_choisir_csv = Button(fenetre, text="Choisir le fichier csv", command=csv_fileSelect)
bouton_choisir_csv.pack()

filename = StringVar(fenetre)
entryCSV = Entry(fenetre, textvariable=filename, width="80")
entryCSV.pack()


# Fonction pour selectionner le dossier de destination
def directorySelect():
    directoryname.set(askdirectory(initialdir="/", title='Choisissez un repertoire'))


bouton_choisir_directory = Button(fenetre, text="Choisir le dossier où mettre le .top généré", command=directorySelect)
bouton_choisir_directory.pack()

directoryname = StringVar(fenetre)
entryDirectory = Entry(fenetre, textvariable=directoryname, width="80")
entryDirectory.pack()


# Permet de convertir les lignes du csv
def replace_question_csv(question):
    print("replace_csv")
    # faire un replace pour convertir le csv en ligne .top
    return question


# Permet de créer le .top avec le header et les lignes du csv
def create_top():
    # Creer le topic
    fichier = open(entryDirectory.get() + "/universite.top", "w")
    fichier.write("topic: ~universite()\nlanguage: frf")

    with open(entryCSV.get(), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            question = row[0]
            reponse = row[1]
            fichier.write("\nu:(" + replace_question_csv(question) + ") " + replace_question_csv(reponse))
            print(reponse)

    fichier.close()


def load():
    print("Transfert vers Nao")
    ##Connection ftp
    host = "169.254.129.162"  # adresse du serveur FTP
    user = "nao"  # votre identifiant
    password = "nao"  # votre mot de passe
    connect = ftp.ftplib(host, user, password)  # on se connecte
    commande = raw_input('CWD dialog')  # entrez la commande à effectuer
    connect.sendcmd(commande)
    ##Ouverture du fichier
    fichier = entryDirectory.get() + "/universite.top"
    file = open(fichier, 'rb')  # ici, j'ouvre le fichier ftp.py
    connect.storbinary('STOR ' + fichier,
                       file)  # ici (où connect est encore la variable de la connexion), j'indique le fichier à envoyer
    file.close()  # on ferme le fichier
    connect.quit()  # où "connect" est le nom de la variable dans laquelle vous avez déclaré la connexion !


def traitement():
    create_top()
    load()


bouton_lancer = Button(fenetre, text="Lancer", command=load)  # mettre la commande qui mènera au traitement
bouton_lancer.pack()

bouton_quitter = Button(fenetre, text="Quitter", command=fenetre.quit)
bouton_quitter.pack()

# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
fenetre.mainloop()
