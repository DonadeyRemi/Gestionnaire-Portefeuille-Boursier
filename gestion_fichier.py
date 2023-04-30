import csv
import json
import os

def write_achat_titre(symbole,date,parts,valeur_loc,taux_conv,valeur_port,frais):
    achat = [symbole,date,parts,valeur_loc,taux_conv,valeur_port,frais,"ACHAT"]

    try : 
        with open("ressources/achat_vente.csv",'a') as ac_vt_file :
            writer_obj = csv.writer(ac_vt_file)
            writer_obj.writerow(achat)

    except Exception as e :
        print(f"[Erreur] : {e}")
        return -1
    
    else : 
        return 0
    
def write_vente_titre(symbole,date,parts,valeur_loc,taux_conv,valeur_port,frais) :
    vente = [symbole,date,parts,valeur_loc,taux_conv,valeur_port,frais,"VENTE"]

    try : 
        with open("ressources/achat_vente.csv",'a') as ac_vt_file :
            writer_obj = csv.writer(ac_vt_file)
            writer_obj.writerow(vente)

    except Exception as e :
        print(f"[Erreur] : {e}")
        return -1
    
    else :
        return 0
    
def write_dividend(symbole,date,valeur,frais,valeur_nette) :
    dividende = [symbole,date,valeur,frais,valeur_nette]

    try :
        with open("ressources/dividendes.csv",'a') as div_file :
            writer_obj = csv.writer(div_file)
            writer_obj.writerow(dividende)

    except Exception as e :
        print(f"[Erreur] : {e}")
        return -1
    
    else : 
        return 0
    
def write_achat_port(port_name,symbole,date,parts,val_symb_loc,val_symb_port,frais):
    erreur = 0
    if os.path.exists(f"ressources/portefeuilles/{port_name}.json") :
        try :
            with open(f"ressources/portefeuilles/{port_name}.json",'r') as port_file:
                port_dict = json.load(port_file)


        except Exception as e :
            print(f"[Erreur] : {e}")
            return -2
        
        if port_dict.get(symbole,0) == 0 :
            port_dict[symbole] = {"date_debut" : date, "parts" : parts, "valeur_moy_inv_loc" : val_symb_loc,"valeur_moy_inv_port":val_symb_port,"somme_inv_loc" : parts*val_symb_loc, "somme_inv_port":parts*val_symb_port, "frais_ac_vt":frais,"val_symb_act_loc":val_symb_loc,"val_symb_act_port":val_symb_port,"somme_act_loc":parts*val_symb_loc,"somme_act_port":parts*val_symb_port,"dividende":0,"frais_div":0}

        else :
            #moyenne ponderee
            port_dict[symbole]["valeur_moy_inv_loc"] = (port_dict[symbole]["parts"]*port_dict[symbole]["valeur_moy_inv_loc"] + parts*val_symb_loc) / (port_dict[symbole]["parts"] + parts)
            port_dict[symbole]["valeur_moy_inv_port"] = (port_dict[symbole]["parts"]*port_dict[symbole]["valeur_moy_inv_port"] + parts*val_symb_port) / (port_dict[symbole]["parts"] + parts)
            port_dict[symbole]["parts"] += parts 
            #on ajoute le nouvel investissement a ce qu'on a deja
            port_dict[symbole]["somme_inv_loc"] += parts*val_symb_loc
            port_dict[symbole]["somme_inv_port"] += parts*val_symb_port
            port_dict[symbole]["frais_ac_vt"] += frais
            #mise en jour du prix
            port_dict[symbole]["val_symb_act_loc"] = val_symb_loc
            port_dict[symbole]["val_symb_act_port"] = val_symb_port
            #mise a jour du prix actuel du portefeuille
            port_dict[symbole]["somme_act_loc"] = port_dict[symbole]["parts"]*val_symb_loc
            port_dict[symbole]["somme_act_port"] = port_dict[symbole]["parts"]*val_symb_port

        # on  enregistre dans le fichier le nouveau port_dict modifier 
        try :
            with open(f"ressources/portefeuilles/{port_name}.json",'w') as port_file: # condition w car on va écraser ancien enregistrement car tout est deja contenue dans port_dict
                json.dump(port_dict,port_file)

        except Exception as e :
            print(f"[Ereur] : {e}")
            return -3

    # si le fichier n'existe pas on le creer et on fait l'enregistrement  
    else :
        port_dict = {symbole : {"date_debut" : date, "parts" : parts, "valeur_moy_inv_loc" : val_symb_loc,"valeur_moy_inv_port":val_symb_port,"somme_inv_loc" : parts*val_symb_loc, "somme_inv_port":parts*val_symb_port, "frais_ac_vt":frais,"val_symb_act_loc":val_symb_loc,"val_symb_act_port":val_symb_port,"somme_act_loc":parts*val_symb_loc,"somme_act_port":parts*val_symb_port,"dividende":0,"frais_div":0}}
        try :
            with open(f"ressources/portefeuilles/{port_name}.json",'w') as port_file:
                json.dump(port_dict,port_file)

        except Exception as e :
            print(f"[Ereur] : {e}")
            return -3
    
    
    return erreur

def write_vente_port(port_name,symbole,date,parts,valeur_loc,taux_conv,valeur_port,frais):
    erreur = 0
    if os.path.exists(f"ressources/portefeuilles/{port_name}.json") :
        try :
            with open(f"ressources/portefeuilles/{port_name}.json",'r') as port_file:
                port_dict = json.load(port_file)


        except Exception as e :
            print(f"[Erreur] : {e}")
            return -2
        
        if port_dict.get(symbole,0) == 0 :
            return -4.1

        elif port_dict[symbole]["parts"] < parts :
            return -4.2

        else :
            port_dict[symbole]["parts"] -= parts
            port_dict[symbole]["somme_inv_loc"] -= valeur_loc
            port_dict[symbole]["somme_inv_port"] -= valeur_port
            port_dict[symbole]["frais_ac_vt"] += frais


        try :
            with open(f"ressources/portefeuilles/{port_name}.json",'w') as port_file:
                json.dump(port_dict,port_file)

        except Exception as e :
            print(f"[Ereur] : {e}")
            return -3

    else :  
        erreur = -6 

    return erreur

def upload_symbole_val_port(port_name,symbole,valeur_act_loc,valeur_act_port):
    erreur = 0
    if os.path.exists(f"ressources/portefeuilles/{port_name}.json") :
        try :
            with open(f"ressources/portefeuilles/{port_name}.json",'r') as port_file :
                port_dict = json.load(port_file)


        except Exception as e :
            print(f"[Erreur] : {e}")
            return -2
        
        if port_dict.get(symbole,0) == 0 :
            return -4.1
        
        else :
            parts = port_dict[symbole]["parts"]
            port_dict[symbole]["val_symb_act_loc"] = valeur_act_loc
            port_dict[symbole]["val_symb_act_port"] = valeur_act_port
            port_dict[symbole]["somme_act_loc"] = parts*valeur_act_loc
            port_dict[symbole]["somme_act_port"] = parts*valeur_act_port

def write_div_port(port_name,symbole,date,valeur,frais,valeur_nette):
    erreur = 0
    if os.path.exists(f"ressources/portefeuilles/{port_name}.json") :
        try :
            with open(f"ressources/portefeuilles/{port_name}.json",'r') as port_file:
                port_dict = json.load(port_file)


        except Exception as e :
            print(f"[Erreur] : {e}")
            return -2
        
        if port_dict.get(symbole,0) == 0 :
            return -5

        else :
            port_dict[symbole]["dividende"] += valeur
            port_dict[symbole]["frais_div"] += frais


        try :
            with open(f"ressources/portefeuilles/{port_name}.json",'w') as port_file:
                json.dump(port_dict,port_file)

        except Exception as e :
            print(f"[Ereur] : {e}")
            return -3 
        
    else :
        erreur = -6

    return erreur

def write_new_symb(symbole,nom,domaine,pays):
    erreur = 0
    symb_info_list = [symbole,nom,domaine,pays]
    try : 
        with open("ressources/symboles_infos.csv",'a') as symb_file :
            writer = csv.writer(symb_file)
            writer.writerow(symb_info_list)

    except Exception as  e :
        print(f"[Erreur] : {e}")
        erreur = -1

    return erreur

def write_prix_symb(symbole,date,prix_cloture_loc):
    erreur = 0
    prix_info = [date,prix_cloture_loc]
    try :
        with open(f"ressources/prix/{symbole}_prix.csv",'a') as symb_prix_file :
            writer = csv.writer(symb_prix_file)
            writer.writerow(prix_info)

    except Exception as e :
        print(f"[Erreur] : {e}")
        erreur = -1

    return erreur

def write_port_history(portefeuille,date,somme_inv_port_loc,somme_inv_port,parts,somme_act_port_loc,somme_act_port,dividendes,frais_div,frais_ac_vt):
    erreur = 0
    port_list_info = [date,parts,somme_inv_port_loc,somme_inv_port,somme_act_port_loc,somme_act_port,dividendes,frais_div,frais_ac_vt]
    try :
        with open(f"ressources/portefeuilles/histoty/{portefeuille}_history.csv",'a') as port_hist_file:
            writer = csv.writer(port_hist_file)
            writer.writerow(port_list_info)

    except Exception as  e :
        print(f"[Erreur] : {e}")
        erreur = -1

    return erreur

def portfeuilles_existant():
    # on récupère le nom de tout les portefeuilles existant
    portefeuilles_name = []

    i = 0
    for root, directories, files in os.walk("ressources/portefeuilles"):  
        if i <=  0 :
            for file in files: # les file sont les fichiers json des portefeuilles à jours
                portefeuilles_name.append(file.split(".")[0])

        i += 1

    return portefeuilles_name

def symboles_portefeuilles(portefeuille):
    liste_symbole = []
    with open(f"ressources/portefeuilles/{portefeuille}.json",'r') as port_file:
        dict_port = json.load(port_file)

    for symb in dict_port.keys():
        liste_symbole.append(symb)

    return liste_symbole
    
if __name__ == "__main__" :
    print(write_achat_titre("STAG.US","10-05-2010",5,45.30,1,45.30,0))
    print(write_achat_port("test","STAG.US","10-05-2010",5,45.30,1,45.30,0))
    print(write_dividend("STAG.US","20-06-2010",0.60,0.1,0.5))
    print(write_div_port("test","STAG.US","20-06-2010",0.6,0.1,0.5))