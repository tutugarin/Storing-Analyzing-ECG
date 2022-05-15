import psycopg2


class DataBaseManagemantSystem:
    def __init__(self, name, password):
        self.con = psycopg2.connect(
            database="postgres",
            user=name,
            password=password,
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
        :return: все строки с данным статусом
        '''
        self.cur.execute("select (id, pulse, status, info) from pulse_signals where status=%s", [status])
        rows = self.cur.fetchall()
        needed_rows = list()
        for row in rows:
            needed_rows.append({"id": row[0], "data": row[1], "status": row[2] + 1, "info": row[3]})
            self.update_record(needed_rows[-1])
        self.con.commit()
        return needed_rows

    def get_record_by_id(self, id):
        self.cur.execute("select (id, pulse, status, info) from pulse_signals where id=%s", [id])
        row = self.cur.fetchall()
        self.con.commit()
        needed_row = ({"id": row[0], "data": row[1], "status": row[2], "info": row[3]})
        return needed_row

    def get_password_by_name(self, name):
        self.cur.execute("select (password) from users where name=%s", [name])
        password = self.cur.fetchall()
        self.con.commit()
        if password[0].size() == 0:
            return "user doesn't exist"
        return password[0][0]

    def update_record(self, new_row):
        self.cur.execute("update pulse_signals set status=%s info=%s where id=%s", [new_row["status"], new_row["info"], new_row["id"]])
        self.con.commit()

    def update_status(self, new_status, name):
        self.cur.execute("update users set is_online=%s where name=%s", [new_status, name])
        self.con.commit()

#    def insert_json_into_postgres(self):

prom = DataBaseManagemantSystem("igor", "i4127493I")
#prom.add_record(75)
print(prom.get_records_by_status(0))