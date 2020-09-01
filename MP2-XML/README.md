# Machine Problem 2

## Requirement

Write a program, supporting the following functions:

- Connect to a remote relational database server that contains the following tables:
    - A **student** table containing 4 columns: (ID, Name, Age, Dept)
    - A **course** table containing 6 columns: (CourseID, CourseName, Capacity, RemainCapacity, CreditHours, Requirement), the data type of Requirement column is xml, you can specify things like prerequisite course or department limitation
    - A **course registration** table containing two foreign key attributes and a grade attribute: (StudentID, CourseID, Grade)
- Insert tuples into student & course table
- Remove tuples from student & course table
- Look up the number of students enrolled in a course
- Check whether a student satisfies the requirement of a course
- Register a student to a course, reject this operation if the course is already at capacity limit or the student cannot register due to unmet requirements (use transaction)
- Remove a student from a course (use transaction)
- Update the capacity of a course, reject this operation if the number of students already enrolled exceeds the new capacity (use transaction)
- Retrieve the list of courses a student have attended in the past
- Retrieve all the course failure records – all the <student, course> pair that the student failed to pass the course (grade < 60)
- Update the grade of a student in a course
- Compute the GPA of a student
- Compute the average grade of students in a course

## Usage

remarks:

- If you use SQL Server on a remote/virtual machine, please open TCP/IP protocol switch, and check your port. 
- If you run this program on a machine where SQL Server is not installed, please make sure whether you have installed an ODBC driver.

## XML Schema

```xml
<xs:element name="Req">
  <xs:complexType>
    <xs:sequence>
      <xs:element name="Pre" type="xs:int" minOccurs="0" maxOccurs="unbounded"/>
      <xs:element name="Dept" type="xs:string" minOccurs="0" maxOccurs="1"/>
    </xs:sequence>
  </xs:complexType>
</xs:element>
```

