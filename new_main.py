import itertools
import json
import os.path
import pprint

from props import ExcelUniversal, IDataLoader
from re import search, match, fullmatch, findall, sub


class Conf:
    FILE_WITH_NAMES = r"D:\Task\task _19"


def input_data():
    with open(r'text.txt', 'r', encoding="utf-8") as file:
        data = [i.strip() for i in file]
        return data


class Props:
    def __init__(self, path=r"D:\Task\task _19\props.xlsx"):
        self._path = path
        self._data = self._serialize_props()
        self._nd_struct = self._create_nd_struct()

    #todo замени на json
    def _serialize_props(self) -> dict[str, dict[str, list[float, ...]]]:
        """Подготовливая данные из props"""
        props: IDataLoader = ExcelUniversal()
        data_props = props.load_data(self._path)
        data_props_new = {}
        for i in data_props:
            name, nd, e = i[2], i[5], i[12]
            if name is None:
                continue
            data_props_new.setdefault(name, {}).setdefault(nd, []).append(e)
        return data_props_new

    def _create_nd_struct(self) -> dict[str, list[float, ...]]:
        nd_struct: dict = {}
        for i in self._data.values():
            for nd, elastics in i.items():
                nd = '-'.join(nd.split('-')[:-1])
                nd_struct.setdefault(self.serialize_nd(nd), []).extend(elastics)
        return nd_struct

    def serialize_nd(self, nd: str) -> str:
        nd = sub(r"-_,\.\s", r"", nd)
        # for i in "-_,. ":
        #     nd = nd.replace(i, "")
        return nd.lower()

    def is_nd(self, nd: str) -> bool:
        return self.serialize_nd(nd) in self._nd_struct

    def search_for_nd(self, nd: str) -> list:
        return self._nd_struct.get(self.serialize_nd(nd), [])


class Check:
    def __init__(self, prop: Props):
        self._props = prop

    def checking(self, name: str, elastic: float = 0):
        number, main_info, nd = self._parse_re(name)
        data = self._props.search_for_nd(nd)
        if len(data) == 0:
            self._parse_nd(nd)

    def _parse_nd(self, nd: str):
        nd = nd.replace(" ", "").lower()
        temp = ['ост', 'гост']
        # todo тут закончил

    def _serialize(self, nd: str):
        return self._props.serialize_nd(nd)

    def _parse_re(self, name):
        temp_match = match(r'(?P<id>^((\d+[-_.])*))(?P<temp>.*?)(?=(ОСТ|ТУ|ТЗ|ГОСТ))(?P<main>.*)(-\d+_\d+\.x_t)$',
                           str(name))
        groups = temp_match.groupdict()
        return groups.values()


if __name__ == "__main__":
    data_names = input_data()
    props = Props()
    check = Check(props)

    for name in data_names:
        check.checking(name)
