import sqlite3


class DatabaseConnector:
    def __init__(self, database):
        self.database = database

    def execute(self, query, *args):
        connection = sqlite3.connect(self.database)  # to prevent different Thread error
        cursor = connection.execute(query, args)
        res = [row for row in cursor]
        connection.commit()
        return res if len(res) > 0 else None

    def create_tables(self):
        connection = sqlite3.connect(self.database)
        connection.execute("""
            create table Student(
                s_id    BIGINT PRIMARY KEY,
                [name]  VARCHAR(50),
                major   VARCHAR(50),
                pass    VARCHAR(50)
            )
        """)
        connection.execute("""
        create table Teacher(
            t_id    BIGINT PRIMARY KEY,
            [name]  VARCHAR(50),
            pass    VARCHAR(50)
        );
        """)
        connection.execute("""
        create table Course(
            "c_id"        INTEGER ,
            [name]        VARCHAR(50),
            unit          INT,
            t_id          BIGINT,
            Notifications VARCHAR(50),
            poll          VARCHAR(4096),
            
            PRIMARY KEY("c_id" AUTOINCREMENT)
        );
        """)
        connection.execute("""
        create table [take](
            c_id    BIGINT,
            s_id    BIGINT,
            [date]  DATETIME DEFAULT CURRENT_TIMESTAMP,
            mark    FLOAT DEFAULT -1,
            choice  INT DEFAULT -1,
        );
        """)
        connection.execute("""
        create table   [User](
            chatId     BIGINT,
            utype      INT,
            [uid]      BIGINT,
            [state]    BIGINT,
            [data]     VARCHAR (50),
        );
        """)
        connection.commit()

    def get_user(self, chat_id):
        return self.execute(f"SELECT * FROM User where chatId = {chat_id}")

    def get_student(self, s_id):
        return self.execute(f"SELECT * FROM Student where s_id = {s_id}")

    def get_teacher(self, t_id):
        return self.execute(f"SELECT * FROM Teacher where t_id = {t_id}")

    def get_course_teacher_login(self, c_id):
        return self.execute(f"""SELECT * FROM Course 
            JOIN User on User.uid = Course.t_id WHERE c_id = {c_id}""")

    def set_user(self, chat_id, utype, uid):
        return self.execute(f"INSERT INTO [User] (chatId, utype, [uid], [state]) VALUES ({chat_id},{utype},{uid},0)")

    def delete_user(self, chat_id):
        return self.execute(f"DELETE FROM [User] where chatId = {chat_id}")

    def get_student_courses(self, s_id):
        return self.execute(f"""SELECT * FROM Student 
            JOIN take on Student.s_id = take.s_id 
            JOIN Course on take.c_id = Course.c_id 
            where Student.s_id = {s_id}""")

    def create_student(self, s_id, name, major, password):
        return self.execute( f'INSERT INTO Student (s_id, [name], major, pass) VALUES ({s_id}, "{name}", "{major}", "{password}")')

    def get_all_taking_courses(self):
        return self.execute(f"SELECT * FROM Course JOIN Teacher on Teacher.t_id = Course.t_id")

    def get_course(self, c_id):
        return self.execute(f"SELECT * FROM Course where c_id = {c_id}")

    def update_user_state(self, chat_id, state):
        return self.execute(f"Update User set state = {state} where chatId = {chat_id}")

    def update_user_data(self, chat_id, data):
        return self.execute(f"Update User set [data] = {data} where chatId = {chat_id}")

    def take_course(self, s_id, c_id):
        return self.execute(f"INSERT INTO take (c_id, s_id, mark) VALUES ({c_id}, {s_id}, {-1})")

    def student_see_course(self, s_id, c_id):
        return self.execute(f"""SELECT * FROM Student 
            JOIN take on Student.s_id = take.s_id 
            JOIN Course on take.c_id = Course.c_id 
            JOIN Teacher on Teacher.t_id = Course.t_id 
            where Student.s_id = {s_id} and Course.c_id={c_id}""")

    def get_teacher_courses(self, t_id):
        return self.execute(f"SELECT * FROM Course where t_id = {t_id}")

    def create_course(self,name, unit, t_id):
        return self.execute(f"""INSERT INTO Course (name, unit, t_id, poll) 
                    VALUES ("{name}", {unit}, {t_id}, "")""")

    def students_of_course(self, c_id):
        return self.execute(f"""SELECT * FROM Student 
            JOIN take on Student.s_id = take.s_id 
            JOIN Course on take.c_id = Course.c_id 
            where Course.c_id={c_id}""")

    def set_student_mark(self, s_id, c_id, mark):
        return self.execute(f"""UPDATE take set mark = {mark} 
                    where s_id = {s_id} and c_id = {c_id}""")

    def is_student_of_course(self, s_id, c_id):
        return self.execute(f"SELECT * FROM take where s_id = {s_id} and c_id = {c_id}")

    def remove_taken_course(self, s_id, c_id):
        return self.execute(f"DELETE FROM take where s_id = {s_id} and c_id = {c_id}")

    def update_course_poll(self, c_id, poll):
        return self.execute(f"Update Course set poll = '{poll}' where c_id = {c_id}")

    def get_course_all_students_chatid(self, c_id):
        return self.execute(f"""SELECT chatId FROM Student 
                   JOIN [User] on [User].uid = Student.s_id
                   JOIN take on Student.s_id = take.s_id 
                   JOIN Course on take.c_id = Course.c_id   
                   where Course.c_id={c_id}""")

    def update_student_choice(self, c_id, s_id, choice):
        return self.execute(f"Update take set choice = {choice} where c_id = {c_id} and s_id = {s_id}")

    def update_course_notif(self, c_id, notif):
        return self.execute(f"Update Course set Notifications = '{notif}' where c_id = {c_id}")
