import tkinter as tk
import creation_figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainApp():
    def __init__(self):
        self.root = tk.Tk()

        self.initWidget()

        self.root.mainloop()

    def initWidget(self):
        self.frame_label = tk.Frame(self.root)

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

        self.canvas_pie_patrimoine_tot = FigureCanvasTkAgg(self.fig_pie_patrimoine_tot, master=self.root)  # A tk.DrawingArea.
        self.canvas_pie_patrimoine_tot.draw()
        self.canvas_pie_patrimoine_tot.get_tk_widget().grid(column=1,row=0,padx=10,pady=10)#pack(side=tk.RIGHT, fill=tk.X,padx=10,pady=10)

        self.fig_line_patrimoine_hist,self.ax_line_patrimoine_hist = plt.subplots(figsize=(10,5))
        self.ax_line_patrimoine_hist.plot([0,1,2,4,5],[10,9,15,16,17])
        self.ax_line_patrimoine_hist.set_title("Evolution du patrimoine")

        self.canvas_line_patrimoine_hist = FigureCanvasTkAgg(self.fig_line_patrimoine_hist,master=self.root)
        self.canvas_line_patrimoine_hist.draw()
        self.canvas_line_patrimoine_hist.get_tk_widget().grid(column=0,columnspan=2,row=1,padx=10,pady=10)#pack(side=tk.BOTTOM,fill=tk.X,padx=10,pady=10)


if __name__ == "__main__" :
    mainwindow = MainApp()
