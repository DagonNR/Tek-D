#Archivo principal que contiene la ejecución de la aplicación en su totalidad

from tables import Base, engine
from gui import Ui_LoginWindow
from user_master import count_area, count_employee, create_initial_area, create_first_user

Base.metadata.create_all(engine)

def create_admin():
    if count_area() == 0:
        create_initial_area()
    if count_employee() == 0:
        create_first_user()

create_admin()

try:
    login_window = Ui_LoginWindow()
except TypeError as e:
    print(f"Ocurrió un error: {e}.")