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
    print("Check Requirement of W&C on the 1st student: ", ctrl.check_requirement(1000113, 100)) # True
    ctrl.register_course(1000113, 100) # enrolled student = 1
    ctrl.register_course(1000214, 100) # 2
    ctrl.register_course(1002098, 100) # 3
    ctrl.register_course(1002079, 100) # failed
    ctrl.register_course(1003342, 100) # failed
    ctrl.remove_registration(1000113, 100) # 2
    print("#Enrolled Student of W&C: ", ctrl.enrolled_student(100)) # 2
    ctrl.update_capacity(100, 5)
    ctrl.register_course(1002079, 100) # 3
    ctrl.register_course(1003342, 100) # 4
    print("#Enrolled Student of W&C: ", ctrl.enrolled_student(100)) # 4
    
    # Part 3
    print("Check Requirement of ICS on the 1st student(CS): ", ctrl.check_requirement(1000113, 101)) # True
    print("Check Requirement of ICS on the 3st student(EE): ", ctrl.check_requirement(1002098, 101)) # False
    ctrl.register_course(1000113, 101) # enrolled student = 1
    ctrl.register_course(1000214, 101) # 2
    ctrl.register_course(1002098, 101) # failed
    ctrl.register_course(1002079, 101) # failed
    ctrl.register_course(1003342, 101) # 3
    ctrl.remove_registration(1003342, 101) # 2
    print("#Enrolled Student of ICS: ", ctrl.enrolled_student(101)) # 2

    # Part 4
    print("Check Requirement of ICS on the 2st student(w/o grade): ", ctrl.check_requirement(1000214, 102)) # False
    ctrl.register_course(1000113, 102) # failed
    ctrl.register_course(1000214, 102) # failed
    print("#Enrolled Student of C++: ", ctrl.enrolled_student(102)) # 0
    ctrl.update_grade(1000113, 101, 90) # give grades to ICS
    ctrl.update_grade(1000214, 101, 51)
    print("Check Requirement of ICS on the 2st student(w/ grade): ", ctrl.check_requirement(1000214, 102)) # True
    print("Check Requirement of ICS on the 5st student(w/o ICS): ", ctrl.check_requirement(1003342, 102)) # False
    ctrl.register_course(1000113, 102) # enrolled student = 1
    ctrl.register_course(1000214, 102) # 2
    ctrl.register_course(1002098, 102) # failed
    ctrl.register_course(1002079, 102) # failed
    ctrl.register_course(1003342, 102) # failed
    print("#Enrolled Student of C++: ", ctrl.enrolled_student(102)) # 2

    # Part 5
    ctrl.update_grade(1000113, 100, 100) # skip (due to no registration)
    ctrl.update_grade(1000214, 100, 99) # give grades to W&C
    ctrl.update_grade(1002098, 100, 91)
    ctrl.update_grade(1002079, 100, 80)
    ctrl.update_grade(1003342, 100, 59)
    ctrl.update_grade(1000113, 102, 89) # give grades to C++
    ctrl.update_grade(1000214, 102, 95)
    print("Academic History of the 1st student: ", ctrl.retrieve_academic_history(1000113)) # 101, 102
    print("GPA of the 1st student: ", ctrl.compute_GPA(1000113)) # (4.0 * 3 + 3.0 * 3) / 6 = 3.5
    print("Academic History of the 2nd student: ", ctrl.retrieve_academic_history(1000214)) # 100, 101, 102
    print("GPA of the 2nd student: ", ctrl.compute_GPA(1000214)) # (4.0 * 2 + 0.0 * 3 + 4.0 * 3) / 8 = 2.5
    print("Average Grade of W&C: ", ctrl.compute_average_grade(100)) # (99 + 91 + 80 + 59) / 4 = 82.25
    print("Average Grade of C++: ", ctrl.compute_average_grade(102)) # (89 + 95) / 2 = 92
    print("Failure History: ", ctrl.retrieve_failure_history()) # 5th student on W&C | 2nd student on ICS

    ctrl.close()

if __name__ == "__main__":
    main()
