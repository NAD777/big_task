import os
import sys

import requests
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

SCREEN_SIZE = [600, 450]


# 52.727525, 41.456136
class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        # self.y, self.x = input().split(", ")
        self.y, self.x = 52.727525, 41.456136

        self.z = 14

        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.refresh()

    def get_coords(self, place):
        url = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b"
        params = {
            "geocode": f"{place}",
            "format": "json"
        }
        response = requests.get(url=url, params=params)
        x, y = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
            "Point"]["pos"].split()
        return x, y

    def getImage(self, x, y):
        map_request = "http://static-maps.yandex.ru/1.x/"
        params = {
            "ll": f"{x},{y}",
            "l": "map",
            "z": f"{self.z}"

        }
        response = requests.get(map_request, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def set_image(self):
        # self.getImage(self.x, self.y)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.update()

    def refresh(self):
        self.getImage(self.x, self.y)
        self.set_image()

    def keyPressEvent(self, event):  # Key_Comma, Key_Period
        if event.key() == QtCore.Qt.Key_Comma:  # < btn
            if self.z < 17:
                self.z += 1

        if event.key() == QtCore.Qt.Key_Period:  # > btn
            if self.z > 1:
                self.z -= 1
        self.refresh()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
