import controller

def main():
    ctrl = controller.DBController()
    ctrl.open(server="localhost,10913", database="mydatabase", uid="user", pwd="password")

if __name__ == "__main__":
    main()
