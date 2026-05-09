from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime 
import os
import tkinter as tk
from tkinter import messagebox, Label, Entry, Button
from PIL import Image, ImageTk

# --- CÁLCULO DE FECHA Y AÑO (FIJAS) ---
fecha_actual = datetime.now()
año_dinamico = str(fecha_actual.year) 
mes_numero = fecha_actual.month

meses = {
    1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
    5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
    9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
}
mes_dinamico = meses.get(mes_numero, "ENERO") # Manejo de respaldo rápido

# --- CONFIGURACIÓN DEL NAVEGADOR (ALTA VELOCIDAD) ---
ruta_descargas = os.path.join(os.path.expanduser('~'), 'Downloads')
chrome_options = Options()
# Modo de ventana minimizada o pequeña para máxima velocidad
chrome_options.add_argument("--window-size=500x500") 
prefs = {
    "download.default_directory": ruta_descargas,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://issstenet2.issste.gob.mx/gastp4/ua/r/talones/comp-pago')
time.sleep(2.5) # Espera ligera, reducida a la mitad

# --- INICIALIZAR LA VENTANA DE LA INTERFAZ GRÁFICA ---
ventana = tk.Tk()
ventana.title("Validador de Captcha - Sistema ISSSTE")
ventana.geometry("400x420")
ventana.configure(bg="#2b2b2b")

# --- LLENADO DE DATOS (OPTIMIZADO) ---
try:
    opcion = driver.find_element(By.XPATH, '//*[text()="EDAD Y TIEMPO"]')
    opcion.click()
    
    # Reducción extrema de esperas entre elementos
    caja_numero = driver.find_element(By.XPATH, '//*[@id="w_78"]/input')
    caja_numero.click()
    caja_numero.clear()
    caja_numero.send_keys("")

    caja_codigo = driver.find_element(By.XPATH, '//*[@id="w_80"]/input')
    caja_codigo.click()
    caja_codigo.clear()
    caja_codigo.send_keys("")

    caja_ano = driver.find_element(By.XPATH, '//*[@id="w_83"]/input')
    caja_ano.click()
    caja_ano.clear()
    caja_ano.send_keys(año_dinamico)

    caja_mes = driver.find_element(By.XPATH, '//*[@id="w_86"]/input')
    caja_mes.click()
    time.sleep(0.2) # Pausa mínima
    
    opcion_mes = driver.find_element(By.XPATH, f'//*[text()="{mes_dinamico}"]')
    opcion_mes.click()
    time.sleep(0.3)
except Exception as e:
    print(f"Error al iniciar sesión: {e}")

# Funciones de la Interfaz
def tomar_captura_y_mostrar():
    global ruta_imagen
    xpath_imagen = '//*[@id="w_90"]'
    try:
        boton_actualizar = driver.find_element(By.XPATH, xpath_imagen)
        ruta_imagen = os.path.join(os.getcwd(), 'captcha_interfaz.png')
        time.sleep(0.3) # Retardo mínimo
        boton_actualizar.screenshot(ruta_imagen)
        
        img = Image.open(ruta_imagen)
        img = img.resize((240, 80), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        lbl_img.config(image=img_tk)
        lbl_img.image = img_tk
    except Exception as e:
        lbl_img.config(text="Cargando Captcha...")

def procesar_codigo():
    codigo = entrada_codigo.get().strip()
    if not codigo:
        messagebox.showwarning("Advertencia", "Por favor, escribe el código de la imagen.")
        return
    
    try:
        caja_captcha = driver.find_element(By.XPATH, '//*[@id="w_96"]/input')
        caja_captcha.click()
        caja_captcha.clear()
        
        # Escritura rápida del captcha
        for char in codigo:
            caja_captcha.send_keys(char)
            time.sleep(0.01) # Reducción drástica del tiempo de escritura
            
        boton_buscar = driver.find_element(By.XPATH, '//*[@id="w_98"]/div/div/span')
        boton_buscar.click()
        
        time.sleep(1.5) # Espera del servidor reducida a 1.5 segundos
        botones_ok = driver.find_elements(By.XPATH, '//*[text()="OK"]')
        
        if len(botones_ok) > 0:
            botones_ok[0].click()
            messagebox.showerror("Error", "Código rechazado. Espera a que la página se actualice...")
            entrada_codigo.delete(0, tk.END)
            tomar_captura_y_mostrar()
            
        else:
            messagebox.showinfo("¡Éxito!", "El captcha fue validado. El documento se descargará en unos segundos.")
            ventana.destroy()
            driver.quit()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# --- ELEMENTOS DE LA INTERFAZ ---
titulo = Label(ventana, text="Ingresa el código Captcha", fg="#f0f0f0", bg="#2b2b2b", font=("Arial", 14, "bold"))
titulo.pack(pady=15)

lbl_img = Label(ventana, bg="#2b2b2b")
lbl_img.pack(pady=10)

entrada_codigo = Entry(ventana, font=("Arial", 14), justify='center', bd=0, relief='flat')
entrada_codigo.pack(pady=10, ipady=5)

btn_enviar = Button(ventana, text="Enviar Código", bg="#4a76a8", fg="white", font=("Arial", 12, "bold"), command=procesar_codigo, relief='flat', padx=15, pady=5)
btn_enviar.pack(pady=15)

# Carga inicial optimizada
tomar_captura_y_mostrar()
ventana.mainloop()