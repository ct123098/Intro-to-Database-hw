import controller

def main():
    ctrl = controller.DBController()
    ctrl.open(server="localhost,10913", database="master", uid="user", pwd="password")
    ctrl.reset_tables()

    # Part 1
    ctrl.insert_student(1000113, "Wade Williams", 20, "CS")
    ctrl.insert_student(1000214, "Dave Harris", 20, "CS")
    ctrl.insert_student(1002098, "Ivan Scott", 18, "EE")
    ctrl.insert_student(1002079, "Daisy White", 21, "EE")
    ctrl.insert_student(1003342, "Lucy Clark", 21, "CS")
    ctrl.insert_student(1004000, "Alice Ant", 1, "ZOO")
    ctrl.delete_student(1004000)
    ctrl.insert_course(100, "Wrting and Communication", 3, 2, "<Req></Req>")
    ctrl.insert_course(101, "Introduction to CS", 4, 3, "<Req><Dept>CS</Dept></Req>")
    ctrl.insert_course(102, "C++", 3, 3, "<Req><Pre>101</Pre><Dept>CS</Dept></Req>")
    ctrl.insert_course(103, "Smart City", 5, 2, "<Req><Pre>101</Pre><Pre>102</Pre><Dept>CS</Dept></Req>")
    ctrl.delete_course(103)

    # Part 2
    print("Check Requirement of W&C on the 1st student: ", ctrl.check_requirement(1000113, 100))
    ctrl.register_course(1000113, 100)
    ctrl.register_course(1000214, 100)
    ctrl.register_course(1002098, 100)
    ctrl.register_course(1002079, 100)
    ctrl.register_course(1003342, 100)
    ctrl.remove_registration(1000113, 100)
    print("#Enrolled Student of W&C: ", ctrl.enrolled_student(100))
    ctrl.update_capacity(100, 5)
    ctrl.register_course(1002079, 100)
    ctrl.register_course(1003342, 100)
    print("#Enrolled Student of W&C: ", ctrl.enrolled_student(100))
    
    # Part 3
    print("Check Requirement of ICS on the 1st student(CS): ", ctrl.check_requirement(1000113, 101))
    print("Check Requirement of ICS on the 3st student(EE): ", ctrl.check_requirement(1002098, 101))
    ctrl.register_course(1000113, 101)
    ctrl.register_course(1000214, 101)
    ctrl.register_course(1002098, 101)
    ctrl.register_course(1002079, 101)
    ctrl.register_course(1003342, 101)
    ctrl.remove_registration(1003342, 101)
    print("#Enrolled Student of ICS: ", ctrl.enrolled_student(101))

    # Part 4
    print("Check Requirement of ICS on the 2st student(w/o grade): ", ctrl.check_requirement(1000214, 102))
    ctrl.register_course(1000113, 102)
    ctrl.register_course(1000214, 102)
    print("#Enrolled Student of C++: ", ctrl.enrolled_student(102))
    ctrl.update_grade(1000113, 101, 90)
    ctrl.update_grade(1000214, 101, 51)
    print("Check Requirement of ICS on the 2st student(w/ grade): ", ctrl.check_requirement(1000214, 102))
    print("Check Requirement of ICS on the 5st student(w/o ICS): ", ctrl.check_requirement(1003342, 102))
    ctrl.register_course(1000113, 102)
    ctrl.register_course(1000214, 102)
    ctrl.register_course(1002098, 102)
    ctrl.register_course(1002079, 102)
    ctrl.register_course(1003342, 102)
    print("#Enrolled Student of C++: ", ctrl.enrolled_student(102))

    # Part 5
    ctrl.update_grade(1000113, 100, 100) # nothing will happen
    ctrl.update_grade(1000214, 100, 99)
    ctrl.update_grade(1002098, 100, 91)
    ctrl.update_grade(1002079, 100, 80)
    ctrl.update_grade(1003342, 100, 59)
    
    ctrl.update_grade(1000113, 102, 99)
    ctrl.update_grade(1000214, 102, 95)

    print("Academic History of the 2st student: ", ctrl.retrieve_academic_history(1000214))
    print("GPA of the 2st student: ", ctrl.compute_GPA(1000214))
    
    print("Average Grade of W&C: ", ctrl.compute_average_grade(100))
    print("Average Grade of C++: ", ctrl.compute_average_grade(102))

    print("Failure History: ", ctrl.retrieve_failure_history())

    ctrl.close()

if __name__ == "__main__":
    main()
