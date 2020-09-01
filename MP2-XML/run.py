import controller

def main():
    ctrl = controller.DBController()
    ctrl.open(server="localhost,10913", database="master", uid="user", pwd="password")
    ctrl.reset_tables()
    ctrl.insert_student(1000113, "Wade Williams", 20, "CS")
    ctrl.insert_student(1000214, "Dave Harris", 20, "CS")
    ctrl.insert_student(1002098, "Ivan Scott", 18, "EE")
    ctrl.insert_student(1002079, "Daisy White", 21, "EE")
    ctrl.insert_student(1003342, "Lucy Clark", 21, "CS")
    ctrl.insert_course(101, "Introduction to CS", 4, 3, "<Req></Req>")
    ctrl.insert_course(102, "C++", 3, 3, "<Req><Pre>101</Pre><Dept>CS</Dept></Req>")
    ctrl.insert_course(103, "Databases", 5, 2, "<Req><Pre>101</Pre><Pre>102</Pre><Dept>CS</Dept></Req>")
    ctrl.enrolled_student(101)
    ctrl.enrolled_student(102)
    ctrl.enrolled_student(103)
    ctrl.update_capacity(101, 5)
    ctrl.check_requirement(1000113, 101)
    ctrl.check_requirement(1000113, 102)
    ctrl.check_requirement(1000113, 103)
    ctrl.close()

if __name__ == "__main__":
    main()
