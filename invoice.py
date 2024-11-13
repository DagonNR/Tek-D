#Inovice and email functions

import flet as ft
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from num2words import num2words
import yagmail, uuid, os
from dotenv import load_dotenv
from datetime import datetime
from database import client_crud, product_crud, invoice_crud
from tables import Invoice

class InvoiceApp:

    def __init__(self):
        pass

    def invoice_buttons(self):
        tax_regime_values = [
            "General de Ley Personas Morales",
            "Personas Morales con Fines no Lucrativos",
            "Residentes en el Extranjero sin Establecimiento Permanente en México",
            "Sociedades Cooperativas de Producción que optan por diferir sus ingresos",
            "Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras",
            "Opcional para Grupos de Sociedades",
            "Coordinados",
            "Régimen Simplificado de Confianza",
        ]
        cfdi_values = [
            "Adquisición de mercancías",
            "Devoluciones, descuentos o bonificaciones",
            "Gastos en general",
            "Construcciones",
            "Mobiliario y equipo de oficina por inversiones",
            "Equipo de transporte",
            "Equipo de computo y accesorios",
            "Dados, troqueles, moldes, matrices y herramental",
            "Comunicaciones telefónicas",
            "Comunicaciones satelitales",
            "Otra maquinaria y equipo",
            "Sin efectos fiscales",
        ]
        payment_values = [
            "Efectivo",
            "Cheque",
            "Depósito",
            "Transferencia electrónica de fondos",
        ]
        iva_values = [
            0,
            4,
            8,
            11,
            12,
            16,
            99,
        ]
        clients = client_crud.read_all()
        client_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(client.id, client.name) for client in clients],
            label="Cliente"
        )
        tax_regime_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(tax_regime) for tax_regime in tax_regime_values],
            label="Régimen fiscal"
        )
        cfdi_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(cfdi) for cfdi in cfdi_values],
            label="CFDI"
        )
        payment_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(payment) for payment in payment_values],
            label="Tipo de pago"
        )
        iva_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(iva) for iva in iva_values],
            label="I.V.A"
        )
        description_textfield = ft.TextField(label="Descripción")
        price_textfield = ft.TextField(label="Precio")
        quantity_textfield = ft.TextField(label="Cantidad")
        t = ft.Text()

        def product_selected(e):
            product = product_dropdown.value
            product_name = product_crud.search(product)

            if product_name is None:
                t.value = f"El producto {product} no se encuentra en la base de datos."
                t.update()
            else:
                price_textfield.value = float(product_name.price)
                print(f"El tipo es: {type(price_textfield.value)} y el valor es: {price_textfield.value}")
                price_textfield.update()

        product_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(pro) for pro in product_crud.get()],
            label="Producto",
            on_change=product_selected,
        )
        
        def invoice_action(e):
            t.value = None
            #price_textfield.value = None
            #print(f"El tipo es: {type(price_textfield.value)} y el valor es: {price_textfield.value}")
            client_value = client_dropdown.value
            tax_regime = tax_regime_dropdown.value
            cfdi = cfdi_dropdown.value
            payment = payment_dropdown.value
            iva = int(iva_dropdown.value)
            #product = [
            #    {"description": description_textfield.value, "price": float(price_textfield.value), "quantity": int(quantity_textfield.value)}
            #]
            description = description_textfield.value
            product = product_dropdown.value
            product_name = product_crud.search(product)
            if product_name is None:
                t.value = f"El producto {product} no se encuentra en la base de datos."
                t.update()
                return
            
            price = float(price_textfield.value)
            print(f"El tipo es: {type(price)} y el valor es: {price}")
            quantity = int(quantity_textfield.value)
            product_quantity = int(product_name.quantity) - int(quantity)
            print(f"el product quantiti es : {product_quantity} y quantiti es {quantity}")
            if product_quantity < 0:
                t.value = f"No se tiene en existencia esas cantidades para el producto {product}, actualmente solo se tiene {product_name.quantity}"
                print(f"No se tiene en existencia esas cantidades para el producto {product}, actualmente solo se tiene {product_name.quantity}")
            else:
                product_name.quantity = product_quantity
                product_crud.update(product_name)
            
                pdf_place, pdf_name, total = self.invoice(client_value, tax_regime, cfdi, payment, iva, product, description, price, quantity)
                table_client = client_crud.search_id(client_value)
                print(f"El id_client es: {table_client} y el id_client.id es {table_client.id}")
                client_id = table_client.id
                client_email = table_client.email
                client_name = table_client.name
                self.email_send(client_email, pdf_place, client_name)
                self.save_invoice(str(pdf_name), description, product, total, client_id)
                t.value = f"La factura se guardó en {pdf_place}, se envio a {client_email}, y se guardo en la base de datos correctamente"

            t.update()

        invoice_button = ft.ElevatedButton(text="Generar Factura", on_click=invoice_action)

        return ft.Column(
            [
                client_dropdown,
                tax_regime_dropdown,
                cfdi_dropdown,
                payment_dropdown,
                iva_dropdown,
                product_dropdown,
                description_textfield,
                price_textfield,
                quantity_textfield,
                invoice_button,
                t,
            ], alignment=ft.alignment.top_center,
        )
    
    def invoice(self, client_id, tax_regime, cfdi, payment, iva, product, description, price, quantity):
        n = str(uuid.uuid4())[:10]
        folder = "facturas"
        os.makedirs(folder, exist_ok=True)
        client = client_crud.read(client_id)
        pdf_name = f"factura_{client.rfc}_{client.name}_{datetime.now().strftime("%d%m%Y")}_{n}.pdf"
        pdf_place = os.path.join(folder, pdf_name)
        
        doc = SimpleDocTemplate(pdf_place, pagesize=letter)
        styles = getSampleStyleSheet()
        style_normal = styles["Normal"]
        img_path = "images/Tek-D.png"
        img = Image(img_path)
        img_size = 100
        img.drawWidth = img_size
        img.drawHeight = img_size
        date = datetime.now().strftime("%d/%m/%Y")
        date_paragraph = Paragraph(f"Fecha: {date}", style_normal)
        subtotal = price * quantity
        iva_decimal = (iva / 100)
        if iva_decimal == 0:
            iva_price = 0
            total = subtotal
        else:    
            iva_price = subtotal * iva_decimal
            total = subtotal + iva_price
            print(f"El total es: {total}")
        price_letter_function = num2words(total, lang="es")
        price_letter = f"{price_letter_function}".upper()

        data_emisor = [
            [Paragraph("Datos del Emisor:", style_normal)],
            [Paragraph("Tek-D", style_normal)],
            [Paragraph("Calle: Av. Tecnológico #354", style_normal)],
            [Paragraph("Colonia: 80 de mayo", style_normal)],
            [Paragraph("CP: 64000", style_normal)],
            [Paragraph("Ciudad: Monterrey   Estado: Nuevo León   País: México", style_normal)],
            [Paragraph("RFC: TEKD890123HXA", style_normal)],
            [Paragraph("Reg. Fiscal: General de Ley Personas Morales", style_normal)]
        ]
        data_receiver = [
            [Paragraph("Datos del Receptor:", style_normal)],
            [Paragraph(f"{client.name}", style_normal)],
            [Paragraph(f"Domicilio: {client.street} #{client.street_number}", style_normal)],
            [Paragraph(f"Colonia: {client.neighborhood}", style_normal)],
            [Paragraph(f"CP: {client.cp}", style_normal)],
            [Paragraph(f"Ciudad: {client.city}   Estado: {client.state}   País: {client.country}", style_normal)],
            [Paragraph(f"RFC: {client.rfc}", style_normal)],
            [Paragraph(f"Reg. Fiscal: {tax_regime}", style_normal)],
            [Paragraph(f"Uso CFDI: {cfdi}", style_normal)]
        ]
        data_details = [
            ["Cantidad", "CFDI", "Producto", "Descripción", "%IVA", "Precio", "Total"],
            [f"{quantity}", Paragraph(f"{cfdi}", style_normal), Paragraph(f"{product}", style_normal), Paragraph(f"{description}", style_normal), f"{iva}%", f"${price}", f"${total}"]
        ]
        data_amounts = [
            ["Importe con letra:", Paragraph(f"( {price_letter} )", style_normal)],
            ["Forma de Pago", f"{payment}"],
            ["Remitir/Enviar:", "NUESTRO CONDUCTO"]
        ]
        data_total = [
            ["SubTotal:", f"${subtotal}"],
            [f"{iva}% IVA:", f"${iva_price}"],
            ["Total:", f"${total}"]
        ]

        table_emisor = Table(data_emisor)
        table_receiver = Table(data_receiver)
        data = [[table_emisor, table_receiver]]
        table_data = Table(data)
        table_data._argW = [250, 250]
        table_details = Table(data_details)
        table_details._argW = [None, 100, 120, None, None, None, None]
        table_amounts = Table(data_amounts)
        table_amounts._argW = [None, 350]
        table_total = Table(data_total)
        space_tables = Spacer(1, 0.2 * inch)
        style0 = TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        style1 = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        style2 = TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('BACKGROUND', (1, 0), (1, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        table_data.setStyle(style0)
        table_details.setStyle(style1)
        table_amounts.setStyle(style2)
        table_total.setStyle(style2)

        elements = []
        elements.append(img)
        elements.append(space_tables)
        elements.append(table_data)
        elements.append(space_tables)
        elements.append(table_details)
        elements.append(space_tables)
        elements.append(table_amounts)
        elements.append(space_tables)
        elements.append(table_total)
        elements.append(space_tables)
        elements.append(date_paragraph)

        doc.build(elements)
        return pdf_place, pdf_name, total
    
    def email_send(self, email, msg, name = None):
        load_dotenv()
        email_env = os.getenv("gmail_app_email")
        password_env = os.getenv("gmail_app_password")
        yag = yagmail.SMTP(email_env, password_env)
    
        if name == None:
            subject = "Contraseña temporal - Tek-D"
            body = f"Adjuntamos tu contraseña temporal {msg}. Saludos,\nTek-D"
            yag.send(
                to=email,
                subject=subject,
                contents=body,
            )
        else:
            subject = "Factura de Compra - Tek-D"
            body = f"Adjuntamos tu factura de compra {name}. Saludos,\nTek-D"
            yag.send(
                to=email,
                subject=subject,
                contents=body,
                attachments=msg,
            )
        print(f"Correo enviado a {email}")
    
    def textfield_update(self, textfield, replace):
        textfield.value = replace
        print(f"el precio es: {replace}")
        textfield.update()

    def save_invoice(self, pdf_name, description, product, total, id_client):
        new_invoice = Invoice(
            name = pdf_name,
            description = description,
            product = product,
            total = total,
            id_client = id_client,
        )
        invoice_crud.create(new_invoice)

invoice_class = InvoiceApp()
"""
class Invoice2:
    def __init__(self, name, description, product, total, id_client):
        self.name = name
        self.description = description
        self.product = product
        self.total = total
        self.id_client = id_client

    def save_invoice(self, pdf_name, description, product, total, id_client):
        new_invoice = Invoice(
            name = pdf_name,
            description = description,
            product = product,
            total = total,
            id_client = id_client,
        )
        invoice_crud.create(new_invoice)"""