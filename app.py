#app exec file

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, \
  QWidget, QPushButton, QTableWidget, QTableWidgetItem, QInputDialog, QFileDialog, QSizePolicy
from PyQt5 import uic
import sys
import subprocess

class VideoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        uic.loadUi("app.ui", self)

        self.inp_video = self.findChild(QLabel, "inpvideo")
        self.filenames = []

        self.uploadbutton = self.findChild(QPushButton, "uploadbutton")
        self.removebutton  = self.findChild(QPushButton, "removevideo")
        self.au_button = self.findChild(QPushButton, "startextract")
        self.errorLabel = self.findChild(QLabel, "errorlabel")
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        self.au_button.clicked.connect(self.action_unit)
        self.uploadbutton.clicked.connect(self.open_file)
        self.removebutton.clicked.connect(self.remove_file)

        self.show()


    def open_file(self):
        path = QFileDialog.getOpenFileNames(
            self, # parent widget
            'Video', # window title
            '', # entry label
            'All Files (*.*)'
        )
        self.filenames = path[0]
        if path != ('', ''):
            self.inp_video.setText('Input video(s): {}'.format(','.join([pth.split('/')[-1] for pth in path[0]])))
    def remove_file(self):
        self.filenames = []
        self.inp_video.setText('Input video(s): ')

    def action_unit(self):
        if self.filenames == []:
            self.errorLabel.setText("Error: Input video first")
        else:
            subprocess.run("/home/sunidhi/Desktop/zurichproj/OpenFace/build/bin/FaceLandmarkVidMulti -vis-track -vis-aus -pose -aus -f \"{}\"".format('\" -f \"'.join(self.filenames)), shell = True)
            import AUtoEmotion as au
            import FrequencyAnalysis as freqan
            for file in self.filenames:
                filename = file.split("/")[-1]
                filename = filename.partition(".")[0]
                # print(filename)
                arg = "~/Desktop/zurichproj/GUIEmotionAnalysis/processed/{}.csv".format(filename)
                # print(au.ExtractEmotion(arg))
                self.emos, extractedpath = au.ExtractEmotion(arg)
                freqan.FreqAnalysis(extractedpath)
                # return (res)

# -pose -gaze -verbose

if __name__ == '__main__':
    app = QApplication([])
    player = VideoWindow()
    app.exec_()