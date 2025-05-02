import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

index_ = ['Title', 'Release_Date', 'Score', 'Genres', 'Platforms', 'Developer', 'Publisher']

df = pd.DataFrame(columns=index_)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
url_start = 'https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2025&page=1'
response = requests.get(url_start, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
container = soup.find('div', {'data-testid'=='navigation-pagination'})
n_pages = container.find_all('span',class_ = 'c-navigationPagination_item c-navigationPagination_item--page enabled')
n_pages = int(n_pages[1].text)


def get_title(soup):
    try:
        title = soup.find('div',{'data-testid':'hero-title'})
        return title.text
    except:
        return None

def get_platforms(soup):
    try:
        details = soup.find('div', class_ = 'c-gameDetails')
        containers = details.find_all('div', class_ = 'c-gameDetails_sectionContainer u-flexbox u-flexbox-column')
        temp = containers[0].find('div',class_ ='c-gameDetails_Platforms u-flexbox u-flexbox-row')
        platforms = temp.find_all('li')
        platforms_string = ''
        for i in range(len(platforms)):
            if i != len(platforms) - 1:
                platforms_string += platforms[i].text.strip()
                platforms_string += '/'
            else:
                platforms_string += platforms[i].text.strip()
        return platforms_string
    except:
        return None

def get_release_date(soup):
    try:
        details = soup.find('div', class_ = 'c-gameDetails')
        containers = details.find_all('div', class_ = 'c-gameDetails_sectionContainer u-flexbox u-flexbox-column')
        temp = containers[0].find('div', class_ = 'c-gameDetails_ReleaseDate u-flexbox u-flexbox-row')
        new_text = temp.text
        return new_text.replace('Initial Release Date: ', '')
    except:
        return None

def get_developer(soup):
    try:
        details = soup.find('div', class_ = 'c-gameDetails')
        containers = details.find_all('div', class_ = 'c-gameDetails_sectionContainer u-flexbox u-flexbox-column')
        temp = containers[1].find('div', class_ = 'c-gameDetails_Developer u-flexbox u-flexbox-row')
        developers = temp.find_all('li')
        d_string = ''
        for i in range(len(developers)):
            if i == len(developers) - 1:
                d_string += developers[i].text.strip()
            else:
                d_string += developers[i].text.strip()
                d_string += '/'
        return d_string
    except:
        return None
    
def get_publisher(soup):
    try:
        details = soup.find('div', class_ = 'c-gameDetails')
        containers = details.find_all('div', class_ = 'c-gameDetails_sectionContainer u-flexbox u-flexbox-column')
        temp = containers[1].find('div', class_ = 'c-gameDetails_Distributor u-flexbox u-flexbox-row')
        publishers = temp.find_all('a')
        string = ''
        for i in range(len(publishers)):
            if i == len(publishers) - 1:
                string += publishers[i].text.strip()
            else:
                string += publishers[i].text.strip()
                string += '/'
        if string == '':
            raise AttributeError
        else:
            return string
    except :
        return None

def get_genres(soup):
    try:
        container = soup.find('div', class_ = 'c-gameDetails_sectionContainer u-flexbox u-flexbox-row u-flexbox-alignBaseline')
        genres = container.find_all('li')
        string = ''
        for i in range(len(genres)):
            if i == len(genres) - 1:
                string += genres[i].text.strip()
            else:
                string += genres[i].text.strip()
                string += '/'
        return string
    except AttributeError:
        return None

def get_score(soup):
    try:
        container = soup.find('div', {'data-testid': 'all-platforms'})
        ind = container.find_all('a')
        numbers = []
        scores = []
        for element in ind:
                number_string = element.find('p').text
                number_List = [int(tok) for tok in number_string.split() if tok.isdigit()]
                numbers.append(number_List[0])
                try:
                    score = int(element.find('span').text)
                    scores.append(score)
                except:
                    continue
        count = sum(numbers)
        weighted_sum = sum(n * s for n,s in zip(numbers, scores))
        weighted_mean = weighted_sum/count
        return round(weighted_mean, 3)
    except:
        return None



def page(soup1):
    base_url = 'https://www.metacritic.com'
    containers = soup1.find_all('div',{'data-testid': 'filter-results'})
    for i in range(len(containers)):
        link = containers[i].find('a', class_ = 'c-finderProductCard_container g-color-gray80 u-grid')['href']
        url_game_solo = base_url + link
        response_temp = requests.get(url_game_solo, headers=headers)
        soup_temp = BeautifulSoup(response_temp.text,'html.parser')
        row = [get_title(soup_temp), get_release_date(soup_temp), get_score(soup_temp), get_genres(soup_temp), get_platforms(soup_temp),
               get_developer(soup_temp), get_publisher(soup_temp)]
        df.loc[len(df)] = row

def get_all_data():
    for i in range(1,n_pages + 1):
        time_start = time.time()
        url_temp = f'https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2025&page={i}'
        response_temp = requests.get(url_temp,headers=headers)
        soup_temp = BeautifulSoup(response_temp.text, 'html.parser')
        page(soup_temp)
        time_end = time.time()
        elapsed_time = time_end-time_start
        print('Operation Successful! '+f'Elapsed time: {elapsed_time:.4f} seconds')

if __name__ == '__main__':
    get_all_data()
    df.to_csv('Metacritic.csv', index=False)