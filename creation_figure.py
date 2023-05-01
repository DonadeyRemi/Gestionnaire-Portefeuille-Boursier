import matplotlib.pyplot as plt
import pandas
import json
import csv
import os
import datetime

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

    return erreur,fig

def figures_patrimoine_tot(arg="somme_act_port",):
    patrimoine_tot_list = []
    patrimoine_tot = 0
    portefeuilles_name = []
    
    i = 0
    for root, directories, files in os.walk("ressources/portefeuilles"):  
        if i <=  0 :
            for file in files: # les file sont les fichiers json des portefeuilles à jours
                file_name_without_ext = file.split(".")[0]
                portefeuilles_name.append(file_name_without_ext)
                with open(f"ressources/portefeuilles/{file_name_without_ext}.json",'r') as port_file :
                    dict_port = json.load(port_file)

                # on fait les calculs
                somme_arg = 0
                for symbole in dict_port.keys():
                    somme_arg += dict_port[symbole][arg]
                    patrimoine_tot += dict_port[symbole][arg]

                patrimoine_tot_list.append(somme_arg)


        i += 1

    # modification de la figure existante
    fig,ax = plt.subplots(figsize=(5,5))
    ax.pie(patrimoine_tot_list,labels=portefeuilles_name,explode=[0.05 for i in range(len(patrimoine_tot_list))],wedgeprops=dict(width=0.5))

    ax.set_title(f"Répartitions des {arg} selon les portefeuilles")
    ax.legend()

    return fig,ax,patrimoine_tot

def figure_hist_patrimoine_tot(arg="somme_act_port"):
    data = pandas.read_csv("ressources/portefeuilles/history/patrimoine_hist.csv")
    
    plt.plot(data)
    
    



if __name__ == "__main__" :
    figure_hist_patrimoine_tot()