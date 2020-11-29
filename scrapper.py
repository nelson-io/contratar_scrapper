# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 12:05:37 2020

@author: Nelson
"""
#import libs
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from tkinter.filedialog import askopenfilename


#import tramites as list



#set path
filename_path = 'C:/Users/Nelson/Documents/contratar_scrapper/tramites.csv'

#import data

tramites = pd.read_csv(filename_path).proc

#initialize scrapper

PATH = 'C:\\Users\\Nelson\\Documents\\Python\\Selenium\\chromedriver.exe'
driver = webdriver.Chrome(PATH)

#get to webpage

driver.get('https://contratar.gob.ar/')

my_df = pd.DataFrame()


    #go to procesos de contratacion
for i in tramites:
    time.sleep(1)
    driver.get('https://contratar.gob.ar/BuscarAvanzado.aspx')
    
    #wait until numproc is generated
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.ID, 'ctl00_CPH1_txtNumeroProceso'))
        )
    
    #insert tramite data
    
    elem_proc_cont = driver.find_element_by_id('ctl00_CPH1_txtNumeroProceso')
    elem_proc_cont.send_keys(i)
    
    #enter in pliego
    
    elem_bt_pliego = driver.find_element_by_id('ctl00_CPH1_btnListarPliegoNumero')
    elem_bt_pliego.click()
    
    time.sleep(2)
    
    #get estado
    
    tramite_estado = driver.find_element_by_id('ctl00_CPH1_GridListaPliegos_ctl02_lblEstadoPliego').text
    #access tramite
    
    elem_num_proc = driver.find_element_by_link_text(i)
    elem_num_proc.click()
    
    WebDriverWait(driver, 120).until(
    EC.presence_of_element_located((By.ID, 'ctl00_CPH1_UCVistaPreviaPliego_UC_InformacionBasica_lblNombreProceso'))
    )
    
    tramite_nombre_proc = driver.find_element_by_id('ctl00_CPH1_UCVistaPreviaPliego_UC_InformacionBasica_lblNombreProceso').text
    
    tramite_exp_num = driver.find_element_by_id('ctl00_CPH1_UCVistaPreviaPliego_usrCabeceraPliego_lblNumExpediente').text
    
    tramite_uoc = driver.find_element_by_id('ctl00_CPH1_UCVistaPreviaPliego_usrCabeceraPliego_lblUnidadOperativa').text
    
    
    if tramite_estado not in ['Fracasado', 'Dejado Sin Efecto', 'Desierto']:
        try:
            tabla_resumen_html = driver.find_element_by_id('ctl00_CPH1_UCVistaPreviaPliego_UCDetalleImputacionAdjudicacion_gvDetalleImputacion').get_attribute('outerHTML')
            tabla_resumen_pd = pd.read_html(tabla_resumen_html)[0]
            
            tabla_resumen_pd['tramite'] = i
            tabla_resumen_pd['tramite_estado'] = tramite_estado
            tabla_resumen_pd['tramite_nombre_proc'] = tramite_nombre_proc
            tabla_resumen_pd['tramite_exp_num'] = tramite_exp_num
            tabla_resumen_pd['tramite_uoc'] = tramite_uoc
            
            
            my_df = my_df.append(tabla_resumen_pd)
        except:
            tabla_resumen_pd = pd.DataFrame(columns = ['Número', 
           'Nombre Constructor', 'Número CUIT', 'Tipo', 'Estado',
           'Fecha perfeccionamiento', 'Monto', 'Moneda', 'tramite',
           'tramite_estado', 'tramite_nombre_proc', 'tramite_exp_num',
           'tramite_uoc'])   
            
            tabla_resumen_pd.loc[0] = None
            
            tabla_resumen_pd['tramite'] = i
            tabla_resumen_pd['tramite_estado'] = tramite_estado + '_error'
            
            my_df = my_df.append(tabla_resumen_pd)   
    else:
        tabla_resumen_pd = pd.DataFrame(columns = ['Número', 
       'Nombre Constructor', 'Número CUIT', 'Tipo', 'Estado',
       'Fecha perfeccionamiento', 'Monto', 'Moneda', 'tramite',
       'tramite_estado', 'tramite_nombre_proc', 'tramite_exp_num',
       'tramite_uoc'])
        
        tabla_resumen_pd.loc[0] = None
        
        tabla_resumen_pd['tramite'] = i
        tabla_resumen_pd['tramite_estado'] = tramite_estado
        tabla_resumen_pd['tramite_nombre_proc'] = tramite_nombre_proc
        tabla_resumen_pd['tramite_exp_num'] = tramite_exp_num
        tabla_resumen_pd['tramite_uoc'] = tramite_uoc

        my_df = my_df.append(tabla_resumen_pd)          
        
    time.sleep(5)   
    
driver.close()





