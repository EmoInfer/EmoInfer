#app exec file

# from asyncio.windows_events import None
from multiprocessing import Process
from typing_extensions import Self
from PyQt5.QtWidgets import *
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QStyle, \
#   QWidget, QPushButton, QTableWidget, QTableWidgetItem, QInputDialog, QFileDialog, QSizePolicy, QScrollArea, QDoubleSpinBox, QHBoxLayout, QComboBox, QSlider
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5 import uic, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, os
import subprocess
import time

from CheckableComboBox import CheckableComboBox
from WorkerThread import WorkerSignals, Worker
import AUtoEmotion as au
import FrequencyAnalysis as freqan
import CombinedAnalysis as coman

OpenFacePath = "/home/sunidhi/Desktop/zurichproj/OpenFace"

class VideoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        uic.loadUi("app.ui", self)

        self.inp_video = self.findChild(QLabel, "inpvideo")
        self.filenames = []

        self.play.setEnabled(False)
        self.play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play.clicked.connect(self.play_video)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)


        self.vidwidget = self.findChild(QVideoWidget,"vidplayer" )
        self.vidplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.vidplayer.setVideoOutput(self.vidwidget)

        self.videos_wid = CheckableComboBox()
        self.videos_wid2 = CheckableComboBox()
        self.lay_vid.addWidget(self.videos_wid)
        self.lay_vid_3.addWidget(self.videos_wid2)


        self.paper.addItem("Cordaro et al., 2018")
        self.paper.addItem("Keltner et al., 2019")
        self.paper.addItem("Du et al., 2014")

        self.paper_seq.addItem("Cordaro et al., 2018")
        self.paper_seq.addItem("Keltner et al., 2019")
        self.paper_seq.addItem("Du et al., 2014")

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

        self.errorlabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)
        self.image_au.setPixmap(QPixmap("images/AU2.png"))
        self.label_8.setPixmap(QPixmap("images/headpose2.png"))
        self.startextractbin.clicked.connect(self.action_unit_bin)
        self.startextractcon.clicked.connect(self.action_unit_con)
        self.uploadbutton.clicked.connect(self.open_file)
        self.removevideo.clicked.connect(self.remove_file)
        self.binary.clicked.connect(self.unhide_bin)
        self.cont.clicked.connect(self.unhide_con)
        self.indanalysis.clicked.connect(self.ind_analysis)
        self.comanalysis.clicked.connect(self.com_analysis)
        self.show_analysis_fig.clicked.connect(self.show_analysis_figures)
        self.extractseq.clicked.connect(self.sequencing_func)

        self.INDEPENDENT = 1
        self.COMBINED = 0

        self.vidplayer.stateChanged.connect(self.mediastate_changed)
        self.vidplayer.positionChanged.connect(self.position_changed)
        self.vidplayer.durationChanged.connect(self.duration_changed)


        self.bin_hidden = True
        self.con_hidden = True
        self.extractedpath = [""]*1000

        self.show()
        self.startextractbin.hide()
        self.spinboxwidget.hide()
        self.startextractcon.hide()
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())


    def play_video(self):
        if self.vidplayer.state() == QMediaPlayer.PlayingState:
            self.vidplayer.pause()
 
        else:
            self.vidplayer.play()
 
 
    def mediastate_changed(self, state):
        if self.vidplayer.state() == QMediaPlayer.PlayingState:
            self.play.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
 
            )
 
        else:
            self.play.setIcon(
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
            self.startextractbin.show()
            self.bin_hidden = False
            self.hide_con()
        self.errorlabel.hide()
    
    def unhide_con(self):
        if self.con_hidden:
            # self.hyperscroll.show()
            self.spinboxwidget.show()
            self.startextractcon.show()
            self.con_hidden = False
            self.hide_bin()
        self.errorlabel.hide()
    
    def hide_bin(self):
        if self.bin_hidden == False:
            self.startextractbin.hide()
            self.bin_hidden = True
        self.errorlabel.hide()
    
    def hide_con(self):
        if self.con_hidden == False:
            # self.hyperscroll.hide()
            self.spinboxwidget.hide()
            self.startextractcon.hide()
            self.con_hidden = True
        self.errorlabel.hide()


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
            self.play.setEnabled(True)
        self.errorlabel.hide()
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
            self.videos_wid2.addItem(filename)
        
    def remove_file(self):
        self.filenames = []
        self.inp_video.setText('Input video(s): ')
        self.errorlabel.hide()

    def execute_ind_analysis(self):
        for i in range(self.videos_wid.model().rowCount()):
            if self.videos_wid.model().item(i).checkState() == Qt.Checked:
                filename = self.videos_wid.model().item(i).data()
                # self.video_select.addItem(filename)
                freqan.FreqAnalysis(filename, "extracted/extracted_{}.csv".format(filename), self.paper.currentText(), self.emotion.currentText())
                

    def execute_com_analysis(self):
        filenames = self.videos_wid.currentData()
        # self.video_select.addItems(filenames)
        coman.CombFreqAnalysis(filenames, len(filenames))
        return "Done"

    def ind_analysis(self):
        self.INDEPENDENT = 1
        self.COMBINED = 0
        filenames = self.videos_wid.currentData()
        self.video_select.addItems(filenames)
        # for i in range(self.videos_wid.model().rowCount()):
        #     if self.videos_wid.model().item(i).checkState() == Qt.Checked:
        #         filename = self.videos_wid.model().item(i).data()
        #         # self.video_select.addItem(filename)
        #         freqan.FreqAnalysis(filename, "extracted/extracted_{}.csv".format(filename), self.paper.currentText(), self.emotion.currentText())

## following code is for multiprocessing 
        # p_i = Process(target=self.execute_ind_analysis, args=())
        # p_i.start()
        # # input("Type any key to quit.")
        # print("Waiting for graph window process to join...")
        # p_i.join()
        # print("Process joined successfully. C YA !")


        self.execute_ind_analysis()
        # worker = Worker(self.execute_ind_analysis) # Any other args, kwargs are passed to the run function
        # worker.signals.result.connect(self.print_output)
        # worker.signals.finished.connect(self.thread_complete)
        # worker.signals.progress.connect(self.progress_fn)

        # # Execute
        # self.threadpool.start(worker)  
        return "Done"
 
        # self.status.setText("")
    def com_analysis(self):
        self.INDEPENDENT = 0
        self.COMBINED = 1
        self.video_select.clear()
        self.execute_com_analysis()
        # worker = Worker(lambda: self.execute_com_analysis) # Any other args, kwargs are passed to the run function
        # worker.signals.result.connect(self.print_output)
        # worker.signals.finished.connect(self.thread_complete)
        # worker.signals.progress.connect(self.progress_fn)

        # # Execute
        # self.threadpool.start(worker)
        # i = 0

        
    def show_analysis_figures(self):
        if self.INDEPENDENT == 1:
            self.paperimg.setPixmap(QPixmap(f"images/{self.paper.currentText()}_{self.video_select.currentText()}.png"))
            self.paperemo.setPixmap(QPixmap(f"images/{self.paper.currentText()}{self.emotion.currentText()}_{self.video_select.currentText()}.png"))
        else:
            name = ''.join(self.videos_wid.currentData())
            self.paperimg.setPixmap(QPixmap(f"images/{self.paper.currentText()}_{name}.png"))
            self.paperemo.setPixmap(QPixmap(f"images/{self.paper.currentText()}{self.emotion.currentText()}_{name}.png"))

    def execute_AU_extract(self, AUint, poseRx, poseRz):
        subprocess.run(OpenFacePath + "/build/bin/FaceLandmarkVidMulti -pose -aus -vis-track -vis-aus -f \"{}\"".format('\" -f \"'.join(self.filenames)), shell=True)
        i = 0
        for file in self.filenames:
            filename = file.split("/")[-1]
            filename = filename.partition(".")[0]
            # print(filename)
            arg = "processed/{}.csv".format(filename)
            # print(au.ExtractEmotion(arg))
            self.emos, self.extractedpath[i] = au.ExtractEmotion(arg, filename, AUint, poseRx, poseRz)
            # freqan.FreqAnalysis(extractedpath)
            i += 1
        return "Done"

    def progress_fn(self, n):
        print("%d%% done" % n)

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def action_unit_bin(self):
        if self.filenames == []:
            self.errorlabel.show()
            self.errorlabel.setText("Error: Input video first")
        else:
            # self.status.setText("Extracting Emotions...")
            # -vis-track -vis-aus
            worker = Worker(lambda: self.execute_AU_extract(None,None,None)) # Any other args, kwargs are passed to the run function
            worker.signals.result.connect(self.print_output)
            worker.signals.finished.connect(self.thread_complete)
            worker.signals.progress.connect(self.progress_fn)

            # Execute
            self.threadpool.start(worker)
            # self.status.setText("Extraction results saved...")
            self.errorlabel.hide()

    def action_unit_con(self):
        if self.filenames == []:
            self.errorlabel.show()
            self.errorlabel.setText("Error: Input video first")
        else:
            worker = Worker(lambda: self.execute_AU_extract(self.AUint.value(), self.poseRx.value(), self.poseRz.value())) # Any other args, kwargs are passed to the run function
            worker.signals.result.connect(self.print_output)
            worker.signals.finished.connect(self.thread_complete)
            worker.signals.progress.connect(self.progress_fn)

            # Execute
            self.threadpool.start(worker)
            # self.status.setText("Extraction results saved...")
            self.errorlabel.hide()

    
                # return (res)
# -pose -gaze -verbose

    def sequencing_func(self):
        import SequenceAnalysis as seqan
        filenames = self.videos_wid2.currentData()
        filename = filenames[0]
        path = "extracted/extracted_{}.csv".format(filename)
        paper = self.paper_seq.currentText()
        paper = paper.split(' ')[0]

        #hyperparameters
        hyp = []
        hyp.append(self.minsup.value())
        hyp.append(self.minsucc.value())
        hyp.append(self.maxsucc.value())
        hyp.append(self.minfl.value())
        hyp.append(self.maxfl.value())


        seqan.seq_analysis(filename, path, paper, hyp)
        new_file = open("sequencing/final_sequences_{paper}_{filename}.txt").read()
        new_mult_emos = open("sequencing/final_mult_sequences_{paper}_{filename}.txt").read()
        new_uniq_emos = open("sequencing/final_uniq_sequences_{paper}_{filename}.txt").read()
        
        self.uniqemo.setText(new_uniq_emos)
        self.mullen.setText(new_file)
        self.mulemo.setText(new_mult_emos)

if __name__ == '__main__':
    app = QApplication([])
    player = VideoWindow()

    app.exec_()