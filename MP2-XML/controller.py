import pyodbc

class DBController():
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open(self, server, database, uid, pwd):
        print(pyodbc.drivers())
        conn_str = """
            DRIVER={{ODBC Driver 17 for SQL Server}};
            SERVER={server};
            DATABASE={database};
            UID={uid};
            PWD={pwd};
        """.format(server=server, database=database, uid=uid, pwd=pwd)
        # print(conn_str)
        # return 
        self.conn = pyodbc.connect(conn_str)
        # print("ok.")
        print("[INFO] connection established.")
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def create_tables(self):
        pass

    def insert_student(self, ID, name, age, dept):
        '''
        Args:
            ID (int)
            name (string)
            age (int)
            dept (string)
        '''
        pass

    def insert_course(self, ID, name, capacity, credit_hour, requirement):
        '''
        Args:
            ID (int)
            name (string)
            capacity (int)
            credit_hour (int)
            requirement (string)
        '''
        pass

    def delete_student(self, ID):
        pass

    def delete_course(self, ID):
        pass

    def enrolled_student(self, courseID):
        '''
        Returns:
            int
        '''
        pass

    def check_requirement(self, studentID, courseID):
        '''
        Returns:
            bool
        '''
        pass

    def register_course(self, studentID, courseID):
        pass

    def remove_registration(self, studentID, courseID):
        pass

    def update_capacity(self, courseID, new_capacity):
        pass

    def retrieve_academic_history(self, studentID):
        '''
        Returns:
            list[int]
        '''
        pass

    def retrieve_failure_history(self):
        '''
        Returns:
            list[(int, int)]
        '''
        pass

    def update_grade(self, studentID, courseID, new_grade):
        pass

    def compute_GPA(self, studentID):
        '''
        Returns:
            float
        '''
        pass

    def compute_average_grade(self, courseID):
        '''
        Returns:
            float
        '''
        pass