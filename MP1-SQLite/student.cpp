#include "sqlite3.h"

#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>

using namespace std;

int callback(void *NotUsed, int argc, char **argv, char **azColName) {}
char *errMsg;

class SimpleController
{
private:
    sqlite3 *db;

public:
    SimpleController(string path)
    {
        int rc = sqlite3_open(path.c_str(), &db);
        if (rc) {
            cout << "[ERROR] Error encontered when opening " << path << endl;
            sqlite3_close(db);
            exit(rc);
        }
        cout << "[INFO] Database " << path << " is opened." << endl;
    }
    ~SimpleController()
    {
        sqlite3_close(db);
    }
    void create_table()
    {
        string sql = "CREATE TABLE IF NOT EXISTS students (ID INT, Name TEXT, GPA REAL, Age INT)";
        int rc = sqlite3_exec(db, sql.c_str(), callback, 0, &errMsg);
        if (rc) {
            cout << "[ERROR] Error encontered when creating table" << endl;
            sqlite3_close(db);
            exit(rc);
        }
    }
    void insert(int id, string name, double GPA, int age) {}
    void remove_by_id(int id) {}
    void select_by_id(int id, string &name, double &GPA, int &age) {}
    void print_tables() {}
    void print_columns() {}
};

void display()
{
    SimpleController *c = new SimpleController("./database.db");
    c->create_table();
    delete c;
}

int main()
{
    display();

    return 0;
}