from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
import requests
import json
import os
from enum import Enum


response = requests.request("POST", url, headers=headers, data=payload)
token=response.json()['data']

def write_a_data(data, type_str, operation, story:list):
    estilo_tipo = ParagraphStyle(
        name='TipoStyle',
        fontName='Helvetica',
        fontSize=12,
        textColor=colors.black,
        spaceAfter=6,
        bold=True
    )

    estilo_datos = ParagraphStyle(
        name='DatosStyle',
        fontName='Helvetica',
        fontSize=12,
        textColor=colors.black
    )

    p_tipo = Paragraph(f"<b>{type_str}:</b>", estilo_tipo)
    story.append(p_tipo)

    p_datos = Paragraph(f"{operation}{data}", estilo_datos)
    story.append(p_datos)

    story.append(Spacer(1, 12))


def write_a_frequency_table(data_table, story):
    table_data = []
    table_data.append(['Lim I', 'Lim. S', 'Frec', 'Frec AC', 'MC', 'Lim IE', 'Lim SE'])
    for data in data_table:
        table_data.append([
            str(data['limInf']),
            str(data['limSup']),
            str(data['frequency']),
            str(data['cumulativeFrequency']),
            str(data['classMark']),
            str(data['limInfEx']),
            str(data['limSupEx'])
        ])

    estilo_tabla = [
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ]

    story.append(Table(table_data, style=estilo_tabla))

    story.append(Spacer(1, 12))


def make_petitions(type:str):
    url = f"http://52.21.60.239:8080/miseri/api/statistic/{type}"
    payload = {}
    headers = {
    'Authorization': token
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data=response.json()['data']

    return make_document(data, data['sensor'])


def make_document(data, title:str):
    story = []
    write_a_data(data['sensor'],"Sensor","",story)
    write_a_frequency_table(data['frequency'],story)
    write_a_data(data['range']['data'],"Range","",story)
    write_a_data(data['amplitude']['data'],"Amplitude","",story)
    write_a_data(data['unit']['data'],"Variation unit","",story)
    write_a_data(data['media']['data'],"Mean","",story)
    write_a_data(data['mediaArit']['data'],"Arithmetic Mean","",story)
    write_a_data(data['moda']['data'],"Moda","",story)
    write_a_data(data['meanDeviation']['data'],"Mean Deviation","",story)
    write_a_data(data['variance']['data'],"Variance","",story)
    write_a_data(data['standardDeviation']['data'],"Standard Deviation","",story)
    write_a_data("Miseri-TEAM", "Made by","", story)

    rute=f"public/{title}_report.pdf"

    if os.path.exists(rute):
        os.remove(rute)
        print("ole")

    doc = SimpleDocTemplate(rute, pagesize=letter)
    doc.build(story)
    print("Document gerenerated successfully.") 
    return rute;



class type(Enum):
    QUALITY='quality'
    LIGHT='light'
    HUMIDITY='humidity'
    TEMPERATURE='temperature'