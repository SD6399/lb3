import datetime
import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QFileDialog, QGridLayout, QLineEdit
from PyQt5.QtGui import QFont, QIcon


class DirectoryEventHandler(FileSystemEventHandler):

    def on_created(self, event):
        callback(f"{datetime.datetime.now()}: {event.src_path} has been created")

    def on_deleted(self, event):
        callback(f"{datetime.datetime.now()}: {event.src_path} has been deleted")

    def on_modified(self, event):
        callback(f"{datetime.datetime.now()}: {event.src_path} has been modified")

    def on_moved(self, event):
        callback(f"{datetime.datetime.now()}: {event.src_path} moved to {event.dest_path}")


def start_observer(path):
    global observer, event_handler
    callback(f"{datetime.datetime.now()}: Started watching {path}")

    observer.schedule(event_handler, path, recursive=True)
    observer.start()


def stop_observer():
    global observer
    observer.stop()
    observer.join()


def callback(message):
    global sctext_log
    sctext_log.append(message)
    return True


def exit():
    global app
    stop_observer()
    app.quit()


def clear():
    global sctext_log
    sctext_log.clear()
    sctext_log.setFont(QFont("Times New Roman", 12))
    sctext_log.setText(f"{datetime.datetime.now()}: application started")
    sctext_log.setReadOnly(True)
    observer.start()


def stop_monitor():
    stop_observer()


def exp_on_txt():
    global sctext_log
    my_file = open("text1.txt", "w+")
    t = sctext_log.toPlainText()
    my_file.write(t)
    my_file.close()
    return True


def exp_on_xml():
    global sctext_log
    my_file = open("text2.xml", "w+")
    t = sctext_log.toPlainText()
    my_file.write(t)
    my_file.close()
    return True


def exp_on_json():
    global sctext_log
    my_file = open("text3.json", "w+")
    t = sctext_log.toPlainText()
    my_file.write(t)
    my_file.close()
    return True


def choose_dir():
    dir_path = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
    if dir_path:
        start_observer(dir_path)


if __name__ == "__main__":
    event_handler = DirectoryEventHandler()
    observer = Observer()

    path = None

    app = QApplication([])
    app.setStyle('Fusion')

    button_choose_dir = QPushButton('Choose a folder')
    button_choose_dir.clicked.connect(choose_dir)
    button_choose_dir.setFixedSize(90, 20)

    button_clear = QPushButton('Clear')
    button_clear.clicked.connect(clear)
    button_clear.setFixedSize(90, 20)

    button_pause = QPushButton('pause')
    button_pause.clicked.connect(stop_monitor)
    button_pause.setFixedSize(90, 20)

    button_to_txt = QPushButton('Export to txt')
    button_to_txt.clicked.connect(exp_on_txt)
    button_to_txt.setFixedSize(90, 20)

    button_to_xml = QPushButton('Export to xml')
    button_to_xml.clicked.connect(exp_on_xml)
    button_to_xml.setFixedSize(90, 20)


    button_to_json = QPushButton('Export to json')
    button_to_json.clicked.connect(exp_on_json)
    button_to_json.setFixedSize(90, 20)

    button_exit = QPushButton('Exit')
    button_exit.clicked.connect(exit)
    button_exit.setFixedSize(90, 20)

    sctext_log = QTextEdit()
    sctext_log.setFont(QFont("Times New Roman", 12))
    sctext_log.setText(f"{datetime.datetime.now()}: application started")
    sctext_log.setReadOnly(True)

    window = QWidget()
    window.setWindowTitle("Folder watcher")
    window.setWindowIcon(QIcon(os.path.dirname(__file__) + "/logo.ico"))
    window.resize(640, 480)
    layout = QGridLayout()
    layout.addWidget(sctext_log, 0, 0, 1, 4)
    layout.addWidget(button_choose_dir, 1, 0, 1, 1)
    layout.addWidget(button_clear, 1, 1, 1, 1)
    layout.addWidget(button_pause, 1, 2, 1, 1)
    layout.addWidget(button_to_txt, 1, 3, 8, 1)
    layout.addWidget(button_to_xml, 1, 2, 8, 1)
    layout.addWidget(button_to_json, 1, 1, 8, 1)
    layout.addWidget(button_exit, 1, 3, 1, 1)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())
