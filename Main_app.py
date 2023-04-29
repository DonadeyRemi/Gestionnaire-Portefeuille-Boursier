import tkinter as tk
from tkinter import ttk
import creation_figure
import gestion_fichier as gf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import os
import datetime

class MainApp():
    def __init__(self):
        self.root = tk.Tk()
        self.createMenu()

        self.initWidget()

        self.root.mainloop()

    def initWidget(self):
        self.frame_dashboard = tk.Frame(self.root)
        self.frame_label = tk.Frame(self.frame_dashboard)

        self.label_patrimoine = tk.Label(self.frame_label,text="Patrimoine Total")
        self.label_patrimoine.pack(side=tk.TOP,fill=tk.Y,padx=10,pady=10)

        self.label_patrimoine_tot = tk.Label(self.frame_label,text="........")
        self.label_patrimoine_tot.pack(side=tk.TOP,fill=tk.Y,padx=10,pady=5)

        self.frame_label.grid(column=0,row=0)

        #création du plot ici car cela évite de charger les données avant l'ouverture de la fenetre mais une fois qu'elle est ouverte
        self.fig_pie_patrimoine_tot,self.ax_pie_patrimoine_tot = plt.subplots(figsize=(5,5))
        self.ax_pie_patrimoine_tot.pie([30,25,45],labels=["Portefeuille-1","Portefeuille-2","Portefeuille-3"])
        self.ax_pie_patrimoine_tot.set_title("Répartition du patrimoine")
        #plt.legend()

        self.canvas_pie_patrimoine_tot = FigureCanvasTkAgg(self.fig_pie_patrimoine_tot, master=self.frame_dashboard)  # A tk.DrawingArea.
        self.canvas_pie_patrimoine_tot.draw()
        self.canvas_pie_patrimoine_tot.get_tk_widget().grid(column=1,row=0,padx=10,pady=10)

        self.fig_line_patrimoine_hist,self.ax_line_patrimoine_hist = plt.subplots(figsize=(10,5))
        self.ax_line_patrimoine_hist.plot([0,1,2,4,5],[10,9,15,16,17])
        self.ax_line_patrimoine_hist.set_title("Evolution du patrimoine")

        self.canvas_line_patrimoine_hist = FigureCanvasTkAgg(self.fig_line_patrimoine_hist,master=self.frame_dashboard)
        self.canvas_line_patrimoine_hist.draw()
        self.canvas_line_patrimoine_hist.get_tk_widget().grid(column=0,columnspan=2,row=1,padx=10,pady=10)
        self.frame_dashboard.pack()

    def createMenu(self):
        self.Menu = tk.Menu(self.root)

        self.menu_dashboard = tk.Menu(self.Menu,tearoff=0)
        self.menu_dashboard.add_command(label="DashBoard",command=self.event_show_dash)
        self.Menu.add_cascade(label="Acceuil",menu=self.menu_dashboard)

        self.menu_portefeuille = tk.Menu(self.Menu,tearoff=0)
        self.menu_portefeuille.add_command(label="Analyse Portefeuille",command=self.event_ana_port)
        self.menu_portefeuille.add_separator()
        self.menu_portefeuille.add_command(label="Nouveau portefeuille",command=self.event_menu_new_port)
        self.menu_portefeuille.add_command(label="Achat titre",command=self.event_achat_titre)
        self.menu_portefeuille.add_command(label="Vente titre",command=self.event_vente_titre)
        self.menu_portefeuille.add_command(label="Ajouter dividende",command=self.event_dividende)
        self.Menu.add_cascade(label="Portefeuille",menu=self.menu_portefeuille)

        self.menu_symbole = tk.Menu(self.Menu,tearoff=0)
        self.menu_symbole.add_command(label="Ajouter symbole",command=self.event_add_symb)
        self.menu_symbole.add_command(label="Mettre a jour symbole",command=self.event_update_symb_hist)
        self.Menu.add_cascade(label="Symbole",menu=self.menu_symbole)

        self.root.config(menu=self.Menu)

    def event_menu_new_port(self):
        self.frame_new_port = tk.Frame(self.root)

        self.frame_info_nv_port = tk.Frame(self.frame_new_port)
        self.label_nom_nv_port = tk.Label(self.frame_info_nv_port, text="Nom du  portefeuille")
        self.label_nom_nv_port.grid(row=0,column=0,padx=5,pady=5)
        self.label_devise_port = tk.Label(self.frame_info_nv_port,text="Devise du portefeuille")
        self.label_devise_port.grid(row=0,column=1,padx=5,pady=5)
        self.var_nom_port = tk.StringVar(value="Portefeuille-1")
        self.entry_nom_nv_port = tk.Entry(self.frame_info_nv_port,textvariable=self.var_nom_port)
        self.entry_nom_nv_port.grid(row=1,column=0,padx=5,pady=5)
        self.entry_nom_nv_port.bind("<Button-1>",self.effacer_nom)
        self.entry_nom_nv_port.bind("<Return>",self.valid_nom_nv_port)

        liste_devise = ["EUR","USD","GBP"]
        self.devise_port = "EUR"
        self.combobox_devise = ttk.Combobox(self.frame_info_nv_port,values=liste_devise)
        self.combobox_devise.grid(row=1,column=1,padx=5,pady=5)
        self.combobox_devise.current(0)
        self.combobox_devise.bind("<<ComboboxSelected>>", self.select_devise)
        self.frame_info_nv_port.pack(side=tk.TOP,fill=tk.X)

        self.frame_list_view_symb = tk.Frame(self.frame_new_port)
        self.label_name_listview = tk.Label(self.frame_list_view_symb,text=f"Symboles présent dans le {self.var_nom_port.get()}")
        self.label_name_listview.pack(side=tk.TOP,fill=tk.X,padx=10,pady=10)

        self.listview_symb = tk.Listbox(self.frame_list_view_symb)
        self.listview_symb.pack(side=tk.TOP,fill=tk.X,padx=10,pady=5)
        self.frame_list_view_symb.pack(side=tk.RIGHT,fill=tk.Y)

        frame_achat_titre = self.create_frame_achat_titre(self.frame_new_port)
        frame_achat_titre.pack(side=tk.LEFT,fill=tk.X)

        #on cache le dashboard
        self.frame_dashboard.pack_forget()
        self.frame_new_port.pack()

    def effacer_nom(self,event):
        print(event)

    def select_devise(self,event):
        self.devise_port = self.combobox_devise.get()
        print(f"Vous avez selectionner comme devise {self.devise_port}")

    def valid_nom_nv_port(self,event):
        self.var_nom_port.set(self.entry_nom_nv_port.get())
        self.label_name_listview.config(text=f"Symboles présent dans le {self.var_nom_port.get()}")

    def create_frame_achat_titre(self,root):
        frame_achat_titre = tk.Frame(self.root)

        self.frame_symb_info = tk.Frame(frame_achat_titre)
        self.label_symbole = tk.Label(self.frame_symb_info,text="Symbole")
        self.label_symbole.grid(row=0,column=0,padx=10,pady=10)

        self.var_symb = tk.StringVar()
        self.entry_symb = tk.Entry(self.frame_symb_info,textvariable=self.var_symb)
        self.entry_symb.grid(row=1,column=0,padx=10,pady=10)
        self.entry_symb.bind("<Return>",self.search_symb)

        self.open_frame_max_info = False
        self.frame_symb_info_max = tk.Frame(self.frame_symb_info)
        self.label_nom_complet = tk.Label(self.frame_symb_info_max,text="Nom complet")
        self.label_nom_complet.grid(row=0,column=0,padx=5,pady=5)
        self.label_domaine = tk.Label(self.frame_symb_info_max,text="Domaine")
        self.label_domaine.grid(row=1,column=0,padx=5,pady=5)
        self.label_pays = tk.Label(self.frame_symb_info_max,text="Pays")
        self.label_pays.grid(row=2,column=0,padx=5,pady=5)
        self.var_nom_complet = tk.StringVar()
        self.entry_nom_complet = tk.Entry(self.frame_symb_info_max,textvariable=self.var_nom_complet)
        self.entry_nom_complet.grid(row=0,column=1,padx=5,pady=5)
        self.var_domaine = tk.StringVar()
        self.entry_domaine = tk.Entry(self.frame_symb_info_max,textvariable=self.var_domaine)
        self.entry_domaine.grid(row=1,column=1,padx=5,pady=5)
        self.var_pays = tk.StringVar()
        self.entry_pays = tk.Entry(self.frame_symb_info_max,textvariable=self.var_pays)
        self.entry_pays.grid(row=2,column=1,padx=5,pady=5)
        #self.frame_symb_info_max.grid(row=0,column=1,columnspan=2) on ne place pas encore ce frame on attend de voir si le symbole est déja dans le fichier

        self.frame_symb_info.pack(side=tk.TOP,fill=tk.X)
        separateur_1 = ttk.Separator(frame_achat_titre,orient=tk.HORIZONTAL)
        separateur_1.pack(side=tk.TOP,fill=tk.X)

        self.frame_achat_info = tk.Frame(frame_achat_titre)
        self.label_parts = tk.Label(self.frame_achat_info,text="Parts")
        self.label_parts.grid(row=0,column=0,padx=5,pady=5)
        self.var_parts = tk.StringVar()
        self.entry_parts = tk.Entry(self.frame_achat_info,textvariable=self.var_parts)
        self.entry_parts.grid(row=0,column=1,padx=5,pady=5)

        self.label_val_loc = tk.Label(self.frame_achat_info,text="Valeur symbole locale")
        self.label_val_loc.grid(row=1,column=0,columnspan=2,padx=5,pady=5)
        self.var_val_loc = tk.StringVar()
        self.entry_val_loc = tk.Entry(self.frame_achat_info,textvariable=self.var_val_loc)
        self.entry_val_loc.grid(row=1,column=2,padx=5,pady=5)
        self.entry_val_loc.bind("<Return>",self.enter_val_loc)

        self.label_val_port = tk.Label(self.frame_achat_info,text="Valeur symbole portefeuille")
        self.label_val_port.grid(row=2,column=0,columnspan=2,padx=5,pady=5)
        self.var_val_port = tk.StringVar()
        self.entry_val_port = tk.Entry(self.frame_achat_info,textvariable=self.var_val_port)
        self.entry_val_port.grid(row=2,column=2,padx=5,pady=5)
        self.entry_val_port.bind("<Return>",self.enter_val_port)

        self.label_frais_achat = tk.Label(self.frame_achat_info,text="Frais achat")
        self.label_frais_achat.grid(row=3,column=0,padx=5,pady=5)
        self.var_frais = tk.StringVar()
        self.entry_frais = tk.Entry(self.frame_achat_info,textvariable=self.var_frais)
        self.entry_frais.grid(row=3,column=1,padx=5,pady=5)

        self.label_taux_conv = tk.Label(self.frame_achat_info,text="Taux de conversion (port/loc)")
        self.label_taux_conv.grid(row=0,column=2,columnspan=2,padx=5,pady=5)
        self.var_taux_conv = tk.StringVar()
        self.entry_taux_conv = tk.Entry(self.frame_achat_info,textvariable=self.var_taux_conv)
        self.entry_taux_conv.grid(row=0,column=4,padx=5,pady=5)

        self.label_somme_loc = tk.Label(self.frame_achat_info,text="Somme investissement (loc): ...")
        self.label_somme_loc.grid(row=1,column=3,columnspan=2,padx=5,pady=5)

        self.label_somme_port = tk.Label(self.frame_achat_info,text="Somme investissement (port): ....")
        self.label_somme_port.grid(row=2,column=3,columnspan=2,padx=5,pady=5)

        self.button_validate_info_symb = tk.Button(self.frame_achat_info,text="Valider")
        self.button_validate_info_symb.grid(row=3,column=4,padx=5,pady=5)
        self.button_validate_info_symb.bind("<Button-1>",self.valid_info_symb)

        self.frame_achat_info.pack(side=tk.TOP,fill=tk.X)

        return frame_achat_titre

    def valid_info_symb(self,event):
        nom_portfeuille = self.var_nom_port.get()
        devise_port = self.combobox_devise.get() #pas encore utilisee est enregistree mais voir pour rajouter
        symbole_name = self.var_symb.get()
        
        parts = 0
        try :
            parts = float(self.var_parts.get())
        except Exception as e :
            print(f"[Erreur] : {e}")
        
        frais_achat = 0
        try :
            frais_achat = float(self.var_frais.get())
        except Exception as e :
            print(f"[Erreur] : {e}")
        
        val_symb_loc = 0
        try :
            val_symb_loc = float(self.var_val_loc.get())
        except Exception as e :
            print(f"[Erreur] : {e}")

        val_symb_port = 0
        try :
            val_symb_port = float(self.var_val_port.get())
        except Exception as e:
            print(f"[Erreur] : {e}")

        somme_symb_loc = parts*val_symb_loc
        somme_symb_port = parts*val_symb_port

        # mise a jour des infos sur le symbole
        if self.open_frame_max_info :
            nom_complet = self.var_nom_complet.get()
            domaine = self.var_domaine.get()
            pays = self.var_pays.get()
            liste_info_symb = [symbole_name,nom_complet,domaine,pays]
            with open("ressources/symboles_infos.csv",'a') as symb_info_file :
                writer = csv.writer(symb_info_file)
                writer.writerow(liste_info_symb)

        er = gf.write_achat_port(nom_portfeuille,symbole_name,str(datetime.date.today()),parts,val_symb_loc,val_symb_port,frais_achat)
        if er == 0 :
            self.listview_symb.insert('end',symbole_name)

            #l'enregistrement a fonctionne on remet balnc les champs
            self.var_symb.set("")
            self.var_nom_complet.set("")
            self.var_domaine.set("")
            self.var_pays.set("")
            self.var_parts.set("")
            self.var_taux_conv.set("")
            self.var_val_loc.set("")
            self.var_val_port.set("")
            self.var_frais.set("")
            self.label_somme_loc.config(text="Somme investissement (loc): ...")
            self.label_somme_port.config(text="Somme investissement (port): ....")

        else :
            print("Il y a eu une erreur dans l'enregistrement du portefeuille")
            print(f"[Erreur] : {er}")

    def search_symb(self,event):
        symbole_name = self.var_symb.get()
        exist = False
        if os.path.exists("ressources/symboles_infos.csv") :
            with open("ressources/symboles_infos.csv",'r') as symb_file :
                for line in csv.reader(symb_file) :
                    if len(line) > 3 :
                        if line[0] == symbole_name :
                            exist = True
                            self.frame_symb_info_max.grid_forget()
                            self.open_frame_max_info = False

        if exist == False:
            self.frame_symb_info_max.grid(row=0,column=1,columnspan=2)
            self.open_frame_max_info = True

    def enter_val_loc(self,event):
        taux_conv = 0
        try : 
            taux_conv = float(self.var_taux_conv.get())
        except Exception as e:
            print(f"[Erreur] : {e}")
        
        val_symb_loc = 0
        try : 
            val_symb_loc = float(self.var_val_loc.get())

        except Exception as e:
            print(f"[Erreur] : {e}")

        parts = 0
        try :
            parts = float(self.var_parts.get())

        except Exception as e :
            print(f"[Erreur] : {e}")

        self.label_somme_loc.config(text=f"Somme investissement (loc):{parts*val_symb_loc}")
        self.var_val_port.set(f"{round(val_symb_loc/taux_conv,2)}")
        self.label_somme_port.config(text=f"Somme investissement (port):{round(val_symb_loc/taux_conv,2)*parts}")

    def enter_val_port(self,event):
        val_symb_port = 0
        try :
            val_symb_port = float(self.var_val_port.get())

        except Exception as e:
            print(f"[Erreur] : {e}")

        parts = 0
        try :
            parts = float(self.var_parts.get())

        except Exception as e:
            print(f"[Erreur] : {e}")

        self.label_somme_port.config(text=f"Somme investissement (port):{val_symb_port*parts}")

    def event_ana_port(self):
        #fonction evenement pour l'analyse d'un portefeuille
        pass

    def event_achat_titre(self):
        #callback pour l'achat d'un titre dans un portefeuille deja creer, utiliser le frame deja construit de l'achat 
        pass

    def event_vente_titre(self):
        #callback menu vente titre portefeuille deja connu , creer nouveau frame adapter de celui de la vente
        pass

    def event_dividende(self):
        #callback menu pour ajouter un dividende sur un titre toujours dans au moins un portfeuille
        pass

    def event_add_symb(self):
        #callback menu pour ajouter un nouveau symbole dans le fichier info symbole ainsi que dans le fichier history correspondant
        pass

    def event_update_symb_hist(self):
        #callback menu pour ajouter une ligne sur l'historique d'un symbole deja enregsitrer dans un fichier
        pass

    def event_show_dash(self):
        self.frame_new_port.pack_forget()
        self.frame_dashboard.pack()

        




if __name__ == "__main__" :
    mainwindow = MainApp()
