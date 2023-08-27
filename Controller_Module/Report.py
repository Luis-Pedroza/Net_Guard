from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from PyQt5.QtWidgets import QMessageBox
import datetime
import os
from UI_Module.UI_Error  import PopUp_Messages

class Report_PDF():
    def saveToPDF(self, path, table, value):
        date = datetime.datetime.now()
        format = "%d-%m-%Y %H:%M"
        actualDate = date.strftime(format)

        if os.path.exists(path):
            directory, base_name = os.path.split(path)
            base_name, extension = os.path.splitext(base_name)
            count = 1
            while os.path.exists(path):
                new_base_name = f"{base_name}{count}"
                path = os.path.join(directory, f"{new_base_name}{extension}")
                count += 1

        self.popUpMessage = PopUp_Messages()
        report = SimpleDocTemplate(path, pagesize=letter, topMargin=30)
        data = []
        newTable = []

        # ***************** Logo *****************
        header_image = "Resources/NetGuard.png"
        image = Image(header_image, width=167, height=75, hAlign='LEFT')
        data.append(image)
        if value:
            text = "Escaneo de conexiones activas"
            dateText = f"Fecha del escaneo: {actualDate}"
        else:
            text = "Tabla de reglas"
            dateText = f"Fecha de creación: {actualDate}"
        
        text = Paragraph(text, style=getSampleStyleSheet()['Heading3'])
        data.append(text)

        dateText = Paragraph(dateText, style=getSampleStyleSheet()['Heading3'])
        dateText.spaceAfter = 20 
        data.append(dateText)

        header = ["Protocolo", "Dirección Local", "Dirección Remota", "Estado", "PID", "Programa"]
        newTable.append(header)


        for row in range(table.rowCount()):
            row_data = []
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item is not None:
                    row_data.append(Paragraph(item.text(), style=getSampleStyleSheet()['Normal']))
                else:
                    row_data.append("")
            newTable.append(row_data)

        # Convert table data to reportlab Table format
        table = Table(newTable, colWidths=90)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        data.append(table)
        report.build(data)
        self.popUpMessage.showMessage('Se guardo el reporte', 'Se guardo el reporte en la carpeta de documentos', QMessageBox.Information)