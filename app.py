from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, \
  QWidget, QPushButton, QTableWidget, QTableWidgetItem, QInputDialog, QFileDialog

app = QApplication([])
window = QMainWindow()

screen = QWidget()
layout = QGridLayout()
screen.setLayout(layout)

yearly_income = QLabel()
yearly_income.setText('Input: ')
layout.addWidget(yearly_income, 0, 0)

tax_rate = QLabel()
tax_rate.setText('Output: ')
layout.addWidget(tax_rate, 0, 1)

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
        yearly_income.setText('Input: {}%'.format(path[0]))

button.clicked.connect(open_file)
layout.addWidget(button, 1, 0, 1, 2)


window.setCentralWidget(screen)
window.setWindowTitle('Emotion inference')
window.setMinimumSize(500, 200)
window.show()

app.exec_()