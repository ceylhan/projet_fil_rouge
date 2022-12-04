from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

increment_balise=4
sortir_boucle=1
datepost = []
identifiant = []
avis = []
dimin_pseudo = []
pays = []
avisverifie = []
etoile = []
commentaire = []
commentaire_date = []
i = 4

dictionaire = {
"Identifiant": identifiant,
"Pseudo": dimin_pseudo,
"Date_poste": datepost,
"Avis": avis,
"Pays": pays,
"Avis_statut": avisverifie,
"Commentaire": commentaire,
"Date_commentaire": commentaire_date,
"Etoile": etoile
}

#Driver pour chrome
driver = webdriver.Chrome('C:\chromedriver.exe')

#Récupération de l'url
driver.get("https://fr.trustpilot.com/review/www.fitnessboutique.fr")

#Agrandit la page et permet surtout d'avoir un format standard à chaque changement de page
driver.maximize_window()

#Date du jour
current_date_time = datetime.now().strftime("%Y_%m_%d_%I%M%S_%p")

#Permet de fermer le POPUP en cliquant sur oui
driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()

#Récupération de la dernière page pour notre boucle
derniere_page = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div[26]/nav/a[6]')                                     
print(derniere_page.text)
conversion_entier = int(derniere_page.text)

while sortir_boucle <= conversion_entier: 
    print("Chargement page " + str(sortir_boucle))
        
    #Pour les logs
    url = driver.current_url
    print("Traitement du site " + url)
    
    time.sleep(1)
    #Recuperation de l'identifiant
    try:
        identifiant_site = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div/section/div/article/aside/div/a/span')

        #La difficulté est de récupérer des valeurs alors que celle-ci peuvent être vides
        #Pour ce faire j'ai exclus le 5 qui n'existe pas en DIV et le 15 qui est un bloc pub et sinon je me sers des try/except pour tester si la valeur existe
        for identifiant_parcour in identifiant_site:
            identifiant.append(identifiant_parcour.text.strip())

            #Je créer deux try catch pour séparer les étoiles et les commentaires (cardinalité : (n,n))
            try:
                if (increment_balise == 15 or increment_balise == 5):
                    increment_balise+=1
                    commentaire_site = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div['+str(increment_balise)+']/article/div[2]/div[2]/div/p')
                    commentaire_date_site = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div['+str(increment_balise)+']/article/div[2]/div[2]/div/time')
                    commentaire.append("Y")
                    commentaire_date.append(commentaire_date_site.text.strip())
                else:
                    commentaire_site = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div['+str(increment_balise)+']/article/div[2]/div[2]/div/p')
                    commentaire_date_site = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div['+str(increment_balise)+']/article/div[2]/div[2]/div/time')
                    commentaire.append("Y")
                    commentaire_date.append(commentaire_date_site.text.strip())
                    
            except:
                commentaire.append("N")
                commentaire_date.append("1 janvier 1900")

            try:
                if (increment_balise == 15 or increment_balise == 5):
                    increment_balise+=1
                    etoile_site = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div['+str(increment_balise)+']/article/section/div[1]/div[1]/img').get_attribute('alt')
                    etoile_separation = etoile_site.split(' ')
                    etoile.append(etoile_separation[1].strip())
                else:
                    etoile_site = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div['+str(increment_balise)+']/article/section/div[1]/div[1]/img').get_attribute('alt')
                    etoile_separation = etoile_site.split(' ')
                    etoile.append(etoile_separation[1].strip())
            except:
                etoile.append(0)

            #print(identifiant)   
            #print(commentaire)
            #print(commentaire_date)
            #print(etoile)
            increment_balise += 1

    except:
        identifiant.append("Aucun identifiant")  

    #Recuperation de la date de l'avis
    try:
        datepost_site = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div/article/section/div[2]/p[2]')
        for datepost_parcour in datepost_site:
            datepost.append(datepost_parcour.text.strip('Date de l\'expérience:'))
        #print(datepost)
    except:
        datepost.append("1 janvier 1900")


    #Nombre d'avis
    try:
        avis_site = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div/article/aside/div/a/div/span')
        for avis_parcour in avis_site:
            avis.append(avis_parcour.text.strip(' avis'))
        #print(avis)    

    except:
        avis.append(0)


    #Diminutif pseudo
    try:
        dimin_pseudo_site = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div/article/aside/div/div/span')
        for dimin_pseudo_parcour in dimin_pseudo_site:
            dimin_pseudo.append(dimin_pseudo_parcour.text.strip())
        #print(dimin_pseudo)    

    except:
        dimin_pseudo.append("NA")

    #Pays
    try:
        pays_site = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div/article/aside/div/a/div/div/span')
        for pays_parcour in pays_site:
            pays.append(pays_parcour.text.strip())
        #print(pays)    

    except:
        pays.append("NA")

    #Avis vérifié
    try:
        avisverifie_site = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div/article/section/div[1]/div[3]/div/span/button/div/span')
        for avisverifie_parcour in avisverifie_site:
            avisverifie.append(avisverifie_parcour.text.strip().encode('encoding : str=UTF8'))
        #print(avisverifie)    

    except:
        avisverifie.append("NA")


    #Ecriture dans le Json à chaque changement de page
    with open('extraction_site_Page_' + str(current_date_time) +'.json', 'w') as mon_fichier:
	    json.dump(dictionaire, mon_fichier)

    sortir_boucle += 1
    if sortir_boucle >= conversion_entier:
        print("Toutes les pages ont été parcourus")
    else:

        increment_balise=4

        #J'ajoute un try except pour relancer le click si celui ci ne marche pas avec un sleep (parfois à cause de la lenteur du site)
        try:
            #on clique sur la page suivante
            page_suivante = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div[26]/nav/a[7]/span')
            page_suivante.click()
        except:
            time.sleep(1)
            page_suivante.click()


driver.quit()



    