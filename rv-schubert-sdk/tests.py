from decimal import Decimal

import pendulum

from .rv_schubert_sdk import RVapi, \
    Transacao1, \
    Transacao3, \
    Transacao5, \
    Recarga
from .test_mockups import Transacao1Mock, Transacao3Mock

from unittest import TestCase


class RVapiTestCase(TestCase):

    def setUp(self):
        self.rv_api = RVapi(homologacao=True)

    def test_get_url_producao(self):
        self.assertEqual(self.rv_api.URL_PRODUCAO, 'https://xml.cellcard.com.br/integracao_xml.php')

    def test_get_url_homologacao(self):
        self.assertEqual(self.rv_api.URL_HOMOLOGACAO, 'https://teste.cellcard.com.br/integracao_xml.php')

    def test_get_versao(self):
        self.assertEqual(self.rv_api.VERSAO, 3.94)

    def test_get_credenciais_homologacao(self):
        self.assertEqual(self.rv_api.CREDENCIAIS, {
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

    def test_set_server_url(self):
        sdk = RVapi()
        self.assertEqual(sdk.SERVER_URL, self.rv_api.URL_PRODUCAO)
        self.assertEqual(sdk.IN_PRODUCTION, True)

        sdk = RVapi(homologacao=True)
        self.assertEqual(sdk.SERVER_URL, self.rv_api.URL_HOMOLOGACAO)
        self.assertEqual(sdk.IN_PRODUCTION, False)

    def test_set_credenciais(self):
        res = self.rv_api.set_credenciais(
            loja="abc",
            nome="def",
            senha="1234"
        )
        self.assertEqual(res.CREDENCIAIS, {
            "loja_primaria": "abc",
            "nome_primario": "def",
            "senha_primaria": "1234"
        })


class Transacao1TestCase(TestCase):

    def setUp(self):
        self.transacao_1 = Transacao1()

    def test_transacao_1_inherit_from_RVapi(self):
        self.assertIsInstance(self.transacao_1, RVapi)

    def test_trasacao_1_execute(self):
        self.assertIsInstance(self.transacao_1.execute(mock=Transacao1Mock().get()), dict)


class Transacao3TestCase(TestCase):

    def setUp(self):
        self.transacao_3 = Transacao3()

    def test_transacao_3_inherit_from_RVapi(self):
        self.assertIsInstance(self.transacao_3, RVapi)

    def test_execute_return_recarga_obj(self):
        self.assertIsInstance(
            self.transacao_3.execute(
                compra=1,
                produto="755",
                mock=Transacao3Mock().get_PAYMENTZ()
            ), Recarga
        )

    def test_execute_PAYMENTEZ_success(self):
        self.transacao_3.execute(
            compra=1,
            produto="775",
            mock=Transacao3Mock().get_PAYMENTZ()
        )


class Transacao5TestCase(TestCase):

    def setUp(self):
        self.transacao_5 = Transacao5()

    def test_transacao_5_inherit_from_RVapi(self):
        self.assertIsInstance(self.transacao_5, RVapi)


class RecargaObjectTestCase(TestCase):

    def test_parse_dict(self):
        recarga = Recarga()
        recarga.parse_dict(Transacao3Mock().get_PAYMENTZ_as_dict())
        self.assertIsInstance(recarga, Recarga)
        self.assertEqual(recarga.VERSAO, 3.94)
        self.assertEqual(recarga.COD_TRANSACAO, 3)
        self.assertEqual(recarga.REENVIO, 0)
        self.assertEqual(recarga.CODIGO, 2988)
        self.assertEqual(recarga.COD_ONLINE, '1686085508')
        self.assertEqual(recarga.PRODUTO, '771')
        self.assertEqual(recarga.PRECO, Decimal('4.83'))
        self.assertEqual(recarga.FACE, Decimal('5.00'))
        self.assertEqual(recarga.VENCIMENTO, pendulum.datetime(year=2019, month=4, day=8))
        self.assertEqual(recarga.PAGO, 0)
        self.assertEqual(recarga.PIN, '35490TESTE897578')
        self.assertEqual(recarga.LOTE, '109')
        self.assertEqual(recarga.SERIE, '121602')
        self.assertEqual(recarga.MENSAGEM, 'Credito para jogos e aplicativos compativeis com PAYMENTEZ  na internet. Clique emADQUIRIR MOEDAS    ou  similar esiga instrucoes na tela.        Mais info em www.paymentez.com')
        self.assertEqual(recarga.DATA_RV, pendulum.datetime(year=2019, month=3, day=13, hour=18, minute=13, second=51))
        self.assertEqual(recarga.DDD, None)
        self.assertEqual(recarga.FONE, None)
        self.assertEqual(recarga.CODIGO_ASSINANTE, None)
        self.assertEqual(recarga.NSU, None)
        self.assertEqual(recarga.POSSUI_BOLETO, None)
