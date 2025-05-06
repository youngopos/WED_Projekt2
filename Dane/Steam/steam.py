import pickle
import requests
from bs4 import BeautifulSoup
import re
import copy
import pandas as pd

index_ = ['Title','Release_date','Early_access','Developer','Publisher',
          'Score_number', 'Score','S_recent_number','S_recent',
          'Price','Achievements','Franchise', 'Curators','Genres','Tags',
          'Languages']
df = pd.DataFrame(columns=index_)

with open('list_links.pkl', 'rb') as f:
    games = pickle.load(f)   

def get_title(soup):
    try:
        container = soup.find('div',id = 'genresAndManufacturer',class_ = 'details_block')
        title = container.find('b')
        return title.next_sibling.strip()
    except AttributeError:
        return 'N/A'

def get_release_date(soup):
    try:
        container = soup.find('div', id = 'genresAndManufacturer', class_ = 'details_block')
        rows_b = container.find_all('b')
        release_date = []
        for row_b in rows_b:
            if 'Release Date:' in row_b.text:
                release_date = row_b.next_sibling.strip()
                break
        if release_date == []:
            raise AttributeError
        else:
            return release_date
    except AttributeError:
        return 'N/A'

def get_genres(soup):
    try:
        container = soup.find('div', id = 'genresAndManufacturer', class_ = 'details_block')
        genre_row = container.find('b', string = 'Genre:')
        genre_span = genre_row.find_next_sibling('span')
        genres = genre_span.find_all('a')
        output = ''
        for i in range(len(genres)):
            if i != len(genres) - 1:
                output = output + genres[i].text.strip() + '/'
            else:
                output = output + genres[i].text.strip()
        return output
    except AttributeError:
        return 'N/A'

def get_developer(soup):
    try:
        container = soup.find('div',id = 'genresAndManufacturer',class_ = 'details_block')
        rows = container.find_all('div',class_ = 'dev_row')
        output = ''
        for row in rows:
            if 'Developer' in row.find('b').text:
                outputs = row.find_all('a')
                output = ''
                for i in range(len(outputs)):
                    if i == len(outputs) - 1:
                        output = output + outputs[i].text.strip()
                        return output
                    else:
                        output = output + outputs[i].text.strip() + '/'
        if output == '':
            raise AttributeError
    except AttributeError:
        return 'N/A'

def get_publisher(soup):
    try:
        container = soup.find('div',id = 'genresAndManufacturer',class_ = 'details_block')
        rows = container.find_all('div',class_ = 'dev_row')
        output = ''
        for row in rows:
            if 'Publisher:' in row.find('b').text:
                outputs = row.find_all('a')
                output = ''
                for i in range(len(outputs)):
                    if i == len(outputs) - 1:
                        output = output + outputs[i].text.strip()
                        return output
                    else:
                        output = output + outputs[i].text.strip() + '/'
        if output == '':
            raise AttributeError        
    except AttributeError:
        return 'N/A'

def get_franchise(soup):
    try:
        container = soup.find('div',id = 'genresAndManufacturer',class_ = 'details_block')
        rows = container.find_all('div',class_ = 'dev_row')
        output = ''
        for row in rows:
            if 'Franchise:' in row.find('b').text:
                outputs = row.find_all('a')
                output = ''
                for i in range(len(outputs)):
                    if i == len(outputs) - 1:
                        output = output + outputs[i].text.strip()
                        return output
                    else:
                        output = output + outputs[i].text.strip() + '/'
        if output == '':
            raise AttributeError        
    except AttributeError:
        return 'N/A'

def get_early_access(soup):
    try:
        container = soup.find('div', id = 'genresAndManufacturer', class_ = 'details_block')
        rows_b = container.find_all('b')
        release_date = []
        for row_b in rows_b:
            if 'Early Access Release Date:' in row_b.text:
                release_date = row_b.next_sibling.strip()
                break
        if release_date == []:
            raise AttributeError
        else:
            return release_date
    except AttributeError:
        return 'N/A'

def get_score(soup):
    try:
        box = soup.find('div', class_ = 'glance_ctn')
        container = box.find('div', id = 'userReviews', class_ = 'user_reviews')
        rows_reviews = container.find_all('div', class_ = 'user_reviews_summary_row')
        # all reviews
        reviews_positive = ''
        reviews_count = ''
        for row in rows_reviews:
            try:
                if row.find('div', class_ = 'subtitle column all').text.strip() == 'All Reviews:':
                    # number_of_reviews
                    reviews_count = row.find('span', class_ = 'responsive_hidden').text.strip()
                    reviews_count = reviews_count.replace('(', '').replace(')','')
                    # positive percentage
                    reviews_positive = row.find('span', class_ = 'nonresponsive_hidden responsive_reviewdesc')
                    reviews_positive = reviews_positive.text.strip()
                    match = re.search(r'(\d+)%', reviews_positive)
                    reviews_positive = match.group(1)
                    return reviews_count, reviews_positive
                else:
                    continue
            except:
                if row.find('div', class_ = 'subtitle column').text.strip() == 'All Reviews:':
                    # number_of_reviews
                    reviews_count = row.find('span', class_ = 'responsive_hidden').text.strip()
                    reviews_count = reviews_count.replace('(', '').replace(')','')
                    # positive percentage
                    reviews_positive = row.find('span', class_ = 'nonresponsive_hidden responsive_reviewdesc')
                    reviews_positive = reviews_positive.text.strip()
                    match = re.search(r'(\d+)%', reviews_positive)
                    reviews_positive = match.group(1)
                    return reviews_count, reviews_positive
        if reviews_count == '' and reviews_positive == '':
            raise AttributeError
    except AttributeError:
        return 'N/A', 'N/A'

def get_score_recent(soup):
    try:
        box = soup.find('div', class_ = 'glance_ctn')
        container = box.find('div', id = 'userReviews', class_ = 'user_reviews')
        rows_reviews = container.find_all('div', class_ = 'user_reviews_summary_row')
        # all reviews
        recent_positive = ''
        recent_count = ''
        for row in rows_reviews:
            try:
                if row.find('div', class_ = 'subtitle column').text.strip() == 'Recent Reviews:':
                    # number_of_reviews
                    recent_count = row.find('span', class_ = 'responsive_hidden').text.strip()
                    recent_count = recent_count.replace('(', '').replace(')','')
                    # positive percentage
                    recent_positive = row.find('span', class_ = 'nonresponsive_hidden responsive_reviewdesc')
                    recent_positive = recent_positive.text.strip()
                    match = re.search(r'(\d+)%', recent_positive)
                    recent_positive = match.group(1)
                    return recent_count, recent_positive
                else:
                    continue
            except:
                if row.find('div', class_ = 'subtitle column all').text.strip() == 'Recent Reviews:':
                    # number_of_reviews
                    recent_count = row.find('span', class_ = 'responsive_hidden').text.strip()
                    recent_count = recent_count.replace('(', '').replace(')','')
                    # positive percentage
                    recent_positive = row.find('span', class_ = 'nonresponsive_hidden responsive_reviewdesc')
                    recent_positive = recent_positive.text.strip()
                    match = re.search(r'(\d+)%', recent_positive)
                    recent_positive = match.group(1)
                    return recent_count, recent_positive
        if recent_count == '' and recent_positive == '':
            raise AttributeError
    except AttributeError:
        return 'N/A', 'N/A'

def get_tags(soup):
    try:
        box = soup.find('div',class_ = 'glance_ctn')
        box = box.find('div', class_ = 'glance_tags_ctn popular_tags_ctn')
        tags = box.find('div', class_ = 'glance_tags popular_tags')
        tags = tags.find_all('a')
        string = ''
        for i in range(len(tags)):
            if i != len(tags) - 1:
                string = string + tags[i].text.strip() + '/'
            else:
                string = string + tags[i].text.strip()
        if string == '':
            raise AttributeError
        else:
            return string
    except AttributeError:
        return 'N/A'
    
def get_price(soup):
    try:
        box = soup.find('div', class_ = 'game_area_purchase')
        box_copy = copy.deepcopy(box)
        price = ''
        try:
            box = box.find('div', class_ = 'game_area_purchase_game_wrapper')
            try:
                price = box.find('div',class_ = 'game_purchase_price price').text.strip()
            except:
                price = box.find('div', class_ = 'discount_original_price').text.strip()
        except:
                box = box_copy.find('div', class_ = 'game_area_purchase_game  ')
                try:
                    price = box_copy.find('div',class_ = 'game_purchase_price price').text.strip()
                except:
                    price = box_copy.find('div', class_ = 'discount_original_price').text.strip()
        if price != '':
            return price
        else:
            raise AttributeError
    except AttributeError:
        return 'N/A'

def get_curators(soup):
    try:
        container = soup.find('div', class_ = 'steam_curators_block block responsive_apppage_reviewblock')
        curators = container.find('div', class_ = 'no_curators_followed').text.strip()
        match = re.search(r'(\d{1,3}(?:,\d{3})*)',curators)
        return int(match.group().replace(',',''))
    except:
        return 'N/A'

def get_achievements(soup):
    try:
        container = soup.find('div', id = 'achievement_block')
        title = container.find('div', class_ = 'block_title').text.strip()
        return int(re.sub(r'\D','',title))
    except:
        return 'N/A'

def get_languages(soup):
    container = soup.find('div', id='languageTable')
    if not container:
        return 'N/A'
    langs = []
    for tr in container.find_all('tr'):
        td = tr.find('td', class_='ellipsis')
        if td and td.text.strip():
            langs.append(td.text.strip())
    return '/'.join(langs) if langs else 'N/A'

def get_data(n):
    for i in range(34950,n):
        page = requests.get(games[i])
        soup_temp = BeautifulSoup(page.text, 'html.parser')
        df.loc[len(df)] = create_row(soup_temp)
        df.to_csv('Steam5.csv', index=False)

def create_row(soup):
    row = [get_title(soup), get_release_date(soup), get_early_access(soup), get_developer(soup), get_publisher(soup),
           get_score(soup)[0], get_score(soup)[1], get_score_recent(soup)[0], get_score_recent(soup)[1],
           get_price(soup),get_achievements(soup),get_franchise(soup),get_curators(soup),get_genres(soup),
           get_tags(soup), get_languages(soup)]
    return row

if __name__ == '__main__':
    get_data(len(games))