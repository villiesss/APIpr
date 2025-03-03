import sqlite3

DATABASE_PATH = 'data.db'

def type_(obj):
    if isinstance(obj, int):
        return obj
    elif isinstance(obj, str):
        return f'"{obj}"'
    else:
        return 0

class DB:
    @staticmethod
    def prerun_chk():
        import os
        if os.path.isfile(DATABASE_PATH):
            return True
        return False
    
    @staticmethod
    def create(query):
        #http://127.0.0.1:8000/api/request?table=users&method=create&id=&username=keklol4&uniq_key=gjghuerqtgdfbg13123&role=
        # Создаем словарь полей для запроса к БД
        SQL_query_params = {k:v for k, v in query.items() if v and k != "method"}
        SQL_query = f"""
            INSERT INTO {SQL_query_params["table"]}
            ({','.join([k for k,v in SQL_query_params.items() if k != "table"])})
            VALUES
            ({','.join([type_(v) for k,v in SQL_query_params.items() if k != "table"])})
        """
        # INSERT INTO users (username, uniq_key) VALUES ("keklol4", "gjghuerqtgdfbg13123")
        conn = sqlite3.connect(DATABASE_PATH)
        cur = conn.cursor()
        try:
            cur.execute(SQL_query)
            # commit() - метод подключения к базе данных, для сохранения изменений
            conn.commit()
            conn.close()
            return {"response": "ok!"}
        except Exception as e:
            return {"SQL_err_response": f"{repr(e)}"}

    @staticmethod
    def read(query):
        #http://127.0.0.1:8000/api/request?table=users&method=read&id=&username=keklol1&uniq_key=&role=
        response = None
        # Создаем словарь полей для запроса к БД
        SQL_query_params = {k:v for k, v in query.items() if v and k != "method"}
        #SQL_query_params = {"table": "users", "username": "keklol1"}
        SQL_query = f"""
            SELECT * FROM {SQL_query_params["table"]} 
            WHERE {' AND '.join([k+'='+type_(v) for k,v in SQL_query_params.items() if k != "table"])}
        """
        #SELECT * FROM users WHERE username=keklol1
        conn = sqlite3.connect(DATABASE_PATH)
        cur = conn.cursor()
        try:
            cur.execute(SQL_query)
            response = cur.fetchall()
            conn.close()
            return response
        except Exception as e:
            return repr(e)

    @staticmethod
    def update(query):
        #http://127.0.0.1:8000/api/request?table=user&method=update&id=5&username=test:tochange&uniq_key=&role=
        # Создаем словарь полей для запроса к БД
        # Исправить работу функции!!!
        SQL_query_params = {k:v for k, v in query.items() if v and k != "method" and "tochange" not in v}
        SQL_update_query_params = {k:v.split(":")[0] for k,v in query.items() if k!="table" and "tochange" in v}

        print(SQL_query_params)
        print(SQL_update_query_params)
        if len(SQL_query_params.values())>1:
            try:
                SQL_query = f"""
                    UPDATE {SQL_query_params["table"]}
                    SET {' , '.join(k+"="+type_(v) for k,v in SQL_update_query_params.items())}
                    WHERE {' AND '.join(k+"="+type_(v) for k,v in SQL_query_params.items() if k != "table")}
                """
                print(SQL_query)
                conn = sqlite3.connect(DATABASE_PATH)
                cur = conn.cursor()
                cur.execute(SQL_query)
                conn.commit()
                conn.close()
                return {"response": "ok"}
            except Exception as e:
                return repr(e)
        else:
            return {"response": "unsupport operation: cannot run update command without query params"}
    @staticmethod
    def delete(query):
        #http://127.0.0.1:8000/api/request?table=users&method=delete&id=&username=keklol1&uniq_key=&role=
        # Создаем словарь полей для запроса к БД
        SQL_query_params = {k:v for k, v in query.items() if v and k != "method"}
        #SQL_query_params = {"table": "users", "username": "keklol1"}
        SQL_query = f"""
            DELETE FROM {SQL_query_params["table"]} 
            WHERE {' AND '.join([k+'='+type_(v) for k,v in SQL_query_params.items() if k != "table"])}
        """
        #DELETE FROM users WHERE username=keklol1
        conn = sqlite3.connect(DATABASE_PATH)
        cur = conn.cursor()
        try:
            cur.execute(SQL_query)
            conn.commit()
            conn.close()
            return {"response": "ok"}
        except Exception as e:
            return {"SQL_delete_err": repr(e)}