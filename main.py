# -*- coding: utf-8 -*-

import sys

import yt_dlp
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtGui
from static.QtUI.freetubedownloader import Ui_MainWindow
import os


class MainWindow(QMainWindow, Ui_MainWindow):

    def progresshook(self, d):
        if d['status'] == 'finished':
            file_tuple = os.path.split(os.path.abspath(d['filename']))
            print("Done downloading {}".format(file_tuple[1]))
        if d['status'] == 'downloading':
            filename = d['filename']
            if len(filename[:-14]) > 70:
                filename = filename[:70] + '...'
            else:
                filename = filename[:-14]
            self.statusBar.showMessage(f"Downloading {filename} {d['_percent_str']} ETA: {d['_eta_str']}")
            self.statusBar.setStyleSheet("background-color : yellow; color: #323232")
            self.statusBar.repaint()
            print(d['filename'], d['_percent_str'], d['_eta_str'])

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(800, 620)
        self.setWindowIcon(QtGui.QIcon('static/img/icon.ico'))
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
            'overwrites': True,
            'progress_hooks': [self.progresshook],
            'ignoreerrors': True
        }
        ydl = yt_dlp.YoutubeDL(ydl_opts)

        try:
            ydl.download(url)
        except Exception as e:
            print(e, e, e)
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
            'outtmpl': f'{out}%(title)s' + '.mp3',
            'progress_hooks': [self.progresshook],
            'ignoreerrors': True
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
            self.video_download(self.urls, self.out_dir)
            self.statusBar.showMessage('Done!')
            self.statusBar.setStyleSheet("background-color : green; color: #eff0f1")

    def audio_download_button(self):
        self.get_urls()
        if self.check():
            self.audio_download(self.urls, self.out_dir)
            self.statusBar.showMessage('Done!')
            self.statusBar.setStyleSheet("background-color : green; color: #eff0f1")

    def browse_button(self):
        self.statusBar.setStyleSheet("background-color : #323232")
        self.statusBar.clearMessage()
        self.statusBar.repaint()
        self.out_dir = QFileDialog.getExistingDirectory(self, 'Browse output directory', '') + '/'
        self.OutEdit.setText(self.out_dir)
        f = open('lastoutput.txt', 'w')
        f.write(self.out_dir)
        f.close()

    def check(self):
        if self.out_dir == 'NODIR':
            self.statusBar.setStyleSheet("background-color : pink; color: #323232")
            self.statusBar.showMessage('Please browse your output directory!')
            return False
        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
