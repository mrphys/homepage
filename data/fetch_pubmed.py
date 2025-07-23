import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time

def fetch_pubmed_ids(author, retmax=200):
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    params = {
        'db': 'pubmed',
        'term': f'{author}[Author]',
        'retmax': retmax,
        'retmode': 'xml'
    }
    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)
    ids = [id_elem.text for id_elem in root.findall('./IdList/Id')]
    return ids

def fetch_pubmed_records(id_list):
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    if not id_list:
        return b''  # return empty bytes if no IDs
    ids = ','.join(id_list)
    params = {
        'db': 'pubmed',
        'id': ids,
        'retmode': 'xml'
    }
    response = requests.get(url, params=params)
    return response.content

def parse_pubmed_xml(xml_data):
    if not xml_data:
        return []
    root = ET.fromstring(xml_data)
    records = []
    for article in root.findall('.//PubmedArticle'):
        try:
            article_title = article.findtext('.//ArticleTitle')
            journal = article.findtext('.//Journal/Title')

            if len(article_title) < 4:
                article_title = pd.NA  # you used np.nan, but pandas NA is cleaner in newer versions

            authors = []
            affiliations = set()

            for author in article.findall('.//AuthorList/Author'):
                last = author.findtext('LastName')
                fore = author.findtext('ForeName')
                if last and fore:
                    authors.append(f"{last} {fore[0]}.")
                elif last:
                    authors.append(last)

                # Affiliation (can be multiple)
                aff_list = author.findall('.//AffiliationInfo/Affiliation')
                for aff in aff_list:
                    if aff is not None and aff.text:
                        affiliations.add(aff.text.strip())

            authors = ', '.join(authors)
            affiliation_str = '; '.join(affiliations) if affiliations else None

            pub_date_elem = article.find('.//Journal/JournalIssue/PubDate')
            pub_date_str = None
            year = None
            if pub_date_elem is not None:
                year = pub_date_elem.findtext('Year')
                medline_date = pub_date_elem.findtext('MedlineDate')
                month = pub_date_elem.findtext('Month')
                day = pub_date_elem.findtext('Day')
                if year:
                    pub_date_str = year
                    if month:
                        pub_date_str += f"-{month}"
                    if day:
                        pub_date_str += f"-{day}"
                elif medline_date:
                    pub_date_str = medline_date

            doi = None
            for article_id in article.findall('.//ArticleIdList/ArticleId'):
                if article_id.attrib.get('IdType') == 'doi':
                    doi = article_id.text
                    break

            records.append({
                'Title': article_title,
                'Journal': journal,
                'Authors': authors,
                'Affiliations': affiliation_str,
                'Year': year,
                'DOI': doi,
                'DocumentType': 'Article',
                'PublicationDate': pub_date_str
            })
        except Exception:
            continue

    # Convert PublicationDate strings to pandas datetime, coercing errors
    for r in records:
        date_str = r['PublicationDate']
        if date_str:
            r['PublicationDate'] = pd.to_datetime(date_str, errors='coerce')
        else:
            r['PublicationDate'] = pd.NaT
    return records



# List of authors to process
authors_list = [
    "Vivek Muthurangu",
    "Jennifer Steeden",
    "Daniel Knight",
    "Michael Quail"
]

# all_authors = [
#     "Yao",
#     "Muthurangu",
#     "Steeden",
#     "Knight",
#     'Quail',
#     'Jiang',
#     'Yong',
#     'Wrobel',
#     'Pascale',
#     'Montalt',
#     'Jaubert',
#     'Baker',
#     'Raman',
#     'Campbell'
# ]

all_records = []

for author in authors_list:
    print(f"Processing author: {author}")
    ids = fetch_pubmed_ids(author, retmax=200)
    xml_data = fetch_pubmed_records(ids)
    records = parse_pubmed_xml(xml_data)
    all_records.extend(records)
    time.sleep(0.5)  # polite pause to avoid hitting API limits

# Convert all records to a DataFrame



df = pd.DataFrame(all_records).drop_duplicates('Title').sort_values('PublicationDate', ascending=False)
# Define regex pattern for affiliation filtering
affil_pattern = r'(?i)\b(UCL|University College London|Great Ormond Street|Royal Free|Cardiovascular Science)\b'

# Keep only rows with matching affiliations
df = df[df['Affiliations'].astype(str).str.contains(affil_pattern, na=False)]

df.to_json('data/pubs.json', orient='records')