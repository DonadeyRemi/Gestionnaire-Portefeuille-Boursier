import tkinter as tk
from tkinter import ttk
import creation_figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        self.menu_portefeuille = tk.Menu(self.Menu,tearoff=0)
        self.menu_portefeuille.add_command(label="Analyse Portefeuille",command=self.event_menu_new_port)
        self.menu_portefeuille.add_separator()
        self.menu_portefeuille.add_command(label="Nouveau portefeuille",command=)
        self.menu_portefeuille.add_command(label="Achat titre",command=)
        self.menu_portefeuille.add_command(label="Vente titre",command=)
        self.menu_portefeuille.add_command(label="Ajouter dividende",command=)
        self.Menu.add_cascade(label="Portefeuille",menu=self.menu_portefeuille)

        self.menu_symbole = tk.Menu(self.Menu,tearoff=0)
        self.menu_symbole.add_command(label="Ajouter symbole",command=)
        self.menu_symbole.add_command(label="Mettre a jour symbole",command=)
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
        self.entry_nom_nv_port.bind("<Enter>",self.valid_nom_nv_port)

        liste_devise = ["EUR","USD","GBP"]
        self.devise_port = "EUR"
        self.combobox_devise = ttk.Combobox(self.frame_info_nv_port,values=liste_devise)
        self.combobox_devise.grid(row=1,column=1,padx=5,pady=5)
        self.combobox_devise.current(0)
        self.combobox_devise.bind("<<ComboboxSelected>>", self.select_devise)
        self.frame_info_nv_port.pack(side=tk.TOP,fill=tk.X)

        self.frame_list_view_symb = tk.Frame(self.frame_new_port)
        self.label_name_listview = tk.Label(self.frame_list_view_symb,text="Symboles présent dans le Portefeuille-1")
        self.label_name_listview.pack(side=tk.TOP,fill=tk.X,padx=10,pady=10)

        self.listview_symb = tk.Listbox(self.frame_list_view_symb)
        self.listview_symb.pack(side=tk.TOP,fill=tk.X,padx=10,pady=5)
        self.frame_list_view_symb.pack(side=tk.RIGHT,fill=tk.Y)

    def effacer_nom(self,event):
        print(event)

    def select_devise(self,event):
        self.devise_port = self.combobox_devise.get()
        print(f"Vous avez selectionner comme devise {self.devise_port}")

    def valid_nom_nv_port(self,event):
        self.var_nom_port.set(self.entry_nom_nv_port.get())
        self.label_name_listview.config(text=f"Symboles présent dans le {self.var_nom_port}")

    def create_frame_achat_titre(self,root):
        frame_achat_titre = tk.Frame(self.root)

        self.frame_symb_info = tk.Frame(frame_achat_titre)
        self.label_symbole = tk.Label(self.frame_symb_info,text="Symbole")
        self.label_symbole.grid(row=0,column=0,padx=10,pady=10)

        self.var_symb = tk.StringVar()
        self.entry_symb = tk.Entry(self.frame_symb_info,textvariable=self.var_symb)
        self.entry_symb.grid(row=1,column=0,padx=10,pady=10)

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
        self.frame_symb_info_max.grid(row=0,column=1,columnspan=2)

        self.frame_symb_info.pack(side=tk.TOP,fill=tk.X)
        separateur_1 = ttk.Separator(frame_achat_titre,orient=tk.HORIZONTAL)
        separateur_1.pack(side=tk.TOP,fill=tk.X)

        self.frame_achat_info = tk.Frame(frame_achat_titre)
        self.label_parts = tk.Label(self.frame_achat_info,text="Parts")
        self.label_parts.grid(row=0,column=0,padx=5,pady=5)

        self.label_val_loc = tk.Label(self.frame_achat_info,text="Valeur symbole locale")
        self.label_val_loc.grid(row=1,column=0,columnspan=2,padx=5,pady=5)

        self.label_val_port = tk.Label(self.frame_achat_info,text="Valeur symbole portefeuille")
        self.label_val_port.grid(row=2,column=0,columnspan=2,padx=5,pady=5)
        self.label_frais_achat = tk.Label(self.frame_achat_info,text="Frais achat")
        self.label_frais_achat.grid(row=3,column=0,padx=5,pady=5)


if __name__ == "__main__" :
    mainwindow = MainApp()
