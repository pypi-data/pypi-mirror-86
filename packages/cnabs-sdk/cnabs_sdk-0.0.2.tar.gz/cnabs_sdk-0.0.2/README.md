# CNABS Openapi Python Sdk

Libs:
- Request: pip install requests
- 打包工具: python -m pip install setuptools wheel twine
- 打包命令： python setup.py sdist bdist_wheel
- 上传: python3 -m twine upload dist/*

`
import cnabssdk.clients
import cnabssdk.deals.deal_api
import cnabssdk.securities.security_api


if __name__ == '__main__':
    cnabssdk.init("20200915-20210915--xx-NQ4g1Wd5CajhkjBk8dXSMAk")
    deals = cnabssdk.deals.deal_api.get_list('建元')
    print('Count: ' + str(len(deals)))
    deal = cnabssdk.deals.deal_api.get_info(deals[0].id)
    print(deal.name)

    securitylist = cnabssdk.securities.security_api.get_list(year= 2020)
    print('Security Count: ' + str(len(securitylist)))
    sec = cnabssdk.securities.security_api.get_detail(securitylist[0].id)
    print(sec.short_name)
`