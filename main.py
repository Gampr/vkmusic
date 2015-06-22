__author__ = 'ivan'

import sys, vk_api
from  PyQt5.QtWidgets import (QApplication, QSlider, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel,
                              QDialog, QMessageBox, QListWidget, QListWidgetItem)
from  PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from  PyQt5.QtCore import QUrl, Qt

class VKwindow(QWidget):

    def __init__(self, vkapi):
        super().__init__()
        self.vk = vkapi
        self.initUI()

    def initUI(self):
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.setGeometry(300, 300, 290, 150)
        self.slider = QSlider(Qt.Horizontal)
        self.playBtn = QPushButton('►')
        self.nextBtn = QPushButton('>')
        self.prevBtn = QPushButton('<')

        self.nextBtn.clicked.connect(self.nextSong)
        self.prevBtn.clicked.connect(self.prevSong)

        self.playBtn.clicked.connect(self.playSong)
        self.setWindowTitle('VK music')
        self.list = QListWidget(self)
        self.list.currentItemChanged.connect(self.selectSong)

        for track in self.vk.method('audio.get').get('items'):
            self.list.addItem(SongWidgetItem(track))
            self.playlist.addMedia(QMediaContent(QUrl(track['url'])))

        hbox.addWidget(self.prevBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.nextBtn)
        hbox.addWidget(self.slider)

        self.player.setPlaylist(self.playlist)
        self.player.positionChanged.connect(self.setPosition)
        vbox.addWidget(self.list)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.show()

    def selectSong(self, curr, prev):
        self.currentTrack = curr
        print(curr.getArtist())

    def playSong(self):
        print(self.currentTrack.getArtist())
        print(self.list.currentRow())
        if self.player.state() == QMediaPlayer.PlayingState and self.list.currentRow() == self.playlist.currentIndex():
            self.player.pause()
            return
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.play()
            return
        self.playlist.setCurrentIndex(self.list.currentRow())
        self.slider.setTickInterval(self.player.duration())
        self.player.play()

    def setPosition(self, pos):
        print(pos)
        self.slider.setTickPosition(pos)

    def nextSong(self):
        tmp = self.list.currentRow()
        size = self.list.count()
        tmp = (tmp + 1) % size
        self.list.setCurrentRow(tmp)
        self.playlist.setCurrentIndex(tmp)
        self.player.play()

    def prevSong(self):
        tmp = self.list.currentRow()
        size = self.list.count()
        tmp = (tmp - 1) % size
        self.list.setCurrentRow(tmp)
        self.playlist.setCurrentIndex(tmp)
        self.player.play()

class SongWidgetItem(QListWidgetItem):
    def __init__(self, track):
        label = track['artist'] + ' - ' + track['title']
        super().__init__(label)
        self.track = track

    def getURL(self):
        return self.track['url']

    def getArtist(self):
        return self.track['artist']



class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initDialog()

    def initDialog(self):
        vbox = QVBoxLayout()
        self.resize(300, 100)
        self.setWindowTitle('Login')
        self.loginBtn = QPushButton('Login', self)
        self.loginBtn.clicked.connect(self.loginClicked)

        self.loginEdit = QLineEdit(self)
        self.loginLabel = QLabel('Login')
        self.passwordEdit = QLineEdit(self)
        self.passwordLabel = QLabel('Password')
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        hboxLogin = QHBoxLayout()
        hboxLogin.addWidget(self.loginLabel)
        hboxLogin.addWidget(self.loginEdit)

        hboxPassword = QHBoxLayout()
        hboxPassword.addWidget(self.passwordLabel)
        hboxPassword.addWidget(self.passwordEdit)
        vbox.addLayout(hboxLogin)
        vbox.addLayout(hboxPassword)
        vbox.addWidget(self.loginBtn)
        self.setLayout(vbox)
        self.show()

    def loginClicked(self):
        try:
            lgn = str(self.loginEdit.text())
            pswd = str(self.passwordEdit.text())
            self.vkapi = vk_api.VkApi(login=lgn, password=pswd, api_version='4876954')
            self.vkapi.authorization()
            self.accept()
        except Exception as ex:
            QMessageBox.information(self, 'Fail', 'Can not to connect.\nPlease try again')

    def getAPI(self):
        return self.vkapi

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loginDialog = LoginDialog()
    if loginDialog.exec_() == QDialog.Accepted:
        window = VKwindow(loginDialog.getAPI())
    sys.exit(app.exec_())
