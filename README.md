# Tek-D
Esta aplicación sirve para la gestión tanto del almacén de productos, usuarios o trabajadores, clientes, facturas de una tienda orientada a la venta de componentes electrónicos de computadora. En esta aplicación se pueden tanto agregar productos, y con estos mismos productos luego hacer facturas las cuales te mandarán al cliente y se verá reflejado los cambios que hagamos dentro de la tabla de productos. Resuelve el problema de la gestión en una empresa que está dedicada a la venta de computadoras, pues con esta aplicación es posible llevar un mejor control, esto debido a las diversas funcionalidades que ésta posee, pues abarca prácticamente todo el tema de gestión y control dentro de una tienda de venta de componentes electrónicos de computadora.

---

## Requisitos del sistema
A continuación, se van a enumerar los requisitos que son necesarios para utilizar la presente aplicación:
- Sistema operativo, ya sea Windows macOS o Linux (es posible que se necesite en bibliotecas adicionales para el soporte de las interfaces gráficas para algunas configuraciones de Linux).
- Conexión a internet.
- Tener la carpeta que contiene el ejecutable y demás archivos para el correcto funcionamiento de la aplicación.

---

## Guía de uso
Para entrar es necesario iniciar sesión, con la cuenta iniciada puedes acceder a todas las funciones del CRUD, para que los cambios se guarden en la base de datos es necesario tener acceso a internet.
Como tal la aplicación tiene como base cuatro botones, estos son:
-	Crear: Sirve para crear nuevas partidas en la base de datos.
-	Modificar: Te deja modificar una partida existente en la base de datos.
-	Eliminar: Te deja eliminar una partida existente en la base de datos.
-	Buscar: Te deja buscar una partida existente en la base de datos.
Estos cuatro botones están presentes en:
-	Productos
-	Clientes
-	Usuarios
Como tal estos botones tienen las mismas funcionalidades, obviamente cada uno para su respectiva tabla y con sus respectivos parámetros, pero en esencia funcionan para lo mismo.
Puedes cerrar sesión, para esto debes desplegar el menú y al final te da la opción, al hacer esto te manda al inicio de sesión, en donde si quieres volver a tener acceso debes escribir nuevamente las credenciales.
Se tiene la opción de cambiar la contraseña, debido que al crear un nuevo usuario se manda un correo electronico a el email registrado, entonces para mayor seguridad se puede cambiar la contraseña tantas veces como sea necesario.

---

## Requisitos técnicos
-	Python: Esto es con el lenguaje de programación Python.
-	Flet: Esta es una biblioteca para realizar interfaces gráficas de manera sencilla y eficiente.
-	MySQL: Esta es la base de datos que se va a utilizar.
-	mysqlclient: Esto es para realizar la conexión entre la base de datos y la aplicación.
-	Amazon Web Sevices: Esta es la nube donde se alojará la base de datos para poder tener acceso desde cualquier lugar con acceso internet.
-	SQLAlchemy: Esto es una biblioteca que permite realizar diversas operaciones con MySQL como la creación de tablas.
-	PyInstaller: Esto es una biblioteca para crear un ejecutable de nuestra aplicación.
-	Bcrypt: Esta es una biblioteca que nos permite realizar diversas operaciones como la encriptación o la desencriptación de un texto.
-	ReportLab: Esto es una biblioteca que nos permite la creación de archivos PDF.
-	python-dotenv: Para el manejo de las variables de entorno.
-	Yagmail: Esta es una biblioteca que nos permite el mandar correos mediante Gmail.

---

## Problemas comunes
-	Debes tener acceso a internet para poder usar la aplicación.
-	Es importante tener activo en Amazon Web Service la base de datos.
-	Al iniciar la aplicación te dirá que tengas cuidado por las credenciales, pero puedes omitir este aviso.
-	Al momento de cerrar la aplicación puede aparecer un mensaje de error, esto puede deberse a la constante actualización de la base de datos, no te preocupes, solo cierra dicha ventana.
