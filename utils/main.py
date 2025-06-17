from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

camers: list =[]
technicians:list=[]
workers:list=[]
data_camers=[]
data_workers=[]
data_technicians=[]
camera_markers = []

class Camers:
    def __init__(self, camer_name, camer_location):
        self.camer_name = camer_name
        self.camer_location = camer_location

    def get_coordinates(self) -> list:
        try:
            url = f"https://pl.wikipedia.org/wiki/{self.camer_location}"
            response = requests.get(url).text
            soup = BeautifulSoup(response, "html.parser")
            longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
            latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
            return [latitude, longitude]
        except Exception as e:
            print(f"Błąd podczas pobierania współrzędnych: {e}")
            return [0.0, 0.0]


class Technician:
    def __init__(self, technician_name, technician_surname, technician_id):
        self.technician_name = technician_name
        self.technician_surname = technician_surname
        self.technician_id = technician_id



class Workers:
    def __init__(self, worker_name, worker_surname, worker_id):
        self.worker_name = worker_name
        self.worker_surname = worker_surname
        self.worker_id = worker_id



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
    text_location = entry_camera_location.get().strip()
    text_camers = entry_name_camers.get().strip()
    text_id = entry_name_id.get().strip()
    text_workers = entry_name_workers.get().strip()
    text_workers_surname = entry_surname_workers.get().strip()
    text_technical = entry_name_technicial.get().strip()
    text_technicial_surname = entry_surname_technicial.get().strip()

    cam = Camers(text_camers, text_location)
    camers.append(cam)

    coordinates = cam.get_coordinates()
    if coordinates != [0.0, 0.0]:
        marker = map_widget.set_marker(coordinates[0], coordinates[1], text=text_camers)
        camera_markers.append(marker)
    else:
        camera_markers.append(None)
    pozycja = listbox_lista_kamer.size() + 1
    wiersz = f"{pozycja}. {text_camers} ({text_id})"
    listbox_lista_kamer.insert(END, wiersz)
    data_camers.append((text_camers, text_id))
    entry_name_camers.delete(0, END)
    entry_name_id.delete(0, END)
    entry_camera_location.delete(0, END)


    worker = Workers(text_workers, text_workers_surname, "-")
    workers.append(worker)
    pozycja = listbox_lista_pracownikow.size() + 1
    wiersz = f"{pozycja}. {text_workers} {text_workers_surname}"
    listbox_lista_pracownikow.insert(END, wiersz)
    data_workers.append((text_workers, text_workers_surname))
    entry_name_workers.delete(0, END)
    entry_surname_workers.delete(0, END)

    # Dodanie konserwatora
    technician_obj = Technician(text_technical, text_technicial_surname, "-")
    technicians.append(technician_obj)
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

        # Usuń marker jeśli istnieje
        marker = camera_markers.pop(i)
        if marker:
            marker.delete()

        # Usuń dane kamery
        data_camers.pop(i)
        camers.pop(i)

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
        # Aktualizacja danych
        data_camers[i] = (new_name, new_id)
        camers[i].camer_name = new_name

        # Aktualizacja markera na mapie (tekst)
        marker = camera_markers[i]
        if marker:
            marker.set_text(new_name)

        # Odświeżenie listy
        listbox_lista_kamer.delete(0, END)
        for idx, (nazwa, id_) in enumerate(data_camers, start=1):
            listbox_lista_kamer.insert(END, f"{idx}. {nazwa}  {id_}")

        # Wyczyść formularz
        entry_name_camers.delete(0, END)
        entry_name_id.delete(0, END)
        button_dodaj_obiekt.config(text="Dodaj", command=dodaj_wszystko)

def show_camers():

    selection = listbox_lista_kamer.curselection()
    if selection:
        i = selection[0]
        name, id_ = data_camers[i]
        label_szczegoly_kamera_name_wartosc.config(text=name)
        label_szczegoly_kamera_id_wartosc.config(text=id_)


# ramka_lista_kamer
label_lista_obiektow=Label(ramka_lista_obiektow, text="Lista kamer")
label_lista_obiektow.grid(row=0, column=0,columnspan=2)
listbox_lista_kamer = Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_kamer.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly_obiektu = Button(ramka_lista_obiektow, text='Pokaż szczegóły', command=show_camers)
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

def show_workers():
    selection = listbox_lista_pracownikow.curselection()
    if selection:
        i = selection[0]
        name, surname = data_workers[i]
        label_szczegoly_worker_name_wartosc.config(text=name)
        label_szczegoly_worker_surname_wartosc.config(text=surname)
#ramka_lista_PRACOWNIKÓW
label_lista_obiektow_klient=Label(ramka_lista_obiektow, text="Lista pracowników")
label_lista_obiektow_klient.grid(row=0, column=3,columnspan=2)
listbox_lista_pracownikow = Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_pracownikow.grid(row=1, column=3, columnspan=3)
button_pokaz_szczegoly_obiektu_klient = Button(ramka_lista_obiektow, text='Pokaż szczegóły', command=show_workers)
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

def show_technicians():
    selection = listbox_lista_konserwatorow.curselection()
    if selection:
        i = selection[0]
        name, surname = data_technicians[i]
        label_szczegoly_tech_name_wartosc.config(text=name)
        label_szczegoly_tech_surname_wartosc.config(text=surname)

#ramka_lista_konserwatorów
label_lista_obiektow_klient=Label(ramka_lista_obiektow, text="Lista konserwatorów")
label_lista_obiektow_klient.grid(row=0, column=6,columnspan=2)
listbox_lista_konserwatorow = Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_konserwatorow.grid(row=1, column=6, columnspan=3)
button_pokaz_szczegoly_obiektu_klient = Button(ramka_lista_obiektow, text='Pokaż szczegóły', command=show_technicians)
button_pokaz_szczegoly_obiektu_klient.grid(row=2, column=6)
button_usun_obiekt_klient = Button(ramka_lista_obiektow, text='Usuń obiekt', command=remove_technician)
button_usun_obiekt_klient.grid(row=2, column=7)
button_edytuj_obiekt_klient=Button(ramka_lista_obiektow, text='Edytuj obiekt', command=edit_technician)
button_edytuj_obiekt_klient.grid(row=2,column=8)

# ramka_formularz
label_formularz=Label(ramka_formularz, text="Formularz")
label_formularz.grid(row=0, column=0, columnspan=2)
label_camera_coords = Label(ramka_formularz, text="Współrzędne kamery:")
label_camera_coords.grid(row=1, column=0, sticky=W)
label_camera_name = Label(ramka_formularz, text="Nazwa kamery:")
label_camera_name.grid(row=2, column=0, sticky=W)
label_id=Label(ramka_formularz, text="ID")
label_id.grid(row=3, column=0, sticky=W)
label_name_workers=Label(ramka_formularz, text="Imie pracownika:")
label_name_workers.grid(row=4, column=0,sticky=W)
label_surname_workers=Label(ramka_formularz, text="Nazwisko Pracownika:")
label_surname_workers.grid(row=5, column=0,sticky=W)
label_name_technicial=Label(ramka_formularz, text="Imie konserwatora:")
label_name_technicial.grid(row=6, column=0,sticky=W)
label_surname_technicial=Label(ramka_formularz, text="Nazwisko konserwatora:")
label_surname_technicial.grid(row=7, column=0,sticky=W)
button_dodaj_obiekt = Button(ramka_formularz, text="Dodaj", command=dodaj_wszystko)
button_dodaj_obiekt.grid(row=8, column=0, columnspan=2)


entry_camera_location = Entry(ramka_formularz)
entry_camera_location.grid(row=1, column=1)

entry_name_camers = Entry(ramka_formularz)
entry_name_camers.grid(row=2, column=1)

entry_name_id = Entry(ramka_formularz)
entry_name_id.grid(row=3, column=1)

entry_name_workers = Entry(ramka_formularz)
entry_name_workers.grid(row=4, column=1)

entry_surname_workers = Entry(ramka_formularz)
entry_surname_workers.grid(row=5, column=1)

entry_name_technicial = Entry(ramka_formularz)
entry_name_technicial.grid(row=6, column=1)

entry_surname_technicial = Entry(ramka_formularz)
entry_surname_technicial.grid(row=7, column=1)


edytowany_typ = StringVar(value="")
edytowany_index = IntVar(value=-1)


label_szczegoly_kamera_name = Label(ramka_szczegoly_obiektow, text="Nazwa kamery:")
label_szczegoly_kamera_name.grid(row=0, column=0)
label_szczegoly_kamera_name_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_kamera_name_wartosc.grid(row=0, column=1)

label_szczegoly_kamera_id = Label(ramka_szczegoly_obiektow, text="ID:")
label_szczegoly_kamera_id.grid(row=0, column=2)
label_szczegoly_kamera_id_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_kamera_id_wartosc.grid(row=0, column=3)

label_szczegoly_worker_name = Label(ramka_szczegoly_obiektow, text="Imię pracownika:")
label_szczegoly_worker_name.grid(row=0, column=4)
label_szczegoly_worker_name_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_worker_name_wartosc.grid(row=0, column=5)

label_szczegoly_worker_surname = Label(ramka_szczegoly_obiektow, text="Nazwisko pracownika:")
label_szczegoly_worker_surname.grid(row=0, column=6)
label_szczegoly_worker_surname_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_worker_surname_wartosc.grid(row=0, column=7)

label_szczegoly_tech_name = Label(ramka_szczegoly_obiektow, text="Imie konserwatora:")
label_szczegoly_tech_name.grid(row=0, column=8)
label_szczegoly_tech_name_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_tech_name_wartosc.grid(row=0, column=9)

label_szczegoly_tech_surname = Label(ramka_szczegoly_obiektow, text="Nazwisko konserwatora:")
label_szczegoly_tech_surname.grid(row=0, column=10)
label_szczegoly_tech_surname_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_tech_surname_wartosc.grid(row=0, column=11)

# ramka_mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=500, corner_radius=5)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23,21.0)
map_widget.set_zoom(6)



root.mainloop()

