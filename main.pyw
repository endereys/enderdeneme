from PyQt5.QtWidgets import QApplication,QWidget,QDialog,QMessageBox
import pyqtgraph,sys
import giris,matplotlib.pyplot as plt
import os
import anaSayfa,datetime,ogrenciEkleDialog,threading

os.chdir("ogrenciler")
ogrenciVerileri = {}
def dosyadanAl():
    for dosya in os.listdir("."):
        fp = open(dosya,"r")
        adi,soyadi = fp.readlines()[:2]
        ogrenciVerileri[adi.strip()+soyadi.strip()] = dosya
        fp.close()

dosyadanAl()

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
        super(anaSayfaPencere, self).__init__()
        self.ui = anaSayfa.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.tableWidgetDersProgrami.currentCellChanged.connect(self.duzenle)
        self.ui.listWidgetTytDeneme.itemDoubleClicked.connect(self.denemeSecildi)
        self.denemeVerileriniAl()
        self.grafikCiz()


    def grafikCiz(self):
        self.ui.widgetTytGrafik.plot(list(range(1,self.tytdenemesayisi+1)),self.tyty)
        self.ui.widgetAytGrafik.plot(list(range(1,self.aytdenemesayisi+1)),self.ayty)

    def denemeSecildi(self):
        pass

    def denemeVerileriniAl(self):
        self.denemeSonuclari = self.kisiDosya.readlines()[2:]
        print(self.denemeSonuclari)
        if len(self.denemeSonuclari):
            for deneme in self.denemeSonuclari:
                if deneme.split(",")[0] == "tyt":
                    self.ui.listWidgetTytDeneme.addItem(deneme)
                    self.tytdenemesayisi+=1
                    self.tyty.append(int(deneme.split(",")[2]))
                else:
                    self.ui.listWidgetAytDeneme.addItem(deneme)
                    self.aytdenemesayisi+=1
                    self.ayty.append(int(deneme.split(",")[2]))


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