#Main user to login first time

import bcrypt
from tables import Employee, Area, session
from database import employee_crud, area_crud

def create_initial_area():
    first_area = Area(
        name = "Administración",
        crud_access = True,
    )
    area_crud.create(first_area)
    session.commit()

def create_first_user():
    password = "admin123"
    password_hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    
    first_user = Employee(
        name = "Admin",
        email = "admin@admin.com",
        password = password_hashed,
        street = "1",
        street_number = "1",
        neighborhood = "1",
        cp = "1",
        city = "1",
        state = "1",
        country = "1",
        area_id = 1,
        salary = 1,
    )

    employee_crud.create(first_user)
    session.commit()

def count_area():
    return area_crud.check_table()

def count_employee():
    return employee_crud.check_table()

#if count_area == 0:
#    create_initial_area()
#if count_employee == 0:
#    create_first_user()