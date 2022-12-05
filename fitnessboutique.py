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

list_customer_name = []
list_review_title = []
list_review = []
list_reply = []
list_rating = []

dico = {}

t1=time.time()

# ---- Récupère le nombre total de page ----

driver.get(const.BASE_URL_FITNESS)
#Récupérer la liste des elements de la pagination
pag_element = driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "pagination-link_item__mkuN3", " " ))]')
#Récupérer le dernier element de la liste, correspondant au nombre total de page
number_page = int(pag_element[-1].text)

# ---- Boucle principale pour parcourir l'ensemble des pages ----

for nb_page in range(1, number_page + 1):
    url_page = f"{const.BASE_URL_FITNESS}page={nb_page}"
    driver.get(url_page)
    
    #Récupère le nom des clients
    try: 
        customer_name_elements = driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "styles_consumerDetails__ZFieb", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "typography_appearance-default__AAY17", " " ))]')
        for i in range (len (customer_name_elements)):
            list_customer_name.append(customer_name_elements[i].text)
    except:
        [list_customer_name.append("NA")for _ in range (const.NUMBER_LINE)]
        
    #Récupère le titre des commentaires
    try: 
        review_title_elements = driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "link_notUnderlined__szqki", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "typography_appearance-default__AAY17", " " ))]')
        for i in range (len (review_title_elements)):
           list_review_title.append(review_title_elements[i].text)    
    except:
        [list_review_title.append("NA")for _ in range (const.NUMBER_LINE)]

    #Récupère les commentaires
    try:
        review_card_elements = driver.find_elements(By.XPATH,'//*[contains(concat( " ", @class, " " ), concat( " ", "styles_reviewCard__hcAvl", " " ))]')
        for review_element in review_card_elements:
            review = review_element.find_elements(By.CSS_SELECTOR, 'p[data-service-review-text-typography = "true"]')
            list_review.append(review[0].text) if review else list_review.append("-")
    except:
       [list_review.append("NA")for _ in range (const.NUMBER_LINE)]

    #Récupère l'info réponse de l'entreprise ou non.
    try: 
        reply_card_elements = driver.find_elements(By.XPATH,'//*[contains(concat( " ", @class, " " ), concat( " ", "styles_reviewCard__hcAvl", " " ))]')
        for reply_element in reply_card_elements:
            reply = reply_element.find_elements(By.CSS_SELECTOR, 'p[data-service-review-business-reply-text-typography="true"]')
            list_reply.append("Oui") if reply else list_reply.append("Non")
    except: 
       [list_reply.append("NA")for _ in range (const.NUMBER_LINE)]

    #Récupère la notation du client pour l'entreprise
    try: 
        rating_elements = driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "styles_reviewHeader__iU9Px", " " ))]//img')
        for element in rating_elements: 
                rating = element.get_attribute('alt')
                list_rating.append(rating.split(" ")[1])
    except:
        [list_rating.append("NA")for _ in range (const.NUMBER_LINE)]


dico = { "Nom client": list_customer_name,
         "Titre commentaire client": list_review_title,
         "Commentaire client": list_review,
         "Réponse entreprise": list_reply,
         "Note client": list_rating
    }

df = pd.DataFrame(data=dico)

timestr = time.strftime("%d%m%Y_%H%M%S")
df.to_json(f"outpoot/Fitness boutique-{timestr}.json", indent=4)
df.to_csv(f"outpoot/Fitness boutique-{timestr}.csv", index_label = "Id", encoding='utf-8-sig')
df.to_excel(f"outpoot/Fitness boutique-{timestr}.xlsx")

t2=time.time()
print (f"Durée programme = {t2-t1}s") #Durée programme = 2934.502588033676s / 49min
 
driver.quit()