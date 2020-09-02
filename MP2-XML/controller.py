import pyodbc

class DBController():
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open(self, server, database, uid, pwd):
        # print(pyodbc.drivers())
        conn_str = """
            DRIVER={{ODBC Driver 17 for SQL Server}};
            SERVER={server};
            DATABASE={database};
            UID={uid};
            PWD={pwd};
        """.format(server=server, database=database, uid=uid, pwd=pwd)
        # print(conn_str)
        # return 
        self.conn = pyodbc.connect(conn_str, autocommit=False)
        # print("ok.")
        print("[INFO] connection established.")
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()
        print("[INFO] connection closed.")

    def reset_tables(self):
        self.conn.autocommit = True
        self.cursor.execute("USE master;")
        self.cursor.execute("DROP DATABASE IF EXISTS mydatabase;")
        self.cursor.execute("CREATE DATABASE mydatabase;")
        self.cursor.execute("USE mydatabase;")
        self.cursor.execute("""
            CREATE TABLE Student (
                ID INT PRIMARY KEY,
                Name VARCHAR(MAX),
                Age INT,
                Dept VARCHAR(MAX)
            );
        """)
        self.cursor.execute("""
            CREATE TABLE Course (
                CourseID INT PRIMARY KEY,
                CourseName VARCHAR(MAX),
                Capacity INT,
                RemainCapacity INT CHECK (RemainCapacity >= 0),
                CreditHour INT,
                Requirement xml
            );
        """)
        self.cursor.execute("""
            CREATE TABLE Registration (
                StudentID INT FOREIGN KEY REFERENCES Student(ID),
                CourseID INT FOREIGN KEY REFERENCES Course(CourseID),
                Grade INT
            );
        """)
        self.conn.autocommit = False
        print("[INFO] tables are reset.")

    def insert_student(self, ID, name, age, dept):
        '''
        Args:
            ID (int)
            name (string)
            age (int)
            dept (string)
        '''
        self.cursor.execute("""
            INSERT INTO Student(ID, Name, Age, Dept)
            VALUES (?, ?, ?, ?)
        """, ID, name, age, dept)
        self.conn.commit()

    def delete_student(self, ID):
        self.cursor.execute("""
            DELETE FROM Student
            WHERE ID = ?
        """, ID)
        self.conn.commit()

    def insert_course(self, ID, name, capacity, credit_hour, requirement):
        '''
        Args:
            ID (int)
            name (string)
            capacity (int)
            credit_hour (int)
            requirement (string)
        '''
        self.cursor.execute("""
            INSERT INTO Course(CourseID, CourseName, Capacity, RemainCapacity, CreditHour, Requirement)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ID, name, capacity, capacity, credit_hour, requirement)
        self.conn.commit()

    def delete_course(self, ID):
        self.cursor.execute("""
            DELETE FROM Course
            WHERE CourseID = ?
        """, ID)
        self.conn.commit()

    def enrolled_student(self, courseID):
        '''
        Returns:
            int
        '''
        row = self.cursor.execute("""
            SELECT Capacity - RemainCapacity AS Cnt
            FROM Course
            WHERE CourseID = ?
        """, courseID).fetchone()
        # print(row)
        res = row.Cnt if row else None
        # print(res)
        return res

    def check_requirement(self, studentID, courseID):
        '''
        Returns:
            bool
        '''
        # Step 1: whether all preresiquite courses have been registered
        # return the number of course not taken
        flag1 = self.cursor.execute("""
            SELECT COUNT(A.CourseID) - COUNT(B.CourseID) AS Flag
            FROM (
                SELECT x.value('.', 'int') AS CourseID
                FROM Course
                CROSS APPLY Requirement.nodes('/Req/Pre') AS T(x)
                WHERE CourseID = ?
            ) A LEFT JOIN (
                SELECT CourseID
                FROM Registration
                WHERE StudentID = ? AND Grade IS NOT NULL
            ) B ON A.CourseID = B.CourseID
        """, courseID, studentID).fetchone().Flag
        # print(flag1)
        if flag1 > 0:
            return False
        # Step 2: whether the department requirement is satisfied
        # return 0 if satisfied, 1 if not satisfied
        flag2 = self.cursor.execute("""
            SELECT COUNT(A.Dept) - COUNT(B.Dept) AS Flag
            FROM (
                SELECT Requirement.value('(/Req/Dept)[1]', 'varchar(max)') AS Dept
                FROM Course
                WHERE CourseID = ?
            ) A LEFT JOIN (
                SELECT Dept
                FROM Student
                WHERE ID = ?
            ) B ON A.Dept = B.Dept
        """, courseID, studentID).fetchone().Flag
        if flag2 == 1:
            return False
        return True

    def register_course(self, studentID, courseID):
        # Step 0: check whether student and course exist
        flag0 = self.cursor.execute("""
            SELECT COUNT(*) AS Flag
            FROM Student, Course
            WHERE ID = ? AND CourseID = ?
        """, studentID, courseID).fetchone().Flag
        if flag0 == 0:
            return
        # Step 1: if the student has already register this course, exit
        # return 0 if not registered, 1 if registered
        flag1 = self.cursor.execute("""
            SELECT COUNT(*) AS Flag
            FROM Registration
            WHERE StudentID = ? AND CourseID = ?
        """, studentID, courseID).fetchone().Flag
        if flag1 == 1:
            return
        # Step 2: if the remain capacity = 0, exit
        # return remain capacity
        flag2 = self.cursor.execute("""
            SELECT RemainCapacity AS Flag
            FROM Course
            WHERE CourseID = ?
        """, courseID).fetchone().Flag
        if flag2 == 0:
            return
        # Step 3: if the student does not meet the requirement, exit
        flag3 = self.check_requirement(studentID, courseID)
        if flag3 == False:
            return
        # Step 4: update course, add registration
        self.cursor.execute("""
            INSERT INTO Registration(StudentID, CourseID, Grade)
            VALUES (?, ?, NULL)
        """, studentID, courseID)
        self.cursor.execute("""
            UPDATE Course
            SET RemainCapacity = RemainCapacity - 1
            WHERE CourseID = ?
        """, courseID)
        self.conn.commit()

    def remove_registration(self, studentID, courseID):
        # Step 1: if the registration does not exist, exit
        # Also, if the grade is given, you cannot remove the registration
        # return number of not graded registration 
        flag1 = self.cursor.execute("""
            SELECT COUNT(*) AS Flag
            FROM Registration
            WHERE StudentID = ? AND CourseID = ?
            AND Grade IS NULL
        """, studentID, courseID).fetchone().Flag
        if flag1 == 0:
            return 
        # Step 2: update course, delete registration
        self.cursor.execute("""
            DELETE Registration
            WHERE StudentID = ? AND CourseID = ?
        """, studentID, courseID)
        self.cursor.execute("""
            UPDATE Course
            SET RemainCapacity = RemainCapacity + 1
            WHERE CourseID = ?
        """, courseID)
        self.conn.commit()

    def update_capacity(self, courseID, new_capacity):
        # update course if the (capacity - new_capacity) <= (remain_capacity)
        self.cursor.execute("""
            UPDATE Course
            SET Capacity = ?, RemainCapacity = RemainCapacity - (Capacity - ?)
            WHERE CourseID = ? AND Capacity - ? <= RemainCapacity
        """, new_capacity, new_capacity, courseID, new_capacity)
        self.conn.commit()

    def retrieve_academic_history(self, studentID):
        '''
        Returns:
            list[int]
        '''
        rows = self.cursor.execute("""
            SELECT CourseID
            FROM Registration
            WHERE StudentID = ?
        """, studentID).fetchall()
        res = [row.CourseID for row in rows]
        # print(res)
        return res

    def retrieve_failure_history(self):
        '''
        Returns:
            list[(int, int)]
        '''
        rows = self.cursor.execute("""
            SELECT StudentID, CourseID
            FROM Registration
            WHERE Grade < 60
        """).fetchall()
        res = [(row.StudentID, row.CourseID) for row in rows]
        # print(res)
        return res

    def update_grade(self, studentID, courseID, new_grade):
        self.cursor.execute("""
            UPDATE Registration
            SET Grade = ?
            WHERE StudentID = ?
            AND CourseID = ?
        """, new_grade, studentID, courseID)
        self.conn.commit()

    def compute_GPA(self, studentID):
        '''
        Returns:
            float
        '''
        row = self.cursor.execute("""
            SELECT SUM(
                CreditHour * CASE
                    WHEN Grade >= 90 THEN 4.0
                    WHEN Grade >= 80 AND Grade < 90 THEN 3.0
                    WHEN Grade >= 70 AND Grade < 80 THEN 2.0
                    WHEN Grade >= 60 AND Grade < 70 THEN 1.0
                    ELSE 0.0
                END
            ) / SUM(CreditHour) AS GPA
            FROM (Registration JOIN Course ON Registration.CourseID = Course.CourseID)
            WHERE StudentID = ?
            AND Grade IS NOT NULL
        """, studentID).fetchone()
        res = row.GPA if row else None
        # print(res)
        return res

    def compute_average_grade(self, courseID):
        '''
        Returns:
            float
        '''
        row = self.cursor.execute("""
            SELECT AVG(1.0 * Grade) AS Ave_grade
            FROM Registration
            WHERE CourseID = ?
            AND Grade IS NOT NULL
        """, courseID).fetchone()
        res = row.Ave_grade if row else None
        # print(res)
        return res
