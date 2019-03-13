import json

import requests
import xmltodict


class RVapi:
    URL_PRODUCAO = "https://xml.cellcard.com.br/integracao_xml.php"
    URL_HOMOLOGACAO = "https://teste.cellcard.com.br/integracao_xml.php"
    SERVER_URL = None
    IN_PRODUCTION = None
    VERSAO = 3.94
    CREDENCIAIS = {
        "loja_primaria": "teste",
        "nome_primario": "teste",
        "senha_primaria": "teste"
    }

    def __init__(self, homologacao=False):
        if homologacao is False:
            self.SERVER_URL = self.URL_PRODUCAO
            self.IN_PRODUCTION = True
        else:
            self.SERVER_URL = self.URL_HOMOLOGACAO
            self.IN_PRODUCTION = False

    def convert_xml_to_dict(self, xml):
        return json.loads(json.dumps(xmltodict.parse(xml.split("?>")[1], process_namespaces=True)))

    def set_credenciais(self, loja: str, nome: str, senha: str):
        self.CREDENCIAIS = {
            "loja_primaria": loja,
            "nome_primario": nome,
            "senha_primaria": senha
        }
        return self

    def doPOST(self, postData):
        # todo: add try except
        response = requests.request(
            "POST",
            self.SERVER_URL,
            data=postData
        )
        return response.text
