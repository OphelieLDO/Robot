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

global topic_name
global topic
global ALDialog
global session
global fenetre

fenetre = Tk()
fenetre.geometry("500x500")
fenetre.title("Programme de conversion NAO")
champ_label = Label(fenetre, text="Outil de conversion de CVS à TOPIC! Le fichier est généré et envoyé sur NAO")
# On affiche le label dans la fenêtre
champ_label.pack()
content = Frame(fenetre)
frame = ScrolledText(content, borderwidth=5, relief="sunken", width=30, height=10)

session = qi.Session()
ALDialog = None
topic_name = None
topic = None


# Permet de convertir les lignes du csv
def replace_question_csv(str):
    str = str.lower()
    # On supprime les caractère spéciaux
    elements = ["/", "#", ":", "-", "!", "_", "@", ";", "~", "'"]
    for elem in elements:
        str = str.replace(elem, " ")
    # On met entre {} les mots non important
    elements = [" s ", " m ", " t ", " j ", " l ", " d ", " qu ", " y a t il "
                                                                  " comment ", " quoi ", " du ", " de ", " des ",
                " la ", " le ", " les ",
                " à ", " quel ", " quels ", " quelle ", " quelles ", " a ", " je ", " tu ", " il ", " que ",
                " elle ", " on ", " y ", " nous ", " vous ", " ils ", " elles ", " mais ", " car ", " et ", " donc ",
                " ni ", " ou ", " car ", " or ", " comme ", " lorsque ", " quand ", " si ", " ce ", " ces ",
                " cette ", " cet ", " un ", " mon ", " ton ", " son ", " notre ", " votre ", " leur ", " ma ", " ta ",
                " sa ", " mes ", " tes ", " ses ", " puis ", " ayant ", " en ", " est ", " à ", " par "]
    for elem in elements:
        str = str.replace(elem, " {" + elem.replace(" ", "") + "} ")
    # On met entre [] les mots similaire
    elements = ([" étudiant ", " etudiant ", " étudiants ", " etudiants ", " élève ", " éleve ", " elève ", " eleve ",
                 " élèves ", "éleves ", " elèves ", " eleves "],
                [" prof ", " professeur ", " enseignant "],
                [" fillière ", " filière ", " filiere ", " filliere " " branche ", " diplôme ", " formation "],
                [" cours ", " classe "],
                [" heure ", " créneau "],
                [" matière ", " enseignement"],
                [" secrétaire ", " assistant ", " assistante ", " responsable "],
                [" bibliothèque ", " BU ", " biliotheque ", " bibliothèques ", " bibliotheques "],
                [" combien ", " nombre "])
    for i in range(len(elements)):
        for j in range(len(elements[i])):
            sous_str = ""
            if elements[i][j] in str:
                for k in range(len(elements[i])):
                    sous_str = sous_str + elements[i][k]
                str = str.replace(elements[i][j], " [" + sous_str + "] ")
                break

    # On supprime les doubles espaces
    while "  " in str:
        str = str.replace("  ", " ")
    return str


# Permet de créer le .top avec le header et les lignes du csv
def create_top(nomtopic):
    # Creer le topic
    if "/" in entryDirectory.get():
        fichier = open(entryDirectory.get() + "/" + nomtopic + ".top", "w")
    else:
        fichier = open(entryDirectory.get() + "\\" + nomtopic + ".top", "w")

    fichier.write("topic: ~" + nomtopic + "()\nlanguage: frf")

    with open(entryCSV.get(), 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            question = row[0]
            reponse = row[1]
            fichier.write("\nu:(" + replace_question_csv(question) + ") " + reponse)
            # Gestion des réponses multiples
            i = 3
            nb = 1
            while len(row) > i:
                if row[i] != "":
                    reponse_user = row[i - 1]
                    reponse_robot = row[i]
                    reponse_user = reponse_user.split("/")
                    reponse_robot = reponse_robot.split("/")
                    if len(reponse_user) == len(reponse_robot):
                        for k in range(len(reponse_robot)):
                            fichier.write(
                                "\n\tu" + str(nb) + ":(" + replace_question_csv(reponse_user[k]) + ") " + reponse_robot[
                                    k])
                i = i + 2
                nb = nb + 1
        fichier.close()


# Fonction pour selectionner le fichier csv
def csv_fileSelect():
    filename.set(askopenfilename(filetypes=(("csv files", "*.csv"), ("all files", "*.*"))))


# Fonction pour selectionner le dossier de destination
def directorySelect():
    directoryname.set(askdirectory(initialdir="/", title='Choisissez un repertoire'))


# Cette fonction permet de transférer à Nao via SFTP
def load2(nomtopic, host):
    nomtopic = entreetopic.get()
    # Connection ftp
    if "/" in entryDirectory.get():
        c_path = entryDirectory.get() + "/" + nomtopic + ".top"
    else:
        c_path = entryDirectory.get() + "\\" + nomtopic + ".top"

    r_path = "/home/nao/dialog/" + nomtopic + ".top"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username="nao", password="nao")
    sftp = ssh.open_sftp()
    sftp.put(c_path, r_path)
    sftp.close()
    ssh.close()


# Permet de lancer nao avec le Topic demandé
def load_nao(nomtopic, host):
    global ALDialog
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
    topic_path = "/home/nao/dialog/" + nomtopic + ".top"

    # Loading the topic given by the user (absolute path is required)
    topf_path = topic_path.decode('utf-8')
    global topic_name
    topic_name = ALDialog.loadTopic(topf_path.encode('utf-8'))

    # Activating the loaded topic
    ALDialog.activateTopic(topic_name)

    # Starting the dialog engine - we need to type an arbitrary string as the identifier
    # We subscribe only ONCE, regardless of the number of topics we have activated
    ALDialog.subscribe('My Module')


def quitter():
    global ALDialog
    global session
    global topic_name
    global fenetre
    try:
        # Stop dialog
        ALDialog.unsubscribe('My Module')
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
    fenetre.destroy()


bouton_choisir_csv = Button(fenetre, text="Choisir le fichier csv", command=csv_fileSelect)
bouton_choisir_csv.pack()

filename = StringVar(fenetre)
entryCSV = Entry(fenetre, textvariable=filename, width="80")
entryCSV.pack()

bouton_choisir_directory = Button(fenetre, text="Choisir le dossier où mettre le .top généré\n"
                                                "Attention: Ne doit pas être un dossier racine",
                                  command=directorySelect)
bouton_choisir_directory.pack()

directoryname = StringVar(fenetre)
entryDirectory = Entry(fenetre, textvariable=directoryname, width="80")
entryDirectory.pack()

champ2 = Label(fenetre, text="\nEntrez le nom du fichier généré (sans le .top)")
champ2.pack()

nomtopic = StringVar()
nomtopic.set("universite")
entreetopic = Entry(fenetre, textvariable=nomtopic, width=30)
entreetopic.pack()
champ3 = Label(fenetre, text="\nEntrez l'IP!")
champ3.pack()
host = StringVar()
host.set("169.254.129.162")
entreeip = Entry(fenetre, textvariable=host, width=30)
entreeip.pack()


def load():
    nomtopic = entreetopic.get()
    host = entreeip.get()
    create_top(nomtopic)
    load2(nomtopic, host)
    load_nao(nomtopic, host)


bouton_nao = Button(fenetre, text="Lancer le programme", command=load)
bouton_nao.pack()

bouton_quitter = Button(fenetre, text="quitter", command=quitter)
bouton_quitter.pack()

# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
fenetre.mainloop()
