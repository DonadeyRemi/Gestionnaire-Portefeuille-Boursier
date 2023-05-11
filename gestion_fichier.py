import csv
import json
import os
import datetime

def write_achat_titre(symbole,date,parts,valeur_loc,taux_conv,valeur_port,frais):
    erreur = 0
    achat = [symbole,date,parts,valeur_loc,taux_conv,valeur_port,frais,"ACHAT"]
    try : 
        with open("ressources/achat_vente.csv",'a',newline='') as ac_vt_file :
            writer_obj = csv.writer(ac_vt_file)
            writer_obj.writerow(achat)

    except Exception as e :
        print(f"[Erreur] : {e}")
        erreur =  -1
    
    return erreur
        
    
def write_vente_titre(symbole,date,parts,valeur_loc,taux_conv,valeur_port,frais) :
    vente = [symbole,date,parts,valeur_loc,taux_conv,valeur_port,frais,"VENTE"]

    try : 
        with open("ressources/achat_vente.csv",'a',newline='') as ac_vt_file :
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
        with open("ressources/dividendes.csv",'a',newline='') as div_file :
            writer_obj = csv.writer(div_file)
            writer_obj.writerow(dividende)
    except Exception as e :
        print(f"[Erreur] : {e}")
        
    
    write_div_port(symbole,date,valeur,frais)
    
def write_achat_port(port_name,symbole,devise_port,taux_conv_achat,date,parts,val_symb_loc,val_symb_port,frais):
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
        
        #ajout d'une nouvelle ligne dans la fichier port history

        # si le fichier n'existe pas on le creer et on fait l'enregistrement 
        #port_list_info = [date,heure,parts,somme_inv_loc,somme_inv_port,somme_act_loc,somme_act_port,frais_ac_vt,dividendes,frais_div]
        parts_tot = 0
        somme_inv_loc_tot = 0
        somme_inv_port_tot = 0
        somme_act_loc_tot = 0
        somme_act_port_tot = 0
        frais_ac_vt_tot = 0
        dividendes_tot = 0
        frais_div_tot = 0
        for symb in port_dict.keys():
            parts_tot += port_dict[symb]["parts"]
            somme_inv_loc_tot += port_dict[symb]["somme_inv_loc"]
            somme_inv_port_tot += port_dict[symb]["somme_inv_port"]
            somme_act_loc_tot += port_dict[symb]["somme_act_loc"]
            somme_act_port_tot += port_dict[symb]["somme_act_port"]
            frais_ac_vt_tot += port_dict[symb]["frais_ac_vt"]
            dividendes_tot += port_dict[symb]["dividende"]
            frais_div_tot += port_dict[symb]["frais_div"]

        port_list_info = [date,datetime.datetime.now().time(),parts_tot,somme_inv_loc_tot,somme_inv_port_tot,somme_act_loc_tot,somme_act_port_tot,frais_ac_vt_tot,dividendes_tot,frais_div_tot]
    else :
        port_dict = {symbole : {"date_debut" : date, "parts" : parts, "valeur_moy_inv_loc" : val_symb_loc,"valeur_moy_inv_port":val_symb_port,"somme_inv_loc" : parts*val_symb_loc, "somme_inv_port":parts*val_symb_port, "frais_ac_vt":frais,"val_symb_act_loc":val_symb_loc,"val_symb_act_port":val_symb_port,"somme_act_loc":parts*val_symb_loc,"somme_act_port":parts*val_symb_port,"dividende":0,"frais_div":0}}
        try :
            with open(f"ressources/portefeuilles/{port_name}.json",'w') as port_file:
                json.dump(port_dict,port_file)

        except Exception as e :
            print(f"[Ereur] : {e}")
            return -3
        
        port_list_info = [date,datetime.datetime.now().time(),parts,parts*val_symb_loc,parts*val_symb_port,parts*val_symb_loc,parts*val_symb_port,frais,0,0]
    
    try :
        with open(f"ressources/portefeuilles/history/{port_name}_history.csv",'a',newline='') as port_hist_file:
            writer = csv.writer(port_hist_file)
            writer.writerow(port_list_info)

    except Exception as  e :
        print(f"[Erreur] : {e}")

    add_line_patrimoine_hist()

    #mise a jour du prix de la devise
    devise_symb = "EUR"
    try : 
        with open(f"ressources/symboles_infos.csv",'r',newline='') as file_symb :
            for row in csv.reader(file_symb) :
                if row[0] == symbole :
                    devise_symb = row[3]

    except Exception as e:
        print(f"[Erreur] : {e}")

    try :
        with open(f"ressources/prix/{devise_port}_{devise_symb}.csv",'a',newline='') as devise_hist_file :
            writer = csv.writer(devise_hist_file)
            writer.writerow([date,datetime.datetime.now().time(),taux_conv_achat])

    except Exception as e :
        print(f"[Erreur] : {e}")

    
    

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
            # avant on met à jour les prix avec la valeur du symbole renseigné
            upload_symbole_val_port(port_name,symbole,valeur_loc,valeur_port)
            # on enlève les parts vendu et rajoute les frais
            port_dict[symbole]["parts"] -= parts
            port_dict[symbole]["frais_ac_vt"] += frais
            # on enlève les parts vendu au 
            port_dict[symbole]["somme_act_loc"] -= parts*valeur_loc
            port_dict[symbole]["somme_act_port"] -= parts*valeur_port
            port_dict[symbole]["somme_inv_loc"] -= port_dict[symbole]["valeur_moy_inv_loc"]*parts
            port_dict[symbole]["somme_inv_port"] -= port_dict[symbole]["valeur_moy_inv_port"]*parts
            


        try :
            with open(f"ressources/portefeuilles/{port_name}.json",'w') as port_file:
                json.dump(port_dict,port_file)

        except Exception as e :
            print(f"[Ereur] : {e}")
            return -3
        
        #on ajoute une ligne de mise a jour dans le fichier historique du portefeuille
        #port_list_info = [date,heure,parts,somme_inv_loc,somme_inv_port,somme_act_loc,somme_act_port,frais_ac_vt,dividendes,frais_div]
        parts_tot = 0
        somme_inv_loc_tot = 0
        somme_inv_port_tot = 0
        somme_act_loc_tot = 0
        somme_act_port_tot = 0
        frais_ac_vt_tot = 0
        dividendes_tot = 0
        frais_div_tot = 0
        for symb in port_dict.keys():
            parts_tot += port_dict[symb]["parts"]
            somme_inv_loc_tot += port_dict[symb]["somme_inv_loc"]
            somme_inv_port_tot += port_dict[symb]["somme_inv_port"]
            somme_act_loc_tot += port_dict[symb]["somme_act_loc"]
            somme_act_port_tot += port_dict[symb]["somme_act_port"]
            frais_ac_vt_tot += port_dict[symb]["frais_ac_vt"]
            dividendes_tot += port_dict[symb]["dividende"]
            frais_div_tot += port_dict[symb]["frais_div"]
        port_list_info = [date,datetime.datetime.now().time(),parts_tot,somme_inv_loc_tot,somme_inv_port_tot,somme_act_loc_tot,somme_act_port_tot,frais_ac_vt_tot,dividendes_tot,frais_div_tot]

        #on enregistre dans le fichier cette nouvelle ligne
        try :
            with open(f"ressources/portefeuilles/history/{port_name}_history.csv",'a',newline='') as port_hist_file:
                writer = csv.writer(port_hist_file)
                writer.writerow(port_list_info)

        except Exception as  e :
            print(f"[Erreur] : {e}")

    else :  
        erreur = -6

    add_line_patrimoine_hist()

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

        try :
            with open(f"ressources/portefeuilles/{port_name}.json",'w') as port_file:
                json.dump(port_dict,port_file)

        except Exception as e :
            print(f"[Erreur] : {e}")

    return erreur

def write_div_port(symbole,date,valeur,frais):
    data = None
    list_port = portfeuilles_existant()
    for port_name in list_port :
        if symbole in symboles_portefeuilles(port_name) :
            try : 
                with open(f"ressources/portefeuilles/{port_name}.json",'r') as port_file :
                    data = json.load(port_file)
            except Exception as e :
                print(f"[Erreur] : {e}")

            if data != None :
                data[symbole]["dividende"] += valeur
                data[symbole]["frais_div"] += frais
            
            try :
                with open(f"ressources/portefeuilles/{port_name}.json",'w') as port_file :
                    json.dump(data,port_file)
            except Exception as e :
                print(f"[Erreur] : {e}")

            if data != None : 
                parts_tot = 0
                somme_inv_loc_tot = 0
                somme_inv_port_tot = 0
                somme_act_loc_tot = 0
                somme_act_port_tot = 0
                frais_ac_vt_tot = 0
                dividendes_tot = 0
                frais_div_tot = 0
                for symb in data.keys():
                    parts_tot += data[symb]["parts"]
                    somme_inv_loc_tot += data[symb]["somme_inv_loc"]
                    somme_inv_port_tot += data[symb]["somme_inv_port"]
                    somme_act_loc_tot += data[symb]["somme_act_loc"]
                    somme_act_port_tot += data[symb]["somme_act_port"]
                    frais_ac_vt_tot += data[symb]["frais_ac_vt"]
                    dividendes_tot += data[symb]["dividende"]
                    frais_div_tot += data[symb]["frais_div"]
                port_list_info = [date,datetime.datetime.now().time(),parts_tot,somme_inv_loc_tot,somme_inv_port_tot,somme_act_loc_tot,somme_act_port_tot,frais_ac_vt_tot,dividendes_tot,frais_div_tot]
                try : 
                    with open(f"ressources/portefeuilles/history/{port_name}_history.csv",'a',newline='') as port_hist_file :
                        writer = csv.writer(port_hist_file)
                        writer.writerow(port_list_info)

                except Exception as e :
                    print(f"[Erreur] : {e}")

def write_new_symb(symbole,nom,domaine,pays):
    erreur = 0
    symb_info_list = [symbole,nom,domaine,pays]
    try : 
        with open("ressources/symboles_infos.csv",'a',newline='') as symb_file :
            writer = csv.writer(symb_file)
            writer.writerow(symb_info_list)

    except Exception as  e :
        print(f"[Erreur] : {e}")
        erreur = -1

    return erreur

def write_prix_symb(symbole,date,heure,prix_cloture_loc,taux_conv):
    erreur = 0
    prix_info = [date,heure,prix_cloture_loc]
    try :
        with open(f"ressources/prix/{symbole}_prix.csv",'a',newline='') as symb_prix_file :
            writer = csv.writer(symb_prix_file)
            writer.writerow(prix_info)

    except Exception as e :
        print(f"[Erreur] : {e}")
        erreur = -1

    #on met a jour le prix dans les portefeuilles
    port_list = portfeuilles_existant()
    for port_name in port_list :
        if symbole in symboles_portefeuilles(port_name):
            upload_symbole_val_port(port_name,symbole,prix_cloture_loc,prix_cloture_loc/taux_conv)
    
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

def add_line_patrimoine_hist():
    #port_list_info = [date,heure,parts,somme_inv_loc,somme_inv_port,somme_act_loc,somme_act_port,frais_ac_vt,dividendes,frais_div]
    parts_pat = 0
    somme_inv_loc_pat = 0
    somme_inv_port_pat = 0
    somme_act_loc_pat = 0
    somme_act_port_pat = 0
    frais_ac_vt_pat = 0
    dividendes_pat = 0
    frais_div_pat = 0 
    i = 0
    for root, directories, files in os.walk("ressources/portefeuilles/history"):  
        if i <=  0 :
            for file in files: # les file sont les fichiers json des portefeuilles à jours
                if file != "patrimoine_hist.csv":
                    with open(f"ressources/portefeuilles/history/{file}",'r',newline='') as file_hist_port :
                        last_line = None
                        for row in csv.reader(file_hist_port) :
                            last_line = row

                        parts_pat += float(last_line[2])
                        somme_inv_loc_pat += float(last_line[3])
                        somme_inv_port_pat += float(last_line[4])
                        somme_act_loc_pat += float(last_line[5])
                        somme_act_port_pat += float(last_line[6])
                        frais_ac_vt_pat += float(last_line[7])
                        dividendes_pat += float(last_line[8])
                        frais_div_pat += float(last_line[9])

        i += 1

    with open(f"ressources/portefeuilles/history/patrimoine_hist.csv",'a',newline='') as pat_hist_file :
        writer = csv.writer(pat_hist_file)
        writer.writerow([datetime.date.today(),datetime.datetime.now().time(),parts_pat,somme_inv_loc_pat,somme_inv_port_pat,somme_act_loc_pat,somme_act_port_pat,frais_ac_vt_pat,dividendes_pat,frais_div_pat])
    
if __name__ == "__main__" :
    print(write_achat_titre("STAG.US","10-05-2010",5,45.30,1,45.30,0))
    print(write_achat_port("test","STAG.US","10-05-2010",5,45.30,1,45.30,0))
    print(write_dividend("STAG.US","20-06-2010",0.60,0.1,0.5))
    print(write_div_port("test","STAG.US","20-06-2010",0.6,0.1,0.5))