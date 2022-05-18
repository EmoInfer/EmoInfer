#app exec file

# from asyncio.windows_events import None
from typing_extensions import Self
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QStyle, \
  QWidget, QPushButton, QTableWidget, QTableWidgetItem, QInputDialog, QFileDialog, QSizePolicy, QScrollArea, QDoubleSpinBox, QHBoxLayout, QComboBox, QSlider
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import subprocess
import time

from CheckableComboBox import CheckableComboBox

OpenFacePath = "/home/sunidhi/Desktop/zurichproj/OpenFace"

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

        self.videos_wid = CheckableComboBox()
        self.lay_vid.addWidget(self.videos_wid)

        # for i in range(12):
        #     att = getattr(self, "checkBox_{}".format(i+1))
        #     att.setHidden(True)


        self.paper.addItem("Cordaro et al., 2018")
        self.paper.addItem("Keltner et al., 2019")
        self.paper.addItem("Du et al., 2014")

        self.emo_list =  [            'Amusement',             'Happiness',                   'Awe',
                                'Pride',              'Surprise',                 'Anger',
                            'Confused',              'Contempt',               'Disgust',
                        'Embarrassment',                  'Fear',                  'Pain',
                                'Shame',              'Interest',               'Sadness',
                    'Happily Surprised',     'Happily Disgusted',         'Sadly Fearful',
                        'Sadly Angry',       'Sadly Surprised',       'Sadly Disgusted',
                    'Fearfully Angry',   'Fearfully Surprised',   'Fearfully Disgusted',
                    'Angrily Surprised',     'Angrily Disgusted', 'Disgustedly Surprised',
                    'Appalled/Hatred']
        for emo in self.emo_list[0:13]:
            self.emotion.addItem(emo)

        self.paper.currentTextChanged[str].connect(self.set_emo_dropdown)

        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)
        self.image_au.setPixmap(QPixmap("images/AU2.png"))
        self.label_8.setPixmap(QPixmap("images/headpose2.png"))
        self.start_extract_bin.clicked.connect(self.action_unit_bin)
        self.start_extract_con.clicked.connect(self.action_unit_con)
        self.uploadbutton.clicked.connect(self.open_file)
        self.removebutton.clicked.connect(self.remove_file)
        self.binary.clicked.connect(self.unhide_bin)
        self.continuous.clicked.connect(self.unhide_con)
        self.indanalysis.clicked.connect(self.ind_analysis)
        self.comanalysis.clicked.connect(self.com_analysis)
        self.show_analysis_fig.clicked.connect(self.show_analysis_figures)

        self.INDEPENDENT = 1
        self.COMBINED = 0

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
 
    def set_emo_dropdown(self, pap):
        self.emotion.clear()
        if pap == "Cordaro et al., 2018":
            self.emotion.addItems(self.emo_list[0:13])
        if pap == "Keltner et al., 2019":
            self.emotion.addItems(self.emo_list[0:15])
        if pap == "Du et al., 2014":
            self.emotion.addItems(self.emo_list)

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
        i = 0
        for file in self.filenames:
            filename = file.split("/")[-1]
            filename = filename.partition(".")[0]
            # att = getattr(self, "checkBox_{}".format(i+1))
            # att = getattr(self, "checkBox_{}".format(i+1))
            # att.setHidden(False)
            # att.setText(filename)
            i += 1
            self.videos_wid.addItem(filename)
        
    def remove_file(self):
        self.filenames = []
        self.inp_video.setText('Input video(s): ')
        self.errorLabel.hide()

    def ind_analysis(self):
        import FrequencyAnalysis as freqan
        self.INDEPENDENT = 1
        self.COMBINED = 0
        i = 0
        # self.progress.setText("Aggregating data...")
        # for file in self.videos_wid.currentData(self.videos_wid):
        #     freqan.FreqAnalysis(file, self.extractedpath[i], self.paper.currentText(), self.emotion.currentText())
        #     i += 1
        self.video_select.show()
        for i in range(self.videos_wid.model().rowCount()):
            if self.videos_wid.model().item(i).checkState() == Qt.Checked:
                filename = self.videos_wid.model().item(i).data()
                self.video_select.addItem(filename)
                freqan.FreqAnalysis(filename, "extracted/extracted_{}.csv".format(filename), self.paper.currentText(), self.emotion.currentText())
        # for file in self.filenames:
        #     filename = file.split("/")[-1]
        #     filename = filename.partition(".")[0]
        #     # att = getattr(self, "checkBox_{}".format(i+1))
        #     # if att.isChecked():
        #     #     self.video_select.addItem(filename)
        #     if self.videos_wid.model().item(i).checkState() == Qt.Checked:
        #         self.video_select.addItem(filename)
        #         freqan.FreqAnalysis(filename, self.extractedpath[i], self.paper.currentText(), self.emotion.currentText())
        #     i += 1
        # self.progress.setText("")
    def com_analysis(self):
        import CombinedAnalysis as coman
        self.INDEPENDENT = 0
        self.COMBINED = 1
        i = 0
        # for i in range(self.videos_wid.model().rowCount()):
        #     if self.videos_wid.model().item(i).checkState() == Qt.Checked:
        #         filename = self.videos_wid.model().item(i).data()
        #         self.video_select.addItem(filename)
        filenames = self.videos_wid.currentData()
        # self.video_select.addItems(filenames)
        self.video_select.clear()
        coman.CombFreqAnalysis(filenames, len(filenames))
        
    def show_analysis_figures(self):
        if self.INDEPENDENT == 1:
            self.paperimg.setPixmap(QPixmap(f"images/{self.paper.currentText()}_{self.video_select.currentText()}.png"))
            self.paperemo.setPixmap(QPixmap(f"images/{self.paper.currentText()}{self.emotion.currentText()}_{self.video_select.currentText()}.png"))
        else:
            name = ''.join(self.videos_wid.currentData())
            self.paperimg.setPixmap(QPixmap(f"images/{self.paper.currentText()}_{name}.png"))
            self.paperemo.setPixmap(QPixmap(f"images/{self.paper.currentText()}{self.emotion.currentText()}_{name}.png"))


    def action_unit_bin(self):
        if self.filenames == []:
            self.errorLabel.show()
            self.errorLabel.setText("Error: Input video first")
        else:
            # self.progress.setText("Extracting Emotions...")
            # -vis-track -vis-aus
            subprocess.run(OpenFacePath + "/build/bin/FaceLandmarkVidMulti -pose -aus -vis-track -vis-aus -f \"{}\"".format('\" -f \"'.join(self.filenames)), shell = True)
            import AUtoEmotion as au
            i = 0
            for file in self.filenames:
                filename = file.split("/")[-1]
                filename = filename.partition(".")[0]
                # print(filename)
                arg = "processed/{}.csv".format(filename)
                # print(au.ExtractEmotion(arg))
                self.emos, self.extractedpath[i] = au.ExtractEmotion(arg, filename, None, None, None)
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
            subprocess.run(OpenFacePath + "/build/bin/FaceLandmarkVidMulti -vis-track -vis-aus -pose -aus -f \"{}\"".format('\" -f \"'.join(self.filenames)), shell = True)
            import AUtoEmotion as au
            i = 0
            for file in self.filenames:
                filename = file.split("/")[-1]
                filename = filename.partition(".")[0]
                # print(filename)
                arg = "processed/{}.csv".format(filename)
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