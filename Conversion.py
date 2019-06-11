# ! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Using ALDialog Methods"""
import os
from tkinter import *
import csv
from ftplib import FTP


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
def replace_question_csv(str):
    elements = ["/", "#", ":", "-", "!", "_", "@", ";", "~", "'", "l'", "j'", "s'", "t'", "m'", "d'", "c'", "n'", "qu'"]
    for elem in elements:
        str = str.replace(elem, " [" + elem + "] ")
    elements = [" s ", " m ", " t ", " j ", " l ", " d ",
                " comment ", " quoi ", " du ", " de ", " des ", " la ", " le ", " les ",
                " à ", " quel ", " quels ", " quelle ", " quelles ", " a ", " je ", " tu ", " il ",
                " elle ", " on ", " nous ", " vous ", " ils ", " elles ", " mais ", " car ", " et ", " donc ",
                " ni ", " ou ", " car ", " or ", " comme ", " lorsque ", " quand ", " si ", " ce ", " ces ",
                " cette ", " cet ", " un ", " mon ", " ton ", " son ", " notre ", " votre ", " leur ", " ma ", " ta "
                " sa ", " mes ", " tes ", " ses "]
    for elem in elements:
        str = str.replace(elem, " [" + elem.replace(" ", "") + "] ")
    str = str.replace("  ", " ")
    return str


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
    connect = FTP(host, user, password)
    connect.sendcmd('CWD dialog')
    ##Ouverture du fichier
    f_name = entryDirectory.get() + "/universite.top"
    f = open(f_name, 'rb')
    connect.storbinary('STOR ' + f_name, f)
    connect.retrlines('LIST')
    f.close()
    connect.close()


def traitement():
    create_top()
    load()


bouton_lancer = Button(fenetre, text="Lancer", command=traitement)  # mettre la commande qui mènera au traitement
bouton_lancer.pack()

bouton_quitter = Button(fenetre, text="Quitter", command=fenetre.quit)
bouton_quitter.pack()

# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
fenetre.mainloop()
