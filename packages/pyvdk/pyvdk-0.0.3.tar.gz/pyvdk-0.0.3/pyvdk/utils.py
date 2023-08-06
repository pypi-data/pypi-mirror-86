from typing import Any
from pathlib import Path
import jinja2


class DictToObject:
    """ Transforms dict to object """

    _raw_dict: dict

    def __init__(self, dict_object: dict) -> None:
        self._raw_dict = dict_object
        for k, v in dict_object.items():
            selected = self.type_handle(v)
            self.__setattr__(k, selected)

    def __repr__(self) -> str:
        return f"<DictToObject: {self._raw_dict}>"

    def get(self, attr: str) -> Any:
        """ Get attribute """

        return self._raw_dict.get(attr)

    @staticmethod
    def type_handle(x: Any) -> Any:
        """ Handle types """

        if isinstance(x, dict):
            return DictToObject(x)
        if isinstance(x, (list, tuple)):
            return [DictToObject.type_handle(i) for i in x]
        return x


class Junk:
    """ Some junk utils """

    @staticmethod
    def form_render(path: str, **kwargs) -> str:
        """ Just jinja2 """

        file_text = Path(path).read_text()
        template = jinja2.Template(file_text)
        return template.render(**kwargs)

    @staticmethod
    def get_chat_id(peer_id: int) -> int:
        """ Get chat id from peer id """

        return int(peer_id - 2e9)