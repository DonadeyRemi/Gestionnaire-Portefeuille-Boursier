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
    
def write_achat_port(port_name,symbole,date,parts,valeur_loc,taux_conv,valeur_port,frais):
    erreur = 0
    if os.path.exists(f"ressources/portefeuilles/{port_name}.json") :
        try :
            with open(f"ressources/portefeuilles/{port_name}.json",'r') as port_file:
                port_dict = json.load(port_file)


        except Exception as e :
            print(f"[Erreur] : {e}")
            return -2
        
        if port_dict.get(symbole,0) == 0 :
            port_dict[symbole] = {"date_debut" : date, "parts" : parts, "somme_inv_loc" : valeur_loc, "somme_inv_port":valeur_port, "frais_ac_vt":frais,"dividende":0,"frais_div":0}

        else :
            port_dict[symbole]["parts"] += parts
            port_dict[symbole]["somme_inv_loc"] += valeur_loc
            port_dict[symbole]["somme_inv_port"] += valeur_port
            port_dict[symbole]["frais_ac_vt"] += frais


        try :
            with open(f"ressources/portefeuilles/{port_name}.json",'w') as port_file:
                json.dump(port_dict,port_file)

        except Exception as e :
            print(f"[Ereur] : {e}")
            return -3
        
    else :
        port_dict = {symbole : {"date_debut" : date, "parts" : parts, "somme_inv_loc" : valeur_loc, "somme_inv_port":valeur_port, "frais_ac_vt":frais,"dividende":0,"frais_div":0}}

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
    
if __name__ == "__main__" :
    print(write_achat_titre("STAG.US","10-05-2010",5,45.30,1,45.30,0))
    print(write_achat_port("test","STAG.US","10-05-2010",5,45.30,1,45.30,0))
    print(write_dividend("STAG.US","20-06-2010",0.60,0.1,0.5))
    print(write_div_port("test","STAG.US","20-06-2010",0.6,0.1,0.5))