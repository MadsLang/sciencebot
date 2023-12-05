import re
import pandas as pd

df = pd.read_csv('data/scopus.csv')


def parse_authors(author_str):
    authors = author_str.split(';')
    authors = [re.findall('^\w+', author.strip())[0] for author in authors]
    if len(authors) > 2: 
        return authors[0] + ' et al. '
    else:
        return ' & '.join(authors)

def parse_llm_response(response):
    answer = response['answer']

    answer_content = answer.split('SOURCES')[0]
    sources = re.findall('SOURCES:(.+)', answer, re.MULTILINE)[0]

    try:
        sources_md = ''
        for source in sources.split(','):
            eid = source.strip()
            authors = parse_authors(df[df['EID'] == eid]['Authors'].fillna('').values[0])
            link = 'https://doi.org/' + df[df['EID'] == eid]['DOI'].fillna('').values[0]
            year = str(df[df['EID'] == eid]['Year'].values[0])
            sources_md = sources_md + f' <a href="{link}">{authors} {year}</a> <br>'

        return answer_content + '<br> <br> Sources: <br>' + sources_md

    except:
        return answer_content



