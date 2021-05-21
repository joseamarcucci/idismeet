import streamlit as st
import pandas as pd
import numpy as np
import pybase64
from fpdf import FPDF
from data.create_data import create_table
from math import ceil
def app():
    #st.markdown('<img style="float: left;" src="https://virtual.usal.edu.ar/branding/themes/Usal_7Julio_2017/images/60usalpad.png" />', unsafe_allow_html=True)
    st.markdown('<style>div[data-baseweb="select"] > div {text-transform: capitalize;}body{background-color:#008357;}</style>', unsafe_allow_html=True)
    st.markdown(
    """<style>
        .css-19ih76x{text-align: left !important}
        .css-17eq0hr {
    background-color: #00b8e1;
    background-attachment: fixed;
    flex-shrink: 0;
    height: 100vh;
    overflow: auto;
    padding: 5rem 1rem;
    position: relative;
    transition: margin-left 300ms ease 0s, box-shadow 300ms ease 0s;
    width: 21rem;
    z-index: 100;
    margin-left: 0px;
}    .css-1v3fvcr {
    display: flex;
    flex-direction: column;
    width: 100%;
    margin-top: -100px;
    overflow: auto;
    -webkit-box-align: center;
    align-items: center;
    }
    </style>
    """, unsafe_allow_html=True) 
   
    st.markdown("<h2 style='text-align: left; color: #00b8e1;'>Asistencia por Docente</h2>", unsafe_allow_html=True)
    buff, col = st.beta_columns([2,2])
    #SHEET_ID = '12D4hfpuIkT7vM69buu-v-r-UYb8xx4wM1zi-34Fs9ck'
    df = pd.read_csv('https://docs.google.com/spreadsheets/d/1ceuBcvEPUa5iTr1uHsZr3UCNxT03mvzN_4u7A4rJtmY/export?format=csv')
   
    
    
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.strftime('%d-%m-%y')
    maxValue = df['Fecha'].max()
    minValue = df['Fecha'].min()
    with buff: st.write('Período:',minValue,' al ',maxValue)
    df=df.sort_values(by=['Correo electrónico del organizador'])
   #df = pd.DataFrame(['Correo electrónico del organizador'], columns= ['Correo electrónico del organizador'])
    #BeforeSymbol = df['Correo electrónico del organizador'].str.split('@').str[0]

    countries = df['Correo electrónico del organizador'].unique()

    country = buff.selectbox('Elegir Docente', countries)

    above_352 = df["Correo electrónico del organizador"] == country
    df=df.sort_values(by=['Fecha'],ascending=False)


    #df = pd.read_csv('/mydrive/MyDrive/multiapps/bbc204.csv')
    #df=df.sort_values(by=['SessionOwner'])
    #options = ['USAL_lti_production', 'USAL_rest_production','josemarcucci']
    alumnos = df[above_352]['Identificador del participante'].unique()
    #usuarios=df[above_352].groupby("Fecha")['Minutos Usados'].sum()
    usuarios=df[above_352].groupby("Fecha", as_index=False).agg({ 'Identificador del participante' : 'nunique'})
    usuarios.index = [""] * len(usuarios)
    usuarios=usuarios.sort_values(by=['Fecha'],ascending=False)
    usuarios.columns = ['Fecha','Cantidad de Participantes']
    buff.table(usuarios)

    
    dias = df[above_352]['Fecha'].unique()
    
    
    #if col.checkbox('Ver detalle'):
    with col:st.write("Detalle de asistentes")
    buff1, col5, buff25,col25 = st.beta_columns([3,1,1,2])
    dia = col.selectbox('Elegir Fecha', dias)
    above_3521 = df["Fecha"] == dia
     #asistencia2=df[above_352][above_3521][['Identificador del participante','Duración']]
    asistencia2=df[above_352][above_3521].groupby(['Fecha','Nombre del participante'],as_index=False)['Duración'].sum()
     #asistencia2=df[above_352][above_3521].groupby(['Nombre del participante', 'Fecha']).agg({ 'Duración' : 'sum'})

     #asistencia2.columns = ['Fecha','Nombre','Duración']

    #st.table(df[['Fecha','Código de reunión','Identificador del participante','Tipo de cliente','Correo electrónico del organizador','Duración','Nombre del participante']])
    asistencia2.index = [""] * len(asistencia2)  
    report_text = st.text_input("Report Text")


    export_as_pdf = st.button("Export Report")

    def create_download_link(val, filename):
      b64 = pybase64.b64encode(val)  # val looks like b'...'
      return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

    if export_as_pdf:
      pdf = FPDF()
      pdf.add_page()
      pdf.set_font('Arial', 'B', 16)
      pdf.cell(40, 10, report_text)
    
      html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")

      st.markdown(html, unsafe_allow_html=True)
    col.table(asistencia2)




