import os
from PyQt6.QtWidgets import (
   QApplication, QWidget, QMainWindow,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt6.QtCore import Qt # потрібна константа Qt.KeepAspectRatio для зміни розмірів із збереженням пропорцій
from PyQt6.QtGui import QPixmap # оптимізована для показу на екрані картинка
 
from PIL import Image
from PIL.ImageQt import ImageQt # Для перенесення графіки з Pillow до QT
from PIL import ImageFilter
from PIL.ImageFilter import SHARPEN
from ui import *
class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.workdir = ''
        self.workimage = ImageProcessor(self)

        '''Запуск програми'''
        self.ui.btn_dir.clicked.connect(self.showFilenamesList)
        self.ui.Iw_files.currentRowChanged.connect(self.showChosenImage)
        
        self.ui.btn_bw.clicked.connect(self.workimage.do_bw)
        self.ui.btn_left.clicked.connect(self.workimage.do_left)
        self.ui.btn_right.clicked.connect(self.workimage.do_right)
        self.ui.btn_shape.clicked.connect(self.workimage.do_sharpen)
        self.ui.btn_flip.clicked.connect(self.workimage.do_flip)

    def filter(self,files, extensions):
        result = []
        for filename in files:
            for ext in extensions:
                if filename.endswith(ext):
                    result.append(filename)
        return result
    
    def chooseWorkdir(self):
        self.workdir = QFileDialog.getExistingDirectory()
    
    def showFilenamesList(self):
        extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
        self.chooseWorkdir()
        if self.workdir:
            filenames = self.filter(os.listdir(self.workdir), extensions)
            self.ui.Iw_files.clear()
            self.ui.Iw_files.addItems(filenames)
    
    def showChosenImage(self):
        if self.ui.Iw_files.currentRow() >= 0:
            filename = self.ui.Iw_files.currentItem().text()
            self.workimage.loadImage(filename)
            self.workimage.showImage(os.path.join(self.workdir, self.workimage.filename))
    
 
class ImageProcessor():
    def __init__(self, widget):
        self.widget = widget
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
 
    def loadImage(self, filename):
        ''' під час завантаження запам'ятовуємо шлях та ім'я файлу '''
        self.filename = filename
        fullname = os.path.join(self.widget.workdir, filename)
        self.image = Image.open(fullname)
 
    def saveImage(self):
        ''' зберігає копію файлу у підпапці '''
        path = os.path.join(self.widget.workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
  
        self.image.save(fullname)
 
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.widget.workdir, self.save_dir, self.filename)
        self.showImage(image_path)
 
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.widget.workdir, self.save_dir, self.filename)
        self.showImage(image_path)
 
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.widget.workdir, self.save_dir, self.filename)
        self.showImage(image_path)
 
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.widget.workdir, self.save_dir, self.filename)
        self.showImage(image_path)
 
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.widget.workdir, self.save_dir, self.filename)
        self.showImage(image_path)
 
    def showImage(self, path):
        #self.ui.lb_image.hide()
        image_path = os.path.join(self.widget.workdir, self.save_dir, self.filename)
        pixmapimage = QPixmap(image_path)
        w, h = self.widget.ui.Ib_image.width(), self.widget.ui.Ib_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        self.widget.ui.Ib_image.setPixmap(pixmapimage)
        self.widget.ui.Ib_image.show()
 
    
app = QApplication([])
ex = Widget()
ex.show()
app.exec()