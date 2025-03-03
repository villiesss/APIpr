#query = {"table": "table_name", "method": "method_name", "useraname": username, ...}
import json
from driver import DB

METHODS = ["create", "read", "update", "delete"]

class Dispatcher:
    def __schema_loader__(self):
        with open("schemas.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def dispatch(self, query):
        response = None
        # Если в строке запроса нет обращения к таблице или отсутствует метод
        if not "table" in query.keys() or not "method" in query.keys():
            return {"response_error": "query must include table name and method type"}
        schemas = self.__schema_loader__()
        # Если в строке запроса указана несуществующая таблица
        if not query["table"] in schemas.keys():
            return {"response_error": "unknown table name"}
        # Если указанный метод не существует в рамках API
        if not query["method"] in METHODS:
            return {"response_error": "unknown method name"}
        # Если набор полей из схемы БД не соответствует набору оставшихся аргументов из запроса
        if schemas[query["table"]] != list(query.keys())[2:]:
            return {"response_error": f"uknown table '{schemas[query["table"]]}' fields"}
        # Проверка не пустые значения по ключам
        if not len(set(list(query.values())[2:])) > 1:
        # if not len() > 1 - если длина объекта больше единицы (содержится больше одного значения)
        #   set() - это набор уникальных данных из списка (или аналогичной структуры)
        #       list()[2:] - прямое преобразование структуры в список. Выбираем из списка все значения, кроме двух первых
        #           query.values() - содержимое строки запроса (строка запроса == словарь). Выбираем из словаря ТОЛЬКО значения
            return {"response_error": "null values error"}
        # Выполнение функции драйвера
        if query["method"] == "read":
            response = DB.read(query)
        elif query["method"] == "create":
            response = DB.create(query)
        elif query["method"] == "delete":
            response = DB.delete(query)
        elif query["method"] == "update":
            response = DB.update(query)
        # Завершение выполнения функции драйвера
        return {"response": response}
