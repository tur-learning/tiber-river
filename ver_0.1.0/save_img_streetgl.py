from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

# Percorso al tuo chromedriver
path_to_chromedriver = "/home/dario/bin/chromedriver-linux64/chromedriver"

# Inizializza il driver del browser in modalità headless
service = Service(executable_path=path_to_chromedriver)
options = webdriver.ChromeOptions()
#options.add_argument('--headless=new')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134')
driver = webdriver.Chrome(service=service, options=options)

larghezza = 1644
altezza = 1075
driver.set_window_size(larghezza, altezza)


# Vai alla pagina web
map_url = f"https://streets.gl/#41.89247,12.47316,45.00,90.00,600.00"
driver.get(map_url)

try:
    alert = driver.switch_to.alert
    alert.accept()  # o alert.dismiss() se vuoi chiuderla
except Exception as e:
    print(f"No alert present: {e}")

# Simula la pressione della combinazione di tasti (ad es. Shift + A)
time.sleep(40)
actions = ActionChains(driver)
actions.key_down(Keys.CONTROL).send_keys('U').key_up(Keys.CONTROL).perform()

# Cattura lo screenshot
driver.save_screenshot('mappa_screenshot.png')

# Chiudi il driver
driver.quit()
