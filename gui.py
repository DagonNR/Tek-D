#Interfaz gráfica

#CAMBIOS NO TAN URGENTES, QUITAR LA CONTRASEÑA DE APLICACIÓN

import flet as ft
import random, string, bcrypt
from database import product_crud, employee_crud, category_crud, area_crud, client_crud, invoice_crud
from tables import Product, Category, Area, Employee, Client, Invoice
from invoice import invoice_class

def Ui_LoginWindow(page: ft.Page):
    page.controls.clear()
    page.update()
    email_login = ft.TextField(label="Email")
    password_login = ft.TextField(label="Password", password=True, can_reveal_password=True)
    t = ft.Text()
    
    def check_login(e):
        t.value = None
        email = email_login.value
        password = password_login.value
        user = employee_crud.search_email(email)

        if user is None:
            t.value = "Usuario no válido"
            page.update()
            return
        
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            Ui_MenuWindow(page)
        else:
            t.value = "Contraseña incorrecta"
            page.update()
    
    def check_password(e):
        Ui_PasswordWindow(page)
        page.update()

    container_login = ft.Container(
        content=ft.Column(
            [
                ft.Text("Inicia sesión", size=20, color="LIGHT_BLUE_50"),
                email_login,
                password_login,
                ft.ElevatedButton(text="Iniciar sesión", on_click=lambda e:check_login(e)),
                ft.ElevatedButton(text="Ir a cambiar contraseña", on_click=lambda e:check_password(e)),
                t,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True
        ),
        width=350,
        height=400,
        border_radius=ft.border_radius.all(20),
        bgcolor=ft.colors.WHITE,
        padding=20,
        alignment=ft.alignment.center
    )

    page.add(
        ft.Row(
            controls=[container_login],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

    page.bgcolor = ft.colors.LIGHT_BLUE_50
    page.update()

def Ui_PasswordWindow(page: ft.Page):
    page.controls.clear()
    page.update()
    email_password = ft.TextField(label="Email")
    current_password_textfield = ft.TextField(label="Contraseña actual", password=True, can_reveal_password=True)
    new_password_textfield = ft.TextField(label="Nueva contraseña", password=True, can_reveal_password=True)
    g = ft.Text()

    def check_login(e):
        Ui_LoginWindow(page)
        page.update()

    def lost_password(e):
        g.value = None
        email = email_password.value
        new_password = new_password_textfield.value
        current_password = current_password_textfield.value
        user = employee_crud.search_email(email)

        if user is None:
            print("Usuario no encontrado")
            g.value = "Usuario no encontrado"
            page.update()
            return
        
        if not bcrypt.checkpw(current_password.encode('utf-8'), user.password.encode("utf-8")):
            print("La contraseña actual es incorrecta")
            g.value = "La contraseña actual es incorrecta"
            page.update()
            return
        
        if not verify_password(new_password):
            print("La nueva contraseña no es válida")
            g.value = "La nueva contraseña no es válida\nDebe tener al menos 8 caracteres, un dígito y una mayúscula"
            page.update()
            return
        
        new_password_hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
        user.password = new_password_hashed
        employee_crud.update(user)
        print("Contraseña cambiada exitosamente")
        g.value = "Contraseña cambiada exitosamente"
        page.update()

    def verify_password(password):
        if len(password) < 8:
            print("La contraseña debe tener al menos 8 caracteres.")
            return False
        if not any(c.isdigit() for c in password):
            print("La contraseña debe contener al menos un dígito.")
            return False
        if not any(c.isupper() for c in password):
            print("La contraseña debe contener al menos una letra mayúscula.")
            return False
        return True

    container_password = ft.Container(
        content=ft.Column(
            [
                ft.Text("Cambiar contraseña", size=20, color="LIGHT_BLUE_50"),
                email_password,
                current_password_textfield,
                new_password_textfield,
                ft.ElevatedButton(text="Cambiar contraseña", on_click=lambda e:lost_password(e)),
                ft.ElevatedButton(text="Ir a iniciar sesión", on_click=lambda e:check_login(e)),
                g,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True
        ),
        width=350,
        height=400,
        border_radius=ft.border_radius.all(20),
        bgcolor=ft.colors.WHITE,
        padding=20,
        alignment=ft.alignment.center
    )

    page.add(
        ft.Row(
            controls=[container_password],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

    page.bgcolor = ft.colors.LIGHT_BLUE_50
    page.update()

def Ui_MenuWindow(page: ft.Page):
    image = ft.Image(src="images/Tek-D.png", width=800, height=800)
    page.controls.clear()
    page.update()
    content_container = ft.Column()
    content_container.controls.append(ft.Container(
        content=image,
        alignment=ft.alignment.center,
    ))

    def logout(e):
        page.controls.clear()
        Ui_LoginWindow(page)
        page.update()
    
    def handle_change(e):
        if isinstance(e, int):
            index = e
        else:
            index = e.control.selected_index

        content_container.controls.clear()
        if index == 0:
            content_container.controls.append(ft.Container(
                content=image,
                alignment=ft.alignment.center,
            ))
        elif index == 1:
            products = product_crud.read_all()
            content_container.controls.append(ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Productos", size=80, color=ft.colors.BLACK),
                        ft.Row(
                            [
                                table("products", products),
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            crud_buttons("products"),
                                            ft.Divider(thickness=3),
                                            text_fields("products"),
                                        ]
                                    ), expand=True, alignment=ft.alignment.top_center,
                                )
                            ], expand=True, spacing=50,
                        ),
                    ], expand=True,
                )
            ))
        elif index == 2:
            users = employee_crud.read_all()
            content_container.controls.append(ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Usuarios", size=80, color=ft.colors.BLACK),
                        ft.Row(
                            [
                                table("users", users),
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            crud_buttons("users"),
                                            ft.Divider(thickness=3),
                                            text_fields("users"),
                                        ]
                                    ), expand=True, alignment=ft.alignment.top_center,
                                )
                            ], expand=True, spacing=50,
                        ),
                    ], expand=True,
                )
            ))
        elif index == 3:
            clients = client_crud.read_all()
            content_container.controls.append(ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Clientes", size=80, color=ft.colors.BLACK),
                        ft.Row(
                            [
                                table("clients", clients),
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            crud_buttons("clients"),
                                            ft.Divider(thickness=3),
                                            text_fields("clients"),
                                        ]
                                    ), expand=True, alignment=ft.alignment.top_center,
                                )
                            ], expand=True, spacing=50,
                        ),
                    ], expand=True,
                )
            ))
        elif index == 4:
            clients = client_crud.read_all()
            content_container.controls.append(ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Facturas", size=80, color=ft.colors.BLACK),
                        ft.Row(
                            [
                                table("clients", clients),
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            invoice_class.invoice_buttons(),
                                        ]
                                    ), expand=True, alignment=ft.alignment.top_center,
                                )
                            ], expand=True, spacing=50,
                        ),
                    ], expand=True,
                )
            ))
        elif index == 5:
            invoice = invoice_crud.read_all()
            content_container.controls.append(ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Tabla Facturas", size=80, color=ft.colors.BLACK),
                        ft.Row(
                            [
                                table("invoice", invoice),
                            ], expand=True, spacing=50,
                        ),
                    ], expand=True,
                )
            ))
        elif index == 6:
            areas = area_crud.read_all()
            content_container.controls.append(ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Áreas", size=80, color=ft.colors.BLACK),
                        ft.Row(
                            [
                                table("area", areas),
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            crud_buttons("area"),
                                            ft.Divider(thickness=3),
                                            text_fields("area"),
                                        ]
                                    ),alignment=ft.alignment.top_center,
                                )
                            ], expand=True,
                        ),
                    ], expand=True,
                )
            ))
        elif index == 7:
            categories = category_crud.read_all()
            content_container.controls.append(ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Categorías", size=80, color=ft.colors.BLACK),
                        ft.Row(
                            [
                                table("category", categories),
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            crud_buttons("category"),
                                            ft.Divider(thickness=3),
                                            text_fields("category"),
                                        ]
                                    ),alignment=ft.alignment.top_center,
                                )
                            ], expand=True, spacing=50,
                        ),
                    ], expand=True,
                )
            ))
        elif index == 8:
            logout(e)

        page.close(drawer)
        page.update()
        reset_dropdown(category, area)

    def handle_dimissal(e):
        page.update()
    
    drawer = ft.NavigationDrawer(
        on_dismiss=handle_dimissal,
        on_change=handle_change,
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Pagina Principal",
                icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.SELL_OUTLINED),
                label="Productos",
                selected_icon=ft.icons.SELL,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.SUPERVISED_USER_CIRCLE_OUTLINED),
                label="Usuarios",
                selected_icon=ft.icons.SUPERVISED_USER_CIRCLE,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PEOPLE_ALT_OUTLINED),
                label="Clientes",
                selected_icon=ft.icons.PEOPLE_ALT,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.INVENTORY),
                label="Facturas",
                selected_icon=ft.icons.INVENTORY_OUTLINED,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.INVENTORY_2),
                label="Tabla Facturas",
                selected_icon=ft.icons.INVENTORY_2_OUTLINED,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.AREA_CHART_OUTLINED),
                label="Áreas",
                selected_icon=ft.icons.AREA_CHART,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.CATEGORY_OUTLINED),
                label="Categorías",
                selected_icon=ft.icons.CATEGORY,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.LOGOUT_OUTLINED),
                label="Cerrar sesión",
                selected_icon=ft.icons.LOGOUT,
            ),
        ],
    )

    def crud_operation(entity, op, form_data=None):
        if entity == "products":
            if op == "create":
                return create_product(form_data)
            elif op == "read":
                return read_product(form_data)
            elif op == "delete":
                return delete_product(form_data)
            elif op == "update":
                return update_product(form_data)
            
        if entity == "users":
            if op == "create":
                return create_user(form_data)
            elif op == "read":
                return read_user(form_data)
            elif op == "delete":
                return delete_user(form_data)
            elif op == "update":
                return update_user(form_data)
            
        if entity == "clients":
            if op == "create":
                return create_client(form_data)
            elif op == "read":
                return read_client(form_data)
            elif op == "delete":
                return delete_client(form_data)
            elif op == "update":
                return update_client(form_data)
            
        elif entity == "area":
            if op == "create":
                return create_area(form_data)
            if op == "read":
                return read_area(form_data)
            if op == "delete":
                return delete_area(form_data)
            if op == "update":
                return update_area(form_data)
            
        elif entity == "category":
            if op == "create":
                return create_category(form_data)
            if op == "read":
                return read_category(form_data)
            if op == "delete":
                return delete_category(form_data)
            if op == "update":
                return update_category(form_data)
    
    def table(entity, items):
        if entity == "products":
            columns = [
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Categoría")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Modelo")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("Cantidad")),
            ]
            rows = [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(item.id))),
                    ft.DataCell(ft.Text(item.category_id)),
                    ft.DataCell(ft.Text(item.name)),
                    ft.DataCell(ft.Text(item.model)),
                    ft.DataCell(ft.Text(str(item.price))),
                    ft.DataCell(ft.Text(str(item.quantity))),
                ]) for item in items
            ]
        elif entity == "users":
            columns = [
                ft.DataColumn(ft.Text("ID", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("Nombre", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("Email", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("Calle", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("# de calle", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("Colonia", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("CP", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("Ciudad", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("Estado", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("País", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("ID área", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("Salario", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("Fecha", style=ft.TextStyle(size=10))),
            ]
            rows = [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(item.id), style=ft.TextStyle(size=8))),
                    ft.DataCell(ft.Text(item.name, style=ft.TextStyle(size=8))),
                    ft.DataCell(ft.Text(item.email, style=ft.TextStyle(size=8))),
                    ft.DataCell(ft.Text(item.street, style=ft.TextStyle(size=8))),
                    ft.DataCell(ft.Text(str(item.street_number), style=ft.TextStyle(size=8))),
                    ft.DataCell(ft.Text(item.neighborhood, style=ft.TextStyle(size=8))),
                    ft.DataCell(ft.Text(str(item.cp), style=ft.TextStyle(size=8))),
                    ft.DataCell(ft.Text(item.city, style=ft.TextStyle(size=8))),
                    ft.DataCell(ft.Text(item.state, style=ft.TextStyle(size=8))),
                    ft.DataCell(ft.Text(item.country, style=ft.TextStyle(size=8))),
                    ft.DataCell(ft.Text(str(item.area_id), style=ft.TextStyle(size=8))),
                    ft.DataCell(ft.Text(str(item.salary), style=ft.TextStyle(size=8))),
                    ft.DataCell(ft.Text(str(item.hiring_date), style=ft.TextStyle(size=8))),
                ]) for item in items
            ]
        elif entity == "clients":
            columns = [
                ft.DataColumn(ft.Text("ID", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("Nombre", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("RFC", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("Email", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("Calle", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("# de calle", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("Colonia", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("CP", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("Ciudad", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("Estado", style=ft.TextStyle(size=10))),
                ft.DataColumn(ft.Text("País", style=ft.TextStyle(size=10))),
            ]
            rows = [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(item.id), style=ft.TextStyle(size=10))),
                    ft.DataCell(ft.Text(item.name, style=ft.TextStyle(size=10))),
                    ft.DataCell(ft.Text(item.rfc, style=ft.TextStyle(size=10))),
                    ft.DataCell(ft.Text(item.email, style=ft.TextStyle(size=10))),
                    ft.DataCell(ft.Text(item.street, style=ft.TextStyle(size=10))),
                    ft.DataCell(ft.Text(str(item.street_number), style=ft.TextStyle(size=10))),
                    ft.DataCell(ft.Text(item.neighborhood, style=ft.TextStyle(size=10))),
                    ft.DataCell(ft.Text(str(item.cp), style=ft.TextStyle(size=10))),
                    ft.DataCell(ft.Text(item.city, style=ft.TextStyle(size=10))),
                    ft.DataCell(ft.Text(item.state, style=ft.TextStyle(size=10))),
                    ft.DataCell(ft.Text(item.country, style=ft.TextStyle(size=10))),
                ]) for item in items
            ]
        elif entity == "invoice":
            columns = [
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Total")),
                ft.DataColumn(ft.Text("ID cliente")),
            ]
            rows = [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(item.id))),
                    ft.DataCell(ft.Text(item.name)),
                    ft.DataCell(ft.Text(item.description)),
                    ft.DataCell(ft.Text(item.product)),
                    ft.DataCell(ft.Text(str(item.total))),
                    ft.DataCell(ft.Text(str(item.id_client))),
                ]) for item in items
            ]
        elif entity == "area":
            columns = [
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Acceso al CRUD"))
            ]
            rows = [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(item.id))),
                    ft.DataCell(ft.Text(item.name)),
                    ft.DataCell(ft.Text("Si" if item.crud_access else "No"))
                ]) for item in items
            ]
        elif entity == "category":
            columns = [
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
            ]
            rows = [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(item.id))),
                    ft.DataCell(ft.Text(item.name)),
                ]) for item in items
            ]

        return ft.DataTable(columns=columns,
                            rows=rows,
                            width=1300,
                            border=ft.border.all(1),
                            border_radius=10,
                            data_row_max_height=100)
    
    def crud_buttons(entity):
        global id_label
        id_label = ft.TextField(label="ID", width=80)
        return ft.Row(
            [
                ft.ElevatedButton(text="Crear", on_click=lambda e: crud_operation(entity, "create")),
                ft.ElevatedButton(text="Modificar", on_click=lambda e: crud_operation(entity, "update")),
                ft.ElevatedButton(text="Eliminar", on_click=lambda e: crud_operation(entity, "delete")),
                ft.ElevatedButton(text="Buscar", on_click=lambda e: crud_operation(entity, "read")),
                id_label,
            ],alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )
    
    category = ft.Dropdown(
        options=[ft.dropdown.Option(text=categories) for categories in category_crud.get()],
        label="Seleccione una categoría"
    )

    area = ft.Dropdown(
        options=[ft.dropdown.Option(text=area) for area in area_crud.get()],
        label="Seleccione una categoría"
    )

    switch = ft.Switch(
        label="Acceso al CRUD",
        value=True
    )

    def text_fields(entity):
        global form_data
        form_data = {}
        form_fields = []

        if entity == "products":
            fields = [
                {"label": "Nombre", "name": "name"},
                {"label": "Modelo", "name": "model"},
                {"label": "Precio", "name": "price"},
                {"label": "Cantidad", "name": "quantity"},
            ]
            form_fields.append(category)
        elif entity == "users":
            fields = [
                {"label": "Nombre", "name": "name"},
                {"label": "Email", "name": "email"},
                {"label": "Calle", "name": "street"},
                {"label": "Número de calle", "name": "street_number"},
                {"label": "Colonia", "name": "neighborhood"},
                {"label": "Código Postal", "name": "cp"},
                {"label": "Ciudad", "name": "city"},
                {"label": "Estado", "name": "state"},
                {"label": "País", "name": "country"},
                {"label": "Salario", "name": "salary"},
            ]
            form_fields.append(area)
        elif entity == "clients":
            fields = [
                {"label": "Nombre", "name": "name"},
                {"label": "RFC", "name": "rfc"},
                {"label": "Email", "name": "email"},
                {"label": "Calle", "name": "street"},
                {"label": "Número de calle", "name": "street_number"},
                {"label": "Colonia", "name": "neighborhood"},
                {"label": "Código Postal", "name": "cp"},
                {"label": "Ciudad", "name": "city"},
                {"label": "Estado", "name": "state"},
                {"label": "País", "name": "country"},
            ]
        elif entity == "area":
            fields = [
                {"label": "Nombre", "name": "name"},
            ]
            form_fields.append(switch)
        elif entity == "category":
            fields = [
                {"label": "Nombre", "name": "name"},
            ]
        
        for field in fields:
            text_fields = ft.TextField(label=field["label"])
            form_data[field["name"]] = text_fields
            form_fields.append(text_fields)
        
        return ft.Column(form_fields)
    
    def reset_dropdown(*dropdowns):
        for dropdown in dropdowns:
            dropdown.value = None
            dropdown.update()
        page.update()

    #Product GUI and operations
    def create_product(e):
        category_name = category_crud.search(category.value)

        new_product = Product(
            category_id = category_name.id,
            name = form_data["name"].value,
            model = form_data["model"].value,
            price = float(form_data["price"].value),
            quantity = int(form_data["quantity"].value),
        )

        print(f"{new_product}")
        product_crud.create(new_product)

        for field in form_data.values():
            field.value = ""
        
        handle_change(1)

    def read_product(e):
        id = id_label.value
        print(f"{id}")
        
        if id.isdigit():
            product = product_crud.read(id)

            if product:
                category.value = category_crud.search_id(product.category_id).name
                form_data["name"].value = product.name
                form_data["model"].value = product.model
                form_data["price"].value = str(product.price)
                form_data["quantity"].value = str(product.quantity)

                #print(f"El category.value es: {category.value}")

                page.update()
            else:
                print(f"Error, no se encontro el producto de ID {id}")
        else:
            print(f"ID no válido {id}")
    
    def delete_product(e):
        if (form_data["name"].value == "" and
            form_data["model"].value == "" and
            form_data["price"].value == "" and
            form_data["quantity"].value == ""):
            print("No tiene datos")
        else:
            product_crud.delete(product_crud.read(id_label.value))
            handle_change(1)
    
    def update_product(e):
        if (form_data["name"].value == "" and
            form_data["model"].value == "" and
            form_data["price"].value == "" and
            form_data["quantity"].value == ""):
            print("No tiene datos")
        else:
            product_up = product_crud.read(id_label.value)

            if product_up:
                product_up.name = form_data["name"].value
                product_up.model = form_data["model"].value
                product_up.price  = form_data["price"].value
                product_up.quantity = form_data["quantity"].value

                product_crud.update(product_up)
                print(f"Producto de id {product_up} actualizado")
                handle_change(1)
            else:
                print(f"ID no válido {product_up}")

    #User GUI and operations
    def password_random():
        character = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(character) for _ in range(12))

    def create_user(e):
        password = password_random()
        password_hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        area_name = area_crud.search(area.value)
        area_name_crud_access = area_name.crud_access
        
        new_user = Employee(
            name = form_data["name"].value,
            email = form_data["email"].value,
            password = password_hashed,
            street = form_data["street"].value,
            street_number = form_data["street_number"].value,
            neighborhood = form_data["neighborhood"].value,
            cp = form_data["cp"].value,
            city = form_data["city"].value,
            state = form_data["state"].value,
            country = form_data["country"].value,
            area_id = area_name.id,
            salary = float(form_data["salary"].value),
        )

        print(f"{new_user}")
        if area_name_crud_access == True:
            invoice_class.email_send(form_data["email"].value, password)
        employee_crud.create(new_user)

        for field in form_data.values():
            field.value = ""
        
        handle_change(2)

    def read_user(e):
        id = id_label.value
        print(f"{id}")
        
        if id.isdigit():
            user = employee_crud.read(id)

            if user:
                form_data["name"].value = user.name
                form_data["email"].value = user.email
                form_data["street"].value = user.street
                form_data["street_number"].value = user.street_number
                form_data["neighborhood"].value = user.neighborhood
                form_data["cp"].value = user.cp
                form_data["city"].value = user.city
                form_data["state"].value = user.state
                form_data["country"].value = user.country
                area.value = area_crud.search_id(user.area_id).name
                form_data["salary"].value = float(user.salary)

                #print(f"El category.value es: {category.value}")

                page.update()
            else:
                print(f"Error, no se encontro el producto de ID {id}")
        else:
            print(f"ID no válido {id}")

    def delete_user(e):
        if (form_data["name"].value == "" and
            form_data["email"].value == "" and
            form_data["street"].value == "" and
            form_data["street_number"].value == "" and
            form_data["neighborhood"].value == "" and
            form_data["cp"].value == "" and
            form_data["city"].value == "" and
            form_data["state"].value == "" and
            form_data["country"].value == "" and
            form_data["salary"].value == ""):
            print("No tiene datos")
        else:
            employee_crud.delete(employee_crud.read(id_label.value))
            handle_change(2)
    
    def update_user(e):
        if (form_data["name"].value == "" and
            form_data["email"].value == "" and
            form_data["street"].value == "" and
            form_data["street_number"].value == "" and
            form_data["neighborhood"].value == "" and
            form_data["cp"].value == "" and
            form_data["city"].value == "" and
            form_data["state"].value == "" and
            form_data["country"].value == "" and
            form_data["salary"].value == ""):
            print("No tiene datos")
        else:
            employee_up = employee_crud.read(id_label.value)

            if employee_up:
                employee_up.name = form_data["name"].value
                employee_up.email = form_data["email"].value
                employee_up.street = form_data["street"].value
                employee_up.street_number = form_data["street_number"].value
                employee_up.neighborhood = form_data["neighborhood"].value
                employee_up.cp = form_data["cp"].value
                employee_up.city = form_data["city"].value
                employee_up.state = form_data["state"].value
                employee_up.country = form_data["country"].value
                employee_up.salary = form_data["salary"].value

                employee_crud.update(employee_up)
                print(f"Usuario de id {employee_up} actualizado")
                handle_change(2)
            else:
                print(f"ID no válido {employee_up}")

    #Client GUI and operations
    def create_client(e):
        new_client = Client(
            name = form_data["name"].value,
            rfc = form_data["rfc"].value,
            email = form_data["email"].value,
            street = form_data["street"].value,
            street_number = form_data["street_number"].value,
            neighborhood = form_data["neighborhood"].value,
            cp = form_data["cp"].value,
            city = form_data["city"].value,
            state = form_data["state"].value,
            country = form_data["country"].value,
        )

        print(f"{new_client}")
        client_crud.create(new_client)

        for field in form_data.values():
            field.value = ""
        
        handle_change(3)
    
    def read_client(e):
        id = id_label.value
        print(f"{id}")
        
        if id.isdigit():
            client = client_crud.read(id)

            if client:
                form_data["name"].value = client.name
                form_data["rfc"].value = client.rfc
                form_data["email"].value = client.email
                form_data["street"].value = client.street
                form_data["street_number"].value = client.street_number
                form_data["neighborhood"].value = client.neighborhood
                form_data["cp"].value = client.cp
                form_data["city"].value = client.city
                form_data["state"].value = client.state
                form_data["country"].value = client.country
                page.update()
            else:
                print(f"Error, no se encontro el producto de ID {id}")
        else:
            print(f"ID no válido {id}")

    def delete_client(e):
        if (form_data["name"].value == "" and
            form_data["rfc"].value == "" and
            form_data["email"].value == "" and
            form_data["street"].value == "" and
            form_data["street_number"].value == "" and
            form_data["neighborhood"].value == "" and
            form_data["cp"].value == "" and
            form_data["city"].value == "" and
            form_data["state"].value == "" and
            form_data["country"].value == ""):
            print("No tiene datos")
        else:
            client_crud.delete(client_crud.read(id_label.value))
            handle_change(3)

    def update_client(e):
        if (form_data["name"].value == "" and
            form_data["rfc"].value == "" and
            form_data["email"].value == "" and
            form_data["street"].value == "" and
            form_data["street_number"].value == "" and
            form_data["neighborhood"].value == "" and
            form_data["cp"].value == "" and
            form_data["city"].value == "" and
            form_data["state"].value == "" and
            form_data["country"].value == ""):
            print("No tiene datos")
        else:
            client_up = client_crud.read(id_label.value)

            if client_up:
                client_up.name = form_data["name"].value
                client_up.rfc = form_data["rfc"].value
                client_up.email  = form_data["email"].value
                client_up.street = form_data["street"].value
                client_up.street_number = form_data["street_number"].value
                client_up.neighborhood = form_data["neighborhood"].value
                client_up.cp = form_data["cp"].value
                client_up.city = form_data["city"].value
                client_up.state = form_data["state"].value
                client_up.country = form_data["country"].value

                client_crud.update(client_up)
                print(f"Producto de id {client_up} actualizado")
                handle_change(3)
            else:
                print(f"ID no válido {client_up}")

    #Area GUI and operations
    def reload_area():
        areas = area_crud.read_all()
        area.options = [ft.dropdown.Option(text=a.name) for a in areas]

    def create_area(e):
        new_area = Area(
            name = form_data["name"].value,
            crud_access = switch.value,
        )

        print(f"{new_area}")
        area_crud.create(new_area)

        for field in form_data.values():
            field.value = ""
        
        reload_area()
        handle_change(6)
    
    def read_area(e):
        id = id_label.value
        print(f"{id}")

        if id.isdigit():
            area = area_crud.read(id)

            if area:
                form_data["name"].value = area.name
                switch.value = area_crud.search_id(area.id).crud_access

                page.update()
            else:
                print(f"Error, no se encontró el área con ID {id}")
        else:
            print(f"ID no válido {id}")
    
    def delete_area(e):
        if (form_data["name"].value == ""):
            print("No tiene datos")
        else:
            area_crud.delete(area_crud.read(id_label.value))
            reload_area()
            handle_change(6)
    
    def update_area(e):
        if (form_data["name"].value == ""):
            print("No tiene datos")
        else:
            area_up = area_crud.read(id_label.value)

            if area_up:
                area_up.name = form_data["name"].value
                area_up.crud_access = switch.value

                area_crud.update(area_up)
                print(f"Area de id {area_up} actualizado")
                reload_area()
                handle_change(6)
            else:
                print(f"ID no válido {area_up}")

    #Category GUI and operations
    def reload_category():
        categories = category_crud.read_all()
        category.options = [ft.dropdown.Option(text=cat.name) for cat in categories]

    def create_category(e):
        new_category = Category(
            name = form_data["name"].value,
        )

        print(f"{new_category}")
        category_crud.create(new_category)

        for field in form_data.values():
            field.value = ""
        
        reload_category()
        handle_change(7)

    def read_category(e):
        id = id_label.value
        print(f"{id}")

        if id.isdigit():
            category = category_crud.read(id)

            if category:
                form_data["name"].value = category.name

                page.update()
            else:
                print(f"Error, no se encontró la categoría con ID {id}")
        else:
            print(f"ID no válido {id}")
    
    def delete_category(e):
        if (form_data["name"].value == ""):
            print("No tiene datos")
        else:
            category_crud.delete(category_crud.read(id_label.value))
            reload_category()
            handle_change(7)

    def update_category(e):
        if (form_data["name"].value == ""):
            print("No tiene datos")
        else:
            category_up = category_crud.read(id_label.value)

            if category_up:
                category_up.name = form_data["name"].value

                category_crud.update(category_up)
                print(f"Categoría de id {category_up} actualizado")
                reload_category()
                handle_change(7)
            else:
                print(f"ID no válido {category_up}")

    page.add(
        ft.Row(
            [
                ft.IconButton(icon=ft.icons.MENU, on_click=lambda e: page.open(drawer))
            ],
            tight=True
        ),
    )

    page.add(
        ft.Column(
            [
                content_container,
            ],
            alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

    page.update()

ft.app(Ui_LoginWindow)