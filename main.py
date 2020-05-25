from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename
from tkinter.ttk import *
import requests, pdfkit, time, threading


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
    l5 = Label(F, text="Ver.1.1")
    l5.grid(column=0, row=4)
    F.title("AUŻS")
    m = Menu(F)
    ni = Menu(m)


    def Prowadz():
        Frame2 = Tk()
        Frame2.title("Wybieranie prowadzącego: ")
        Frame2.geometry('450x200')
        Frame2.resizable(0, 0)
        l1 = Label(Frame2, text="Wybierz prowadzącego: ")
        l1.grid(column=0, row=0)

        combo = Combobox(Frame2)
        combo.grid(column=1, row=0)
        combo['values'] = ("Dr Zawada", "Dr Gołębiewski")
        combo.current(0)
        l2 = Label(Frame2, text="Wybierz prowadzacego lub wpisz URL")
        l2.grid(column=1, row=2)
        l3 = Label(Frame2, text = "")
        l3.grid(column=1,row=3)
        l4 = Label(Frame2, text = "")
        l4.grid(column=1,row=5)


        def worker_start(fdir):
            l4.config(text = "")
            l3.config(text = "Trwa pobieranie, czekaj...")
            bar.grid(column=1,row=4)

            if combo.get() == "Dr Zawada":
                url = 'https://cs.pwr.edu.pl/zawada/kwjp/'
            elif combo.get() == "Dr Gołębiewski":
                url = 'https://cs.pwr.edu.pl/golebiewski/#teaching/1920/aisd.php'
            else:
                url = combo.get()

            bar.start()
            pdfkit.from_url(url, fdir)
            bar.stop()
            bar.grid_forget()
            l4.config(text = "Pobrano!")
            btn['state']='normal'


        def wybieranie():
            fdir = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=(("PDF", "*.pdf"), ("Wszystkie pliki", "*.*")))
            print(fdir)

            btn['state']='disabled'
            threading.Thread(target=worker_start, args=(fdir,)).start()

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


    ni.add_command(label='Lista Prowadzących', command=Prowadz)
    m.add_cascade(label='Opcje', m=ni)
    ni2 = Menu(m)
    ni2.add_command(label='Podstawowa pomoc', command=Pomoc)
    m.add_cascade(label='Pomoc', m=ni2)
    F.config(menu=m)
    F.mainloop()


Frame1()
