import requests

def busqueda_producto(producto):
    
    headers = {
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'accept': 'application/json',
    'sec-ch-ua-mobile': '?0'
    }

    params = {
        '_q': '{}'.format(producto),
        'map': 'ft',
        '__pickRuntime': 'appsEtag,blocks,blocksTree,components,contentMap,extensions,messages,page,pages,query,queryData,route,runtimeMeta,settings'
    }

    response = requests.get('https://www.disco.com.uy/{}'.format(producto), params=params, headers=headers)
    print(response.json())
