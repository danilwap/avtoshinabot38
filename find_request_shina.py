import requests
import json
from utils import get_end_data


class Shina:
    def __init__(self, name, price, available, quantity, season, store, stores):
        self.name = name
        self.price = price
        self.available = available
        self.quantity = quantity
        self.season = season
        self.store = store
        self.stores = stores


class AllShins:
    def __init__(self, need_season):
        self.shins = []
        self.all_stores = []
        self.result_dict = {}
        self.result_return_str = ""
        self.result_return_list = []
        self.need_season = str(need_season)

    def add_shina(self, shina: Shina):
        # Фильтрует по тому, чтобы в наличие было больше 4
        if int(shina.quantity) < 4 and shina.store == 'IRKUTSK':
            return
        if not shina.season or not self.need_season:
            return
        if self.need_season in shina.season:
            if shina.store not in self.all_stores:
                self.all_stores.append(shina.store)
                if shina.store == 'IRKUTSK':
                    self.result_dict[shina.store] = "<b>=== В наличии: ===</b>\n"
                    self.result_dict[shina.store] += f"{shina.name} - <b>{shina.price} ₽</b>\n"
                else:
                    self.result_dict[
                        shina.store] = f"<b>=== Доставка {get_end_data(shina.store.split('_'[-1]))}: ===</b>\n"
                    self.result_dict[shina.store] += f"{shina.name} - <b>{shina.price} ₽</b>\n"
            else:
                self.result_dict[shina.store] += f"{shina.name} - <b>{shina.price} ₽</b>\n"
            self.shins.append(shina)

    def create_res(self):

        if "IRKUTSK" in self.result_dict:
            self.result_return_str += f"{self.result_dict['IRKUTSK']}\n"

        for i in range(40):
            if f'STORE_{i}' in self.result_dict:
                if len(self.result_return_str + "\n" + self.result_dict[f'STORE_{i}']) < 3500:
                    self.result_return_str += f"{self.result_dict[f'STORE_{i}']}\n"
                else:
                    self.result_return_list.append(self.result_return_str)
                    self.result_return_str = f"{self.result_dict[f'STORE_{i}']}\n"
        self.result_return_list.append(self.result_return_str)
        return self.result_return_list

    def __call__(self, *args, **kwargs):
        if len(self.result_dict) >= 1:
            return self.create_res()
        else:
            return ['Таких шин нет в наличии. Попробуйте ввести другой размер.']


def find_shina(weight=205, height=55, radius=16, season='Зимн'):
    try:
        result = requests.get(f"https://avtoshina38.ru/api/?w={weight}&h={height}&r={radius}").text
        result_python = json.loads(result)

        result_dict = AllShins(season)
        if len(result_python) >= 1:
            for i in result_python:
                result_dict.add_shina(
                    Shina(name=i['NAME'], price=i['PRICE'], available=i['AVAILABLE'], quantity=i['QUANTITY'], store=i["STORE"],
                          season=i["SEASON"],
                          stores=i['STORES']))
        result = result_dict()

        return result
    except Exception as ex:
        print(ex)
        return ['Таких шин нет в наличии. Попробуйте ввести другой размер.']
