from tkinter import *
from tkinter import font
import mysql.connector
import tkinter.messagebox


class Produit:

    def __init__(self, id: int, nom: str, txt: str, prix: int, qtt: int, id_categorie: int):
        self.qtt = qtt
        self.nom = nom
        self.prix = prix
        self.__id = id
        self.txt = txt
        self.id_categorie = id_categorie

    def get_infos(self):
        return "ID: " + str(self.__id) + "  |  " + self.nom + "  |  Prix: " + str(self.prix) + "€  |  Quantité: " + str(self.qtt) + "  |  Catégorie: " + get_categorie_nom(self.id_categorie) + "  |  description: " + self.txt

    def get_id(self):
        return self.__id


Produit_list: list[Produit] = []
categorie_list: dict = {}


def add_item(top, nom, txt, prix, qtt, id_categorie):
    if len(nom) > 0 and len(txt) > 0 and len(prix) > 0 and len(qtt) > 0:
        try:
            db_cursor.execute(
                "INSERT INTO Produit (nom, descripton, prix, quantite, id_categorie) VALUES ('" + nom + "', '" + txt + "', " + prix + ", " + qtt + ", " + str(
                    id_categorie) + ");")
            db.commit()

            close_win(top)
        except Exception as e:
            tkinter.messagebox.showerror("Erreur !", "Impossible d'ajouter le Produit: " + str(e))

def modify_item(top, id, nom, txt, prix, qtt, id_categorie):
    if len(nom) > 0 and len(txt) > 0 and len(prix) > 0 and len(qtt) > 0:
        try:
            db_cursor.execute("UPDATE Produit SET quantite = " + qtt + " WHERE id=" + str(id) + ";")
            db_cursor.execute("UPDATE Produit SET nom = '"+nom+"' WHERE id="+str(id)+";")
            db_cursor.execute("UPDATE Produit SET prix = " + prix + " WHERE id=" + str(id) + ";")
            db_cursor.execute("UPDATE Produit SET id_categorie = " + str(id_categorie) + " WHERE id=" + str(id) + ";")
            db_cursor.execute("UPDATE Produit SET descripton = '" + txt + "' WHERE id=" + str(id) + ";")
            db.commit()
        except Exception as e:
            tkinter.messagebox.showerror("Erreur !", "Impossible de modifier le Produit: " + str(e))


def ouvrir_Produit_remove_window():
    items = item_list.curselection()
    if len(items) > 0:
        Produit_index = items[0]
        if tkinter.messagebox.askyesno("Confirmer", "Supprimer le Produit sélectionné ("+Produit_list[Produit_index].nom+") ?"):
            try:
                db_cursor.execute("DELETE FROM Produit WHERE id="+str(Produit_list[Produit_index].get_id())+";")
                db.commit()
            except Exception as e:
                tkinter.messagebox.showerror("Erreur !", "Impossible de supprimer le Produit: " + str(e))


def ouvrir_Produit_edit_window():
    items = item_list.curselection()
    if len(items) > 0:
        selected_Produit = Produit_list[items[0]]

        top = Toplevel(window)
        top.geometry("500x700")
        top.grab_set()

        label_nom = Label(top, text="Nom:")
        label_nom.pack(pady=4)

        champs_nom = Entry(top)
        champs_nom.insert(0, selected_Produit.nom)
        champs_nom.pack(pady=8)

        label_txt = Label(top, text="Description:")
        label_txt.pack(pady=4)

        champs_txt = Entry(top)
        champs_txt.insert(0, selected_Produit.txt)
        champs_txt.pack(pady=8)

        label_prix = Label(top, text="Prix:")
        label_prix.pack(pady=4)

        champs_prix = Entry(top)
        champs_prix.insert(0, str(selected_Produit.prix))
        champs_prix.pack(pady=8)

        label_qtt = Label(top, text="Quantité:")
        label_qtt.pack(pady=4)

        champs_qtt = Entry(top)
        champs_qtt.insert(0, str(selected_Produit.qtt))
        champs_qtt.pack(pady=8)

        categorie_label = Label(top, text="Catégorie:", padx=16)
        categorie_label.pack(pady=4)
        categorie = StringVar()

        categories = []
        for cat in categorie_list:
            categories.append(cat)
        if len(categories) > 0:
            categorie.set(get_categorie_nom(selected_Produit.id_categorie))
        else:
            categories.append("---")
        categorie_option = OptionMenu(top, categorie, *categories)
        categorie_option.pack(pady=4)

        button_validate = Button(
            top, text="Modifier", command=lambda: modify_item(
                top, selected_Produit.get_id(), champs_nom.get(), champs_txt.get(), champs_prix.get(), champs_qtt.get(),
                get_categorie_id(categorie.get()))
        )
        button_validate.pack(pady=4)
        button_cancel = Button(top, text="Annuler", command=lambda: close_win(top))
        button_cancel.pack(pady=4)

def close_win(top):
    top.destroy()
    
   
def ouvrir_Produit_add_window():
    top = Toplevel(window)
    top.geometry("500x700")
    top.grab_set()
    top.resizable(width=False, height=False)

    label_nom = Label(top, text="Nom:")
    label_nom.pack(pady=4)

    champs_nom = Entry(top)
    champs_nom.pack(pady=6)

    label_txt = Label(top, text="descripton:")
    label_txt.pack(pady=4)

    champs_txt = Entry(top)
    champs_txt.pack(pady=6)

    label_prix = Label(top, text="Prix:")
    label_prix.pack(pady=4)

    champs_prix = Entry(top)
    champs_prix.pack(pady=6)

    label_qtt = Label(top, text="Quantité:")
    label_qtt.pack(pady=4)

    champs_qtt = Entry(top)
    champs_qtt.pack(pady=6)

    categorie_label = Label(top, text="Catégorie:", padx=16)
    categorie_label.pack(pady=4)
    categorie = StringVar()

    categories = []
    for cat in categorie_list:
        categories.append(cat)
    if len(categories) > 0:
        categorie.set(categories[0])
    else:
        categories.append("")
    categorie_option = OptionMenu(top, categorie, *categories)
    categorie_option.pack(pady=6)

    button_validate = Button(
        top, text="Ajouter", command=lambda: add_item(
            top, champs_nom.get(), champs_txt.get(), champs_prix.get(), champs_qtt.get(), get_categorie_id(categorie.get()))
    )
    button_validate.pack(pady=6)
    button_cancel = Button(top, text="Annuler", command=lambda: close_win(top))
    button_cancel.pack(pady=6)
    
    

def get_categorie_nom(id_categorie):
    for categorie in categorie_list:
        if categorie_list[categorie] == id_categorie:
            return categorie
    return str(id_categorie)


def get_categorie_id(nom):
    for categorie in categorie_list:
        if categorie == nom:
            return categorie_list[categorie]
    return nom


try:
    db = mysql.connector.connect(host="localhost", user="root", password="root", database="boutique")
except Exception as e:
    tkinter.messagebox.showerror("Erreur !", "Impossible de se connecter au serveur: "+str(e))
    exit(-1)

db_cursor = db.cursor()
try:
    db_cursor.execute("USE boutique")
except Exception as e:
    tkinter.messagebox.showerror("Erreur !", "Impossible d'accéder à la base de données \"boutique\": "+str(e))
    db_cursor.close()
    exit(-1)

window = Tk(className="Tableau de bord")
font.nametofont("TkDefaultFont").configure(size=12)
window.geometry("500x600")
window.resizable(width=False, height=False)


item_list_frame = Frame(window, pady=16)
item_list = Listbox(item_list_frame, width=92, height=16)

item_list.grid(column=0, row=0, sticky=(N, W, E, S))
scrollbar = Scrollbar(item_list_frame, orient=VERTICAL, command=item_list.yview)
scrollbar.grid(column=1, row=0, sticky=(N, S))
item_list['yscrollcommand'] = scrollbar.set
item_list_frame.grid_columnconfigure(0, weight=1)
item_list_frame.grid_rowconfigure(0, weight=1)

add_item_button = Button(item_list_frame, text="Ajouter...", command=lambda: ouvrir_Produit_add_window())
add_item_button.grid(pady=10)
edit_item_button = Button(item_list_frame, text="Modifier...", command=lambda: ouvrir_Produit_edit_window())
edit_item_button.grid(pady=10)
remove_item_button = Button(item_list_frame, text="Supprimer...", command=lambda: ouvrir_Produit_remove_window())
remove_item_button.grid(pady=10)
reload_items_button = Button(item_list_frame, text="Actualiser...", command=lambda: ouvrir_Produit_edit_window())
reload_items_button.grid(pady=10)
ouvrir_Produit_edit_window()

item_list_frame.pack()

window.mainloop()

db_cursor.close()