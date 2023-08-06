import rapidfuzz
import re
from googlesearch import search
from bs4 import BeautifulSoup
import requests
from rapidfuzz import fuzz
from rapidfuzz import process

def get_urls(tag, n, language):
    urls = [url for url in search(tag, stop=n, lang=language)]
    return urls


def link_checker(a,b):
    #checks if the links contain the name of the page something similar to the compnay name or not
    # doing this because sometimes the website contains links to other pages apart from the website page, 
    # and we cannot just do an exact check whether the compnay name is present in the link or not because sometimes the links have different names

    # we will use the function fuzz.partial_ratio which is very good in identifying the similarity in this case

    test = fuzz.partial_ratio(a, b)

    if test >= 40: # using this similarity has a lot of drawbacks too, sometimes the wesbite name is an abbreviation
        # we need to come up with something more intelligent to be able to use such a system properly
        # till then I am keeping the threshold very low
        #print(f'true checked ^^^^^ : {a} and {b}')
        return True
    
    else :
        #print(f'false checked ^^^^^ : {a} and {b}')
        return False




def finder(url):
    #social = 'facebook'
    #url = 'https://www.example.com/' # the input can be full link or just example.com
    url = url.lower() # lower case any string right away

    ## THIS WILL HANDLE THE VARIATIONS IN THE INPUT LINK
    name = re.sub(r'https?:\/\/(www\.?)?', '', url) # this will delete the front part of the url
    name = re.sub(r'(\.\w{2,3}){1,2}\/?\w*\/?$', '', name ) # 
    #name # contains the name of the website

    #####################################################################
    # GOOGLING THE LINKS
    # we are using 'name' while searching, this is debatable 'url' can also be used
    facebook_ggl = get_urls(f'{name} company facebook', 1 , 'en')[0].lower()
    facebook_ggl = re.sub('\?.*', '', facebook_ggl)
    #print(facebook_ggl)
    if 'facebook' not in facebook_ggl or name not in facebook_ggl:  facebook_ggl = ''


    twitter_ggl = get_urls(f'{name} company twitter', 1 , 'en')[0].lower()
    twitter_ggl = re.sub('\?.*', '', twitter_ggl)
    #print(twitter_ggl)
    if 'twitter' not in twitter_ggl or name not in twitter_ggl : twitter_ggl = ''


    instagram_ggl = get_urls(f'{name} company instagram', 1 , 'en')[0].lower()
    instagram_ggl = re.sub('\?.*', '', instagram_ggl)
    #print(instagram_ggl)
    if 'instagram' not in instagram_ggl or name not in instagram_ggl: instagram_ggl = ''


    linkedin_ggl = get_urls(f'{name} company linkedin', 1 , 'en')[0].lower()
    linkedin_ggl = re.sub('\?.*', '', linkedin_ggl)
    #print(linkedin_ggl)
    if 'linkedin' not in linkedin_ggl or name not in linkedin_ggl : linkedin_ggl = ''



    ggl_values = { 
        'facebook' :facebook_ggl,
        'twitter' :twitter_ggl,
        'instagram' : instagram_ggl,
        'linkedin' :linkedin_ggl
    }

    #ggl_values    
    ######################################################################


    try:
        page = requests.get(url).text # intial scrape, using the googled name of the company to rectify any spelling mistakes
    except:
        print("An error occured.")   


    

    soup = BeautifulSoup(page, 'lxml')# INITIAL SCRAPE TO FIND ALL THE LINKS WE SCRAPE
    #print(soup.prettify())
    html_text = str(soup) 

    all_links = re.findall(r'"http[a-zA-Z0-9\.\-\=\&\?\/\:\_]+"', html_text) # finds all possible links present in the initial scrape
    if all_links :
        #print(all_links) 
        all_flag = 1 
        #facebook_list = [x.lower() for x in facebook_list[0] if self.link_checker(self.input_company_name.lower(), x.lower())]
        all_links = [x.lower().replace('"','') for x in all_links if 'facebook' not in x.lower() and 'instagram' not in x.lower() and 'twitter' not in x.lower() and 'linkedin' not in x.lower() ]
    else: all_flag = 0 


    all_links = [a for a in all_links if fuzz.partial_ratio(url,a)>=60 and 'api' not in a and 'admin' not in a and 'score' not in a and 'schema' not in a ]
    all_links = all_links[:10] # scrape just 5 extra links to save time, we may increase this limit later on
    all_links.append(url)
    all_links=list(set(all_links))
    # all_links



    #######################################################################
    # SCRAPE ALL THE LINKS ONE BY ONE
    collector = []

    for link in all_links:
        try:
            page = requests.get(link).text 
            soup = BeautifulSoup(page, 'lxml')# for the initial scrape
            #print(soup.prettify())
            html_text = str(soup)
        except:
            print("An error occured.")
            html_text = ''



    # mail_list = re.findall(r'\w+@\w+\.{1}[a-zA-Z0-9\-\.]+', html_text)
    # if mail_list: 
    #     ma_flag = 1
    #     mail_list = set([x.lower().replace('"','') for x in mail_list])
    # else: ma_flag = 0 


    #facebook_list = re.findall(r'".+facebook.+"', html_text) # '\w+@\w+\.{1}\w+' for emails, https:\/\/www\.linkedin\.com\/company\/.+ for linkedin links
    facebook_list = re.findall(r'"http[a-zA-Z0-9\.\-\=\&\?\/\:\_]+facebook[a-zA-Z0-9\.\-\=\&\?\/\:\_]+"', html_text) # '\w+@\w+\.{1}\w+' for emails, https:\/\/www\.linkedin\.com\/company\/.+ for linkedin 

    if facebook_list : 
        fb_flag = 1 
        #facebook_list = [x.lower() for x in facebook_list[0] if self.link_checker(self.input_company_name.lower(), x.lower())]
        facebook_list = set([x.lower().replace('"','') for x in facebook_list if link_checker(url, x.lower().replace('"','')) and 'sharer' not in x.lower() and '.svg' not in x.lower() and '.png' not in x.lower()  and '.js' not in x.lower()  ])
    else: fb_flag = 0

    #linkedin_list = re.findall(r'https:\/\/www\.linkedin\.com\/company\/[a-zA-Z0-9\-\.]+', html_text)
    linkedin_list = re.findall(r'"http[a-zA-Z0-9\.\-\=\&\?\/\:\_]+linkedin[a-zA-Z0-9\.\-\=\&\?\/\:\_]+"', html_text)
    if linkedin_list: 
        ln_flag = 1
        linkedin_list = set([x.lower().replace('"','') for x in linkedin_list if link_checker(url, x.lower().replace('"','')) and '.svg' not in x.lower()  and '.png' not in x.lower()  ])
    else: ln_flag = 0

    twitter_list = re.findall(r'"http[a-zA-Z0-9\.\-\=\&\?\/\:\_]+twitter[a-zA-Z0-9\.\-\=\&\?\/\:\_]+"', html_text)
    if twitter_list: 
        tw_flag = 1 
        twitter_list = set([x.lower().replace('"','') for x in twitter_list if link_checker(url, x.lower().replace('"','')) and 'platform' not in x.lower() and '.svg' not in x.lower() and '.png' not in x.lower() ])
    else: tw_flag = 0

    #instagram_list = re.findall(r'https:\/\/www\.instagram\.com\/[a-zA-Z0-9\-\.\_]+', html_text)
    #instagram_list = [x.lower() for x in instagram_list if self.link_checker(self.input_company_name.lower(), x.lower()) ]
    instagram_list = re.findall(r'"http[a-zA-Z0-9\.\-\=\&\?\/\:\_]+instagram[a-zA-Z0-9\.\-\=\&\?\/\:\_]+"', html_text)
    if instagram_list: 
        in_flag = 1
        instagram_list = set([x.lower().replace('"','') for x in instagram_list if link_checker(url, x.lower().replace('"','')) and '.svg' not in x.lower() and '.png' not in x.lower()  ])
    else: in_flag = 0



    new_value = {
        'input_url': url, 
        #'email': mail_list,
        #'actual_link': str(response.url),  
        # 'link': a , # earlier we were outputting the entire link by using: str(response.url), 
        'facebook': facebook_list, # making a set eleminates the occasional duplicate links that get captured
        'linkedin': linkedin_list, 
        'twitter': twitter_list, 
        'instagram': instagram_list,
        'total_flags': fb_flag + ln_flag + tw_flag + in_flag
        }
    

    collector.append(new_value)
    #print(new_value)
    ##################################################################

    # JOINING ALL THE DICTIONARIES

    twitter = []
    linkedin = []
    facebook = []
    instagram = []


    for j in collector : # joining all the dictionaries
        twitter.extend(j['twitter'])
        linkedin.extend(j['linkedin'])
        facebook.extend(j['facebook'])
        instagram.extend(j['instagram'])


    # remove any common links that might come


    twitter = list(set(twitter))
    linkedin = list(set(linkedin))
    facebook = list(set(facebook))
    instagram = list(set(instagram))


    scraped_value = {
    'input_url': url, 
    'facebook': facebook,
    'linkedin': linkedin, 
    'twitter': twitter, 
    'instagram': instagram,
    }

    #################################################################
    # COMBINE THE LINKS IN THE TWO DICTIOANRIES

    scraped_value['facebook'].append(ggl_values['facebook'])
    scraped_value['linkedin'].append(ggl_values['linkedin'])
    scraped_value['twitter'].append(ggl_values['twitter'])
    scraped_value['instagram'].append(ggl_values['instagram'])

    output_dict = {
        'facebook': list(set(scraped_value['facebook'])),
        'linkedin': list(set(scraped_value['linkedin'])),
        'twitter': list(set(scraped_value['twitter'])),
        'instagram': list(set(scraped_value['instagram']))
    }

    ################################################################
    # PICK THE BEST LINKS FOR EACH CATEGORY

    for soc in ['facebook','twitter','linkedin','instagram']:

        prev_score = 0
        container = ''

        for n in range (len(output_dict[soc])):
            new_score = fuzz.partial_ratio(output_dict[soc][n],name)
            if new_score > prev_score:
                container = output_dict[soc][n]
                prev_score = new_score

        output_dict[soc] = container


    return output_dict




# function call to test
print(finder('https://www.citroen.co.uk/'))