from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from FileImport import write_csv
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import time

#Pour rentrer dans chaque page
increment_page = 4

sortir_boucle= 1

#On initialise nos listes pour le scrapping
domaine = []
titre = []
trustScore = []
nombreAvis = []
pourcentage5etoiles = []
pourcentage4etoiles = []
pourcentage3etoiles = []
pourcentage2etoiles = []
pourcentage1etoiles = []

#Driver pour chrome
driver = webdriver.Chrome('C:\chromedriver.exe')

#Récupération de l'url
driver.get("https://fr.trustpilot.com/categories/shopping_fashion?page=1")

#Agrandit la page et permet surtout d'avoir un format standard à chaque changement de page
driver.maximize_window()

#Date du jour
current_date_time = datetime.now().strftime("%Y_%m_%d_%I%M%S_%p")

#Récupération des titres de la page qui nous serve à passer d'un site à l'autre
page_site = driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "styles_displayName__GOhL2", " " ))]')

#Permet de fermer le POPUP en cliquant sur oui
driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()

#Récupération de la dernière page pour notre boucle
derniere_page = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div[2]/div/section/div[24]/nav/a[6]/span')
conversion_entier = int(derniere_page.text)

while sortir_boucle <= conversion_entier: 
    print("Chargement page " + str(sortir_boucle))
    for page_parcour in page_site:
        


        #On rentre dans le site
        driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div[2]/div/section/div[' + str(increment_page) +']/a/div[2]').click()
        
        #Sleep pour laisser le temps d'afficher la seconde page, sinon erreur car il essaie de scrap sans que la page ne soit complètement affichée
        time.sleep(3)

        #Pour les logs
        url = driver.current_url
        print("Traitement du site " + url)

        #Titre
        titre_site = driver.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "title_displayName__TtDDM", " " ))]')
        titre.append(titre_site.text.strip())
        #print(titre)

        #Domaine / catégorie
        try:
            domaine_site = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[1]/nav/ol')
            derniere_categorie = (domaine_site.text.split('\n'))
            domaine.append(derniere_categorie[-2])
            #print(domaine)
        except:
            domaine.append("Shopping & mode")

        #Récupération du score de la marque
        try:
            trusScore_site = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div[2]/div[1]/h2/span')
            trustScore.append(trusScore_site.text.replace('.', ',').strip())
            #print(trustScore)

        except:
            trustScore.append(0)

        #Nombre d'avis
        try:
            nombreAvis_site = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div[2]/div[1]/p')   
            nombreAvis.append(nombreAvis_site.text.replace(' ', '').strip('Total:'))
            #print(nombreAvis)
        except:
            nombreAvis.append(0)

        #Pourcentage 5 étoiles
        try:
            pourcentage5etoiles_site = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div[2]/div[2]/label[1]/p[2]')
            pourcentage5etoiles.append(pourcentage5etoiles_site.text.strip(' %'))
            #print(pourcentage5etoiles)
        except:
            pourcentage5etoiles.append(0)

        #Pourcentage 4 étoiles
        try:
            pourcentage4etoiles_site = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div[2]/div[2]/label[2]/p[2]')
            pourcentage4etoiles.append(pourcentage4etoiles_site.text.strip(' %'))
            #print(pourcentage4etoiles)
        except:
            pourcentage4etoiles.append(0)

        #Pourcentage 3 étoiles
        try:
            pourcentage3etoiles_site = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div[2]/div[2]/label[3]/p[2]')
            pourcentage3etoiles.append(pourcentage3etoiles_site.text.strip(' %'))
            #print(pourcentage3etoiles)
        except:
            pourcentage3etoiles.append(0)

        #Pourcentage 2 étoiles
        try:
            pourcentage2etoiles_site = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div[2]/div[2]/label[4]/p[2]')
            pourcentage2etoiles.append(pourcentage2etoiles_site.text.strip(' %'))
            #print(pourcentage2etoiles)
        except:
            pourcentage2etoiles.append(0)

        #Pourcentage 1 étoiles
        try:
            pourcentage1etoiles_site = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div[2]/div[2]/label[5]/p[2]')
            pourcentage1etoiles.append(pourcentage1etoiles_site.text.strip(' %'))
            #print(pourcentage1etoiles)
        except:
            pourcentage1etoiles.append(0)


        increment_page += 1
        #Retour sur la page précédente
        driver.back()

    sortir_boucle += 1
    if sortir_boucle >= 170:
        print("Toutes les pages ont été parcourus")
    else:
        increment_page=4
        #on clique sur la page suivante
        driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div[2]/div/section/div[24]/nav/a[7]/span').click()
        #Même chose que pour le précédent sleep
        time.sleep(3)



driver.quit()

Resultat = pd.DataFrame(list(zip(domaine,titre,trustScore,nombre_avis, pourcentage5etoiles,pourcentage4etoiles,pourcentage3etoiles,pourcentage2etoiles,pourcentage1etoiles)), columns=["Catégorie", "Titre","Score","Avis","5 etoiles", "4 etoiles", "3 etoiles", "2 etoiles", "1 etoiles"])

#Extraction en csv avec la date
Resultat.to_csv('extraction_site_'+ str(current_date_time) +'.csv', index = True)




