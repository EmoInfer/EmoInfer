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
import SequenceAnalysis as seqan
import matplotlib.pyplot as plt
import numpy as np
import statistics as stats

OpenFacePath = "/home/sunidhi/Desktop/zurichproj/OpenFace"

class VideoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        uic.loadUi("app.ui", self)

        self.filenames = []

### VIDEO PLAYER
        self.playbutton.setEnabled(False)
        self.playbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        # self.play.clicked.connect(self.play_video)
        self.playbutton.clicked.connect(self.play_video)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)

        self.vidwidget = QVideoWidget()
        self.verticalLayout_vid.addWidget(self.vidwidget)
        # self.vidwidget = self.findChild(QVideoWidget,"vidwidget" )
        self.vidplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.vidplayer.setVideoOutput(self.vidwidget)

        self.vidplayer.stateChanged.connect(self.mediastate_changed)
        self.vidplayer.positionChanged.connect(self.position_changed)
        self.vidplayer.durationChanged.connect(self.duration_changed)
### VIDEO PLAYER

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
        self.vid_res = {}
        self.combined_filename = ""

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
            # self.vidplayer.setVideoOutput(self.vidwidget)
            self.vidplayer.play()

 
 
    def mediastate_changed(self, state):
        if self.vidplayer.state() == QMediaPlayer.PlayingState:
            self.playbutton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
 
            )
 
        else:
            self.playbutton.setIcon(
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
            self.playbutton.setEnabled(True)
            self.vidplayer.play()
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
        self.vid_res = {}
        for i in range(self.videos_wid.model().rowCount()):
            if self.videos_wid.model().item(i).checkState() == Qt.Checked:
                filename = self.videos_wid.model().item(i).data()
                paper = self.paper.currentText()
                paper = paper.split(' ')[0]
                emotion = self.emotion.currentText()
                time_gran = self.time_gran.value()
                # self.video_select.addItem(filename)
                res = freqan.FreqAnalysis(filename, "extracted/extracted_{}.csv".format(filename), paper, emotion, time_gran)
                self.vid_res[filename] = {'per':res[0], 'data_to_plot1':res[1], 'inds':res[2], 'medians':res[3], 'quartile1':res[4], 'quartile3':res[5], 'whiskers_min':res[6], 'whiskers_max':res[7]}
                

    def execute_com_analysis(self):
        self.vid_res = {}
        filenames = self.videos_wid.currentData()
        filename = "".join(filenames)
        self.combined_filename = filename
        paper = self.paper.currentText()
        paper = paper.split(' ')[0]
        emotion = self.emotion.currentText()
        time_gran = self.time_gran.value()
        # self.video_select.addItems(filenames)
        res = coman.CombFreqAnalysis(filenames, len(filenames), paper, emotion, time_gran)
        self.vid_res[filename] = {'per':res[0], 'data_to_plot1':res[1], 'inds':res[2], 'medians':res[3], 'quartile1':res[4], 'quartile3':res[5], 'whiskers_min':res[6], 'whiskers_max':res[7]}


    def ind_analysis(self):
        self.INDEPENDENT = 1
        self.COMBINED = 0
        filenames = self.videos_wid.currentData()
        self.video_select.addItems(filenames)

        # self.execute_ind_analysis()
        worker = Worker(self.execute_ind_analysis) # Any other args, kwargs are passed to the run function
        # worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # # Execute
        self.threadpool.start(worker)  
        return "Done"
 
        # self.status.setText("")
    def com_analysis(self):
        self.INDEPENDENT = 0
        self.COMBINED = 1
        # self.video_select.clear()
        self.video_select.addItem("Combined")
        # self.execute_com_analysis()
        worker = Worker(self.execute_com_analysis) # Any other args, kwargs are passed to the run function
        # worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # # Execute
        self.threadpool.start(worker)
        # i = 0
        return "Done"

        
    def show_analysis_figures(self):
        filename = self.video_select.currentText()
        paper = self.paper.currentText()
        paper = paper.split(' ')[0]
        emotion = self.emotion.currentText()
        if self.COMBINED == 1 or filename == "Combined":
            filename = self.combined_filename

        per = self.vid_res[filename]['per']
        data_to_plot1 = self.vid_res[filename]['data_to_plot1']
        inds = self.vid_res[filename]['inds']
        medians = self.vid_res[filename]['medians']
        quartile1 = self.vid_res[filename]['quartile1']
        quartile3 = self.vid_res[filename]['quartile3']
        whiskers_min = self.vid_res[filename]['whiskers_min']
        whiskers_max = self.vid_res[filename]['whiskers_max']

        if not os.path.exists(f"images/{paper}/{filename}/"):
            os.makedirs(f"images/{paper}/{filename}/")

        plt.figure()
        i = 0
        if paper == "Cordaro":
            emos = self.emo_list[0:13]
        if paper == "Keltner":
            emos = self.emo_list[0:15]
        if paper == "Du":
            emos = self.emo_list
        max_val = 0
        max_emo = emotion
        for emo in emos:
            plt.bar([i+1],[per[i][paper + '_'].sum()], label=emo)
            if max_val < per[i][paper + '_'].sum():
                max_val = per[i][paper + '_'].sum()
                max_emo = emo                
            i += 1
        # pap = "Cordaro et al., 2018"
        plt.legend(loc='best')
        plt.ylabel('# of frames x # of faces')
        plt.xlabel('Emotion')
        plt.title(label=paper+" et al.")
        plt.savefig(f"images/{paper}/{filename}/FreqBarGraph.png")
        plt.close()

        ## start with emotion specific

        fig = plt.figure()

        # Create an axes instance
        ax = fig.add_axes([0,0,1,1])

        # Create the boxplot
        parts = ax.violinplot(data_to_plot1, showmeans=True, showmedians=True, showextrema=True)
        for pc in parts['bodies']:
            pc.set_facecolor('white')
            pc.set_edgecolor('black')
            pc.set_alpha(1)

        ax.scatter(inds, medians, marker='o', color='white', s=30, zorder=3)
        ax.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
        ax.vlines(inds, whiskers_min, whiskers_max, color='k', linestyle='-', lw=1)
        plt.ylim(0, 100)
        plt.xlim(0,2)
        # plt.legend(loc='best')
        plt.title(emotion)
        plt.xlabel(paper+" et al.")
        plt.ylabel("percentage")
        plt.savefig(f"images/{paper}/{filename}/{emotion}.png", bbox_inches='tight')
        plt.close(fig)
        
        try:
            std2 = stats.stdev(data_to_plot1[0])
        except:
            std2 = -1
        mn2 = stats.mean(data_to_plot1[0])
        intrng2_first, intrng2_second = np.percentile(data_to_plot1[0], [75,25])
        intrng2 = intrng2_first - intrng2_second
        
        self.high_inc.setText("Emotion with highest incidence :  " + max_emo)
        self.avg_inc.setText("Average % emotion incidence = " + str("%.2f" % mn2))
        self.std_dev.setText("Std. deviation (%  emotion incidence) = " + str("%.2f" % std2))
        self.int_rng.setText("Interquartile range (%  emotion incidence) = " + str("%.2f" % intrng2))
        self.paperimg.setPixmap(QPixmap(f"images/{paper}/{filename}/FreqBarGraph.png"))
        self.paperemo.setPixmap(QPixmap(f"images/{paper}/{filename}/{emotion}.png"))

    def execute_AU_extract(self, AUint, poseRx, poseRz):
        os.system(OpenFacePath + "/build/bin/FaceLandmarkVidMulti -pose -aus -vis-track -vis-aus -f \"{}\"".format('\" -f \"'.join(self.filenames)))
        i = 0
        for file in self.filenames:
            filename = file.split("/")[-1]
            filename = filename.partition(".")[0]
            # print(filename)
            arg = "processed/{}.csv".format(filename)

            #create directory
            if not os.path.exists(f"extracted/"):
                os.makedirs(f"extracted/")
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

    def execute_seq_analysis(self, filenames, n_videos, paper, hyp):
        strs = seqan.seq_analysis(filenames, n_videos, paper, hyp)
        return strs

    def output_seq(self, strs):
        self.uniqemo.setText(strs[0])
        self.mullen.setText(strs[1])
        self.mulemo.setText(strs[2])

    def sequencing_func(self):
        filenames = self.videos_wid2.currentData()
        # filename = filenames[0]
        # path = "extracted/extracted_{}.csv".format(filename)
        paper = self.paper_seq.currentText()
        paper = paper.split(' ')[0]

        #hyperparameters
        hyp = []
        hyp.append(self.minsup.value())
        hyp.append(self.minsucc.value())
        hyp.append(self.maxsucc.value())
        hyp.append(self.minfl.value())
        hyp.append(self.maxfl.value())

        #create directory
        if not os.path.exists(f"sequencing/"):
            os.makedirs(f"sequencing/")

        if filenames == []:
            self.errorlabel.show()
            self.errorlabel.setText("Error: Select video first")
        else:
            worker = Worker(lambda: self.execute_seq_analysis(filenames, len(filenames), paper, hyp)) # Any other args, kwargs are passed to the run function
            worker.signals.result.connect(self.output_seq)
            worker.signals.finished.connect(self.thread_complete)
            worker.signals.progress.connect(self.progress_fn)

            # Execute
            self.threadpool.start(worker)
            self.errorlabel.hide()
        



if __name__ == '__main__':
    app = QApplication([])
    player = VideoWindow()

    app.exec_()