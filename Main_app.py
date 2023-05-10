import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import creation_figure
import gestion_fichier as gf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import json
import os
import datetime
import time

class MainApp():
    def __init__(self):
        self.root = tk.Tk()
        self.createMenu()
        self.date_choose = None

        self.initWidget()

        self.root.mainloop()

    def initWidget(self):
        self.create_frame_dashboard()
        self.event_show_dash()

    def event_update_dashboard(self,event):
        #apport des figures
        self.fig_pie_tot,self.ax_pie_tot,self.patrimoine_tot = creation_figure.figures_patrimoine_tot(self.combobox_args.get())
        self.label_patrimoine_tot.config(text=f"{self.combobox_args.get()} : {round(self.patrimoine_tot,2)}") # mise a jour 

        self.canvas_pie_patrimoine_tot = FigureCanvasTkAgg(self.fig_pie_tot, master=self.frame_dashboard)  # A tk.DrawingArea.
        self.canvas_pie_patrimoine_tot.draw()
        self.canvas_pie_patrimoine_tot.get_tk_widget().grid(column=1,row=0,padx=10,pady=10)

        self.fig_line_patrimoine_hist,self.ax_line_patrimoine_hist = plt.subplots(figsize=(10,5))
        self.ax_line_patrimoine_hist.plot([0,1,2,4,5],[10,9,15,16,17])
        self.ax_line_patrimoine_hist.set_title("Evolution du patrimoine")

        self.canvas_line_patrimoine_hist = FigureCanvasTkAgg(self.fig_line_patrimoine_hist,master=self.frame_dashboard)
        self.canvas_line_patrimoine_hist.draw()
        self.canvas_line_patrimoine_hist.get_tk_widget().grid(column=0,columnspan=2,row=1,padx=10,pady=10)

    def create_frame_dashboard(self,init=True):
        self.frame_dashboard = tk.Frame(self.root)
        self.frame_label = tk.Frame(self.frame_dashboard)

        self.label_patrimoine = tk.Label(self.frame_label,text="Patrimoine Total")
        self.label_patrimoine.pack(side=tk.TOP,fill=tk.Y,padx=10,pady=10)

        list_args_show = ["parts","somme_inv_loc","somme_inv_port","somme_act_loc","somme_act_port"]
        self.combobox_args = ttk.Combobox(self.frame_label,values=list_args_show)
        
        self.combobox_args.current(4)
        self.combobox_args.pack(side=tk.TOP,fill=tk.Y,padx=10,pady=5)
        self.combobox_args.bind("<<ComboboxSelected>>",self.event_update_dashboard)

        self.label_patrimoine_tot = tk.Label(self.frame_label,text="........")
        self.label_patrimoine_tot.pack(side=tk.TOP,fill=tk.Y,padx=10,pady=5)

        self.frame_label.grid(column=0,row=0)

        #apport des figures
        self.fig_pie_tot,self.ax_pie_tot,self.patrimoine_tot = creation_figure.figures_patrimoine_tot(self.combobox_args.get())
        self.label_patrimoine_tot.config(text=f"{self.combobox_args.get()} : {round(self.patrimoine_tot,2)}") # mise a jour 

        self.canvas_pie_patrimoine_tot = FigureCanvasTkAgg(self.fig_pie_tot, master=self.frame_dashboard)  # A tk.DrawingArea.
        self.canvas_pie_patrimoine_tot.draw()
        self.canvas_pie_patrimoine_tot.get_tk_widget().grid(column=1,row=0,padx=10,pady=10)

        self.fig_line_patrimoine_hist,self.ax_line_patrimoine_hist = plt.subplots(figsize=(10,5))
        self.ax_line_patrimoine_hist.plot([0,1,2,4,5],[10,9,15,16,17])
        self.ax_line_patrimoine_hist.set_title("Evolution du patrimoine")

        self.canvas_line_patrimoine_hist = FigureCanvasTkAgg(self.fig_line_patrimoine_hist,master=self.frame_dashboard)
        self.canvas_line_patrimoine_hist.draw()
        self.canvas_line_patrimoine_hist.get_tk_widget().grid(column=0,columnspan=2,row=1,padx=10,pady=10)

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

    def create_frame_new_port(self):
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

        self.frame_achat_titre = self.create_frame_achat_titre(self.frame_new_port)
        self.frame_achat_titre.pack(side=tk.LEFT,fill=tk.X)
        self.frame_new_port.pack()


    def event_menu_new_port(self):
        self.frame_dashboard.pack_forget()
        try : 
            self.frame_achat_port.destroy()
            self.frame_achat_titre_port.destroy()
        
        except Exception as e:
            print(f"[Erreur] : {e}")
            print("le frame achat titre n'existe pas")

        try :
            self.frame_vente_port.destroy()

        except Exception as e:
            print(f"[Erreur] : {e}")
            print("le frame vente titre n'existe pas")
        
        self.create_frame_new_port()
        

    def effacer_nom(self,event):
        self.var_nom_port.set("")

    def select_devise(self,event):
        self.devise_port = self.combobox_devise.get()
        print(f"Vous avez selectionner comme devise {self.devise_port}")

    def valid_nom_nv_port(self,event):
        self.var_nom_port.set(self.entry_nom_nv_port.get())
        self.label_name_listview.config(text=f"Symboles présent dans le {self.var_nom_port.get()}")
        self.listview_symb.delete(0,'end')

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

        self.button_date_chooser = tk.Button(self.frame_achat_info,text="Choisir une date")
        self.button_date_chooser.grid(row=3,column=2,padx=5,pady=5)
        self.button_date_chooser.bind("<Button-1>",self.date_chooser_event)
        
        
        self.frame_achat_info.pack(side=tk.TOP,fill=tk.X)

        return frame_achat_titre

    def valid_info_symb(self,event):
        if self.date_choose == None : 
            self.date_choose = datetime.date.today()
        nom_portfeuille =  None
        try :
            nom_portfeuille = self.var_nom_port.get()

        except Exception as e :
            print(f"[Erreur] : {e}")
            print("ce n'est pas le portefeuille dans un entry")

        try :
            nom_portfeuille = self.combobox_port.get()
        except Exception as e:
            print(f"[Erreur] : {e}")
            print("ce n'est pas le nom du portefeuille dans la combobox")
        
        #devise_port = self.combobox_devise.get() #pas encore utilisee est enregistree mais voir pour rajouter
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

        taux_conv_achat = 1
        try : 
            taux_conv_achat = float(self.var_taux_conv.get())
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

        er = gf.write_achat_port(nom_portfeuille,symbole_name,str(self.date_choose),parts,val_symb_loc,val_symb_port,frais_achat)
        gf.write_achat_titre(symbole_name,str(self.date_choose),parts,val_symb_loc,taux_conv_achat,val_symb_port,frais_achat)
        gf.write_prix_symb(symbole_name,str(self.date_choose),datetime.datetime.now().time(),val_symb_loc)
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

    def date_chooser_event(self,event):
        self.dialog_date = tk.Toplevel(self.root)
        self.cal = Calendar(self.dialog_date)
        self.cal.pack(side=tk.TOP)
        button_annuler = tk.Button(self.dialog_date,text="Annuler")
        button_annuler.bind("<Button-1>",self.annuler_date_chooser_event)
        button_annuler.pack(side=tk.LEFT)
        button_validate = tk.Button(self.dialog_date,text="Valider date")
        button_validate.bind("<Button-1>",self.validate_date_chooser_event)
        button_validate.pack(side=tk.RIGHT)

    def annuler_date_chooser_event(self,event):
        self.dialog_date.destroy()

    def validate_date_chooser_event(self,event):
        self.date_choose = self.cal.selection_get()
        self.button_date_chooser.config(text=f"{self.date_choose}")
        self.dialog_date.destroy()
    
    def enter_val_loc(self,event):
        print("vous avez valider le prix loc du titre")
        taux_conv = 1
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

    def create_frame_achat_port(self):
        self.frame_achat_port = tk.Frame(self.root)

        self.frame_info_port = tk.Frame(self.frame_achat_port)
        self.label_nom_port = tk.Label(self.frame_info_port, text="Nom du  portefeuille")
        self.label_nom_port.grid(row=0,column=0,padx=5,pady=5)
        
        # on récupère le nom de tout les portefeuilles existant
        portefeuilles_name = gf.portfeuilles_existant()

        self.combobox_port = ttk.Combobox(self.frame_info_port,values=portefeuilles_name)
        self.combobox_port.grid(row=1,column=0,padx=5,pady=5)
        self.combobox_port.current(0)
        self.combobox_port.bind("<<ComboboxSelected>>", self.select_port)
        self.frame_info_port.pack(side=tk.TOP,fill=tk.X)

        self.frame_list_view_symb_port = tk.Frame(self.frame_achat_port)
        self.label_name_listview_port = tk.Label(self.frame_list_view_symb_port,text=f"Symboles présent dans le {self.combobox_port.get()}")
        self.label_name_listview_port.pack(side=tk.TOP,fill=tk.X,padx=10,pady=10)

        self.listview_symb = tk.Listbox(self.frame_list_view_symb_port)
        self.listview_symb.pack(side=tk.TOP,fill=tk.X,padx=10,pady=5)
        self.frame_list_view_symb_port.pack(side=tk.RIGHT,fill=tk.Y)

        self.frame_achat_titre_port = self.create_frame_achat_titre(self.frame_achat_port)
        self.frame_achat_titre_port.pack(side=tk.LEFT,fill=tk.X)

        self.frame_achat_port.pack()


    def event_achat_titre(self):
        self.frame_dashboard.pack_forget()
        try : 
            self.frame_new_port.destroy()
            self.frame_achat_titre.destroy()
        except Exception as e:
            print(f"[Erreur] : {e}")
            print("le frame nv port existe pas")
        
        try : 
            self.frame_achat_port.destroy()
            self.frame_achat_titre_port.destroy()

        except Exception as e:
            print(f"[Erreur] : {e}")
            print("le frame achat titre existe pas")

        try :
            self.frame_vente_port.destroy()

        except Exception as e:
            print(f"[Erreur] : {e}")
            print("le frame vente titre existe pas")

        self.create_frame_achat_port()

    def select_port(self,event):
        #on efface la list view
        self.listview_symb.delete(0,'end')
        
        portefeuille_name = self.combobox_port.get()
        self.label_name_listview_port.config(text=f"Symboles présent dans le {self.combobox_port.get()}")

        #mise a jour des symboles dans le portfeuille
        with open(f"ressources/portefeuilles/{portefeuille_name}.json",'r') as port_file:
            dict_port = json.load(port_file)

        for symb in dict_port.keys():
            self.listview_symb.insert('end',symb)
    
    def select_port_vente(self,event):
        print("vous avez selectionner un portefuille")
        portefeuille_name = self.combobox_port_vente.get()
        liste_symbole = gf.symboles_portefeuilles(portefeuille_name)
        print(liste_symbole)
        self.combobox_symbole_vente.config(values=liste_symbole)
        self.combobox_symbole_vente.current(0)

    def valid_vente(self,event):
        self.date_choose = datetime.date.today()
        parts_vente = 0
        try :
            parts_vente = float(self.var_parts_vente.get())

        except Exception as e :
            print(f"[Erreur] : {e}")

        taux_conv_vente = 1
        try : 
            taux_conv_vente = float(self.var_taux_conv_vente.get())

        except Exception as e :
            print(f"[Erreur] : {e}")

        val_loc_vente = 0
        try :
            val_loc_vente = float(self.var_val_loc_vente.get())

        except Exception as e :
            print(f"[Erreur] : {e}")

        val_port_vente = 0
        try : 
            val_port_vente = float(self.var_val_port_vente.get())

        except Exception as e:
            print(f"[Erreur] : {e}")

        frais_vente = 0
        try :
            frais_vente = float(self.var_frais_vente.get())
        except Exception as e:
            print(f"[Erreur] : {e}")

        er = gf.write_vente_port(self.combobox_port_vente.get(),self.combobox_symbole_vente.get(),str(self.date_choose),parts_vente,val_loc_vente,taux_conv_vente,val_port_vente,frais_vente)
        gf.write_vente_titre(self.combobox_symbole_vente.get(),str(self.date_choose),parts_vente,val_loc_vente,taux_conv_vente,val_port_vente,frais_vente)
        gf.write_prix_symb(self.combobox_symbole_vente.get(),str(self.date_choose),datetime.datetime.now().time(),val_loc_vente)

        if er == 0 :
            self.var_parts_vente.set("")
            self.var_taux_conv_vente.set("")
            self.var_val_loc_vente.set("")
            self.var_val_port_vente.set("")
            self.var_frais_vente.set("")

    def valid_val_loc_vente(self,event):
        parts_vente = 0
        try :
            parts_vente = float(self.var_parts_vente.get())

        except Exception as e :
            print(f"[Erreur] : {e}")

        taux_conv_vente = 1
        try : 
            taux_conv_vente = float(self.var_taux_conv_vente.get())

        except Exception as e :
            print(f"[Erreur] : {e}")

        val_loc_vente = 0
        try :
            val_loc_vente = float(self.var_val_loc_vente.get())

        except Exception as e :
            print(f"[Erreur] : {e}")

        val_port_vente = round(val_loc_vente/taux_conv_vente,2)
        self.var_val_port_vente.set(f"{val_port_vente}")
    
    def event_vente_titre(self):
        self.frame_dashboard.pack_forget()
        try : 
            self.frame_new_port.destroy()
            self.frame_achat_titre.destroy()
            
        except Exception as e:
            print(f"[Erreur] : {e}")
            print("le frame nv port existe pas")

        self.create_frame_vente_port()

    def create_frame_vente_port(self):
        self.frame_vente_port = tk.Frame(self.root)

        self.frame_info_vente_port = tk.Frame(self.frame_vente_port)
        self.label_nom_vente_port = tk.Label(self.frame_info_vente_port, text="Nom du  portefeuille")
        self.label_nom_vente_port.grid(row=0,column=0,padx=5,pady=5)
        self.label_symb_port_vente = tk.Label(self.frame_info_vente_port,text="Symbole")
        self.label_symb_port_vente.grid(row=0,column=1,padx=5,pady=5)
        

        liste_portefeuille = gf.portfeuilles_existant()
        self.combobox_port_vente = ttk.Combobox(self.frame_info_vente_port,values=liste_portefeuille)
        self.combobox_port_vente.grid(row=1,column=0,padx=5,pady=5)
        self.combobox_port_vente.current(0)
        self.combobox_port_vente.bind("<<ComboboxSelected>>", self.select_port_vente)
        

        liste_symbole_port = gf.symboles_portefeuilles(self.combobox_port_vente.get())
        self.combobox_symbole_vente = ttk.Combobox(self.frame_info_vente_port,values=liste_symbole_port)
        self.combobox_symbole_vente.grid(row=1,column=1,padx=5,pady=5)
        self.combobox_symbole_vente.current(0)
        self.frame_info_vente_port.pack(side=tk.TOP,fill=tk.X)

        self.frame_vente_titre = tk.Frame(self.frame_vente_port)
        self.label_parts_vente = tk.Label(self.frame_vente_titre,text="Parts")
        self.label_parts_vente.grid(row=0,column=0,padx=5,pady=5)
        self.var_parts_vente = tk.StringVar()
        self.entry_parts_vente = tk.Entry(self.frame_vente_titre,textvariable=self.var_parts_vente)
        self.entry_parts_vente.grid(row=0,column=1,padx=5,pady=5)
        self.label_taux_conv_vente = tk.Label(self.frame_vente_titre,text="Taux de conversion")
        self.label_taux_conv_vente.grid(row=0,column=2,padx=5,pady=5)
        self.var_taux_conv_vente = tk.StringVar()
        self.entry_taux_conv_vente = tk.Entry(self.frame_vente_titre,textvariable=self.var_taux_conv_vente)
        self.entry_taux_conv_vente.grid(row=0,column=3,padx=5,pady=5)
        self.label_val_loc_vente = tk.Label(self.frame_vente_titre,text="Valeur locale titre")
        self.label_val_loc_vente.grid(row=1,column=0,padx=5,pady=5)
        self.var_val_loc_vente = tk.StringVar()
        self.entry_val_loc_vente = tk.Entry(self.frame_vente_titre,textvariable=self.var_val_loc_vente)
        self.entry_val_loc_vente.grid(row=1,column=1,padx=5,pady=5)
        self.entry_val_loc_vente.bind("<Return>",self.valid_val_loc_vente)
        self.label_val_port_vente = tk.Label(self.frame_vente_titre,text="Valeur portefeuille titre")
        self.label_val_port_vente.grid(row=1,column=2,padx=5,pady=5)
        self.var_val_port_vente = tk.StringVar()
        self.entry_val_port_vente = tk.Entry(self.frame_vente_titre,textvariable=self.var_val_port_vente)
        self.entry_val_port_vente.grid(row=1,column=3,padx=5,pady=5)
        self.label_frais_vente = tk.Label(self.frame_vente_titre,text="Frais de vente")
        self.label_frais_vente.grid(row=2,column=0)
        self.var_frais_vente = tk.StringVar()
        self.entry_frais_vente = tk.Entry(self.frame_vente_titre,textvariable=self.var_frais_vente)
        self.entry_frais_vente.grid(row=2,column=1,padx=5,pady=5)
        self.button_validate_vente = tk.Button(self.frame_vente_titre,text="Valider la vente")
        self.button_validate_vente.grid(row=2,column=3,padx=5,pady=5)
        self.button_validate_vente.bind("<Button-1>",self.valid_vente)
        self.button_date_chooser = tk.Button(self.frame_vente_titre,text="Choisir une date")
        self.button_date_chooser.grid(row=3,column=2,padx=5,pady=5)
        self.button_date_chooser.bind("<Button-1>",self.date_chooser_event)
        
        self.frame_vente_titre.pack(side=tk.TOP,fill=tk.X)

        self.frame_vente_port.pack()

    def event_dividende(self):
        #callback menu pour ajouter un dividende sur un titre toujours dans au moins un portfeuille
        pass

    def event_add_symb(self):
        #callback menu pour ajouter un nouveau symbole dans le fichier info symbole ainsi que dans le fichier history correspondant
        pass

    def event_update_symb_hist(self):
        #callback menu pour ajouter une ligne sur l'historique d'un symbole deja enregsitrer dans un fichier
        toplevel_update_symb = tk.Toplevel(self.root)

        liste_port = gf.portfeuilles_existant()
        liste_symb = []
        for port in liste_port :
            liste_symb = gf.symboles_portefeuilles(port)
            for symb in liste_symb :
                if symb not in liste_symb :
                    liste_symb.append(symb)

        self.combobox_symb = ttk.Combobox(toplevel_update_symb,values=liste_symb)
        self.combobox_symb.current(0)
        self.combobox_symb.pack(side=tk.TOP)

        self.button_date_chooser = tk.Button(toplevel_update_symb,text="Choisir une date")
        self.button_date_chooser.pack(side=tk.TOP)
        self.button_date_chooser.bind("<Button-1>",self.date_chooser_event)

        label_prix_update = tk.Label(toplevel_update_symb,text="Prix (locale)")
        label_prix_update.pack(side=tk.LEFT)

        self.var_prix_update = tk.StringVar()
        entry_prix_update = tk.Entry(toplevel_update_symb,textvariable=self.var_prix_update)
        entry_prix_update.pack(side=tk.RIGHT)
        entry_prix_update.bind("<Return>",self.validate_update_symb_event)

        button_validate_update_prix_symb = tk.Button(toplevel_update_symb,text="Valider le prix")
        button_validate_update_prix_symb.bind("<Button-1>",self.validate_update_symb_event)
        button_validate_update_prix_symb.pack(side=tk.BOTTOM)

    def validate_update_symb_event(self,event):
        self.date_choose = datetime.date.today()
        prix_symb_update = 0 
        try : 
            prix_symb_update = float(self.var_prix_update.get())

        except Exception as e :
            print(f"[Erreur] : {e}")

        gf.write_prix_symb(self.combobox_symb.get(),self.date_choose,datetime.datetime.now().time(),prix_symb_update)

    def event_show_dash(self):
        try : 
            self.frame_new_port.destroy()
            self.frame_achat_titre.destroy()
        except Exception as e :
            print(f"[Erreur] : {e}")
            print("le frame nv port n'existe pas")

        try : 
            self.frame_achat_port.destroy()
            self.frame_achat_titre_port.destroy()

        except Exception as e:
            print(f"[Erreur] : {e}")
            print("le frame achat titre n'existe pas")

        try :
            self.frame_vente_port.destroy()

        except Exception as e:
            print(f"[Erreur] : {e}")
            print("le frame vente titre n'existe pas")

        self.frame_dashboard.pack()

        




if __name__ == "__main__" :
    mainwindow = MainApp()
