#Funciones para agregar, eliminar, consultar, y modificar valores en la base de datos

from tables import session, Client, Employee, Area, Product, Category, Invoice

class CRUD:

    def __init__(self, session, model):
        self.session = session
        self.model = model
    
    def create(self, object):
        self.session.add(object)
        self.session.commit()
    
    def read(self, id_read):
        return self.session.query(self.model).get(id_read)

    def read_all(self):
        return self.session.query(self.model).order_by(self.model.id).all()

    def update(self, object):
        self.session.merge(object)
        self.session.commit()
    
    def delete(self, object):
        self.session.delete(object)
        self.session.commit()

    def get(self):
        get = self.session.query(self.model).all()
        return[self.name for self in get]

    def search(self, name):
        return self.session.query(self.model).filter_by(name=name).first()
    
    def search_id(self, id):
        return self.session.query(self.model).filter_by(id=id).first()
    
    def search_email(self, email):
        return self.session.query(self.model).filter_by(email=email).first()
    
    def check_table(self):
        return session.query(self.model).count()

client_crud = CRUD(session, Client)
employee_crud = CRUD(session, Employee)
area_crud = CRUD(session, Area)
product_crud = CRUD(session, Product)
category_crud = CRUD(session, Category)
invoice_crud = CRUD(session, Invoice)
"""

class ClientCRUD(CRUD):

    def __init__(self, session):
        super().__init__(session)

class EmployeCRUD(CRUD):
    
    def __init__(self, session):
        super().__init__(session)

class ProductCRUD(CRUD):

    def __init__(self, session):
        super().__init__(session)

employee_crud = EmployeCRUD(session)
product_crud = ProductCRUD(session)
client_crud = ClientCRUD(session)

def get_products():
    session = session
    products = session.query(Product).all()
    session.close()
    return products

products = get_products()



if __name__ == "__main__":
    PRUEBAS DE FUNCIONAMIENTO
    new_employe = Employee(name = "Daniel", email = "daniel@hotmail.com", domicile = "Av Siempre Viva", area = "Servicio técnico", salary = 10000)
    employee_crud.create(new_employe)
    new_employe2 = Employee(name = "Pedro", email = "pedro@hotmail.com", domicile = "Av Siempre Muerta", area = "Caja", salary = 5000)
    employee_crud.create(new_employe2)

    read_employee = employee_crud.read(Employee, 1)
    if bool(read_employee) == True:
            print(read_employee.id)
            print(read_employee.name)
            print(read_employee.email)
            print(read_employee.domicile)
            print(read_employee.area)
            print(read_employee.salary)
            print(read_employee.hiring_date)
    else:
        print("Usuario no encontrado")

    delete_employee = employee_crud.read(Employee, 2)
    employee_crud.delete(delete_employee)

    new_employe3 = Employee(name = "Gaston", email = "gaston@hotmail.com", domicile = "Av Siempre Estable", area = "Ventas", salary = 8000)
    employee_crud.create(new_employe3)
    
    new_employe = Employee(name = "Daniel", email = "daniel@hotmail.com", domicile = "Av Siempre Viva", area = "Servicio técnico", salary = 10000)
    employee_crud.create(new_employe)
    password1 = "tomate"
    hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
    bcrypt.checkpw(password1.encode('utf-8'), hashed_password)
    new_user = User(email = "daniel@hotmail.com", password = hashed_password, employee_id = 1)
    user_crud = UserCRUD(session)
    user_crud.create(new_user)
    
    def login(email, password):
        user = session.query(User).filter_by(email = email).first()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            print("Inicio de sesión exitoso")
            return user
        else:
            print("Email o contraseña incorrectos")
            return None
    
    login("daniel@hotmail.com", password1)"""
    