import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QSystemTrayIcon, QMenu, QAction,qApp
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QCursor
import random
import math

class ScreenMate(QMainWindow):
    def __init__(self):
        super(ScreenMate, self).__init__()
        self.initUI()

    def initUI(self):
        # 창 투명도 설정
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        #self.setWindowIcon(QIcon(AWAKE_PNG+"1.png"))
        self.setWindowTitle("HungryCatMate")

        #고양이 설정
        label = QLabel(self)
        pixmap = QPixmap("./sprites/HungryCat_left")  # 이미지 경로 설정
        label.setPixmap(pixmap)
        label.setGeometry(0, 0, pixmap.width(), pixmap.height())
        self.cat = label

        label = QLabel(self)
        pixmap = QPixmap("./sprites/fish")
        label.setPixmap(pixmap)
        label.setGeometry(0, 0, pixmap.width(), pixmap.height())
        self.fish = label
        self.fish.setHidden(True)
        self.isFish = False
        self.direction = random.randrange(0,360)
        self.showMaximized()
        self.SetTimer()
            
    def SetTimer(self):
        self.timer1 = QTimer()
        self.timer2 = QTimer()
        self.timer3 = QTimer()
        self.catfishtimer = QTimer()
        self.timer1.timeout.connect(self.moveImage)
        self.timer2.timeout.connect(self.moveCat)
        self.timer3.timeout.connect(self.stop)

        self.timer1.start(random.randrange(8000,10000))
        
        self.timer3.start(random.randrange(3000,6000))

    def moveImage(self):
        self.direction = random.randrange(0,360)
        if self.direction < 180:
            self.cat.setPixmap(QPixmap("./sprites/HungryCat_left"))
        else:
            self.cat.setPixmap(QPixmap("./sprites/HungryCat_right"))
        self.timer2.start(35)
        
    def moveCat(self):
        position = self.cat.pos()
        
        new_x = position.x()
        new_y = position.y()
        speed = 4
        new_x += int(math.cos(math.radians(self.direction))*speed)
        new_y += int(math.sin(math.radians(self.direction))*speed)

        
        if new_x > QApplication.desktop().width():
            new_x = QApplication.desktop().width()
        elif new_x < 0:
            new_x = 0
        
        if new_y > QApplication.desktop().height():
            new_y = QApplication.desktop().height()
        elif new_y < 0:
            new_y = 0
        
        print(new_x)
        print(new_y)
        self.cat.move(new_x,new_y)
    
    def stop(self):
        self.timer2.stop()
    
    def changeImage(self,img_path):
        pixmap = QPixmap(img_path)
        self.cat.setPixmap(pixmap)

    def takeFish(self):
        self.isFish = False
        self.fish.setHidden(False)
        self.fishmovetimer = QTimer(self)
        self.fishmovetimer.timeout.connect(self.moveFishToCusor)
        self.fishmovetimer.start(10)
        
    def moveFishToCusor(self):
        self.fish.move(QCursor.pos() - QPoint(self.fish.width()//2, self.fish.height()//2))
        
        
    def mousePressEvent(self,event):
        self.isFish = True
        self.fishmovetimer.stop()
        self.findFish()
    
    def findFish(self):
        self.timer1.stop()
        self.timer2.stop()
        self.timer3.stop()
        self.catfishtimer.timeout.connect(self.moveCatToFish)
        self.catfishtimer.start(500)
        direction = self.fish.pos() - self.cat.pos()
        if(direction.x() >= 0):
            self.cat.setPixmap(QPixmap("./sprites/HungryCat_red_right"))
        else:
            self.cat.setPixmap(QPixmap("./sprites/HungryCat_red_left"))
            
    
    def moveCatToFish(self):
        if self.isFish == False:
            self.SetTimer()
            self.catfishtimer.stop()
            self.cat.setPixmap(QPixmap("./sprites/HungryCat_right"))
            return
            
        self.catfishtimer.start(15)
        direction = self.fish.pos() - self.cat.pos()
        direction_length = direction.manhattanLength()
        if direction_length < 5:
            self.catfishtimer.stop()
            self.eatFish()
            return
        
        unit_direction = direction / direction_length
        speed = 3
        new_pos = self.cat.pos() + speed*unit_direction
        self.cat.move(new_pos)
    
    def eatFish(self):
        self.isFish = False
        self.cat.setPixmap(QPixmap("./sprites/HungryCat_right"))
        self.SetTimer()
        self.fish.setHidden(True)

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self,icon,app,parent=None):
        super(SystemTrayIcon,self).__init__(icon,parent)
        self.setToolTip("HungryCatMate")
        
        menu = QMenu(parent)
        
        exitAction = QAction("Exit",self)
        exitAction.triggered.connect(qApp.quit)
        menu.addAction(exitAction)

        fishAction = QAction(QIcon("./sprites/fish"),"Give Fish",self)
        fishAction.triggered.connect(app.takeFish)
        menu.addAction(fishAction)
        
        
        self.setContextMenu(menu)

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = ScreenMate()
    icon = QIcon("./sprites/HungryCat_left")
    tray = SystemTrayIcon(icon,ex)
    tray.show()
    ex.show()
    sys.exit(app.exec_())
