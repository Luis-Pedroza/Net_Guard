# ***************************************************
# FILE: Report.py
#
# DESCRIPTION:
#
# The provided code defines a Python class called ReportPDF
# for generating and saving PDF reports. This class is designed to
# create PDF reports from tabular data, with options for specifying
# the report's title and adding page numbers. It leverages the
# ReportLab library for PDF generation and relies on PyQt5 for
# graphical user interface components like message boxes.
#
# AUTHOR:  Luis Pedroza
# CREATED: 01/09/2023 (dd/mm/yy)
# ******************* ********************************

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib import colors, pagesizes, styles
from reportlab.pdfgen import canvas
import datetime
import os


class ReportPDF():
    """
    A class for generating and saving PDF reports.

    Methods:
        save_to_PDF(self, report_path: str, data_table: QTableWidget, save_value: bool)
            Saves a PDF report based on the provided data and options.

        add_page_number(self, canvas: canvas.Canvas, doc: SimpleDocTemplate)
            Adds page numbers to the generated PDF.

    """
    def save_to_PDF(self, report_path: str, data_table, save_value: bool):
        """
        Saves a PDF report based on the provided data and options.

        Args:
            report_path (str): The path where the PDF report will be saved.
            data_table (QTableWidget): The table widget containing the data for the report.
            save_value (bool): Indicates whether the report is for active connections (True) or firewall rules (False).

        Returns:
            None

        Raises:
            None

        Example Usage:
            pdf_report = ReportPDF()
            pdf_report.save_to_PDF('reports', data_widget, True)

        """
        try:
            date = datetime.datetime.now()
            format = "%d-%m-%Y %H:%M"
            current_date = date.strftime(format)
            report_path = f"{report_path}/Report.pdf"

            if os.path.exists(report_path):
                directory, base_name = os.path.split(report_path)
                base_name, extension = os.path.splitext(base_name)
                count = 1
                while os.path.exists(report_path):
                    new_base_name = f"{base_name}{count}"
                    report_path = os.path.join(directory, f"{new_base_name}{extension}")
                    count += 1

            report = SimpleDocTemplate(report_path, pagesize=pagesizes.letter, topMargin=30)
            header_template = []
            table_template = []
            data_template = []

            header_image = "Resources/NetGuard.png"
            image = Image(header_image, width=167, height=75, hAlign='LEFT')

            if save_value:
                text = "Active connections"
                header = ["Protocol", "Local Address", "Remote Address", "State", "PID", "Program"]
            else:
                text = "List of Firewall rules"
                header = ["Rule", "Enable", "Profile", "Action", "Direction", "Protocol"]

            date_text = f"Date: {current_date}"

            current_text = f'{text}\n{date_text}'
            current_text = Paragraph(current_text, style=styles.getSampleStyleSheet()['Heading3'])
            header_template.append([image, current_text])

            header_table = Table(header_template, colWidths=[370, 150])
            header_table.spaceAfter = 20
            data_template.append(header_table)

            table_template.append(header)

            for row in range(data_table.rowCount()):
                row_data = []
                for col in range(data_table.columnCount()):
                    item = data_table.item(row, col)
                    if item is not None:
                        row_data.append(Paragraph(item.text(), style=styles.getSampleStyleSheet()['Normal']))
                    else:
                        row_data.append("")
                table_template.append(row_data)

            data_table = Table(table_template, colWidths=90)
            data_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            data_template.append(data_table)
            report.build(data_template, onFirstPage=self.add_page_number, onLaterPages=self.add_page_number)
        except Exception as exception:
            raise ErrorReport('ERROR: Report_Save', str(exception))

    def add_page_number(self, canvas: canvas.Canvas, doc: SimpleDocTemplate):
        """
        Adds page numbers to the generated PDF.

        Args:
            canvas: The PDF canvas.
            doc: The PDF document.

        Returns:
            None

        Raises:
            None

        Example Usage:
            Called automatically by the PDF generation process.

        """
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.drawRightString(550, 20, text)


class ErrorReport(Exception):
    def __init__(self, error_code, error_description):
        super().__init__(error_description)
        self.error_code = error_code
