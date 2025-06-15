from tkinter import *
import tkintermapview

#from utils.notatki2 import listbox_lista_obiektow

camers: list =[]
technicians:list=[]
workers:list=[]
data_camers=[]
data_workers=[]
data_technicians=[]

class Camers:
    def __init__(self,camer_name,camer_location):
        self.camer_name = camer_name
        self.camer_location = camer_location
        self.coordinates = self.get_coordinates()
        self.marker=map_widget.set_marker(self.coordinates[0],self.coordinates[1])

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        url = f"https://pl.wikipedia.org/wiki/{self.camer_location}"
        response = requests.get(url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        print(longitude)
        print(latitude)
        return [latitude, longitude]

class technician:
    def __init__(self,technician_name,technician_surname,technician_id):
        self.technician_name =technician_name
        self.technician_surname=technician_surname
        self.technician_id=technician_id
        self.coordinates=self.get_coordinates()
        self.marker=map_widget.set_marker(self.coordinates[0],self.coordinates[1])

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        url = f"https://pl.wikipedia.org/wiki/{self.client_location2}"
        response = requests.get(url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        print(longitude)
        print(latitude)
        return [latitude, longitude]


class Workers:
    def __init__(self,worker_name,worker_surname,worker_id):
        self.worker_name =worker_name
        self.worker_surname =worker_surname
        self.worker_id=worker_id
        self.coordinates=self.get_coordinates()
        self.marker=map_widget.set_marker(self.coordinates[0],self.coordinates[1])

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        url = f"https://pl.wikipedia.org/wiki/{self.worker_location}"
        response = requests.get(url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        print(longitude)
        print(latitude)
        return [latitude, longitude]



root = Tk()
root.geometry("1200x760")
root.title("Ramka")


ramka_lista_obiektow=Frame(root)
ramka_formularz=Frame(root)
ramka_szczegoly_obiektow=Frame(root)
ramka_mapa=Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0,columnspan=2)
ramka_mapa.grid(row=2, column=0, columnspan=2)

def dodaj_wszystko():
    text_camers = entry_name_camers.get()
    text_id = entry_name_id.get()
    text_workers = entry_name_workers.get()
    text_workers_surname = entry_surname_workers.get()
    text_technical = entry_name_technicial.get()
    text_technicial_surname = entry_surname_technicial.get()


    if text_camers.strip():
        pozycja = listbox_lista_kamer.size() + 1
        wiersz = f"{pozycja}. {text_camers}  {text_id}"
        listbox_lista_kamer.insert(END, wiersz)
        data_camers.append((text_camers, text_id))
        entry_name_camers.delete(0, END)
        entry_name_id.delete(0, END)

    if text_workers.strip():
        pozycja = listbox_lista_pracownikow.size() + 1
        wiersz = f"{pozycja}. {text_workers} {text_workers_surname}"
        listbox_lista_pracownikow.insert(END, wiersz)
        data_workers.append((text_workers, text_workers_surname))
        entry_name_workers.delete(0, END)
        entry_surname_workers.delete(0, END)

    if text_technical.strip():
        pozycja = listbox_lista_konserwatorow.size() + 1
        wiersz = f"{pozycja}. {text_technical} {text_technicial_surname}"
        listbox_lista_konserwatorow.insert(END, wiersz)
        data_technicians.append((text_technical, text_technicial_surname))
        entry_name_technicial.delete(0, END)
        entry_surname_technicial.delete(0, END)

def remove_camers():
    selection = listbox_lista_kamer.curselection()
    if selection:
        i = selection[0]
        data_camers.pop(i)
        listbox_lista_kamer.delete(0, END)
        for idx, (nazwa, id_) in enumerate(data_camers, start=1):
            listbox_lista_kamer.insert(END, f"{idx}. {nazwa}  {id_}")

def edit_camers():
    selection = listbox_lista_kamer.curselection()
    if selection:
        i = selection[0]
        name, id_ = data_camers[i]

        entry_name_camers.delete(0, END)
        entry_name_camers.insert(0, name)

        entry_name_id.delete(0, END)
        entry_name_id.insert(0, id_)
        edytowany_index.set(i)
        button_dodaj_obiekt.config(text="Zapisz", command=update_camers)

def update_camers():
    i = edytowany_index.get()
    new_name = entry_name_camers.get()
    new_id = entry_name_id.get()

    if new_name.strip():
        data_camers[i] = (new_name, new_id)

        listbox_lista_kamer.delete(0, END)
        for idx, (nazwa, id_) in enumerate(data_camers, start=1):
            listbox_lista_kamer.insert(END, f"{idx}. {nazwa}  {id_}")
        entry_name_camers.delete(0, END)
        entry_name_id.delete(0, END)
        button_dodaj_obiekt.config(text="Dodaj", command=dodaj_wszystko)

# ramka_lista_kamer
label_lista_obiektow=Label(ramka_lista_obiektow, text="Lista kamer")
label_lista_obiektow.grid(row=0, column=0,columnspan=2)
listbox_lista_kamer = Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_kamer.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly_obiektu = Button(ramka_lista_obiektow, text='Pokaż szczegóły')
button_pokaz_szczegoly_obiektu.grid(row=2, column=0)
button_usun_obiekt = Button(ramka_lista_obiektow, text='Usuń obiekt', command=remove_camers)
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt = Button(ramka_lista_obiektow, text='Edytuj obiekt', command=edit_camers)
button_edytuj_obiekt.grid(row=2, column=2)

def remove_worker():
    selection = listbox_lista_pracownikow.curselection()
    if selection:
        i = selection[0]
        data_workers.pop(i)
        listbox_lista_pracownikow.delete(0, END)
        for idx, (imie, nazwisko) in enumerate(data_workers, start=1):
            listbox_lista_pracownikow.insert(END, f"{idx}. {imie} {nazwisko}")

def edit_worker():
    selection = listbox_lista_pracownikow.curselection()
    if selection:
        i = selection[0]
        imie, nazwisko = data_workers[i]

        entry_name_workers.delete(0, END)
        entry_name_workers.insert(0, imie)

        entry_surname_workers.delete(0, END)
        entry_surname_workers.insert(0, nazwisko)

        edytowany_index.set(i)
        edytowany_typ.set("pracownik")

        button_dodaj_obiekt.config(text="Zapisz", command=update_worker)

def update_worker():
    i = edytowany_index.get()
    new_imie = entry_name_workers.get()
    new_nazwisko = entry_surname_workers.get()

    if new_imie.strip():
        data_workers[i] = (new_imie, new_nazwisko)

        listbox_lista_pracownikow.delete(0, END)
        for idx, (imie, nazwisko) in enumerate(data_workers, start=1):
            listbox_lista_pracownikow.insert(END, f"{idx}. {imie} {nazwisko}")

        entry_name_workers.delete(0, END)
        entry_surname_workers.delete(0, END)

        button_dodaj_obiekt.config(text="Dodaj", command=dodaj_wszystko)

#ramka_lista_PRACOWNIKÓW
label_lista_obiektow_klient=Label(ramka_lista_obiektow, text="Lista pracowników")
label_lista_obiektow_klient.grid(row=0, column=3,columnspan=2)
listbox_lista_pracownikow = Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_pracownikow.grid(row=1, column=3, columnspan=3)
button_pokaz_szczegoly_obiektu_klient=Button(ramka_lista_obiektow, text='Pokaż szczegóły')
button_pokaz_szczegoly_obiektu_klient.grid(row=2, column=3)
button_usun_obiekt_klient = Button(ramka_lista_obiektow, text='Usuń obiekt', command=remove_worker)
button_usun_obiekt_klient.grid(row=2, column=4)
button_edytuj_obiekt_klient=Button(ramka_lista_obiektow, text='Edytuj obiekt', command=edit_worker)
button_edytuj_obiekt_klient.grid(row=2, column=5)

def remove_technician():
    selection = listbox_lista_konserwatorow.curselection()
    if selection:
        i = selection[0]
        data_technicians.pop(i)
        listbox_lista_konserwatorow.delete(0, END)
        for idx, (imie, nazwisko) in enumerate(data_technicians, start=1):
            listbox_lista_konserwatorow.insert(END, f"{idx}. {imie} {nazwisko}")

def edit_technician():
    selection = listbox_lista_konserwatorow.curselection()
    if selection:
        i = selection[0]
        imie, nazwisko = data_technicians[i]

        entry_name_technicial.delete(0, END)
        entry_name_technicial.insert(0, imie)

        entry_surname_technicial.delete(0, END)
        entry_surname_technicial.insert(0, nazwisko)

        edytowany_index.set(i)
        edytowany_typ.set("konserwator")

        button_dodaj_obiekt.config(text="Zapisz", command=update_technician)

def update_technician():
    i = edytowany_index.get()
    new_imie = entry_name_technicial.get()
    new_nazwisko = entry_surname_technicial.get()

    if new_imie.strip():
        data_technicians[i] = (new_imie, new_nazwisko)

        listbox_lista_konserwatorow.delete(0, END)
        for idx, (imie, nazwisko) in enumerate(data_technicians, start=1):
            listbox_lista_konserwatorow.insert(END, f"{idx}. {imie} {nazwisko}")

        entry_name_technicial.delete(0, END)
        entry_surname_technicial.delete(0, END)

        button_dodaj_obiekt.config(text="Dodaj", command=dodaj_wszystko)

#ramka_lista_konserwatorów
label_lista_obiektow_klient=Label(ramka_lista_obiektow, text="Lista konserwatorów")
label_lista_obiektow_klient.grid(row=0, column=6,columnspan=2)
listbox_lista_konserwatorow = Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_konserwatorow.grid(row=1, column=6, columnspan=3)
button_pokaz_szczegoly_obiektu_klient=Button(ramka_lista_obiektow, text='Pokaż szczegóły')
button_pokaz_szczegoly_obiektu_klient.grid(row=2, column=6)
button_usun_obiekt_klient = Button(ramka_lista_obiektow, text='Usuń obiekt', command=remove_technician)
button_usun_obiekt_klient.grid(row=2, column=7)
button_edytuj_obiekt_klient=Button(ramka_lista_obiektow, text='Edytuj obiekt', command=edit_technician)
button_edytuj_obiekt_klient.grid(row=2,column=8)






# ramka_formularz
label_formularz=Label(ramka_formularz, text="Formularz")
label_formularz.grid(row=0, column=0, columnspan=2)
label_name_camer=Label(ramka_formularz, text="Nazwa kamery:")
label_name_camer.grid(row=1, column=0, sticky=W)
label_id=Label(ramka_formularz, text="ID")
label_id.grid(row=2, column=0, sticky=W)
label_name_workers=Label(ramka_formularz, text="Imie pracownika:")
label_name_workers.grid(row=3, column=0,sticky=W)
label_surname_workers=Label(ramka_formularz, text="Nazwisko Pracownika:")
label_surname_workers.grid(row=4, column=0,sticky=W)
label_name_technicial=Label(ramka_formularz, text="Imie konserwatora:")
label_name_technicial.grid(row=5, column=0,sticky=W)
label_surname_technicial=Label(ramka_formularz, text="Nazwisko konserwatora:")
label_surname_technicial.grid(row=6, column=0,sticky=W)
button_dodaj_obiekt = Button(ramka_formularz, text="Dodaj", command=dodaj_wszystko)
button_dodaj_obiekt.grid(row=8, column=0, columnspan=2)


entry_name_camers=Entry(ramka_formularz)
entry_name_camers.grid(row=1, column=1)
entry_name_id=Entry(ramka_formularz)
entry_name_id.grid(row=2, column=1)
entry_name_workers=Entry(ramka_formularz)
entry_name_workers.grid(row=3, column=1)
entry_surname_workers=Entry(ramka_formularz)
entry_surname_workers.grid(row=4, column=1)
entry_name_technicial=Entry(ramka_formularz)
entry_name_technicial.grid(row=5, column=1)
entry_surname_technicial=Entry(ramka_formularz)
entry_surname_technicial.grid(row=6, column=1)
edytowany_typ = StringVar(value="")
edytowany_index = IntVar(value=-1)


# ramka_mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=500, corner_radius=5)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23,21.0)
map_widget.set_zoom(6)



root.mainloop()

