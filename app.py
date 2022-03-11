#app exec file

# from asyncio.windows_events import None
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, \
  QWidget, QPushButton, QTableWidget, QTableWidgetItem, QInputDialog, QFileDialog, QSizePolicy, QScrollArea, QDoubleSpinBox
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap
import sys
import subprocess
import time

class VideoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        uic.loadUi("app.ui", self)

        self.inp_video = self.findChild(QLabel, "inpvideo")
        self.filenames = []

        self.uploadbutton = self.findChild(QPushButton, "uploadbutton")
        self.removebutton  = self.findChild(QPushButton, "removevideo")
        self.start_extract_bin = self.findChild(QPushButton, "startextractbin")
        self.start_extract_con = self.findChild(QPushButton, "startextractcon")
        self.errorLabel = self.findChild(QLabel, "errorlabel")
        self.image_au = self.findChild(QLabel, "image_au")
        self.hyper_area = self.findChild(QScrollArea, "hyperscroll")
        self.binary = self.findChild(QPushButton,"binary")
        self.continuous = self.findChild(QPushButton,"cont")
        self.AUint = self.findChild(QDoubleSpinBox, "AUint")
        self.poserx = self.findChild(QDoubleSpinBox, "poseRx")
        self.poserz = self.findChild(QDoubleSpinBox, "poseRx")
        self.indanalysis = self.findChild(QPushButton, "indanalysis")
        self.comanalysis = self.findChild(QPushButton, "comanalysis")

        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)
        self.image_au.setPixmap(QPixmap("Facial-action-units-for-upper-and-lower-part-of-the-face-10.png"))
        self.start_extract_bin.clicked.connect(self.action_unit_bin)
        self.start_extract_con.clicked.connect(self.action_unit_con)
        self.uploadbutton.clicked.connect(self.open_file)
        self.removebutton.clicked.connect(self.remove_file)
        self.binary.clicked.connect(self.unhide_bin)
        self.continuous.clicked.connect(self.unhide_con)
        self.indanalysis.clicked.connect(self.ind_analysis)

        self.bin_hidden = True
        self.con_hidden = True
        self.extractedpath = [""]*1000

        self.show()
        self.start_extract_bin.hide()
        self.hyper_area.hide()

    def unhide_bin(self):
        if self.bin_hidden:
            self.start_extract_bin.show()
            self.bin_hidden = False
            self.hide_con()
        self.errorLabel.hide()
    
    def unhide_con(self):
        if self.con_hidden:
            self.hyper_area.show()
            self.con_hidden = False
            self.hide_bin()
        self.errorLabel.hide()
    
    def hide_bin(self):
        if self.bin_hidden == False:
            self.start_extract_bin.hide()
            self.bin_hidden = True
        self.errorLabel.hide()
    
    def hide_con(self):
        if self.con_hidden == False:
            self.hyper_area.hide()
            self.con_hidden = True
        self.errorLabel.hide()


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
        self.errorLabel.hide()
        
    def remove_file(self):
        self.filenames = []
        self.inp_video.setText('Input video(s): ')
        self.errorLabel.hide()

    def ind_analysis(self):
        import FrequencyAnalysis as freqan
        i = 0
        for file in self.filenames:
            freqan.FreqAnalysis(self.extractedpath[i])
            i += 1

    def action_unit_bin(self):
        if self.filenames == []:
            self.errorLabel.show()
            self.errorLabel.setText("Error: Input video first")
        else:
            subprocess.run("/home/sunidhi/Desktop/zurichproj/OpenFace/build/bin/FaceLandmarkVidMulti -vis-track -vis-aus -pose -aus -f \"{}\"".format('\" -f \"'.join(self.filenames)), shell = True)
            import AUtoEmotion as au
            i = 0
            for file in self.filenames:
                filename = file.split("/")[-1]
                filename = filename.partition(".")[0]
                # print(filename)
                arg = "~/Desktop/zurichproj/GUIEmotionAnalysis/processed/{}.csv".format(filename)
                # print(au.ExtractEmotion(arg))
                self.emos, self.extractedpath[i] = au.ExtractEmotion(arg, None, None, None)
                # freqan.FreqAnalysis(extractedpath)
                i += 1
            self.errorLabel.hide()

    def action_unit_con(self):
        if self.filenames == []:
            self.errorLabel.show()
            self.errorLabel.setText("Error: Input video first")
        else:
            subprocess.run("/home/sunidhi/Desktop/zurichproj/OpenFace/build/bin/FaceLandmarkVidMulti -vis-track -vis-aus -pose -aus -f \"{}\"".format('\" -f \"'.join(self.filenames)), shell = True)
            import AUtoEmotion as au
            i = 0
            for file in self.filenames:
                filename = file.split("/")[-1]
                filename = filename.partition(".")[0]
                # print(filename)
                arg = "~/Desktop/zurichproj/GUIEmotionAnalysis/processed/{}.csv".format(filename)
                # print(au.ExtractEmotion(arg))
                self.emos, self.extractedpath[i] = au.ExtractEmotion(arg, self.AUint.value(), self.poserx.value(), self.poserz.value())
                i += 1
            self.errorLabel.hide()

            
                # return (res)
# -pose -gaze -verbose


if __name__ == '__main__':
    app = QApplication([])
    player = VideoWindow()

    app.exec_()