# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 17:03:24 2016

@author: ap4409
"""

# ----------------------------------------------------------------------------
# HEADERS
# ----------------------------------------------------------------------------

import requests
import json
from helpTool import printToCSV

# ----------------------------------------------------------------------------
# INPUTS
# ----------------------------------------------------------------------------

MY_API_KEY = '90f27a834604bb6313c5b3d68811a379';
count = 200; # results returned
search_terms_list = ['title(fibrinolysis)','tak(clot lysis)','thrombolysis+mathematical','fibrinolysis+modeling'];

#Other useful search macros
# abs() for abstract
# tak() for abstract, title and keywords
# authors()

for search_terms in search_terms_list:

    print('Running through ' + search_terms)

# ----------------------------------------------------------------------------
# ARTICLE SEARCH/ABSTRACT RETRIEVAL
# ----------------------------------------------------------------------------

    # API inputs
    search_url = 'http://api.elsevier.com/content/search/scidir?count='+ str(count) + '&query=' + search_terms;
    headers = {'Accept':'application/json', 'X-ELS-APIKey': MY_API_KEY}
    
    # API request
    page_request = requests.get(search_url, headers=headers)
    print(page_request.status_code)
    
    # Unpack json
    page = json.loads(page_request.content.decode("utf-8"))
    store = page['search-results']['entry'];
    
    # Cycle through each paper, retrieve information
    it = -1;
    title = []; authors = []; date = []; link = []; eid = []; abstract = [];
    for paper in store:
        
        try: 
            
            it += 1;
            titleCur   = paper['dc:title'];
            authorsCur = paper['authors'];
            dateCur    = paper['prism:coverDisplayDate']
            linkCur    = paper['link'][0]['@href'];
            eidCur     = paper['eid']
                    
            title.append(titleCur)
            authors.append(authorsCur)
            date.append(dateCur)
            link.append(linkCur)
            eid.append(eidCur) 
            
            # Retrieve abstract
            abstract_request = requests.get(linkCur, headers=headers);
            abstractjson = json.loads(abstract_request.content.decode("utf-8"))
            
            try:            
                abstract.append(abstractjson['full-text-retrieval-response']['coredata']['dc:description'])
            
            except:
                abstract.append('N/A');
             
        except:
            
            # Specify where it failed
            print('Failed at paper # ' + str(it))
            
            continue;
            
    # ----------------------------------------------------------------------------
    # SAVING RESULTS
    # ----------------------------------------------------------------------------
    
    printToCSV('science_direct'+search_terms+'.csv',['title','authors','date','link','eid','abstract'],
               title,authors,date,link,eid,abstract)
               
               
               
               
               


