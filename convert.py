# Convertitore Intellij to Netbeans
#By VincenzoT
import shutil
def apriFile(file, permission):
    try:
        return open(file, permission)
    except FileNotFoundError as e:
        print("** File Non Trovato %s**" %file)
    except PermissionError:
        print("** Permessi insufficenti per aprire il file %s**\n\n" %file)
    except Exception:
        print("** Si è verificato un errore durante la conversione:  %s**\n\n" %file)

def resetFolder():
    with apriFile("template/project.xml", "r") as templateProjectXML:
        with apriFile("nbproject/project.xml", "w") as outputProjectXML:
            outputProjectXML.write(templateProjectXML.read())

    with apriFile("template/project.properties", "r") as templateProperties:
        with apriFile("nbproject/project.properties", "w") as outputProperties:
            outputProperties.write(templateProperties.read())

def copiaCartella(src, dist):
    try:
        shutil.copytree(src, dist)  
    except FileExistsError:
        print("Il file esiste gia")
    except FileNotFoundError:
        print("Cartella trovata in: " + dist)
    except Exception as e:
        print("Errore, processo annullato")

def getProgetto(path):
    return str(path).split("/")[path.count("/")]

def rinominaProgetto():
    global srcPath
    file = apriFile("nbproject/project.xml", "r")
    lines = file.readlines()
    file.close()

    for i,line in enumerate(lines):
        if "<name>******************</name>" in line:
            lines[i] = "<name>%s</name>\n" % getProgetto(srcPath)

    with apriFile("nbproject/project.xml", "w") as file:
        file.write(''.join(lines))

print("Programma convertitore Intellij Netbeans.")
print("Inserisci il percorso file del progetto")

srcPath = input("Percorso: ").strip(" ")
dstPath = srcPath + "_NB"

rinominaProgetto()
copiaCartella(srcPath + "/src", dstPath + "/src")  # Copy coding
copiaCartella("nbproject", dstPath + "/nbproject")  # Copy settings

resetFolder()
print("\n\nProgetto Convertito!\nGuarda la nuova cartella creata!")
