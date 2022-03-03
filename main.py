import sys
import os

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QPushButton, QLabel, QListWidget,
                             QHBoxLayout, QVBoxLayout,
                             QFileDialog)
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt
from image_process import ImageManager
import styles

manager = ImageManager()

BASE_DIR = os.getcwd()
EXTENSIONS = ["jpeg", "jpg", "bmp", "png", "gif"]

app = QApplication(sys.argv)
# Widgets
main_window = QWidget()
main_window.setWindowTitle("PhotoEditor")
main_window.resize(700, 500)
main_window.setWindowIcon(QIcon("rodjer.png"))
# Buttons
btn_chose_dir = QPushButton("Dir")
btn_rotate_left = QPushButton("Left")
btn_rotate_right = QPushButton("Right")
btn_mirror = QPushButton("Mirror")
btn_sharpness = QPushButton("Sharpness")
btn_bw = QPushButton("Black/White")
btns_line = [btn_rotate_left, btn_rotate_right, btn_mirror, btn_sharpness, btn_bw]

files_list = QListWidget()
image_label = QLabel("Image")
image_label.setAlignment(Qt.AlignCenter)

btn_back = QPushButton("Back")
btn_back.setStyleSheet(styles.nav_btn_style)
btn_forward = QPushButton("Forward")
btn_forward.setStyleSheet(styles.nav_btn_style)
btn_save = QPushButton("Save")
btn_save.setStyleSheet(styles.save_btn_style)

# Layouts
main_layout = QHBoxLayout()
left_main = QVBoxLayout()
right_main = QVBoxLayout()
layout_btns = QHBoxLayout()
layout_label = QHBoxLayout()
layout_btns_history = QHBoxLayout()

# Add widget to layout
left_main.addWidget(btn_chose_dir)
left_main.addWidget(files_list)
[layout_btns.addWidget(btn) for btn in btns_line]
layout_btns_history.addStretch(1)
layout_btns_history.addWidget(btn_back)
layout_btns_history.addWidget(btn_save)
layout_btns_history.addWidget(btn_forward)
layout_btns_history.addStretch(1)
layout_label.addWidget(image_label)
right_main.addLayout(layout_label, 95)
right_main.addLayout(layout_btns_history)
right_main.addLayout(layout_btns)

main_layout.addLayout(left_main, 20)
main_layout.addLayout(right_main, 80)
main_window.setLayout(main_layout)


#########################################################
# Functional                                            #
#########################################################
def add_processor_update_bar(func):
    def wrapper():
        processor = manager.current_processor
        if processor is None:
            return
        func(processor)
        update_navigate_bar()
        show_image(processor.get_image())

    return wrapper


def show_files_list():
    workdir = QFileDialog.getExistingDirectory()
    if not workdir:
        return
    file_names = os.listdir(workdir)
    os.chdir(workdir)
    files_image = filter(is_image, file_names)
    files_list.clear()
    files_list.addItems(files_image)


def is_image(filename: str) -> bool:
    image_path = os.path.join(os.getcwd(), filename)
    is_file = os.path.isfile(image_path)
    return filename.split(".")[-1] in EXTENSIONS and is_file


def show_chosen_image():
    if files_list.currentRow() >= 0:
        filename = files_list.currentItem().text()
        processor = manager.get_or_create(os.getcwd(), filename)
        update_navigate_bar()
        image = processor.get_image()
        show_image(image)


def update_navigate_bar():
    processor = manager.current_processor
    if processor is None or processor.size <= 1:
        btn_back.hide()
        btn_save.hide()
        btn_forward.hide()
        return
    btn_save.setEnabled(False) if processor.head == 0 else btn_save.setEnabled(True)
    btn_back.setEnabled(False) if processor.head == 0 else btn_back.setEnabled(True)
    (btn_forward.setEnabled(False) if processor.head == processor.size - 1
     else btn_forward.setEnabled(True))
    btn_back.show()
    btn_save.show()
    btn_forward.show()


def show_image(image):
    image_label.hide()
    pixmap = QPixmap(QImage(image))
    width, height = image_label.width(), image_label.height()
    pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio)
    image_label.setPixmap(pixmap)
    image_label.show()


@add_processor_update_bar
def do_bw(processor):
    processor.do_bw()


@add_processor_update_bar
def do_mirror(processor):
    processor.rotate_mirror()


@add_processor_update_bar
def do_left(processor):
    processor.rotate_left()


@add_processor_update_bar
def do_right(processor):
    processor.rotate_right()


@add_processor_update_bar
def do_sharp(processor):
    processor.make_sharpness()


def show_previously():
    processor = manager.current_processor
    if processor is None:
        return
    image = processor.get_back()
    show_image(image)
    update_navigate_bar()


def show_next():
    processor = manager.current_processor
    if processor is None:
        return
    image = processor.get_front()
    show_image(image)
    update_navigate_bar()


def save_image():
    processor = manager.current_processor
    if processor is None:
        return
    path_to = QFileDialog.getSaveFileName()
    if path_to[0]:
        processor.save_image(path_to[0])


#########################################################
#  Run application                                      #
#########################################################
btn_chose_dir.clicked.connect(show_files_list)
btn_bw.clicked.connect(do_bw)
btn_mirror.clicked.connect(do_mirror)
btn_rotate_left.clicked.connect(do_left)
btn_rotate_right.clicked.connect(do_right)
btn_sharpness.clicked.connect(do_sharp)

btn_back.clicked.connect(show_previously)
btn_forward.clicked.connect(show_next)
btn_save.clicked.connect(save_image)

files_list.currentRowChanged.connect(show_chosen_image)

btn_back.hide()
btn_save.hide()
btn_forward.hide()
main_window.show()
app.exec()
