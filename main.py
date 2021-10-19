import sys
import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import design


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.show_weather)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Enter:
            self.show_weather()

    def show_weather(self):
        self.listWidget.clear()
        # city_name = 'Chelyabinsk,RU'
        city_name = self.lineEdit.text()
        self.lineEdit.setText('')
        appid = 'd8f26124dbb3d62c82a9f08e27df4c02'
        period = {'00': 'ночь', '06': 'утро', '12': 'день', '18': 'вечер'}
        r = requests.get('http://api.openweathermap.org/data/2.5/forecast',
                         params={'q': city_name, 'appid': appid,
                                 'units': 'metric', 'lang': 'ru'})
        data = r.json()

        if data['cod'] == '200':
            self.listWidget.addItem(data['city']['name'])
            for i in data['list']:
                date_time = i['dt_txt'][:11]
                tmp = i['dt_txt'][11:13]
                if tmp in period.keys():
                    date_time += period[tmp]
                    msg = date_time + f"\t{i['main']['temp']:7}\t℃ \t" + i['weather'][0]['description']
                    self.listWidget.addItem(msg)

        else:
            self.listWidget.addItem(city_name)
            msg = f"Error {data['cod']} {data['message']}"
            self.listWidget.addItem(msg)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
