import cnabssdk.clients
import cnabssdk.common.base_entry;
import cnabssdk.deals.entries;

def get_list(keyworkds = "", status = "", year = "", catalog = "", orgname = ""):
    url = "products/openapi/deals"
    params = {
        "keywords": keyworkds,
        "status": status,
        "year": year,
        "catalog": catalog,
        "orgname": orgname
        }
    data = cnabssdk.clients.cnabsclient().get(url, params)
    results = []
    for d in data:
        dlist = cnabssdk.deals.entries.deal_list_entry()
        dlist.__dict__.update(d.__dict__)
        results.append(dlist)
    
    return results

def get_info(dealIdOrName):
    url = "products/openapi/deals/" + dealIdOrName
    data = cnabssdk.clients.cnabsclient().get(url, {})
    deal = cnabssdk.deals.entries.deal_info_entry()
    if(data != None):
        deal.__dict__.update(data.__dict__)
    return (deal)

