from .rv_schubert_sdk import RVapi

from unittest import TestCase


class RVapiTestCase(TestCase):

    def setUp(self):
        self.rv_api = RVapi()

    def test_get_url_producao(self):
        self.assertEqual(self.rv_api.URL_PRODUCAO, 'https://xml.cellcard.com.br/integracao_xml.php')

    def test_get_url_homologacao(self):
        self.assertEqual(self.rv_api.URL_HOMOLOGACAO, 'https://teste.cellcard.com.br/integracao_xml.php')

    def test_get_versao(self):
        self.assertEqual(self.rv_api.VERSAO, 3.94)

    def test_get_credenciais_homologacao(self):
        self.assertEqual(self.rv_api.CREDENCIAIS_HOMOLOGACAO, {
            "loja_primaria": "teste",
            "nome_primario": "teste",
            "senha_primaria": "teste"
        })

    def test_convert_xml_to_dict(self):
        xml = """
            <?xml version="1.0" encoding="ISO-8859-1" ?>
            <cellcard>
                <versao>3.94</versao>
                <codigoTransacao>1</codigoTransacao>
                <loja>136</loja>
                <operadoras>
                    <qtdOperadoras>27</qtdOperadoras>
                    <operadora>
                        <codigoOperadora>M5</codigoOperadora>
                        <estadosAtuantes>
                            <qtdEstadosOperadora>27</qtdEstadosOperadora>
                            <estadoOperadora>AC</estadoOperadora>
                            <estadoOperadora>AL</estadoOperadora>
                        </estadosAtuantes>
                    </operadora>
                    <operadora>
                        <codigoOperadora>SC</codigoOperadora>
                        <estadosAtuantes>
                            <qtdEstadosOperadora>27</qtdEstadosOperadora>
                            <estadoOperadora>AC</estadoOperadora>
                            <estadoOperadora>AL</estadoOperadora>
                        </estadosAtuantes>
                    </operadora>
                </operadoras>
            </cellcard>
        """
        self.assertIsInstance(self.rv_api.convert_xml_to_dict(xml), dict)
        print(self.rv_api.convert_xml_to_dict(xml))
