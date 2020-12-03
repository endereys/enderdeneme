from PyQt5.QtWidgets import QApplication,QWidget,QDialog,QMessageBox,QTableWidgetItem
import pyqtgraph,sys
import giris
import os
import anaSayfa,datetime,ogrenciEkleDialog,threading,requests,bs4
import tytDenemeDialog,aytDenemeDialog,sonuc
import webbrowser as wb


if not os.path.isdir("ogrenciler"):
    os.mkdir("ogrenciler")
os.chdir("ogrenciler")
ogrenciVerileri = {}
def dosyadanAl():
    for dosya in os.listdir("."):
        fp = open(dosya,"r")
        adi,soyadi = fp.readlines()[:2]
        ogrenciVerileri[adi.strip()+soyadi.strip()] = dosya
        fp.close()

dosyadanAl()

class sonucPencere(QDialog):

    def __init__(self,puan,siralama):
        super(sonucPencere, self).__init__()
        self.ui = sonuc.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.label.setText(str(puan))
        self.ui.label_2.setText(str(siralama))


class tytDenemeEklePencere(QDialog):

    def __init__(self):
        super(tytDenemeEklePencere, self).__init__()
        self.ui = tytDenemeDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButtonTamam.clicked.connect(self.tamam)

    def tamam(self):
        veriler = []
        veriler.append(self.ui.spinBoxSosyal.value())
        veriler.append(self.ui.spinBoxTurkce.value())
        veriler.append(self.ui.spinBoxMatematik.value())
        veriler.append(self.ui.spinBoxFizik.value())
        veriler.append(self.ui.spinBoxBiyoloji.value())
        veriler.append(self.ui.spinBoxKimya.value())
        self.veriler = veriler
        self.accept()

class aytDenemeEklePencere(QDialog):

    def __init__(self):
        super(aytDenemeEklePencere, self).__init__()
        self.ui = tytDenemeDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButtonTamam.clicked.connect(self.tamam)

    def tamam(self):
        veriler = []
        veriler.append(self.ui.spinBoxSosyal.value())
        veriler.append(self.ui.spinBoxTurkce.value())
        veriler.append(self.ui.spinBoxMatematik.value())
        veriler.append(self.ui.spinBoxFizik.value())
        veriler.append(self.ui.spinBoxBiyoloji.value())
        veriler.append(self.ui.spinBoxKimya.value())
        self.veriler = veriler
        self.accept()

class ogrenciEklePencere(QDialog):

    def __init__(self):
        super(ogrenciEklePencere, self).__init__()
        self.ui = ogrenciEkleDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButtonTamam.clicked.connect(self.tamam)

    def tamam(self):
        isim = self.ui.lineEditIsim.text().lower()
        soyisim = self.ui.lineEditSoyIsim.text().lower()
        if len(isim)>0 and len(soyisim)>0:
            dosyaismi = isim+soyisim
            dosya = open(dosyaismi+".txt","w")
            dosya.write(isim+"\n"+soyisim)
            dosya.close()
            self.accept()
        else:
            QMessageBox.warning(self,"HATA","Düzgün Veri Giriniz")
            self.reject()

class anaSayfaPencere(QDialog):

    def __init__(self,kisiDosya):
        self.tytdenemesayisi = 0
        self.aytdenemesayisi = 0
        self.ayty = []
        self.tyty = []
        self.kisiDosya = open(kisiDosya,"r+")
        self.kisiDosyaStr = kisiDosya
        super(anaSayfaPencere, self).__init__()
        self.ui = anaSayfa.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.tableWidgetDersProgrami.currentCellChanged.connect(self.duzenle)
        self.ui.listWidgetTytDeneme.itemDoubleClicked.connect(self.denemeSecildi)
        self.ui.pushButtonTytDenemeEkle.clicked.connect(self.tytDenemeEkle)
        self.ui.pushButtonAytDenemeEkle.clicked.connect(self.aytDenemeEkle)
        self.ui.pushButtonHesapla.clicked.connect(self.siralamaHesapla)
        self.ui.pushButtonKaydet.clicked.connect(self.kaydetDersProgrami)
        self.denemeVerileriniAl()
        self.grafikCiz()
        self.dersProgramiCek()

    def dersProgramiCek(self):
        self.ui.tableWidgetDersProgrami.clear()
        f = open(self.kisiDosyaStr,"r")
        veriler = f.readlines()[2:]
        for veri in veriler:
            if veri[0].isnumeric():
                ss,program = veri.split(":")
                satir,sutun = ss.split(",")
                self.ui.tableWidgetDersProgrami.setItem(int(satir),int(sutun),QTableWidgetItem(program))
        f.close()

    def kaydetDersProgrami(self):
        f = open(self.kisiDosyaStr,"a")
        for satir in range(0,10):
            for sutun in range(0,7):
                if self.ui.tableWidgetDersProgrami.item(int(satir),int(sutun)):
                    print("a")
                    f.write("\n%s,%s:%s"%(satir,sutun,self.ui.tableWidgetDersProgrami.item(int(satir),int(sutun)).text()))

        f.close()


    def siralamaHesapla(self):
        wb.open("https://puango.net/")

    def tytDenemeEkle(self):
        self.kisiDosya = open(self.kisiDosyaStr,"a")
        tarih = datetime.date.today()
        eklePencere = tytDenemeEklePencere()
        if eklePencere.exec_():
            toplamnet = 0
            for net in eklePencere.veriler:
                toplamnet+=int(net)
            tarihs = "%s:%s:%s"%(tarih.day,tarih.month,tarih.year)
            self.kisiDosya.write("\n"+"tyt,"+tarihs+","+str(toplamnet))
            self.kisiDosya.close()
            self.denemeVerileriniAl()
            self.grafikCiz()

    def aytDenemeEkle(self):
        self.kisiDosya = open(self.kisiDosyaStr,"a")
        tarih = datetime.date.today()
        eklePencere = tytDenemeEklePencere()
        if eklePencere.exec_():
            toplamnet = 0
            for net in eklePencere.veriler:
                toplamnet+=int(net)
            tarihs = "%s:%s:%s"%(tarih.day,tarih.month,tarih.year)
            self.kisiDosya.write("\n"+"ayt,"+tarihs+","+str(toplamnet))
            self.kisiDosya.close()
            self.denemeVerileriniAl()
            self.grafikCiz()


    def grafikCiz(self):
        self.ui.widgetTytGrafik.plot(list(range(1,self.tytdenemesayisi+1)),self.tyty)
        self.ui.widgetAytGrafik.plot(list(range(1,self.aytdenemesayisi+1)),self.ayty)

    def denemeSecildi(self):
        pass

    def denemeVerileriniAl(self):
        self.tytdenemesayisi = 0
        self.aytdenemesayisi = 0
        self.ayty = []
        self.tyty = []
        self.kisiDosya = open(self.kisiDosyaStr, "r")
        self.denemeSonuclari = self.kisiDosya.readlines()[2:]
        self.ui.listWidgetTytDeneme.clear()
        self.ui.listWidgetAytDeneme.clear()
        if len(self.denemeSonuclari):
            for deneme in self.denemeSonuclari:
                if deneme.split(",")[0] == "tyt":
                    self.ui.listWidgetTytDeneme.addItem(deneme)
                    self.tytdenemesayisi+=1
                    self.tyty.append(int(deneme.split(",")[2]))
                elif deneme.split(",")[0] == "ayt":
                    self.ui.listWidgetAytDeneme.addItem(deneme)
                    self.aytdenemesayisi+=1
                    self.ayty.append(int(deneme.split(",")[2]))
        self.kisiDosya.close()


    def duzenle(self):
        sutun = self.ui.tableWidgetDersProgrami.currentColumn()
        satir = self.ui.tableWidgetDersProgrami.currentRow()
        veri = self.ui.tableWidgetDersProgrami.item(satir,sutun)
        if veri:
            if len(veri.text()) > 20:
                self.ui.tableWidgetDersProgrami.item(satir,sutun).setText(veri.text()+"\n")

class girisPencere(QDialog):

    def __init__(self):
        super(girisPencere, self).__init__()
        self.ui = giris.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.listWidgetOgrenciler.addItems(list(ogrenciVerileri.keys()))
        self.ui.listWidgetOgrenciler.doubleClicked.connect(self.secildi)
        self.ui.pushButtonEkle.clicked.connect(self.ogrenciEkle)
        self.ui.pushButtonSil.clicked.connect(self.ogrenciSil)

    def ogrenciEkle(self):
        p = ogrenciEklePencere()
        if p.exec_():
            dosyadanAl()
            self.ui.listWidgetOgrenciler.addItem(list(ogrenciVerileri.keys())[-1])

    def ogrenciSil(self):
        seciliogrenci = self.ui.listWidgetOgrenciler.item(self.ui.listWidgetOgrenciler.currentRow())
        if seciliogrenci:
            os.remove(ogrenciVerileri[seciliogrenci.text()])
            self.ui.listWidgetOgrenciler.takeItem(self.ui.listWidgetOgrenciler.currentRow())


    def secildi(self):
        secilenKisi = list(ogrenciVerileri.keys())[self.ui.listWidgetOgrenciler.currentIndex().row()]
        secilenDosya = ogrenciVerileri[secilenKisi]
        self.destroy()
        anaSayfaPencere(secilenDosya).exec_()

uyg = QApplication(sys.argv)
pencere = girisPencere()
pencere.show()
uyg.exec_()