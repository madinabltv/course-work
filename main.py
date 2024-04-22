import numpy as np
from skimage import io, img_as_float32, img_as_ubyte
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from filter import chromatic_removal

class ImageRestorationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        self.load_button = QPushButton('Загрузить изображение', self)
        self.load_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_button)

        self.save_button = QPushButton('Сохранить изображение', self)
        self.save_button.clicked.connect(self.save_image)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        self.setGeometry(100, 100, 640, 480)
        self.setWindowTitle('Восстановление изображения')

    def load_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Выбрать изображение', '', 'Images (*.png *.jpg *.bmp)')
        if file_path:
            img = img_as_float32(io.imread(file_path))
            self.restore_image(img)

    def restore_image(self, img):

        self.restored_img = chromatic_removal(img, L_hor=7, L_ver=4, rho=np.array([-0.25, 1.375, -0.125]), tau=15. / 255,
                                         gamma_1=128. / 255, gamma_2=64. / 255)
        
        self.display_image(img, self.restored_img)

    def display_image(self, img, restored_img):
        plt.figure()
        plt.subplot(1, 2, 1)
        plt.imshow(img)
        plt.subplot(1, 2, 2)
        plt.imshow(restored_img)
        plt.show()

    def save_image(self):
        if self.restored_img is not None:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, 'Сохранить изображение', '', 'Images (*.png)')
            if file_path:
                io.imsave(file_path +".png", img_as_ubyte(self.restored_img))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageRestorationApp()
    ex.show()
    sys.exit(app.exec_())
