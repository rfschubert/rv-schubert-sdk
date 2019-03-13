import json

import xmltodict


class RVapi:
    URL_PRODUCAO = "https://xml.cellcard.com.br/integracao_xml.php"
    URL_HOMOLOGACAO = "https://teste.cellcard.com.br/integracao_xml.php"
    VERSAO = 3.94
    CREDENCIAIS_HOMOLOGACAO = {
        "loja_primaria": "teste",
        "nome_primario": "teste",
        "senha_primaria": "teste"
    }

    def convert_xml_to_dict(self, xml):
        return json.loads(json.dumps(xmltodict.parse(xml.split("?>")[1], process_namespaces=True)))
