import yfinance as yf
import csv
import matplotlib.pyplot as plt

class Compte():
    def __init__(self,nom_compte):
        self.nom_compte = nom_compte

    def addTrade(self,symbole,date,time,type_ac,quantity,loc_price,frais,taux_change,valeur):
        with open(f"Trade_adjustement_{self.nom_compte}.csv",'a') as fichier :
            spamwriter = csv.writer(fichier, delimiter=';')
            spamwriter.writerow([symbole,date,time,type_ac,quantity,loc_price,frais,taux_change,round(valeur,2)])

        print("Trade well add to the account")

    def addDividende(self,symbole,date_payment,date_execution,gross_pay_loc,frais,net_pay_loc,net_pay_cpt):
        with open(f"Dividende_{self.nom_compte}.csv",'a') as fichier :
            spamwriter = csv.writer(fichier,delimiter=';')
            spamwriter.writerow([symbole,date_payment,date_execution,gross_pay_loc,frais,net_pay_loc,net_pay_cpt])
            

        print("Dividende well add to the account")
        
    
    def compute_gain(self,symbole):
        possess = []
        with open(f"Trade_adjustement_{self.nom_compte}.csv",'r') as fichier :
            spamreader = csv.reader(fichier,delimiter=";")
            for ligne in spamreader :
                if len(ligne) > 0 :
                    if ligne[0] == f"{symbole}.US" :
                        possess.append((float(ligne[5]),float(ligne[4])))
                    
        dividende = []
        """
        with open(f"Dividende_{self.nom_compte}.csv",'r') as fichier :
            spamreader = csv.reader(fichier,delimiter=";")
            for ligne in spamreader :
                if ligne[0] == symbole :
                    possess.append(ligne[6])"""
                    
        symbole_ticker = yf.Ticker(symbole)
        actual_price = symbole_ticker.fast_info['lastPrice']
        
        ticker_taux_change = yf.Ticker('EUR=X')
        taux_act = ticker_taux_change.fast_info['lastPrice']
        
        nb_part = 0
        capital_gain = 0
        somme = 0
        for ele in possess :
            capital_gain += (actual_price - ele[0])*ele[1]
            nb_part += ele[1]
            somme += ele[0]*ele[1]
            
        dividende_gain = sum(dividende)
        
        currency_gain = ((nb_part*actual_price)/taux_act) - somme
        
        return (capital_gain,dividende_gain,currency_gain,(capital_gain+dividende_gain+currency_gain))
    
    def compute_repart_tot(self):
        dico_actif_parts = {}
        dico_actif_somme = {}
        with open(f"Trade_adjustement_{self.nom_compte}.csv",'r') as fichier :
            spamreader = csv.reader(fichier,delimiter=";")
            for ligne in spamreader :
                if len(ligne) > 0 :
                    actif_parts = dico_actif_parts.get(ligne[0],0)
                    actif_parts += float(ligne[4])
                    actif_somme = dico_actif_somme.get(ligne[0],0)
                    actif_somme += float(ligne[5])
                    dico_actif_parts[ligne[0]] = actif_parts
                    dico_actif_somme[ligne[0]] = actif_somme
                
        
        fig,(ax1,ax2) = plt.subplots(1,2)
        fig.suptitle("Repartition totale")
        ax1.pie(dico_actif_parts.values(),labels=dico_actif_parts.keys(),autopct='%1.1f%%')
        ax1.set_title("Par parts")
        ax2.pie(dico_actif_somme.values(),labels = dico_actif_somme.keys(),autopct='%1.1f%%')
        ax2.set_title("Par somme")
        
        plt.plot()
        
    def compute_repart_country(self):
        dico_pays_part = {}
        dico_pays_somme = {}
        with open(f"Trade_adjustement_{self.nom_compte}.csv",'r') as fichier :
            spamreader = csv.reader(fichier,delimiter=";")
            for ligne in spamreader :
                if len(ligne) > 0 :
                    id_pays = ligne[0].split('.')[1]
                    pays_part = dico_pays_part.get(id_pays,0)
                    pays_part += float(ligne[4])
                    pays_somme = dico_pays_somme.get(id_pays,0)
                    pays_somme += float(ligne[5])
                    dico_pays_part[id_pays] = pays_part
                    dico_pays_somme[id_pays] = pays_somme
                    
        fig,(ax1,ax2) = plt.subplots(1,2)
        fig.suptitle("Repartition par pays")
        ax1.pie(dico_pays_part.values(),labels=dico_pays_part.keys(),autopct='%1.1f%%')
        ax1.set_title("Par parts")
        ax2.pie(dico_pays_somme.values(),labels = dico_pays_somme.keys(),autopct='%1.1f%%')
        ax2.set_title("Par somme")
        
        plt.plot()
    



if __name__ == "__main__" :
    cpt = Compte("xtb1")
    #cpt.addTrade('TUP.UK','03-01-2023','10:10:00','ACHAT',1,12.0,0,1,12.0)
    #print(cpt.compute_gain("AAPL"))
    cpt.compute_repart_tot()
    cpt.compute_repart_country()