import argparse
import datetime
import os
import requests
from bs4 import BeautifulSoup

def extract_info(url:str) -> dict:

    information = {}
    responce = requests.get(url)
    soup = BeautifulSoup(responce.text, 'html.parser')
    try:
        description = soup.find('meta',attrs={"name":"description"}).get('content')
        information['description'] = description # problem description
    except:
        print('No description found')
        information['description'] = 'No description found'
        
    try:
        title = soup.find('span', class_='mr-2 text-label-1 dark:text-dark-label-1 text-lg font-medium').text
        information['title'] = title # problem title (set to file name)
    except:
        print('No title found')
        information['title'] = 'No title found'
        
    try: 
        difficulty = soup.find(lambda tag: tag.name == 'div' and
                                'inline-block' in tag.get('class', []) and
                                'rounded-[21px]' in tag.get('class', []) and
                                'bg-opacity-[.15]' in tag.get('class', []) and
                                'px-2.5' in tag.get('class', []) and
                                'py-1' in tag.get('class', []) and
                                'text-xs' in tag.get('class', []) and
                                'font-medium' in tag.get('class', []) and
                                'capitalize' in tag.get('class', []) and
                                'dark:bg-opacity-[.15]' in tag.get('class', [])
                    )
        information['difficulty'] = difficulty.text
    except:
        print('No difficulty found')
        information['difficulty'] = 'No difficulty found'
        
    return information

    
    
def create_file(url) -> None:
    information = extract_info(url)
    date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    file_name = information['title'] + '.py'
    description = information['description']
    description = '\n'.join(line for line in description.splitlines() if line.strip())
    difficulty = information['difficulty']
    title = information['title']
    template = """
# {title}
# {url}
# Date: {date}

# Difficulty: {difficulty}

# {description} 

# my solution
def main(): 
    
    pass

    
# Notes:


# Best solution:
def best():

    pass

if __name__ == '__main__':
    main()
    """.strip()
    content = template.format(title=title, url=url, date=date, difficulty=difficulty, description='# ' + description.replace('\n', '\n# '))
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            f.write(content)
        print('File created: ', file_name)
    else:
        print('File already exists')
    
def main():
    parser = argparse.ArgumentParser(description='Create a file from a leetcode problem url')
    parser.add_argument('url', type=str, help='url of the leetcode problem')
    args = parser.parse_args()
    create_file(args.url)

if __name__ == '__main__':
    main()