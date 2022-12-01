from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from FileImport import write_csv
from datetime import datetime

#Driver pour chrome
driver = webdriver.Chrome('C:\chromedriver.exe')

#Récupération de l'url
driver.get("https://fr.trustpilot.com/categories/food_beverages_tobacco")


#Variable pour incrémenter les pages du sites..
increment_page = 1

sortir_boucle= 1

#On initialise nos variables pour le scrapping
localisation = []
reviews = []
trustScore = []
titre = []
type_compagnie = []

current_date_time = datetime.now().strftime("%Y_%m_%d_%I%M%S_%p")

#Boucle pour récupérer les informations des pages
while sortir_boucle==1:

    #Récupération de la balise
    titre_site = driver.find_elements(By.CLASS_NAME, 'styles_displayName__GOhL2')

    #On test si le titre de la marque est renseigné sinon on part du principe qu'on se trouve à la dernière page
    #et que donc il n'y a plus d'informations à scrapper
    if not(titre_site):
        print("Page vide")
        sortir_boucle=2
    else:
        print("La page=" + str(increment_page) + " est chargée")
    
        #Récupération du titre de la marque
        for titre_parcour in titre_site:
            titre.append(titre_parcour.text.strip())

        #Récupération du score de la marque
        trustScore_site = driver.find_elements(By.CLASS_NAME, 'styles_trustScore__8emxJ')
            
        for trustScore_parcour in trustScore_site:
            trustScore.append(trustScore_parcour.text.strip())

        #Récupération du nombre d'avis
        reviews_site = driver.find_elements(By.CLASS_NAME, 'styles_ratingText__yQ5S7')

        for reviews_parcour in reviews_site:
            reviews.append(reviews_parcour.text.strip())

        #Récupération de la localisation
        localisation_site = driver.find_elements(By.CLASS_NAME, 'styles_location__ILZb0')

        for localisation_parcour in localisation_site:
            localisation.append(localisation_parcour.text.strip())


        #Récupération du type de la compagnie
        type_compagnie_site = driver.find_elements(By.CLASS_NAME, 'typography_appearance-default__AAY17')

        
        for type_compagnie_parcour in type_compagnie_site:
            type_compagnie.append(type_compagnie_parcour.text.strip())

        increment_page += 1
        driver.get("https://fr.trustpilot.com/categories/food_beverages_tobacco?page=" + str(increment_page) +"")



Resultat = pd.DataFrame(list(zip(titre,trustScore,reviews,localisation, type_compagnie)), columns=["Titre","Score","Vote","Localisation", "type_compagnie"])

#Extraction en csv avec la date
Resultat.to_csv('extraction_site_'+ str(current_date_time) +'.csv', index = True)




