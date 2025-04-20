from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Lancer le navigateur
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://fr.toyota.be/modeles?sortOrder=modelIndex")

wait = WebDriverWait(driver, 10)

# Attendre que tous les éléments des modèles soient présents
elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="model-results-main"]/div[2]/article')))

print(f"Nombre de modèles trouvés : {len(elements)}")

# Liste pour stocker les données
models_data = []

# Parcourir chaque élément de modèle
for idx, element in enumerate(elements, start=1):
    try:
        # Construire le XPath dynamique pour chaque modèle
        xpath = f'//*[@id="model-results-main"]/div[2]/article[{idx}]/div[1]/div[1]'
        model_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        raw_text = model_element.text
        lines = raw_text.split("\n")

        # Structurer les données dans un dictionnaire
        data = {
            "Nom du modèle": lines[0] if len(lines) > 0 else "",
            "Prix du véhicule": lines[1] if len(lines) > 1 else "",
            "Mensualité": lines[2] if len(lines) > 2 else "",
            "Durée du financement": lines[4] if len(lines) > 4 else "",
            "TAEG": lines[5] if len(lines) > 5 else "",
            "Type de carburant": lines[6] if len(lines) > 6 else ""
        }

        models_data.append(data)
    except Exception as e:
        print(f"Erreur lors de l'extraction du modèle {idx} : {e}")

# Créer le DataFrame
df = pd.DataFrame(models_data)

# Afficher le DataFrame
print(df)



# Fermer le navigateur
driver.quit()
