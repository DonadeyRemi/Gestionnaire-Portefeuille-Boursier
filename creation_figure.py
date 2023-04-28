import matplotlib.pyplot as plt
import json
import csv
import os

def repartition_actifs_parts(portefeuille,arg="parts"):
    erreur = 0
    if os.path.exists(f"ressources/portefeuilles/{portefeuille}.json") :
        with open(f"ressources/portefeuilles/{portefeuille}.json",'r') as port_file :
            try :
                dict_port = json.load(port_file)

            except Exception as e:
                print(f"[Erreur] : {e}")
                erreur = -2

    liste_arg = []
    for symb in dict_port.keys():
        liste_arg.append(dict_port[symb][arg])

    # création de la figure
    fig,ax = plt.subplots(figsize=(8,8))
    ax.pie(liste_arg,labels=dict_port.keys())

    ax.set_title(f"Répartitions des actifs par {arg}")
    plt.legend()

    return erreur

def figures_patrimoine_tot():
    patrimoine_tot = 0
    portefeuilles_name = []
    
    i = 0
    for root, directories, files in os.walk("ressources/portefeuilles"):  
        if i <=  0 :
            for file in files: # les file sont les fichiers json des portefeuilles à jours
                portefeuilles_name.append(file.split(".")[0])
                with open(f"ressources/portefeuilles/{file}.json",'r') as port_file :
                    dict_port = json.load(port_file)

                # on fait les calculs
                for symbole in dict_port.keys():
                    pass

        i += 1



if __name__ == "__main__" :
    pie_patrimoine_tot()