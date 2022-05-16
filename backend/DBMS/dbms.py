import psycopg2
import json


class DataBaseManagemantSystem:
    def __init__(self):
        self.con = psycopg2.connect(
            database="postgres",
            user="igor",
            password="i4127493I",
            host="10.50.5.1"
        )
        self.cur = self.con.cursor()

    def __del__(self):
        self.con.close()

    def add_user(self, name, password, email):
        self.cur.execute("insert into users (email, name, password) values (%s, %s, %s)", [email, name, password])
        self.con.commit()

    def add_record(self, pulse):
        self.cur.execute("insert into pulse_signals (pulse) values (%s) returning id;", [pulse])
        id = self.cur.fetchall()
        self.con.commit()
        return id[0][0]

    def get_records_by_status(self, status):
        '''
        :param status: status == 0 - данные только что пришли с сайта
                       status == 1 - данные ушли в машинку и обрабатываются
                       status == 2 - данные обработаны машинкой
                       status == 3 - данные отданы пользователю
                       status == 4 - данные не требуются, процесс надо убить
        :return: все строки с данным статусом
        '''
        self.cur.execute("select * from pulse_signals where status=%s", [status])
        rows = self.cur.fetchall()
        needed_rows = list()
        for row in rows:
            needed_rows.append({"id": row[0], "pulse": row[1], "status": row[2], "info": row[3]})
        return needed_rows

    def get_record_by_id(self, id):
        self.cur.execute("select * from pulse_signals where id=%s", [id])
        row = self.cur.fetchone()
        self.con.commit()
        needed_row = ({"id": row[0], "pulse": row[1], "status": row[2], "info": row[3]})
        return needed_row

    def check_user(self, email):
        self.cur.execute("select exists(select from users where email=%s);", [email])
        return self.cur.fetchall()[0][0]

    def update_record(self, new_row):
        self.cur.execute("update pulse_signals set status=%s where id=%s", [new_row["status"], new_row["id"]])
        self.cur.execute("update pulse_signals set info=%s where id=%s", [new_row["info"], new_row["id"]])
        self.con.commit()

    def update_flag(self, new_flag, email):
        self.cur.execute("update users set is_online=%s where email=%s", [new_flag, email])
        self.con.commit()

    def update_status_by_email(self, new_status, email):
        self.cur.execute("select (last_id) from users where email=%s", [email])
        id = self.cur.fetchone()[0]
        self.cur.execute("update pulse_signals set status=%s where id=%s", [new_status, id])
        self.con.commit()

    def get_info_by_email(self, email):
        self.cur.execute("select * from users where email=%s", [email])
        row = self.cur.fetchone()
        self.con.commit()
        needed_row = ({"email": row[0], "name": row[1], "password": row[2], "is_login": row[3]})
        if row[4] != -1:
            more_info = self.get_record_by_id(row[4])
            needed_row["status"] = more_info["status"]
            needed_row["info"] = more_info["info"]
        return needed_row

    def insert_json_into_postgres(self, email, file):
        record_list = json.load(file)
        pulse = record_list["points"][-1]["fpVal"]
        self.add_record(pulse)