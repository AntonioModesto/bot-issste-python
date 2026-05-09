# 🏛️ ISSSTE Captcha Automator & PDF Downloader

Este script de Python automatiza el proceso de acceso al portal de comprobantes de pago del **ISSSTE**. Utiliza **Selenium** para la navegación web y **Tkinter** para proporcionar una interfaz gráfica (GUI) que permite al usuario resolver el captcha de forma cómoda y rápida.

## 🚀 Características

- **Llenado Automático:** El script detecta el año y mes actual para preseleccionar los datos en el portal.
- **Interfaz de Captcha:** Extrae la imagen del captcha y la muestra en una ventana de Python para evitar navegar manualmente.
- **Optimización de Velocidad:** Tiempos de pausa (`sleep`) ajustados para una navegación rápida.
- **Descarga Directa:** Configurado para guardar los archivos PDF directamente en la carpeta de descargas del usuario sin diálogos adicionales.

## 🛠️ Requisitos

Para ejecutar este proyecto, necesitas tener instalado:

1. **Python 3.x**
2. **Google Chrome** (versión reciente)
3. **Dependencias:**
   ```bash
   pip install selenium pillow
