from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def codigos_municipios_ordenados():
    #TODO: Colocar os orgaos e id / funcao e id
    url = "https://api-dados-abertos.tce.ce.gov.br/municipios"
    response = requests.get(url)
    data = response.json()
    data_dict = {}
    for municipio in data['data']:
        data_dict[municipio['codigo_municipio']] = municipio['nome_municipio']

    data_dict_order = sorted(data_dict.items())
    return data_dict_order


@app.get("/despesas_economicas/{id_municipio}/{ano}")
def despesas_economica(id_municipio,ano):
    url = 'https://api-dados-abertos.tce.ce.gov.br/despesa_categoria_economica?codigo_municipio={0}&exercicio_orcamento={1}00'.format(id_municipio,ano)
    response = requests.get(url)
    data = response.json()
    despesas_list = []
    despesas_dict = {}
    valor = 0

    for despesas in data['data']:
        despesas_list.append({'descricao':despesas["nome_elemento_despesa"],'valor_previsto':despesas["valor_total_fixado"]})

        if despesas["nome_elemento_despesa"] not in despesas_dict.keys():
            despesas_dict[despesas["nome_elemento_despesa"].strip(" ")] = 0
    

    #despesas_list_order = sorted(despesas_list, key=lambda dicionario:dicionario['valor_previsto'])

    return despesas_dict


#TODO: colocar porcentagem de cada categoria de nota e limitar os anos de pesquisa
@app.get("/notas_fiscais/{id_municipio}/{ano}")
def notas_fiscais_categoria(id_municipio,ano):
    url = 'https://api-dados-abertos.tce.ce.gov.br/notas_fiscais?codigo_municipio={0}&exercicio_orcamento={1}00&quantidade=100&deslocamento=0'.format(id_municipio,ano)
    response = requests.get(url)
    data = response.json()
    notas = {'quantidade total':data['data']['length'],'tipo da nota':{'serviço':0,'mercadoria':1,'serviço avulsa':0,'mercadoria avulsa':0,
                                                                       'mercadoria produtor':0,'mercadoria e serviço':0},'notas':[]}

    for nota in data['data']['data']:
        notas['notas'].append(nota)
        if nota['tipo_nota_fiscal'] == "M":
            notas['tipo da nota']['mercadoria'] +=1
        elif nota['tipo_nota_fiscal'] == "S":
            notas['tipo da nota']['serviço'] +=1
        elif nota['tipo_nota_fiscal'] == "A":
            notas['tipo da nota']['mercadoria avulsa'] +=1
        elif nota['tipo_nota_fiscal'] == "P":
            notas['tipo da nota']['mercadoria produtor'] +=1
        elif nota['tipo_nota_fiscal'] == "X":
            notas['tipo da nota']['mercadoria e serviço'] +=1
        elif nota['tipo_nota_fiscal'] == "V":
            notas['tipo da nota']['serviço avulsa'] +=1

    return notas



#TODO: valores empenhados,liquidados e pagos nas despesas