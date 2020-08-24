#include "sqlite3.h"

#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <sstream>
#include <vector>

using namespace std;

struct Student
{
    int id;
    string name;
    double GPA;
    int age;
};
vector<Student> vec;

static char *errMsg = NULL;
static int callback(void *p, int argc, char **argv, char **azColName)
{
    // cerr << "callback" << endl;
    vector<Student> *vec = (vector<Student>*)p;
    Student s = {};
    for (int i = 0; i < argc; i++) {
        if (strcmp(azColName[i], "ID") == 0) s.id = atoi(argv[i]);
        else if (strcmp(azColName[i], "Name") == 0) s.name = argv[i];
        else if (strcmp(azColName[i], "GPA") == 0) s.GPA = atof(argv[i]);
        else if (strcmp(azColName[i], "Age") == 0) s.age = atoi(argv[i]);
        // cerr << azColName[i] << " = " << (argv[i] ? argv[i] : "NULL") << " | ";
    }
    // cerr << endl;
    vec->push_back(s);
    return 0;
}

string to_string(const string &s)
{
    return "'" + s + "'";
}

class SimpleController
{
private:
    sqlite3 *db;

public:
    SimpleController(const string &path)
    {
        int rc = sqlite3_open(path.c_str(), &db);
        handle_error(rc, NULL, "Error encontered when opening " + path);
        cout << "[INFO] Database " << path << " is opened." << endl;
    }
    ~SimpleController()
    {
        sqlite3_close(db);
    }
    void handle_error(int rc, char *errMsg, const string &prtMsg)
    {
        if (rc) {
            cout << "[ERROR] " << prtMsg << endl;
            cout << "[ERROR] " << "error code: " << rc << endl;
            if (errMsg != NULL) sqlite3_free(errMsg);
            sqlite3_close(db);
            exit(rc);
        }
    }
    void remove_table()
    {
        string sql = "DROP TABLE IF EXISTS Students;";
        cout << ">>> " << sql << endl;
        int rc = sqlite3_exec(db, sql.c_str(), callback, 0, &errMsg);
        handle_error(rc, errMsg, "Error encontered when creating table");
        cout << "[INFO] Table Students is removed" << endl;
    }
    void create_table()
    {
        string sql = "CREATE TABLE IF NOT EXISTS Students (ID INT, Name TEXT, GPA REAL, Age INT);";
        cout << ">>> " << sql << endl;
        int rc = sqlite3_exec(db, sql.c_str(), callback, 0, &errMsg);
        handle_error(rc, errMsg, "Error encontered when creating table");
        cout << "[INFO] Table Students is created" << endl;
    }
    void insert(int id, const string &name, double GPA, int age)
    {
        string sql = "INSERT INTO Students (ID, Name, GPA, Age) VALUES (" 
            + to_string(id) + ", " + to_string(name) + ", " + to_string(GPA) + ", " + to_string(age) + ");";
        cout << ">>> " << sql << endl;
        int rc = sqlite3_exec(db, sql.c_str(), callback, 0, &errMsg);
        handle_error(rc, errMsg, "Error encontered when inserting");
    }
    void remove_by_id(int id)
    {
        string sql = "DELETE FROM Students WHERE ID = " + to_string(id) + ";";
        cout << ">>> " << sql << endl;
        int rc = sqlite3_exec(db, sql.c_str(), callback, 0, &errMsg);
        handle_error(rc, errMsg, "Error encontered when inserting");
    }
    void select_by_id(int id) {
        string sql = "SELECT Name, GPA, Age FROM Students WHERE ID = " + to_string(id) + ";";
        cout << ">>> " << sql << endl;
        vector<Student> vec;
        int rc = sqlite3_exec(db, sql.c_str(), callback, &vec, &errMsg);
        handle_error(rc, errMsg, "Error encontered when inserting");
        if (vec.size() > 0)
            for (int i = 0; i < vec.size(); i++)
                cerr << "Name = " << vec[i].name << " | GPA = " << vec[i].GPA << " | Age = " << vec[i].age << endl;
        else
            cerr << "Not Found." << endl;
    }
    void select_all()
    {
        string sql = "SELECT ID, Name, GPA, Age FROM Students";
        cout << ">>> " << sql << endl;
        vector<Student> vec;
        int rc = sqlite3_exec(db, sql.c_str(), callback, &vec, &errMsg);
        handle_error(rc, errMsg, "Error encontered when inserting");
        for (int i = 0; i < vec.size(); i++)
            cerr << "ID = " << vec[i].id << " | Name = " << vec[i].name << " | GPA = " << vec[i].GPA 
                << " | Age = " << vec[i].age << endl;
    }
};

int main()
{
    SimpleController *c = new SimpleController("./database.db");
    c->remove_table();
    c->create_table();
    c->insert(100, "Alice", 4.0, 18);
    c->insert(200, "Bob", 3.9, 19);
    c->insert(300, "Charles", 3.85, 20);
    c->insert(400, "Dave", 3.8, 21);
    c->select_all();
    c->remove_by_id(200);
    c->remove_by_id(150);
    c->select_by_id(200);
    c->select_by_id(100);
    c->select_all();
    delete c;

    return 0;
}

