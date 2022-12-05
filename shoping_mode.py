from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
import pandas as pd
import constants as const
import time


serv_obj=Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=serv_obj)

driver.maximize_window()
#driver.implicitly_wait(5)

list_company_url = []
list_company_name = []

list_reviews_number = []
list_rating = []
list_category = []

list_rating_5stars = []
list_rating_4stars = []
list_rating_3stars = []
list_rating_2stars = []
list_rating_1stars = []

t1=time.time()

# ---- Récupère le nombre total de page ----

driver.get(const.BASE_URL_SHOP)
#Récupérer la liste des elements de la pagination
pag_element = driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "pagination-link_item__mkuN3", " " ))]')
#Récupérer le dernier element de la liste, correspondant au nombre total de page
number_page = int(pag_element[-1].text)

# ---- Parcours de l'ensemble des pages pour récuper les URL des entreprises ---- 

for nb_page in range (1,number_page + 1):
    url_page = f"{const.BASE_URL_SHOP}page={nb_page}"
    driver.get(url_page)    
    try:
        company_url_element = driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "styles_linkWrapper__UWs5j", " " ))]')
        for element in company_url_element: 
            url_entrerise = element.get_attribute('href')
            #Tous les URL figurent dans la liste list_company_url
            list_company_url.append(url_entrerise) 
    except:
        pass

# ---- Parcours de l'ensemble des URL obtenu dans la première boucle pour scraper les infos ---- 

for url_ent in list_company_url:
    driver.get(url_ent)
    
    #Récupère le nom des entreprises
    try: 
        company_name_element = driver.find_element(By.XPATH, '//*[@id="business-unit-title"]/h1/span[1]')
        list_company_name.append(company_name_element.text.strip())
    except:
        list_company_name.append("NA")
    
    #Récupère le nombre d'avis des entreprises
    try:
        reviews_number_element = driver.find_element(By.XPATH, '//*[@id="business-unit-title"]/span/span')
        list_reviews_number.append(reviews_number_element.text.split('•')[0].strip())
    except:
        list_reviews_number.append("NA")

    #Récupère la Note globale des entreprises
    try:
        rating_element = driver.find_element(By.XPATH, '//*[@id="business-unit-title"]/div/div/p')
        list_rating.append(rating_element.text)
    except:
        list_rating.append("NA")

    #Récupère la sous catégorie des entreprises (celle qui apparait juste avant le nom de l'entreprise dans la barre de navigation)
    try: 
        taille = len(driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "breadcrumb_breadcrumbLink__p1PMo", " " ))]'))
        category_element = driver.find_element(By.XPATH, f'//*[@id="__next"]/div/div/div/main/div/div[1]/nav/ol/li[{taille-1}]')
        list_category.append(category_element.text)

    except:
        list_category.append("NA")

    #Récupère le pourcentage d'avis des entreprises
    try:
        rating_percent_element = driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "styles_percentageCell__cHAnb", " " ))]')        
        list_rating_5stars.append(rating_percent_element[0].text.split(' ')[0])
        list_rating_4stars.append(rating_percent_element[1].text.split(' ')[0])
        list_rating_3stars.append(rating_percent_element[2].text.split(' ')[0])
        list_rating_2stars.append(rating_percent_element[3].text.split(' ')[0])
        list_rating_1stars.append(rating_percent_element[4].text.split(' ')[0])

    except: 
        list_rating_5stars.append("NA")
        list_rating_4stars.append("NA")
        list_rating_3stars.append("NA")
        list_rating_2stars.append("NA")
        list_rating_1stars.append("NA")

timestr = time.strftime("%d%m%Y_%H%M%S")

df = pd.DataFrame(list(zip(list_company_name, list_reviews_number, list_rating, list_category, list_rating_5stars, list_rating_4stars, list_rating_3stars,list_rating_2stars, list_rating_1stars)), columns=['Nom entreprise', 'Nombre d\'avis', 'Note de l\'entreprise', 'Catégorie', 'Pourcentage 5 étoiles','Pourcentage 4 étoiles','Pourcentage 3 étoiles','Pourcentage 2 étoiles','Pourcentage 1 étoile' ])
df.to_excel(f"outpoot/Shopping & Mode-{timestr}.xlsx")
df.to_csv(f"outpoot/Shopping & Mode-{timestr}.csv", index_label = "Id", encoding='utf-8-sig')


t2=time.time()
print (f"Durée programme = {t2-t1}s") # Durée programme = 3412.3557200431824s (56min52s)

driver.quit()