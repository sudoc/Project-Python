from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.filedialog import asksaveasfilename
from tkinter.ttk import *
from tokenize import String
import requests, pdfkit, time, threading, mysql.connector
from mysql.connector import Error
from mysql.connector.locales.eng import client_error


def db_connect():
    """Function returns MySQL connector."""
    return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="wyk"
            )


def db_connect_and_fetch(query, *vars):
    """
    Function fetch data from DB.

    Function connects do the DB, executes SQL query,
    fetch output of given query and return this output.
    """
    result = ""
    try:
        conn = db_connect()
        if conn.is_connected():
            cursor = conn.cursor()
            if vars:
                for var in vars:
                    cursor.execute(query, var)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
    except Error as e:
        print ("Database query failed!", e)
    finally:
        if(conn.is_connected()):
            cursor.close()
            conn.close()
    return result


def db_connect_and_exec(query, *vars):
    """
    Function executes query on DB.

    Function connects do the DB, executes SQL query
    (function does not provide output).
    """
    try:
        conn = db_connect()
        if conn.is_connected():
            cursor = conn.cursor()
            if vars:
                for var in vars:
                    cursor.execute(query, var)
            else:
                cursor.execute(query)
            conn.commit()
    except Error as e:
        print ("Database query failed!", e)
    finally:
        if(conn.is_connected()):
            cursor.close()
            conn.close()
 

def Frame1():
    F = Tk()
    F.geometry('310x100')
    F.resizable(0, 0)
    l1 = Label(F, text="Witaj w aplikacji do ułatwiania życia studentom!")
    l1.grid(column=0, row=0)
    l2 = Label(F, text="Projekt jest w fazie rozwojowej, proszę o cierpliwość.")
    l2.grid(column=0, row=1)
    l3 = Label(F, text="Aplikacja zapisuje wybrane strony prowadzących do pliku.")
    l3.grid(column=0, row=2)
    l4 = Label(F, text="Aby rozpocząć, wybierz prowadzącego z menu Opcje.")
    l4.grid(column=0, row=3)
    l5 = Label(F, text="Ver.1.2")
    l5.grid(column=0, row=4)
    F.title("AUŻS")
    m = Menu(F)
    ni = Menu(m)


    def Prowadz():
        # fetch lecturers from db
        lista = []
        sql = "Select Nazwa from dane"
        sql_result = db_connect_and_fetch(sql)
        for i in sql_result:
            lista.append(i)

        Frame2 = Tk()
        Frame2.title("Wybieranie prowadzącego: ")
        Frame2.geometry('450x200+500+300')
        Frame2.resizable(0, 0)
        l1 = Label(Frame2, text="Wybierz prowadzącego: ")
        l1.grid(column=0, row=0)

        combo = Combobox(Frame2)
        combo.grid(column=1, row=0)
        combo['values'] = lista
        combo.current(0)
        l2 = Label(Frame2, text="Wybierz prowadzacego lub wpisz URL")
        l2.grid(column=1, row=2)
        l3 = Label(Frame2, text = "")
        l3.grid(column=1,row=3)
        l4 = Label(Frame2, text = "")
        l4.grid(column=1,row=5)


        def worker_start(fdir, url):
            l4.config(text = "")
            l3.config(text = "Trwa pobieranie, czekaj...")
            bar.grid(column=1,row=4)

            if url == "":
                url = combo.get()

            bar.start()
            pdfkit.from_url(url, fdir)
            bar.stop()
            bar.grid_forget()
            l4.config(text = "Pobrano!")
            btn['state']='normal'


        def wybieranie():
            fdir = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                filetypes=(("PDF", "*.pdf"),
                                                           ("Wszystkie pliki", "*.*")))

            sql2 = "Select Strona from dane where Nazwa = %s"
            var2 = (combo.get(),)
            sql2_result = db_connect_and_fetch(sql2, var2)
            url = sql2_result[0][0]
            btn['state']='disabled'
            threading.Thread(target=worker_start, args=(fdir, url,)).start()

        bar = Progressbar(Frame2, orient=HORIZONTAL, length=100, mode='determinate')
        btn = Button(Frame2, text="Wybierz", command=wybieranie)
        btn.grid(column=1, row=1)
        Frame2.mainloop()


    def Pomoc():
        Frame4 = Tk()
        Frame4.title("Pomoc")
        Frame4.geometry('350x200')
        l = Label(Frame4, text="Aplikacja do ułatwiania życia studentom(Aużs)")
        l.grid(column=0, row=0)
        l2 = Label(Frame4, text="Służy ona do wyszukiwania prowadzących a następnie,")
        l2.grid(column=0, row=1)
        l3 = Label(Frame4, text="pobiera zawartość z ich stron i zapisuje do formatu pdf.")
        l3.grid(column=0, row=2)
        l = Label(Frame4, text="")
        l.grid(column=0, row=3)
        Frame4.mainloop()

    def Dod():
        def baza():
            sql = "Insert into dane (Nazwa,Strona) values (%s,%s)"
            var = (e.get(), e2.get())
            l = Label(f4, text="")
            l.grid(column=2, row=0)
            l2 = Label(f4, text="")
            l2.grid(column=2, row=1)
            l3 = Label(f4, text="")
            l3.grid(column=1, row=3)
            l4 = Label(f4, text="")
            l4.grid(column=1, row=3)
            if e.get() is "":
                l.config(text="Nazwa nie może być pusta!")
                l.after(3000, l.destroy)
            elif e2.get() is "":
                l2.config(text="Strona nie może być pusta!")
                l2.after(3000, l2.destroy)
            else:
                sql2 = "Select Nazwa,Strona from dane where Nazwa = %s AND Strona = %s"
                var2 = (e.get(), e2.get())
                sql2_result = db_connect_and_fetch(sql2, var2)
                i = 0
                for x in sql2_result:
                    i = i + 1
                print(i)
                if i is 0:
                    db_connect_and_exec(sql, var)
                    l3.config(text="Wpisano do bazy!")
                    l3.after(3000, l3.destroy)
                else:
                    l4.config(text="Te dane są już wpisane!")
                    l4.after(3000, l4.destroy)
            print(e.get())

        f4 = Tk()
        f4.title("Dodawanie Prowadzącego")
        f4.geometry('450x200+500+300')
        l = Label(f4, text="Wpisz tytuł i nazwisko: ")
        l.grid(column=0, row=0)
        e = Entry(f4)
        e.grid(column=1, row=0)
        l2 = Label(f4, text="Wpisz pełny adres strony: ")
        l2.grid(column=0, row=1)
        e2 = Entry(f4)
        e2.grid(column=1, row=1)
        b = Button(f4, text="Dodaj", command=baza)
        b.grid(column=1, row=2)
        f4.mainloop()

    def usun():
        # fetch lecturers from db
        lista = []
        sql = "Select Nazwa from dane"
        sql_result = db_connect_and_fetch(sql)
        for i in sql_result:
            lista.append(i)

        f5 = Tk()
        f5.geometry("450x250+500+300")
        f5.title("Usuwanie Nazwy")
        la1 = Label(f5, text="Wybierz prowadzącego")
        la1.grid(column=0, row=0)
        box = Combobox(f5)
        box.grid(column=1,row=0)
        box['values'] = lista
        box.current(0)

        def baza():
            l = Label(f5,text="")
            l.grid(column=1,row=2)
            sql2 = "Select * from dane where Nazwa = %s"
            var2 = (box.get(), )
            sql2_result = db_connect_and_fetch(sql2,var2)
            i = 0
            for x in sql2_result:
                i = i + 1
            if i is 0:
                l.config(text="Nie ma takiego rekordu")
                l.after(3000,l.destroy)
            else:
                sql3 = "Delete from dane where Nazwa = %s"
                var3 = (box.get(), )
                db_connect_and_exec(sql3, var3)
                l.config(text="Usunięto poprawnie!")
                l.after(3000, l.destroy)

        b = Button(f5,text="Usun", command = baza)
        b.grid(column=1,row=1)
        f5.mainloop()

    ni.add_command(label='Lista Prowadzących', command=Prowadz)
    ni.add_command(label="Dodaj prowadzącego", command=Dod)
    ni.add_command(label="Usuń prowadzącego", command=usun)
    m.add_cascade(label='Opcje', m=ni)
    ni2 = Menu(m)
    ni2.add_command(label='Podstawowa pomoc', command=Pomoc)
    m.add_cascade(label='Pomoc', m=ni2)
    F.config(menu=m)
    F.mainloop()


Frame1()
