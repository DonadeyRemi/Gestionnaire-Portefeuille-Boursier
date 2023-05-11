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
    fig,ax = plt.subplots()
    ax.pie(liste_arg,labels=dict_port.keys())

    ax.set_title(f"Répartitions des actifs par {arg}")

    return fig,ax

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
    data = pandas.read_csv("ressources/portefeuilles/history/patrimoine_hist.csv",names=["date","time","parts","somme_inv_port","somme_inv_loc","somme_act_port","somme_act_loc","frais_ac_vt","dividendes","frais_div"])
    
    print(data.head())
    
    fig,ax = plt.subplots(figsize=(8,5))
    ax.set_title(f"Evolution de du patrimoine arg = {arg}")
    ax.plot(data["date"],data[arg])
    ax.set_xlabel("Time")
    ax.set_ylabel("Patrimoine")
    plt.legend()

    #plt.show()

    return fig,ax

def figure_ev_port(port_name,arg="somme_act_port"):
    data = pandas.read_csv(f"ressources/portefeuilles/history/{port_name}_history.csv",names=["date","time","parts","somme_inv_port","somme_inv_loc","somme_act_port","somme_act_loc","frais_ac_vt","dividendes","frais_div"])
    
    print(data.head())
    
    fig,ax = plt.subplots(figsize=(8,5))
    ax.set_title(f"Evolution de du patrimoine arg = {arg}")
    ax.plot(data["date"],data[arg])
    ax.set_xlabel("Time")
    ax.set_ylabel("Patrimoine")
    plt.legend()

    #plt.show()

    return fig,ax

    



if __name__ == "__main__" :
    fig,ax = repartition_actifs_parts("XTB",arg="somme_act_port")
    plt.show()