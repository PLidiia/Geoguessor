CITIES = ['Кемерово', 'Москва', 'Хабаровск', 'Оттава', 'Вашингтон', 'Санкт-Петербург', 'Сидней',
          'Сан-Паулу', 'Брага', 'Найроби']

import random
import sys

import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QStackedWidget


class Geoguessor(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('guess.ui', self)
        self.pixmap = QPixmap('spam.png')
        self.pixmap_1 = QPixmap('spam.png')
        self.pixmap_2 = QPixmap('spam.png')
        self.cur_item = 0
        self.move_list.hide()
        self.lat = ''
        self.long = ''
        self.list_names.addItems(CITIES)
        self.list_names.sortItems()
        self.cur_city_click = 'nothing'
        self.start_play.clicked.connect(self.start_cities)
        self.list_names.itemClicked.connect(self.clicked_item)
        self.ready_to_answer.clicked.connect(self.check_user_answer)
        self.move_list.clicked.connect(self.move_image)

    def move_image(self):
        item_num = (self.cur_item + 1) % 3
        self.cur_item = item_num
        if item_num == 1:
            self.image.setPixmap(self.pixmap_1)
        elif item_num == 2:
            self.image.setPixmap(self.pixmap_2)
        else:
            self.image.setPixmap(self.pixmap)

    def check_user_answer(self):
        if self.asnwer_city.text() == self.cur_city_click:
            self.win_message.setText(f'Вы отгадали город {self.asnwer_city.text()}')
        else:
            self.win_message.setText(f'Вы не отгадали город, попробуйте ещё раз')

    def clicked_item(self, item):
        name_city = item.text()
        self.move_list.show()
        self.list_names.hide()
        self.cur_city_click = name_city
        api_server_geo = 'http://geocode-maps.yandex.ru/1.x/'
        params_geo = {
            'geocode': name_city,
            'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
            'format': 'json'
        }
        response = requests.get(api_server_geo, params=params_geo)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            toponym_coodrinates = toponym_coodrinates.split(' ')
            api_server_static_maps = 'http://static-maps.yandex.ru/1.x/'
            spn_data = ['0.005', '0.0005']
            # спутник или схема
            random_data_type_layout_map = ['sat', 'map']
            num_item_random_data_type_layout_map = random.randint(0, 1)
            params_static_maps_1 = {
                'll': ','.join(toponym_coodrinates),
                'spn': ','.join(spn_data),
                'l': random_data_type_layout_map[num_item_random_data_type_layout_map]
            }
            toponym_coord_1 = float(toponym_coodrinates[0]) + 0.009
            toponym_coord_2_2 = float(toponym_coodrinates[1]) + 0.006
            toponym_coodrinates_1 = [str(toponym_coord_1), str(toponym_coord_2_2)]
            params_static_maps_2 = {
                'll': ','.join(toponym_coodrinates_1),
                'spn': ','.join(spn_data),
                'l': random_data_type_layout_map[num_item_random_data_type_layout_map]
            }
            toponym_coord_1_2 = float(toponym_coodrinates[0]) + 0.005
            toponym_coord_2_2 = float(toponym_coodrinates[1]) + 0.002
            toponym_coodrinates_2 = [str(toponym_coord_1_2), str(toponym_coord_2_2)]
            params_static_maps_3 = {
                'll': ','.join(toponym_coodrinates_2),
                'spn': ','.join(spn_data),
                'l': random_data_type_layout_map[num_item_random_data_type_layout_map]
            }
            response_map_centre_image_1 = requests.get(api_server_static_maps, params=params_static_maps_1)
            response_map_image_2 = requests.get(api_server_static_maps, params=params_static_maps_2)
            response_map_image_3 = requests.get(api_server_static_maps, params=params_static_maps_3)
            if response_map_centre_image_1:
                map_file_1 = "map.png"
                with open(map_file_1, "wb") as file:
                    # сначала центры города
                    file.write(response_map_centre_image_1.content)
                    self.choice_city.setText('')
                    self.pixmap = QPixmap(map_file_1)
                    self.image.setPixmap(self.pixmap)
            else:
                print("Ошибка выполнения запроса:")
                print(response_map_centre_image_1)
                print("Http статус:", response_map_centre_image_1.status_code, "(", response_map_centre_image_1.reason,
                      ")")
                sys.exit(1)
            if response_map_image_2:
                map_file_2 = "map1.png"
                with open(map_file_2, "wb") as file:
                    file.write(response_map_image_2.content)
                    self.choice_city.setText('')
                    self.pixmap_1 = QPixmap(map_file_2)
            else:
                print("Ошибка выполнения запроса:")
                print(response_map_image_2)
                print("Http статус:", response_map_image_2.status_code, "(", response_map_image_2.reason,
                      ")")
                sys.exit(1)
            if response_map_image_3:
                map_file_3 = "map2.png"
                with open(map_file_3, "wb") as file:
                    file.write(response_map_image_3.content)
                    self.choice_city.setText('')
                    self.pixmap_2 = QPixmap(map_file_3)
            else:
                print("Ошибка выполнения запроса:")
                print(response_map_image_2)
                print("Http статус:", response_map_image_2.status_code, "(", response_map_image_2.reason,
                      ")")
                sys.exit(1)
        else:
            print("Ошибка выполнения запроса:")
            print(response)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

    def start_cities(self):
        self.pixmap = QPixmap('')
        self.image.setPixmap(self.pixmap)
        self.choice_city.setText('Выберите город из списка')
        self.list_names.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Geoguessor()
    widget = QStackedWidget()
    widget.addWidget(ex)
    widget.setFixedWidth(1500)
    widget.setFixedHeight(1500)
    widget.show()
    sys.__excepthook__ = except_hook
    sys.exit(app.exec())

