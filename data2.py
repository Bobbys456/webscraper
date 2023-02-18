from ssl import Options
from typing import KeysView
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd 
from nltk.corpus import stopwords
import os, shutil
import string
#from pyvirtualdisplay import Display
nltk_stopwords = set(stopwords.words('english'))
import sys 



def get_review_summary(result_set):
    rev_dict = {'reviewRating': [],
        'dateCreated': [],
        'reviewBody' : []}
    for result in result_set:
        review_rate = int(str(result.find('span', class_='Fam1ne EBe2gf')["aria-label"])[6]) 
        review_time = result.find('span',class_='dehysf lTi8oc').text
        review_text = result.find('div',class_='Jtu6Td').text
        rev_dict['reviewRating'].append(review_rate)
        rev_dict['dateCreated'].append(review_time)
        rev_dict['reviewBody'].append(review_text)
    import pandas as pd    
    return(pd.DataFrame(rev_dict))




def run(company): 

        
        #display = Display(visible=0, size=(800, 800))  
        #display.start()
        driver = webdriver.Chrome("/usr/bin/chromedriver")

        driver.get("https://www.google.com/")
        #identify search box
        m = driver.find_element("name","q")
        #enter search text for company
        
        m.send_keys(company)
        time.sleep(0.2)
        #perform Google search with Keys.ENTER
        m.send_keys(Keys.RETURN)

        driver.maximize_window() # For maximizing window
        driver.implicitly_wait(30) 
        time.sleep(1)# gives an implicit wait for 20 seconds

        driver.find_element("xpath", "/html/body/div[7]/div/div[11]/div[2]/div[3]/div/div[2]/div/div[1]/div[2]/div[2]/div/div/span[3]/span/a/span").click() 





        scrollable_div = driver.find_element('xpath','/html/body/span[2]/g-lightbox/div/div[2]/div[3]/span/div/div/div/div[2]')


        print(driver.execute_script('return arguments[0].scrollHeight', 
                        scrollable_div)) 

        top = -1
        bottom = False 
        #Scroll as many times as necessary to load all reviews
        while (not bottom ): 
                
                '''print out all the values 
                print("client:   " + str(driver.execute_script('return arguments[0].clientHeight', 
                        scrollable_div)))
                print("offset:   " + str(driver.execute_script('return arguments[0].offsetHeight', 
                        scrollable_div)))
                print("scroll:   "  + str(driver.execute_script('return arguments[0].scrollHeight', 
                        scrollable_div)))
                print("scrollTop:   "  + str(driver.execute_script('return arguments[0].scrollTop', 
                        scrollable_div)))
                print("offsettop:   "  + str(driver.execute_script('return arguments[0].offsetTop', 
                        scrollable_div)))
                print("clienttop:   "  + str(driver.execute_script('return arguments[0].clientTop', 
                        scrollable_div)))
                print("pageyoffset:   "  + str(driver.execute_script('return arguments[0].pageYOffset', 
                        scrollable_div)))
                print("-"* 100)
                '''


        #move page down 
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', 
                        scrollable_div)

                if(driver.execute_script('return arguments[0].scrollHeight', 
                        scrollable_div) == top): 
                        bottom = True

                top = driver.execute_script('return arguments[0].scrollHeight', 
                        scrollable_div)
        
                time.sleep(1)

        response = BeautifulSoup(driver.page_source, 'html.parser')


        reviews = response.find_all('div', class_='WMbnJf vY6njf gws-localreviews__google-review')

        data = get_review_summary(reviews)





        good = data.loc[data[r'reviewRating'] >= 4].reviewBody
        bad = data.loc[data[r'reviewRating'] < 3].reviewBody

        getWords(good, "good", company)
        getWords(bad, "bad", company)

def getWords(df, sent, company): 
    df = df.dropna()

    wordList = {}

    for row in df:
        row = row.split()
        for word in row: 
            
            word = word.lower().translate(str.maketrans('', '', string.punctuation))
            if word not in nltk_stopwords:
                if word in wordList and len(word) > 0: 
                    wordList[word] += 1; 
                else: 
                    wordList[word] = 1; 

   
    d = pd.Series(wordList, name = 'Count')
    
    d.reset_index()

    data = pd.DataFrame(d)
    data.reset_index(inplace=True)
    data.rename(columns={'index': 'Word'}, inplace=True)
    data = data.sort_values(by=['Count'], ascending=False).reset_index(drop=True).head(30)
    print(data)
    path = os.path.join(datafolder, sent, company + "reviews.csv")
    data.to_csv(path, index=False)
   
        

def mergeDataFiles(goodOrBad): 
        Dataframes = []
        for path in os.listdir(path = os.path.join(datafolder, goodOrBad)):
                print(path)
                df = pd.read_csv(os.path.join(datafolder,goodOrBad, path))
                Dataframes.append(df)
        collected = pd.concat(Dataframes).groupby('Word').sum().sort_values(by=['Count'], ascending=False)
        collected.to_csv(os.path.join(datafolder,goodOrBad, "summary.csv"))
    
def main(): 
        
        folder = datafolder
        for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
        try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
        except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        file = open("companies.txt", "r")
        data = file.read()
        company_list = data.split('\n')

        for company in company_list: 
                if( len(company) > 1): 
                        run(company)
        
        mergeDataFiles('good')
        mergeDataFiles('bad')

        
datafolder = 'reviews'
main() 

