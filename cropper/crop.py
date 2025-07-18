
import sys
import os
import argparse
from pathlib import Path
from PIL import Image
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QRect, QPoint, QCoreApplication

class FinalCoords:
    start = None
    end = None
final_coords = FinalCoords()

def get_cli_options ():
    parser = argparse.ArgumentParser(
        prog="Cropper",
    )

    parser.add_argument('-d', '--directory')
    parser.add_argument('-c', '--coords', required=False)

    return parser.parse_args(sys.argv[1:])

def do_cropping ():
    opts = get_cli_options()
    uncropped_dir = Path(opts.directory)
    os.makedirs(os.path.join(str(uncropped_dir.parent), 'CROPPED'+uncropped_dir.name))
    cropped_dir = uncropped_dir.parent.joinpath('CROPPED'+uncropped_dir.name)
    for file in uncropped_dir.iterdir():
        with Image.open(str(file)) as im:
            im_crop = im.crop((final_coords.start.x(), final_coords.start.y(), final_coords.end.x(), final_coords.end.y()))
            im_crop.save(cropped_dir.joinpath(file.name))

class ImageLabel(QLabel):
    def __init__(self, image_path):
        super().__init__()
        self.pixmap = QPixmap(image_path)
        self.setPixmap(self.pixmap)
        self.start_point = None
        self.end_point = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.end_point = self.start_point
            self.update()

    def mouseMoveEvent(self, event):
        if self.start_point:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.start_point:
            final_coords.start = self.start_point
            final_coords.end = self.end_point
            do_cropping()
            QCoreApplication.quit()
            

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.pixmap:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            if self.start_point and self.end_point:
                painter.drawRect(QRect(self.start_point, self.end_point))

class MainWindow(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("Draw Box on Image")
        self.image_label = ImageLabel(image_path)
        self.setCentralWidget(self.image_label)
        self.resize(self.image_label.pixmap.size())

def parse_coords(coords):
    coordlist = [int(x) for x in coords.split(",")]
    final_coords.start = QPoint(coordlist[0], coordlist[1])
    final_coords.end = QPoint(coordlist[2], coordlist[3])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    opts = get_cli_options()
    if opts.coords:
        parse_coords(opts.coords)  
        do_cropping()  
    else:
        window = MainWindow(str(Path(opts.directory).iterdir().__next__()))  # Replace with your image path
        window.show()
        sys.exit(app.exec_())
