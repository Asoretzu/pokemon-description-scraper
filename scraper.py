"""Web Scraper for all the Pokemon descriptions."""

import requests
import lxml.html as html


HOME_URL = 'https://pokemondb.net/pokedex/all'
XPATH_LINK = '//div[@class="grid-row"]/div/div[@class="resp-scroll"]/table/tbody/tr/td[@class="cell-name"]/a/@href'
XPATH_DESC = '//div[@class="resp-scroll"]/table/tbody/tr/td[@class="cell-med-text"]/text()'
XPATH_NAME = '//main/h1/text()'


def parse_description(link):
    """Parsing function."""
    try:
        link = 'https://pokemondb.net' + link
        response = requests.get(link)

        if response.status_code == 200:
            page = response.content.decode('utf-8')
            parsed = html.fromstring(page)

            try:
                name = parsed.xpath(XPATH_NAME)
                description = parsed.xpath(XPATH_DESC)[0]
                description = description.replace('\"', '')
            except IndexError:
                return
            
            return name, description

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    """Main function"""
    with open("raw_descriptions.txt", mode='w') as f:
        try:
            response = requests.get(HOME_URL)

            if response.status_code == 200:
                home = response.content.decode('utf-8')
                parsed = html.fromstring(home)
                links_pokemon = parsed.xpath(XPATH_LINK)

                for link in links_pokemon:
                    info = parse_description(link)

                    try:
                        print(''.join(map(str, info[0])))
                        
                        f.write(''.join(map(str, info[0])))
                        f.write(', ')
                        f.write(info[1])
                        f.write('\n')
                    
                    except TypeError:
                        f.write('\n')

            else:
                raise ValueError(f'Error: {response.status_code}')
        except ValueError as ve:
            print(ve)


def parse_cleaner():
    with open('clean_descriptions.txt', mode='w') as r:
        lines_seen = set()
        with open('raw_descriptions.txt', mode='r') as f:
            for line in f:
                if line not in lines_seen:
                    r.write(line)
                    lines_seen.add(line)


def main():
    print('Starting scraping.')
    parse_home()
    print('Starting cleaning.')
    parse_cleaner()
    print('Finish scraping.')


if __name__ == "__main__":
    main()