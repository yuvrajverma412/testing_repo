# pip3 install pubchempy
import pubchempy as pcp

def freeTextSearchPubChem(text):
    """
    Free text search on PubChem for a given search term 
    and returns matching drug and its synonyms joined
    Args:
        text: text or drug name to search
    Returns: 
        drug_name: matching drug name
        drug_synonyms : synonyms joined using '|' symbol of matching drug
    """

    drug_name = text.lower()
    syns = pcp.get_synonyms(text, 'name')
    if len(syns)>0:
        syns = syns[0]['Synonym']
        syns = list(map(lambda x: x.lower(),sorted(list(set(syns)))))
        if drug_name in syns:
            syns.remove(drug_name)
    elif len(syns)==0:
        syns = [] 
        drug_name = ''  
    drug_synonyms = '|'.join(syns)
    return drug_name, drug_synonyms
