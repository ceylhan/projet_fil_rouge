from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

increment_page=4
sortir_boucle=1
datepost = []
identifiant = []
avis = []
dimin_pseudo = []
pays = []
avisverifie = []
etoile = []
commentaire = []


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

    #Recuperation de la date de l'avis
    try:
        datepost_site = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div/article/section/div[2]/p[2]')
        for datepost_parcour in datepost_site:
            datepost.append(datepost_parcour.text.strip('Date de l\'expérience:'))
        print(datepost)
    except:
        datepost.append("1 janvier 1900")

    #Recuperation de l'identifiant
    try:
        identifiant_site = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div/section/div/article/aside/div/a/span')
                                                                                                 
        for identifiant_parcour in identifiant_site:
            identifiant.append(identifiant_parcour.text.strip())
        print(identifiant)    

    except:
        identifiant.append("Aucun identifiant")

    #Nombre d'avis
    try:
        avis_site = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div/article/aside/div/a/div/span')
                                                    #//*[contains(concat( " ", @class, " " ), concat( " ", "typography_appearance-subtle__8_H2l", " " ))]
                                                    #//*[@id="__next"]/div/div/div/main/div/div[4]/section/div[9]/article/aside/div/a/div/span
        for avis_parcour in avis_site:
            avis.append(avis_parcour.text.strip(' avis'))
        print(avis)    

    except:
        avis.append(0)


    #Diminutif pseudo
    try:
        dimin_pseudo_site = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div/article/aside/div/div/span')
                                                        #//*[contains(concat( " ", @class, " " ), concat( " ", "avatar_avatarName__ehkAr", " " ))]
                                                            #//*[@id="__next"]/div/div/div/main/div/div[4]/section/div[10]/article/aside/div/div/span
        for dimin_pseudo_parcour in dimin_pseudo_site:
            dimin_pseudo.append(dimin_pseudo_parcour.text.strip())
        print(dimin_pseudo)    

    except:
        dimin_pseudo.append("NA")

    #Pays
    try:
        pays_site = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div/article/aside/div/a/div/div/span')
                                                    #//*[@id="__next"]/div/div/div/main/div/div[4]/section/div[4]/article/aside/div/a/div/div/span
                                                    #.theme-provider_theme-default__IISCt , #__next , .layout_wrapper__s2pss , .layout_content__o0ojo , .styles_container__AimE_ , .styles_mainContent__nFxAv , .styles_reviewsContainer__3_GQw , .styles_reviewCard__9HxJJ , .styles_reviewCard__hcAvl , .styles_consumerInfoWrapper__KP3Ra , .styles_consumerDetailsWrapper__p2wdr , .styles_consumerDetails__ZFieb , .styles_consumerExtraDetails__fxS4S , .styles_detailsIcon__Fo_ua
        for pays_parcour in pays_site:
            pays.append(pays_parcour.text.strip())
        print(pays)    

    except:
        pays.append("NA")

    #Avis vérifié
    try:
        avisverifie_site = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div/article/section/div[1]/div[3]/div/span/button/div/span')
        for avisverifie_parcour in avisverifie_site:
            avisverifie.append(avisverifie_parcour.text.strip())
        print(avisverifie)    

    except:
        avisverifie.append("NA")

    #Récupération des étoiles
    #try:
    #    etoile_site = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div/article/section/div[1]/div[1]/img//@alt')

    #    for etoile_parcour in etoile_site:
    #        print(etoile_parcour)
    #        etoile.append(etoile_site.text.strip())
            
    #        if (int(recuperation_numero[2]) < 3):
    #            try:
    #                reponse_site = driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "styles_wrapper__ib2L5", " " ))]')
    #                reponse.append("Y")
    #                date_reponse = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div[9]/article/div[2]/div[2]/div/time')
    #                
    #            except:
    #                reponse.append("N")

    #    print(etoile)    

    #except:
    #    pays.append("NA")

    dictionaire = {
	"Identifiant": identifiant,
	"Pseudo": dimin_pseudo,
    "date du poste": datepost,
	"Avis": avis,
    "Pays": pays,
    "Avis statut": avisverifie
    }

    with open('extraction_site_Page_' + str(current_date_time) +'.json', 'w') as mon_fichier:
	    json.dump(dictionaire, mon_fichier)

    sortir_boucle += 1
    if sortir_boucle >= conversion_entier:
        print("Toutes les pages ont été parcourus")
    else:
        time.sleep(1)
        increment_page=4
        #J'ajoute un try except pour relancer le click si celui ci ne marche pas
        try:
            #on clique sur la page suivante
            test = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div[26]/nav/a[7]/span')
            test.click()
        except:
            time.sleep(2)
            test.click()
        
        #Même chose que pour le précédent sleep
        time.sleep(1)


driver.quit()



    