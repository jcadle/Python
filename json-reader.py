import json
import pandas as pd
import datetime
import pathlib
# file definitions
directory = r"C:\Users\cadlej\OneDrive - Reed Elsevier Group ICO Reed Elsevier Inc\Documents\Jupyter Notebooks\Plymouth\OneDrive_1_6-14-2024"
authorLookup = r"C:\Users\cadlej\OneDrive - Reed Elsevier Group ICO Reed Elsevier Inc\Documents\Jupyter Notebooks\Plymouth\Plymouth Person ORCIDs.xlsx"

# initialize fields for new excel file
fields = ['pureid', 'uuid', 'title', 'abstract', 'keywords', 'supplemental_files', 'validated', 'pages', 'issn', 'isbn', 'language', 'doi', 'source_publication', 'visibility', 'managing_org', 'org_unit', 'versionType',
                  'publication_date', 'embargo_date', 'volnum', 'issnum', 'fulltext_url', 'fulltext_all', 'links', 'ext_ids', 'distribution_license', 'document_type', 'orcid', 'raw_orcid']
for i in range(1, 31):
    fields.extend(('author{}_fname'.format(i), 'author{}_mname'.format(i), 'author{}_lname'.format(i), 'author{}_suffix'.format(i),  'author{}_email'.format(i), 'author{}_institution'.format(i), 'author{}_is_corporate'.format(i)))



# Function to format Orcid field
def formatOrcid(orcid, name):
    orcList = []
    for n, person in enumerate(name):
        if len(person) > 1:
            orcItem = str( '<li>' + person + ': <a href="https://orcid.org/' + orcid[n] + '" target="_blank" title="ORCiD for ' + person + '">' + orcid[n] + '</a></li>')
            orcList.extend(orcItem)
    if len(orcList) > 0:
        return '<ul>' + ''.join(orcList) + '</ul>'
    else:
        return ""
#read json files and pull data
for file in pathlib.Path(directory).iterdir():
    if file.suffix == '.json':
        print(file.name)
        filename = file.name + ".xlsx"
        #initialize new excel file
        results = pd.DataFrame(columns=fields)
        with open(file, mode="r", encoding='utf-8') as read_file:
            data = json.load(read_file)
            for i, article in enumerate(data['items']):
                # Get Author information
                authorUuidList = []
                for j, author in enumerate(article['personAssociations'], start=1):
                    try: results.loc[i,'author{}_fname'.format(j)] = author['name']['firstName']
                    except: results.loc[i,'author{}_fname'.format(j)] = "N/A"
                    try: results.loc[i,'author{}_lname'.format(j)] = author['name']['lastName']
                    except: results.loc[i,'author{}_fname'.format(j)] = "N/A"
                    try: results.loc[i, 'author{}_institution'.format(j)] = author['organisationalUnits'][0]['name']['text'][0]['value']
                    except: pass
                    try: authorUuidList.append(author['person']['uuid'])
                    except: pass
                # ORCID block
                try: 
                    with open(authorLookup, mode="rb") as f:
                        lookup = pd.read_excel(f)
                        myOrcid = []
                        myOrcidName = []
                        for uuid in authorUuidList:
                            myOrcid.append(''.join(list(lookup.loc[lookup["UUID"] == uuid, "ORCID"])))
                            myOrcidName.append(''.join(list(lookup.loc[lookup["UUID"] == uuid, "Name"])))
                        #print(myOrcid, myOrcidName)
                        results.loc[i, 'raw_orcid'] = myOrcid
                        results.loc[i, 'orcid'] = formatOrcid(myOrcid, myOrcidName)
                except: 
                    results.loc[i, 'orcid'] = "No ORCIDs Found"
                # Pure ID and UUID
                results.loc[i, 'pureid'] = article['pureId']
                results.loc[i, 'uuid'] = article['uuid']
                #Title field is stored in different places depending on the json file type
                try: results.loc[i, 'title'] = article['title']['text'][0]['value']
                except: pass
                try: results.loc[i, 'title'] = article['title']['value']
                except: pass
                try: results.loc[i, 'title'] = article['title']
                except: pass
                # Validated field
                try: results.loc[i, 'validated'] = article['workflow']['value']['text'][0]['value']
                except: pass
                # Keywords
                try: results.loc[i, 'keywords'] = article['keywordGroups'][0]['keywordContainers'][0]['freeKeywords'][0]['freeKeywords']
                except: keywords="No Keywords Found"
                # full-text file(s)
                fileList = []
                try:
                    results.loc[i, 'fulltext_url'] = article['electronicVersions'][0]['file']['fileURL']
                    for file in article['electronicVersions']:
                        fileList.append(file['file']['url'])
                    results.loc[i, 'fulltext_all'] = ', '.join(fileList)
                except: pass
                try:
                    results.loc[i, 'fulltext_url'] = article['documents'][0]['url']
                    for file in article['documents']:
                        fileList.append(file['url'])
                    results.loc[i, 'fulltext_all'] = ', '.join(fileList)
                except: pass
                # Abstract
                try:
                    results.loc[i, 'abstract'] = article['abstract']['text'][0]['value']
                except: pass
                try:
                    results.loc[i, 'abstract'] = article['descriptions'][0]['value']['text'][0]['value']
                except: pass
                # Document Type
                try:
                    results.loc[i, 'document_type'] = article['documents'][0]['documentType']['term']['text'][0]['value']
                except: results.loc[i, 'document_type'] = article['type']['term']['text'][0]['value']
                #try: 
                    #results.loc[i, 'document_type'] = article['type']['term']['text'][0]['value']
                #except: pass
                # Publication Date
                try:
                    year = article['publicationDate']['year']
                    try: month = article['publicationDate']['month']
                    except: month = 1
                    try: day = article['publicationDate']['day']
                    except: day = 1
                except: pass
                try:
                    year = article['publicationStatuses'][0]['publicationDate']['year']
                    try: month = article['publicationStatuses'][0]['publicationDate']['month']
                    except: month = 1
                    try: day = article['publicationStatuses'][0]['publicationDate']['day']
                    except: day = 1
                except: pass
                try:
                    year = article['awardDate']['year']
                    try: month = article['awardDate']['month']
                    except: month = 1
                    try: day = article['awardDate']['day']
                    except: day = 1
                except: pass
                try:
                    date = datetime.datetime(year,month,day)
                    results.loc[i, 'publication_date'] = date 
                except: pass
                # else: results.loc[i, 'publication_date'] = "No Dates Found"
                # Additional Files
                try:
                    addFileList = []
                    for link in article['additionalFiles']:
                        addFileList.append(link['file']['fileURL'])
                    results.loc[i, 'supplemental_files'] = addFileList
                except: pass
                # Visibility
                try: results.loc[i, 'visibility'] = article['visibility']['value']['text'][0]['value']
                except: pass
                # Managing Org
                try: results.loc[i, 'managing_org'] = article['managingOrganisationalUnit']['name']['text'][0]['value']
                except: pass
                # Org Unit
                try: results.loc[i, 'org_unit'] = article['organisationalUnits'][0]['name']['text'][0]['value']
                except: results.loc[i, 'org_unit'] = "No Org Unit Found"
                # Pages
                try: results.loc[i, 'pages'] = article['pages']
                except: pass
                # DOI
                try: results.loc[i, 'doi'] = article['doi']
                except: pass
                try: results.loc[i, 'doi'] = article['electronicVersions'][0]['doi']
                except: pass
                # Source Publication
                try: results.loc[i, 'source_publication'] = article['journalAssociation']['title']['value']
                except: pass
                try: results.loc[i, 'source_publication'] = article['hostPublicationTitle']['value']
                except: pass
                # Volume
                try: results.loc[i, 'volnum'] = article['volume']
                except: pass
                # Issue
                try: results.loc[i, 'issnum'] = article['journalNumber']
                except: pass
                # ISSN
                try: results.loc[i, 'issn'] = article['journalAssociation']['issn']['value']
                except: pass
                # ISBN
                try: results.loc[i, 'isbn'] = article['isbns'][0]
                except: pass
                # Language
                try: results.loc[i, 'language'] = article['language']['term']['text'][0]['value']
                except: pass
                # Embargo Date
                try: results.loc[i, 'embargo_date'] = article['electronicVersions'][0]['embargoPeriod']['endDate']
                except: pass
                try: results.loc[i, 'embargo_date'] = article['documents'][0]['embargoDate']
                except: pass
                # Creative Commons
                try: results.loc[i, 'distribution_license'] = article['electronicVersions'][0]['licenseType']['term']['text'][0]['value']
                # try: results.loc[i, 'distribution_license'] = article['electronicVersions'][-1]['pureId']['text'][0]['value']['term']['licenseType']
                except: pass
                try:
                    try: results.loc[i, 'distribution_license'] = article['documents'][0]['documentLicense']['term']['text'][0]['value']
                    except: results.loc[i, 'distribution_license'] = article['documentLicense']['term']['text'][0]['value']
                except: pass
                # Links
                try: 
                    linksList = []
                    for link in article['links']:
                        linksList.append(link['url'])
                    results.loc[i, 'links'] = linksList
                except: pass
                # External IDs
                try:
                    results.loc[i, 'ext_ids'] = article['info']['additionalExternalIds']
                except: pass
            # write to file    
            results.to_excel(filename, encoding="utf-8", index=False)
