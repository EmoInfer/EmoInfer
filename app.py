#app exec file

# from asyncio.windows_events import None
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QStyle, \
  QWidget, QPushButton, QTableWidget, QTableWidgetItem, QInputDialog, QFileDialog, QSizePolicy, QScrollArea, QDoubleSpinBox, QHBoxLayout, QComboBox, QSlider
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
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
        self.progress = self.findChild(QLabel, "status")
        self.playBtn = self.findChild(QPushButton,"play")
        self.slider = self.findChild(QSlider,"slider")

        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)


        self.vidwidget = self.findChild(QVideoWidget,"vidplayer" )
        self.vidplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.vidplayer.setVideoOutput(self.vidwidget)

        self.start_extract_bin = self.findChild(QPushButton, "startextractbin")
        self.start_extract_con = self.findChild(QPushButton, "startextractcon")
        self.spinboxes = self.findChild(QWidget, "spinboxwidget")
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
        self.paper = self.findChild(QComboBox, "paper")
        self.emotion = self.findChild(QComboBox, "emotion")
        self.paperimg = self.findChild(QLabel,"paperimg")
        self.paperemo = self.findChild(QLabel,"paperemo")


        self.paper.addItem("Keltner et al., 2019")
        self.paper.addItem("Cordaro et al., 2018")
        self.paper.addItem("Du et al., 2014")

        emo_list =  [            'Amusement',             'Happiness',                   'Awe',
                                'Pride',              'Surprise',                 'Anger',
                            'Confused',              'Contempt',               'Disgust',
                        'Embarrassment',                  'Fear',                  'Pain',
                                'Shame',              'Interest',               'Sadness',
                    'Happily Surprised',     'Happily Disgusted',         'Sadly Fearful',
                        'Sadly Angry',       'Sadly Surprised',       'Sadly Disgusted',
                    'Fearfully Angry',   'Fearfully Surprised',   'Fearfully Disgusted',
                    'Angrily Surprised',     'Angrily Disgusted', 'Disgustedly Surprised',
                    'Appalled/Hatred']
        for emo in emo_list:
            self.emotion.addItem(emo)


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

        self.vidplayer.stateChanged.connect(self.mediastate_changed)
        self.vidplayer.positionChanged.connect(self.position_changed)
        self.vidplayer.durationChanged.connect(self.duration_changed)


        self.bin_hidden = True
        self.con_hidden = True
        self.extractedpath = [""]*1000

        self.show()
        self.start_extract_bin.hide()
        self.spinboxes.hide()
        self.start_extract_con.hide()

    def play_video(self):
        if self.vidplayer.state() == QMediaPlayer.PlayingState:
            self.vidplayer.pause()
 
        else:
            self.vidplayer.play()
 
 
    def mediastate_changed(self, state):
        if self.vidplayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
 
            )
 
        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
 
            )
 
    def position_changed(self, position):
        self.slider.setValue(position)
 
 
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
 
 
    def set_position(self, position):
        self.vidplayer.setPosition(position)
 

    def unhide_bin(self):
        if self.bin_hidden:
            self.start_extract_bin.show()
            self.bin_hidden = False
            self.hide_con()
        self.errorLabel.hide()
    
    def unhide_con(self):
        if self.con_hidden:
            # self.hyper_area.show()
            self.spinboxes.show()
            self.start_extract_con.show()
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
            # self.hyper_area.hide()
            self.spinboxes.hide()
            self.start_extract_con.hide()
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
            self.vidplayer.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(self.filenames[0])))
            # self.vidplayer.setVideoOutput(self.vidwidget)
            self.playBtn.setEnabled(True)
        self.errorLabel.hide()
        
    def remove_file(self):
        self.filenames = []
        self.inp_video.setText('Input video(s): ')
        self.errorLabel.hide()

    def ind_analysis(self):
        import FrequencyAnalysis as freqan
        i = 0
        # self.progress.setText("Aggregating data...")
        for file in self.filenames:
            freqan.FreqAnalysis(self.extractedpath[i], self.paper.currentText(), self.emotion.currentText())
            i += 1

        self.paperimg.setPixmap(QPixmap(f"{self.paper.currentText()}.png"))
        self.paperemo.setPixmap(QPixmap(f"{self.paper.currentText()}{self.emotion.currentText()}.png"))
        # self.progress.setText("")
        

    def action_unit_bin(self):
        if self.filenames == []:
            self.errorLabel.show()
            self.errorLabel.setText("Error: Input video first")
        else:
            # self.progress.setText("Extracting Emotions...")
            # -vis-track -vis-aus
            subprocess.run("/home/sunidhi/Desktop/zurichproj/OpenFace/build/bin/FaceLandmarkVidMulti -pose -aus -f \"{}\"".format('\" -f \"'.join(self.filenames)), shell = True)
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
            # self.progress.setText("Extraction results saved...")
            self.errorLabel.hide()

    def action_unit_con(self):
        if self.filenames == []:
            self.errorLabel.show()
            self.errorLabel.setText("Error: Input video first")
        else:
            # self.progress.setText("Extracting Emotions...")
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
            # self.progress.setText("Extraction results saved...")
            self.errorLabel.hide()

            
                # return (res)
# -pose -gaze -verbose


if __name__ == '__main__':
    app = QApplication([])
    player = VideoWindow()

    app.exec_()