import cnabssdk.clients
import cnabssdk.common.base_entry;
import cnabssdk.deals.entries;

def get_list(keywords="", beginDate="", endDate="", dealStatus="", year="", catalog="", orgName=""):
    url = "products/openapi/securities"
    params = {
        "keywords": keywords,
        "begin": beginDate,
        "end": endDate,
        "status": dealStatus,
        "year": year,
        "catalog": catalog,
        "orgName": orgName
    }
    return cnabssdk.clients.cnabsclient().get(url, params)

def get_detail(securityCodeOrId):
    url = "products/openapi/securities/" + securityCodeOrId
    return cnabssdk.clients.cnabsclient().get(url, {})