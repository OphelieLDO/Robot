# ! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Using ALDialog Methods"""
from ScrolledText import *

from tkinter import *
import csv
import paramiko
import qi

# Création de la fenetre et titre
from tkinter.filedialog import askopenfilename, askdirectory

fenetre = Tk()
fenetre.geometry("500x400")
fenetre.title("Convertisseur de csv à top")
champ_label = Label(fenetre, text="Outil de conversion de CVS à TOPIC!")
# On affiche le label dans la fenêtre
champ_label.pack()
content = Frame(fenetre)
frame = ScrolledText(content, borderwidth=5, relief="sunken", width=30, height=10)

session = qi.Session()
ALDialog = None
topic_name = None


def quitter():
    try:
        global ALDialog
        global session
        global topic_name
        global root
        ALDialog.unsubscribe('universite')
        # Deactivating the topic
        # Loading the topic given by the user (absolute path is required)
        ALDialog.deactivateTopic(topic_name)
        # now that the dialog engine is stopped and there are no more activated topics,
        # we can unload our topic and free the associated memory
        ALDialog.unloadTopic(topic_name)
        session.close()
        fenetre.destroy()
        sys.exit()
    except RuntimeError:
        print("\nCan't connect to Naoqi")
        fenetre.destroy()
        sys.exit(1)


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
    str = str.lower()
    elements = ["/", "#", ":", "-", "!", "_", "@", ";", "~", "'", "l'", "j'", "s'", "t'", "m'", "d'", "c'", "n'", "qu'"]
    for elem in elements:
        str = str.replace(elem, " {" + elem + "} ")
    elements = [" s ", " m ", " t ", " j ", " l ", " d ",
                " comment ", " quoi ", " du ", " de ", " des ", " la ", " le ", " les ",
                " à ", " quel ", " quels ", " quelle ", " quelles ", " a ", " je ", " tu ", " il ", " que "
                                                                                                    " elle ", " on ",
                " nous ", " vous ", " ils ", " elles ", " mais ", " car ", " et ", " donc ",
                " ni ", " ou ", " car ", " or ", " comme ", " lorsque ", " quand ", " si ", " ce ", " ces ",
                " cette ", " cet ", " un ", " mon ", " ton ", " son ", " notre ", " votre ", " leur ", " ma ", " ta ",
                " sa ", " mes ", " tes ", " ses ", " puis ", " ayant ", " en ", " est ", " à "]
    for elem in elements:
        str = str.replace(elem, " {" + elem.replace(" ", "") + "} ")
    str = str.replace("  ", " ")
    return str


# Permet de créer le .top avec le header et les lignes du csv
def create_top():
    # Creer le topic
    if "/" in entryDirectory.get():
        fichier = open(entryDirectory.get() + "/universite.top", "w")
    else:
        fichier = open(entryDirectory.get() + "\\universite.top", "w")

    fichier.write("topic: ~universite()\nlanguage: frf")

    with open(entryCSV.get(), 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            question = row[0]
            reponse = row[1]
            fichier.write("\nu:(" + replace_question_csv(question) + ") " + reponse)
        fichier.close()


def load2(ip):
    print("Transfert vers Nao")
    # Connection ftp
    host = "169.254.129.162"  # adresse du serveur FTP
    if "/" in entryDirectory.get():
        c_path = open(entryDirectory.get() + "/universite.top", "w")
    else:
        c_path = open(entryDirectory.get() + "\\universite.top", "w")
    r_path = "/home/nao/dialog"

    transport = paramiko.Transport(host, 22)
    transport.connect(username="nao", password="nao")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(c_path, r_path)

    sftp.close()
    transport.close()


def conversion():
    create_top()


bouton_lancer = Button(fenetre, text="Lancer la conversion",
                       command=conversion)  # mettre la commande qui mènera au traitement
bouton_lancer.pack()

champip = Label(fenetre, text="\n\nLancer NAO\n Attention, il faut avoir transférer le .top dans nao au préalable\n"
                              "\nEntrez l'IP!")
champip.pack()
host = StringVar()
host.set("169.254.129.162")
entreeip = Entry(fenetre, textvariable=host, width=30)
entreeip.pack()


def load():
    host = entreeip.get()
    print (host)
    frame.insert(END, "\n" + "Demarrage sur ip : " + host)
    try:
        global session
        global ALDialog
        session.connect("tcp://{}:{}".format(str(host), 9559))
        ALDialog = session.service("ALDialog")

    except RuntimeError:
        raise Exception("Impossible de se connecter")

    """
    This example uses ALDialog methods.
    It's a short dialog session with one topic.
    """
    # Getting the service ALDialog
    frame.insert(END, "\n" + "Chargement du dialogue")
    # download_data()
    topic_path = "/home/nao/dialog/universite.top"
    # Loading the topic given by the user (absolute path is required)
    topf_path = topic_path.decode('utf-8')
    print ("step 1")
    global topic_name
    topic_name = ALDialog.loadTopic(topf_path.encode('utf-8'))

    # Activating the loaded topic
    ALDialog.activateTopic(topic_name)

    # Starting the dialog engine - we need to type an arbitrary string as the identifier
    # We subscribe only ONCE, regardless of the number of topics we have activated
    ALDialog.subscribe('universite')
    print ("step 2")


def lancer_nao():
    load()


bouton_nao = Button(fenetre, text="Lancer le topic sur NAO", command=lancer_nao)
bouton_nao.pack()

bouton_quitter = Button(fenetre, text="quitter", command=quitter)
bouton_quitter.pack()

# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
fenetre.mainloop()
