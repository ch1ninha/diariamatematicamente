def db_mapear_numeros(dicionario):
    """
    Input: Dicionario para mapear, é preciso ter uma chave que tenha dois atributos 'num1' e 'num2'
           representando cada numero daquela tentativa.
           
    Output: Uma lista com a (<n_da_tentativa>, <numero_1>, <numero_2>, <acertou?>)"""
    def inner_db_map_create(key):
        tentativa = dicionario[key]['tentativa']
        resultado = dicionario[key]['resultado']
        acertou = False
        if tentativa == resultado:
            acertou = True
        return (int(key), int(dicionario[key].get('num1')),
                int(dicionario[key].get('num2')), acertou)

    return list(map(inner_db_map_create,dicionario))