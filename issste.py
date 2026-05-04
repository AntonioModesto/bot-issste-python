from twocaptcha import TwoCaptcha
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime # <--- Herramienta para el tiempo agregada

# --- CALCULANDO LA FECHA DE HOY ---
fecha_actual = datetime.now()
año_dinamico = str(fecha_actual.year) # Saca el año actual, ej. "2026"
mes_numero = fecha_actual.month

# Diccionario para traducir el número del mes a texto
meses = {
    1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
    5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
    9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
}
mes_dinamico = meses[mes_numero]

print(f"Iniciando... El programa detectó que estamos en: {mes_dinamico} de {año_dinamico}")

driver = webdriver.Chrome()
driver.get('https://issstenet2.issste.gob.mx/gastp4/ua/r/talones/comp-pago')
time.sleep(5) 

try:
    # --- 0. TIPO DE PENSIÓN ---
    print("Seleccionando Edad y Tiempo...")
    xpath_edad_tiempo = '//*[text()="EDAD Y TIEMPO"]'
    opcion_edad = driver.find_element(By.XPATH, xpath_edad_tiempo)
    opcion_edad.click()
    
    time.sleep(2)

    # --- 1. NÚMERO DE PENSIÓN ---
    xpath_numero = '//*[@id="w_78"]/input'
    caja_numero = driver.find_element(By.XPATH, xpath_numero)
    caja_numero.click()
    caja_numero.clear()
    caja_numero.send_keys("653066")

    # --- 2. CÓDIGO DE DEUDO ---
    xpath_codigo = '//*[@id="w_80"]/input'
    caja_codigo = driver.find_element(By.XPATH, xpath_codigo)
    caja_codigo.click()
    caja_codigo.clear()
    caja_codigo.send_keys("0") 

    # --- 3. AÑO ---
    xpath_ano = '//*[@id="w_83"]/input'
    caja_ano = driver.find_element(By.XPATH, xpath_ano)
    caja_ano.click()
    caja_ano.clear()
    caja_ano.send_keys(año_dinamico) # <--- Usando la variable del año

    # --- 4. MES (Modo Humano con Variable) ---
    xpath_mes = '//*[@id="w_86"]/input' 
    caja_mes = driver.find_element(By.XPATH, xpath_mes)
    
    print(f"Abriendo el menú de meses para buscar {mes_dinamico}...")
    caja_mes.click() 
    time.sleep(1)    
    
    # Le decimos a Python que busque en la pantalla el mes exacto que toca
    xpath_mes_dinamico = f'//*[text()="{mes_dinamico}"]' 
    opcion_dinamica = driver.find_element(By.XPATH, xpath_mes_dinamico)
    opcion_dinamica.click() 

    print("¡Todos los datos llenados como jefe!")
    
except Exception as e:
    print(f"Error en algún cuadrito: {e}")

time.sleep(30)
driver.quit()