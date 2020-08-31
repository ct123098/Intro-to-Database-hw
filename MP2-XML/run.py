import controller

def main():
    ctrl = controller.DBController()
    ctrl.open(server="localhost,10913", database="mydatabase", uid="user", pwd="password")
    ctrl.reset_tables()
    ctrl.insert_student(1000113, "Wade Williams", 20, "CS")
    ctrl.insert_student(1000214, "Dave Harris", 20, "CS")
    ctrl.insert_student(1002098, "Ivan Scott", 18, "EE")
    ctrl.insert_student(1002079, "Daisy White", 21, "EE")
    ctrl.insert_student(1003342, "Lucy Clark", 21, "CS")
    ctrl.insert_course(101, "Introduction to CS", 4, 3, "<Req></Req>")
    ctrl.insert_course(102, "C++", 3, 3, "<Req><PrerequisiteCourse>101</PrerequisiteCourse><Dept>CS</Dept></Req>")
    ctrl.close()

if __name__ == "__main__":
    main()
