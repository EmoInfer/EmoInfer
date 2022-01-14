#app exec file

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, \
  QWidget, QPushButton, QTableWidget, QTableWidgetItem, QInputDialog, QFileDialog, QSizePolicy
import subprocess

class VideoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.inp_video = QLabel()
        self.inp_video.setText('Input: ')
        self.filename = ''

        self.button = QPushButton()
        self.button.setText('Upload video')

        self.au_button = QPushButton()
        self.au_button.setText('Extract Emotions')

        self.model_output = QLabel()
        self.model_output.setText('Output: ')

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        self.au_button.clicked.connect(self.action_unit)
        self.button.clicked.connect(self.open_file)

        layout.addWidget(self.inp_video, 0, 0)
        layout.addWidget(self.model_output, 0, 1)
        layout.addWidget(self.button, 1, 0, 1, 2)
        layout.addWidget(self.au_button, 2, 0, 1, 2)
        layout.addWidget(self.errorLabel)

    def open_file(self):
        path = QFileDialog.getOpenFileNames(
            self, # parent widget
            'Video', # window title
            '', # entry label
            'All Files (*.*)'
        )
        self.filenames = path[0]
        if path != ('', ''):
            self.inp_video.setText('Input: {}%'.format(','.join(path[0])))

    def action_unit(self):
        if self.filenames == []:
            self.errorLabel.setText("Error: Input video first")
        else:
            subprocess.run("/home/sunidhi/Desktop/zurichproj/OpenFace/build/bin/FaceLandmarkVidMulti -verbose -aus -pose -gaze -f \"{}\"".format('\" -f \"'.join(self.filenames)), shell = True)


if __name__ == '__main__':

    app = QApplication([])
    window = QMainWindow()

    screen = QWidget()
    layout = QGridLayout()
    screen.setLayout(layout)

    player = VideoWindow(window)
    # player.resize(640, 480)
    # player.show()


    window.setCentralWidget(screen)
    window.setWindowTitle('Emotion inference')
    window.setMinimumSize(500, 200)
    window.show()

    app.exec_()