import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
index_ = ['Title',
          'Main_story_polled','Main_story_average','Main_story_median','Main_story_rushed','Main_story_leisure',
          'Main_with_extras_polled','Main_with_extras_average','Main_with_extras_median','Main_with_extras_rushed','Main_with_extras_leisure',
          'Completion_polled','Completion_average','Completion_median','Completion_rushed','Completion_leisure',
          'Speedrun_any_polled','Speedrun_any_average','Speedrun_any_median','Speedrun_any_fastest','Speedrun_any_longest',
          'Speedrun_full_polled','Speedrun_full_average','Speedrun_full_median','Speedrun_full_fastest','Speedrun_full_longest']
df = pd.DataFrame(columns= index_)

def get_title(soup):
    try:
        title = soup.find('div', class_ = 'GameHeader_profile_header__q_PID shadow_text').text.strip()
        return title
    except:
        return 'N/A'

def get_main_single(soup):
    table_list = soup.find_all('table')
    table = None
    for i in range(len(table_list)):
        box = table_list[i].find('thead')
        if box.find_all('td')[0].text.strip() == 'Single-Player':
            table = table_list[i]
            break
        else:
            continue
    if table == None:
        string = 'Not single'
        return string
    container = table_list[i].find('tbody')
    rows = container.find_all('tr', class_ = 'spreadsheet')
    data_single = []
    for row in rows:
        y = row.find_all('td')
        for i in range(len(y)):
            data_single.append(y[i].text.strip())
    
    main_story = ['N/A' for i in range(5)]
    main_extras = ['N/A' for i in range(5)]
    completion = ['N/A' for i in range(5)]
    for k in range(len(data_single)//6):
        if data_single[6*k] == 'All PlayStyles':
            continue
        else:
            if data_single[6*k] == 'Main Story':
                main_story = data_single[(6*k+1):(6*k+6)]
            elif data_single[6*k] == 'Main + Extras':
                main_extras = data_single[(6*k+1):(6*k+6)]
            elif data_single[6*k] == 'Completionist':
                completion = data_single[(6*k+1):(6*k+6)]
    
    return main_story, main_extras, completion


def get_speedrun(soup):
    table_list = soup.find_all('table')
    table = None
    any_percent = ['N/A' for i in range(5)]
    percent_full = ['N/A' for i in range(5)]
    for i in range(len(table_list)):
        box = table_list[i].find('thead')
        if box.find_all('td')[0].text.strip() == 'Speedruns':
            table = table_list[i]
            break
        else:
            continue
    if table == None:
        return any_percent, percent_full
    container = table_list[i].find('tbody')
    rows = container.find_all('tr', class_ = 'spreadsheet')
    data_single = []
    for row in rows:
        y = row.find_all('td')
        for i in range(len(y)):
            data_single.append(y[i].text.strip())
    for k in range(len(data_single)//6):
        if data_single[6*k] == 'Any%':
            any_percent = data_single[(6*k+1):(6*k+6)]
        elif data_single[6*k] == '100%':
            percent_full = data_single[(6*k+1):(6*k+6)]
    return any_percent, percent_full


    

def prepare_soup(i):
    url = f'https://howlongtobeat.com/game/{i}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        }
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def check_if_empty(soup):
    body = soup.find('body')
    try:
        factor = body.find('h1')
        if factor.text == '404 - Not Found':
            return True
        else:
            return False
    except:
        return False
    pass

def main():
    for k in range(84243,100000):
        zupa = prepare_soup(k)
        if check_if_empty(zupa) == True:
            continue
        row = []
        if get_title(zupa) == 'N/A':
            continue
        row.append(get_title(zupa))
        lista = get_main_single(zupa)
        if type(lista) == str:
            continue
        else:
            for element in lista:
                for mini_element in element:
                    row.append(mini_element)
        lista_speedrun = get_speedrun(zupa)
        for element in lista_speedrun:
            for mini in element:
                row.append(mini)
        df.loc[len(df)] = row
        df.to_csv('Howlongtobeat2.csv',
                    index=False)
if __name__ == '__main__':
    main()