#Fonction qui permet de remplacer les caractères spéciaux
def replaceCaracter(txt, newtxt):
    newChar = txt.replace(txt, newtxt)
    return newChar

#Caractère spéciaux remplacé par espace
#lettre toute seule " a " [a]
replaceCaracter("'", " ")
replaceCaracter("/", " ")
replaceCaracter("#", " ")
replaceCaracter(":", " ")
replaceCaracter("/", " ")
replaceCaracter("!", " ")
replaceCaracter("-", " ")
replaceCaracter("_", " ")
replaceCaracter("~", " ")

replaceCaracter("comment", "[comment]") #txt.replace(",", "") remplace comment par un vide
replaceCaracter("quoi", "[quoi]")
replaceCaracter("qui", "[qui]")
replaceCaracter("de", "[de]")
replaceCaracter(" s ", "[s]")
replaceCaracter("m'", "[m]")
replaceCaracter("/", "")
replaceCaracter(";", "")
replaceCaracter("", "")


