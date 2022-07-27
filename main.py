# -*- coding: utf-8 -*-

import sys

import yt_dlp
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

from static.QtUI.freetubedownloader import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(800, 620)
        self.setFocus()
        self.linksEdit.setPlainText("")
        self.statusBar.setStyleSheet("background-color : white")

        self.urls = []
        self.out_dir = 'NODIR'
        try:
            f = open('lastoutput.txt', 'r').readlines()
            f = f[0].strip()
            self.out_dir = f
            self.OutEdit.setText(self.out_dir)
        except Exception as e:
            self.check()

        self.VideoButton.clicked.connect(self.video_download_button)
        self.AudioButton.clicked.connect(self.audio_download_button)
        self.BrowseButton.clicked.connect(self.browse_button)

    def video_download(self, url, out):
        ydl_opts = {
            'outtmpl': f'{out}%(title)s' + '.mp4',
            'overwrites': True
        }
        ydl = yt_dlp.YoutubeDL(ydl_opts)

        try:
            ydl.download(url)
        except Exception as e:
            return e

    def audio_download(self, url, out):
        ydl_opts = {
            'format': 'mp3/bestaudio/best',
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'ffmpeg_location': 'static/ffmpeg/bin/',
            'overwrites': True,
            'outtmpl': f'{out}%(title)s' + '.mp3'
        }
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        try:
            ydl.download(url)
        except Exception as e:
            return e

    def get_urls(self):
        text = self.linksEdit.toPlainText()
        urls = text.split('\n')
        self.urls = urls

    def video_download_button(self):
        self.get_urls()
        if self.check():
            self.statusBar.showMessage('Downloading!')
            self.statusBar.setStyleSheet("background-color : yellow")
            self.statusBar.repaint()
            self.video_download(self.urls, self.out_dir)
            self.statusBar.showMessage('Done!')
            self.statusBar.setStyleSheet("background-color : green")

    def audio_download_button(self):
        self.get_urls()
        if self.check():
            self.statusBar.showMessage('Downloading!')
            self.statusBar.setStyleSheet("background-color : yellow")
            self.statusBar.repaint()
            self.audio_download(self.urls, self.out_dir)
            self.statusBar.showMessage('Done!')
            self.statusBar.setStyleSheet("background-color : green")

    def browse_button(self):
        self.statusBar.setStyleSheet("background-color : white")
        self.statusBar.clearMessage()
        self.statusBar.repaint()
        self.out_dir = QFileDialog.getExistingDirectory(self, 'Browse output directory', '') + '/'
        self.OutEdit.setText(self.out_dir)
        f = open('lastoutput.txt', 'w')
        f.write(self.out_dir)
        f.close()

    def check(self):
        if self.out_dir == 'NODIR':
            self.statusBar.setStyleSheet("background-color : pink")
            self.statusBar.showMessage('Please browse your output directory!')
            return False
        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
