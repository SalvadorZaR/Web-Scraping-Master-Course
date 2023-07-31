import random
from time import sleep 
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Seteando el user-agent en selenium

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

# Instanciar el driver de selenium para controlar el navegador

driver = webdriver.Chrome(service = Service('./chromedriver'),options=opts)

# Página que requiero
driver.get('https://www.olx.com.ar/autos_c378')
sleep(3)
driver.refresh() # Solución a bug en donde los anuncios sólo cargan alhacer refresh
sleep(6) # Espera a que se cargue le botón para desplegar mas vehiculos

# Busqueda de boton
boton = driver.find_element(By.XPATH, '//button[@data-aut-id="btnLoadMore"]')
for i in range(3):
    try:
        boton.click()
        sleep(random.uniform(8.0,10.0))
        boton = driver.find_element(By.XPATH, '//button[@data-aut-id="btnLoadMore"]') # el botón desaparece y vuelve a aparecer por lo que lo vuelvo a buscar para realizar la siguiente iteración
    except:
        break

# Dentro del DOM que ya se ha cargado con los datos que necesitamos, comenzamos el scrapping
autos = driver.find_elements(By.XPATH, '//li[@data-aut-id="itemBox"]')

# La variable autos al tener el metodo 'find_elements' regresa una lista con los resultados encontrados en el DOM, por lo que es posible iterarla para extraer información 
for auto in autos: 
    try:
        # Por cada anuncio hallo el precio
        precio = auto.find_elements(By.XPATH,'.//span[@data-aut-id="itemPrice"]').text
        print(precio)

    # Por cada anuncio hallo la descripción 
        descripcion = auto.find_elements(By.XPATH,'.//div[@data-aut-id="itemTitle"]').text
        print(descripcion)
    
    except Exception as e: 
        print('Anuncio carece de precio y descripción')
    

    