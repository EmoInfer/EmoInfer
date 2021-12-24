from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, \
  QWidget, QPushButton, QTableWidget, QTableWidgetItem, QInputDialog, QFileDialog

app = QApplication([])
window = QMainWindow()

screen = QWidget()
layout = QGridLayout()
screen.setLayout(layout)

inp_video = QLabel()
inp_video.setText('Input: ')
layout.addWidget(inp_video, 0, 0)

model_output = QLabel()
model_output.setText('Output: ')
layout.addWidget(model_output, 0, 1)

button = QPushButton()
button.setText('Upload video')

def open_file():
    path = QFileDialog.getOpenFileName(
        window, # parent widget
        'Video', # window title
        '', # entry label
        'All Files (*.*)'
    )
    if path != ('', ''):
        inp_video.setText('Input: {}%'.format(path[0]))

button.clicked.connect(open_file)
layout.addWidget(button, 1, 0, 1, 2)


window.setCentralWidget(screen)
window.setWindowTitle('Emotion inference')
window.setMinimumSize(500, 200)
window.show()

app.exec_()