from decimal import Decimal

import pendulum

from rv_schubert_sdk import RVapi, \
    Transacao1, \
    Transacao3, \
    Transacao5, \
    Recarga, ErroRV, Produto, Operadora
from .test_mockups import Transacao1Mock, Transacao3Mock, ErrosMock, Transacao5Mock

from rv_schubert_sdk import FoneIncompletoInvalido, LimiteCreditoInsuficiente, EstoqueInsuficiente, \
    TelefoneNaoAutorizado, SenhaInvalida, MaximoNumeroConexoesAtingida, SistemaEmManutencao, \
    OperadoraProdutoNaoEncontrado, CodigoInvalido, ValorInvalido, Timeout, CompraExpirada, CompraInexistente, \
    UsuarioLojaNaoEncontrado, ParametrosInsuficientes, CompraJaConfirmada, BoletoNaoEncontrado, \
    ParametrosNaoEnviadosViaPOST, CodigoTransacaoNaoInformado, VersaoNaoInformada, UsuarioSemNivelDeAcesso, \
    CobrancaAindaNaoVisualizada, TransacaoNaoPermitida

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

    def test_transacao_5_oi_phone_credit_success(self):
        result = self.transacao_5.execute(
            compra="2990",
            produto="1021",
            ddd="47",
            fone="99999999",
            mock=Transacao5Mock().get_recarga_oi_20()
        )

        self.assertIsInstance(result, Recarga)
        self.assertEqual(result.VERSAO, 3.94)
        self.assertEqual(result.COD_TRANSACAO, 5)
        self.assertEqual(result.REENVIO, 0)
        self.assertEqual(result.CODIGO, 2990)
        self.assertEqual(result.COD_ONLINE, '1686085733')
        self.assertEqual(result.PRODUTO, '1021')
        self.assertEqual(result.PRECO, Decimal("48.25"))
        self.assertEqual(result.FACE, Decimal("50.00"))
        self.assertEqual(result.VENCIMENTO, pendulum.datetime(year=2019, month=4, day=8).date())
        self.assertEqual(result.PAGO, 0)
        self.assertEqual(result.DDD, '47')
        self.assertEqual(result.FONE, '99999999')
        self.assertEqual(result.MENSAGEM,
                         'FACA UMA RECARGADA OI DE R$20 E GANHE 1 GB POR 7 DIAS.INTERNET+VOZ+LIGACOES+TUDO+JUNTO+PARA VOCEUSAR, BASTA RECARREGAR. DIA.INTERNET+VOZ+LIGACOES+TUDO+JUNTO+PARA VOCE')
        self.assertEqual(result.NSU, '100607')
        self.assertEqual(result.DATA_RV, pendulum.datetime(year=2019, month=3, day=19, hour=14, minute=5, second=23))


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
        self.assertEqual(recarga.VENCIMENTO, pendulum.datetime(year=2019, month=4, day=8).date())
        self.assertEqual(recarga.PAGO, 0)
        self.assertEqual(recarga.PIN, '35490TESTE897578')
        self.assertEqual(recarga.LOTE, '109')
        self.assertEqual(recarga.SERIE, '121602')
        self.assertEqual(recarga.MENSAGEM,
                         'Credito para jogos e aplicativos compativeis com PAYMENTEZ  na internet. Clique emADQUIRIR MOEDAS    ou  similar esiga instrucoes na tela.        Mais info em www.paymentez.com')
        self.assertEqual(recarga.DATA_RV, pendulum.datetime(year=2019, month=3, day=13, hour=18, minute=13, second=51))
        self.assertEqual(recarga.DDD, None)
        self.assertEqual(recarga.FONE, None)
        self.assertEqual(recarga.CODIGO_ASSINANTE, None)
        self.assertEqual(recarga.NSU, None)
        self.assertEqual(recarga.POSSUI_BOLETO, None)


class ProdutoObjectTestCase(TestCase):

    def test_build_produto_from_dict(self):
        produto = Produto().build_from_dict(Transacao1Mock().get_produto_dict())

        self.assertEqual(produto.CODIGO_PRODUTO, Transacao1Mock().get_produto_dict()['codigoProduto'])
        self.assertEqual(produto.NOME_PRODUTO, Transacao1Mock().get_produto_dict()['nomeProduto'])
        self.assertEqual(produto.PRECO_COMPRA_PRODUTO, Decimal(Transacao1Mock().get_produto_dict()['precocompraProduto']))
        self.assertEqual(produto.PRECO_VENDA_PRODUTO, Decimal(Transacao1Mock().get_produto_dict()['precovendaProduto']))
        self.assertEqual(produto.VALIDADE_PRODUTO, Transacao1Mock().get_produto_dict()['validadeProduto'])
        self.assertEqual(produto.MODELO_RECARGA, Transacao1Mock().get_produto_dict()['modeloRecarga'])
        self.assertEqual(produto.VALOR_MINIMO_PRODUTO, Decimal(Transacao1Mock().get_produto_dict()['valorMinimoProduto']))
        self.assertEqual(produto.VALOR_MAXIMO_PRODUTO, Decimal(Transacao1Mock().get_produto_dict()['valorMaximoProduto']))
        self.assertEqual(produto.VALOR_INCREMENTO_PRODUTO, Decimal(Transacao1Mock().get_produto_dict()['valorIncrementoProduto']))
        self.assertEqual(produto.ULTIMA_ATUALIZACAO_PRODUTO, pendulum.parse(Transacao1Mock().get_produto_dict()['ultima_atualizacaoProduto']))
        self.assertEqual(produto.PRECO_VARIAVEL_PRODUTO, Decimal(Transacao1Mock().get_produto_dict()['precoVariavelProduto']))
        self.assertEqual(produto.ESTADOS_PRODUTO_PIN, Transacao1Mock().get_produto_dict()['estadosProdutoPin']['estadoProduto'])


class OperadoraObjectTestCase(TestCase):

    def test_build_operadora_from_dict(self):
        operadora = Operadora().build_from_dict(Transacao1Mock().get_operadora_dict())

        self.assertEqual(operadora.CODIGO_OPERADORA, Transacao1Mock().get_operadora_dict()['codigoOperadora'])
        self.assertEqual(operadora.NOME_OPERADORA, Transacao1Mock().get_operadora_dict()['nomeOperadora'])
        self.assertEqual(operadora.ULTIMA_ATUALIZACAO_OPERADORA, pendulum.parse(Transacao1Mock().get_operadora_dict()['ultimaAtualizacaoOperadora']))
        self.assertEqual(operadora.ESTADOS_ATUANTES, Transacao1Mock().get_operadora_dict()['estadosAtuantes']['estadoOperadora'])
        self.assertEqual(len(operadora.PRODUTOS), 3)
        self.assertIsInstance(operadora.PRODUTOS[0], Produto)


class ErrosTestCase(TestCase):

    def setUp(self):
        self.error_builder = ErrosMock()

    def test_errors(self):
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(FoneIncompletoInvalido, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(1, "Fone Incompleto / Invalido"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(LimiteCreditoInsuficiente, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(2, "Limite de Crédito Insuficiente"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(EstoqueInsuficiente, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(3, "Estoque Insuficiente"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(TelefoneNaoAutorizado, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(4, "Telefone não autorizado"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(SenhaInvalida, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(5, "Senha Inválida"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(MaximoNumeroConexoesAtingida, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(6, "Máximo número de conexões atingida"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(SistemaEmManutencao, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(7, "Sistema em Manutenção"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(OperadoraProdutoNaoEncontrado, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(8, "Operadora / Produto não encontrado"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(CodigoInvalido, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(9, "Código inválido"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(ValorInvalido, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(10, "Valor Inválido"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(Timeout, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(11, "Timeout"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(CompraExpirada, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(13, "Compra Expirada"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(CompraInexistente, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(14, "Compra inexistente"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(UsuarioLojaNaoEncontrado, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(15, "Usuario/Loja não encontrados"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(ParametrosInsuficientes, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(16, "Parâmetros Insuficientes"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(CompraJaConfirmada, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(17, "Compra já confirmada"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(BoletoNaoEncontrado, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(18, "Boleto não Encontrado"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(ParametrosNaoEnviadosViaPOST, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(19, "Parametros não enviados via POST"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(CodigoTransacaoNaoInformado, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(20, "Codigo de Transacao não informado"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(VersaoNaoInformada, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(21, "Versão não informada"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(UsuarioSemNivelDeAcesso, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(22, "Usuário sem nível de acesso"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(CobrancaAindaNaoVisualizada, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(23, "Cobrança ainda não visualizada"))
        with self.assertRaises(ErroRV):
            self.assertTrue(issubclass(TransacaoNaoPermitida, ErroRV))
            RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(24, "Transação não permitida"))


class HomologacaoUnitTest(TestCase):
    """
    Unit tests relacionados a homologacao juntamente a RV TEcnologia

    Os resultados dos testes abaixo sao printados no console para poder ser enviados para a RV
    """

    def test_1_consulta_valores(self):
        print("##################################################")
        print("CONSULTA DE VALORES")
        print("##################################################")

        pass

        print("##################################################")

    def test_5_transacoes_pin_confirmada(self):
        print("##################################################")
        print("5 TRANSACOES PIN - CONFIRMADAS")
        print("##################################################")

        pass

        print("##################################################")

    def test_5_transacoes_online_confirmada(self):
        print("##################################################")
        print("5 TRANSACOES ONLINE - CONFIRMADA")
        print("##################################################")

        pass

        print("##################################################")

    def test_5_transacoes_online_cancelada(self):
        print("##################################################")
        print("5 TRANSACOES ONLINE - CANCELADA")
        print("##################################################")

        pass

        print("##################################################")

    def test_1_transacao_online_confirmada_valor_variavel_prod_1180(self):
        print("##################################################")
        print("1 TRANSACAO ONLINE - CONFIRMADA - VALOR VARIAVEL PROD 1180")
        print("##################################################")

        pass

        print("##################################################")


DICT = {
    'cellcard': {
        'versao': '3.94',
        'codigoTransacao': '1',
        'loja': '136',
        'operadoras': {
            'qtdOperadoras': '27',
            'operadora': [{
                'codigoOperadora': 'M5',
                'nomeOperadora': 'TIM',
                'ultimaAtualizacaoOperadora': '2009-04-03 15:05:37',
                'estadosAtuantes': {
                    'qtdEstadosOperadora': '27',
                    'estadoOperadora': [
                        'AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE',
                        'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'
                    ]
                },
                'produtos': {
                    'qtdProdutos': '8',
                    'produto': [{
                        'codigoProduto': 'M65',
                        'nomeProduto': 'PREFACE9.9',
                        'precocompraProduto': '9.5535',
                        'precovendaProduto': '9.90',
                        'validadeProduto': '0',
                        'modeloRecarga': 'ONLINE',
                        'valorMinimoProduto': '9.90',
                        'valorMaximoProduto': '9.90',
                        'valorIncrementoProduto': '0.00',
                        'ultima_atualizacaoProduto': '2017-09-01 15:40:15',
                        'precoVariavelProduto': '0',
                        'estadosProdutoPin': {
                            'qtdEstadosProduto': '24',
                            'estadoProduto': [
                                'AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS',
                                'MT', 'PA', 'PB', 'PE', 'PI', 'RJ', 'RN', 'RO', 'RR', 'SE', 'SP', 'TO'
                            ]
                        }
                    },{
                            'codigoProduto': 'M53',
                            'nomeProduto': 'TIM R$10',
                            'precocompraProduto': '9.65',
                            'precovendaProduto': '10.00',
                            'validadeProduto': '0',
                            'modeloRecarga': 'ONLINE',
                            'valorMinimoProduto': '10.00',
                            'valorMaximoProduto': '10.00',
                            'valorIncrementoProduto': '0.00',
                            'ultima_atualizacaoProduto': '2017-08-07 09:19:26',
                            'precoVariavelProduto': '0',
                            'estadosProdutoPin': {
                                'qtdEstadosProduto': '27',
                                'estadoProduto': [
                                    'AC',
                                    'AL',
                                    'AM',
                                    'AP',
                                    'BA',
                                    'CE',
                                    'DF',
                                    'ES',
                                    'GO',
                                    'MA',
                                    'MG',
                                    'MS',
                                    'MT',
                                    'PA',
                                    'PB',
                                    'PE',
                                    'PI',
                                    'PR',
                                    'RJ',
                                    'RN',
                                    'RO',
                                    'RR',
                                    'RS',
                                    'SC',
                                    'SE',
                                    'SP',
                                    'TO'
                                ]
                            }
                    },{
                            'codigoProduto': 'M55',
                            'nomeProduto': 'TIM R$15',
                            'precocompraProduto': '14.475',
                            'precovendaProduto': '15.00',
                            'validadeProduto': '0',
                            'modeloRecarga': 'ONLINE',
                            'valorMinimoProduto': '15.00',
                            'valorMaximoProduto': '15.00',
                            'valorIncrementoProduto': '0.00',
                            'ultima_atualizacaoProduto': '2017-05-23 13:56:01',
                            'precoVariavelProduto': '0',
                            'estadosProdutoPin': {
                                'qtdEstadosProduto': '27',
                                'estadoProduto': [
                                    'AC',
                                    'AL',
                                    'AM',
                                    'AP',
                                    'BA',
                                    'CE',
                                    'DF',
                                    'ES',
                                    'GO',
                                    'MA',
                                    'MG',
                                    'MS',
                                    'MT',
                                    'PA',
                                    'PB',
                                    'PE',
                                    'PI',
                                    'PR',
                                    'RJ',
                                    'RN',
                                    'RO',
                                    'RR',
                                    'RS',
                                    'SC',
                                    'SE',
                                    'SP',
                                    'TO']}}
                    ]
                }
            },
                {
                    'codigoOperadora': 'M2',
                    'nomeOperadora': 'CLARO',
                    'ultimaAtualizacaoOperadora': '2009-02-17 10:20:11',
                    'estadosAtuantes': {
                        'qtdEstadosOperadora': '20',
                        'estadoOperadora': [
                            'AL',
                            'AM',
                            'BA',
                            'CE',
                            'DF',
                            'ES',
                            'GO',
                            'MA',
                            'MG',
                            'PA',
                            'PB',
                            'PE',
                            'PI',
                            'PR',
                            'RJ',
                            'RN',
                            'RS',
                            'SC',
                            'SE',
                            'SP']},
                    'produtos': {
                        'qtdProdutos': '8',
                        'produto': [
                            {
                                'codigoProduto': 'M42',
                                'nomeProduto': 'CLARO R$10',
                                'precocompraProduto': '9.65',
                                'precovendaProduto': '10.00',
                                'validadeProduto': '30',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '10.00',
                                'valorMaximoProduto': '10.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2014-05-12 14:18:06',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': 'M39',
                                'nomeProduto': 'CLARO R$13',
                                'precocompraProduto': '12.545',
                                'precovendaProduto': '13.00',
                                'validadeProduto': '30',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '13.00',
                                'valorMaximoProduto': '13.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2012-11-12 12:35:03',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': 'M59',
                                'nomeProduto': 'CLARO R$15',
                                'precocompraProduto': '14.475',
                                'precovendaProduto': '15.00',
                                'validadeProduto': '30',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '15.00',
                                'valorMaximoProduto': '15.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2015-07-29 14:11:52',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': 'M52',
                                'nomeProduto': 'CLARO 20+2',
                                'precocompraProduto': '19.3',
                                'precovendaProduto': '20.00',
                                'validadeProduto': '60',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '20.00',
                                'valorMaximoProduto': '20.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2014-10-06 14:51:29',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': 'M5',
                                'nomeProduto': 'CLARO 30+4',
                                'precocompraProduto': '28.95',
                                'precovendaProduto': '30.00',
                                'validadeProduto': '90',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '30.00',
                                'valorMaximoProduto': '30.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2012-02-07 12:01:11',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': 'M66',
                                'nomeProduto': 'CLARO 40+6',
                                'precocompraProduto': '38.6',
                                'precovendaProduto': '40.00',
                                'validadeProduto': '90',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '40.00',
                                'valorMaximoProduto': '40.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2017-06-30 10:24:24',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': 'M6',
                                'nomeProduto': 'CLARO 50+8',
                                'precocompraProduto': '48.25',
                                'precovendaProduto': '50.00',
                                'validadeProduto': '150',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '50.00',
                                'valorMaximoProduto': '50.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2010-04-19 16:33:48',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': 'M7',
                                'nomeProduto': 'CLA 100+18',
                                'precocompraProduto': '96.5',
                                'precovendaProduto': '100.00',
                                'validadeProduto': '150',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '100.00',
                                'valorMaximoProduto': '100.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2016-06-29 16:19:27',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}}]}},
                {
                    'codigoOperadora': 'M3',
                    'nomeOperadora': 'VIVO',
                    'ultimaAtualizacaoOperadora': '2009-02-04 16:14:11',
                    'estadosAtuantes': {
                        'qtdEstadosOperadora': '27',
                        'estadoOperadora': [
                            'AC',
                            'AL',
                            'AM',
                            'AP',
                            'BA',
                            'CE',
                            'DF',
                            'ES',
                            'GO',
                            'MA',
                            'MG',
                            'MS',
                            'MT',
                            'PA',
                            'PB',
                            'PE',
                            'PI',
                            'PR',
                            'RJ',
                            'RN',
                            'RO',
                            'RR',
                            'RS',
                            'SC',
                            'SE',
                            'SP',
                            'TO']},
                    'produtos': {
                        'qtdProdutos': '8',
                        'produto': [
                            {
                                'codigoProduto': 'M41',
                                'nomeProduto': 'VIVO R$15',
                                'precocompraProduto': '14.475',
                                'precovendaProduto': '15.00',
                                'validadeProduto': '30',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '15.00',
                                'valorMaximoProduto': '15.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2013-06-03 16:11:43',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': 'M45',
                                'nomeProduto': 'VIVO R$20',
                                'precocompraProduto': '19.3',
                                'precovendaProduto': '20.00',
                                'validadeProduto': '45',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '20.00',
                                'valorMaximoProduto': '20.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2017-10-31 08:51:26',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': 'M12',
                                'nomeProduto': 'VIVO R$25',
                                'precocompraProduto': '24.125',
                                'precovendaProduto': '25.00',
                                'validadeProduto': '45',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '25.00',
                                'valorMaximoProduto': '25.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2017-10-31 08:51:50',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': 'M13',
                                'nomeProduto': 'VIVO R$35',
                                'precocompraProduto': '33.775',
                                'precovendaProduto': '35.00',
                                'validadeProduto': '90',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '35.00',
                                'valorMaximoProduto': '35.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2011-11-09 11:32:41',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': 'M62',
                                'nomeProduto': 'VIVO R$40',
                                'precocompraProduto': '38.6',
                                'precovendaProduto': '40.00',
                                'validadeProduto': '90',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '40.00',
                                'valorMaximoProduto': '40.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2016-10-24 11:48:29',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': 'M14',
                                'nomeProduto': 'VIVO R$50',
                                'precocompraProduto': '48.25',
                                'precovendaProduto': '50.00',
                                'validadeProduto': '120',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '50.00',
                                'valorMaximoProduto': '50.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2011-11-09 11:32:41',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': 'M16',
                                'nomeProduto': 'VIVO R$100',
                                'precocompraProduto': '96.5',
                                'precovendaProduto': '100.00',
                                'validadeProduto': '180',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '100.00',
                                'valorMaximoProduto': '100.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2011-11-09 11:32:41',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': 'M15',
                                'nomeProduto': 'VIVO R$60',
                                'precocompraProduto': '57.9',
                                'precovendaProduto': '60.00',
                                'validadeProduto': '120',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '60.00',
                                'valorMaximoProduto': '60.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2011-08-12 17:07:11',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '1',
                                    'estadoProduto': 'SP'}}]}},
                {
                    'codigoOperadora': '3',
                    'nomeOperadora': 'OI',
                    'ultimaAtualizacaoOperadora': '2010-03-25 11:47:06',
                    'estadosAtuantes': {
                        'qtdEstadosOperadora': '27',
                        'estadoOperadora': [
                            'PR',
                            'PI',
                            'PE',
                            'PB',
                            'PA',
                            'MT',
                            'MS',
                            'MG',
                            'MA',
                            'GO',
                            'ES',
                            'DF',
                            'CE',
                            'BA',
                            'AP',
                            'AM',
                            'AL',
                            'AC',
                            'RJ',
                            'RN',
                            'RO',
                            'RR',
                            'RS',
                            'SC',
                            'SE',
                            'SP',
                            'TO']},
                    'produtos': {
                        'qtdProdutos': '11',
                        'produto': [
                            {
                                'codigoProduto': '1971',
                                'nomeProduto': 'OI R$8',
                                'precocompraProduto': '7.72',
                                'precovendaProduto': '8.00',
                                'validadeProduto': '30',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '8.00',
                                'valorMaximoProduto': '8.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2015-11-20 15:32:25',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '4',
                                    'estadoProduto': [
                                        'BA',
                                        'CE',
                                        'MG',
                                        'PE']}},
                            {
                                'codigoProduto': '1488',
                                'nomeProduto': 'OI R$10',
                                'precocompraProduto': '9.65',
                                'precovendaProduto': '10.00',
                                'validadeProduto': '30',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '10.00',
                                'valorMaximoProduto': '10.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2014-09-20 14:16:06',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': '1419',
                                'nomeProduto': 'OI R$14',
                                'precocompraProduto': '13.51',
                                'precovendaProduto': '14.00',
                                'validadeProduto': '30',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '14.00',
                                'valorMaximoProduto': '14.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2014-07-25 16:13:58',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': '1018',
                                'nomeProduto': 'OI R$20',
                                'precocompraProduto': '19.30',
                                'precovendaProduto': '20.00',
                                'validadeProduto': '45',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '20.00',
                                'valorMaximoProduto': '20.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2013-05-13 09:05:15',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': '1019',
                                'nomeProduto': 'OI R$25',
                                'precocompraProduto': '24.13',
                                'precovendaProduto': '25.00',
                                'validadeProduto': '45',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '25.00',
                                'valorMaximoProduto': '25.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2013-05-13 09:06:02',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': '1595',
                                'nomeProduto': 'OI R$30',
                                'precocompraProduto': '28.95',
                                'precovendaProduto': '30.00',
                                'validadeProduto': '45',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '30.00',
                                'valorMaximoProduto': '30.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2014-11-24 17:40:49',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': '1628',
                                'nomeProduto': 'OI R$35',
                                'precocompraProduto': '33.78',
                                'precovendaProduto': '35.00',
                                'validadeProduto': '45',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '35.00',
                                'valorMaximoProduto': '35.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2015-01-26 16:03:23',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': '2068',
                                'nomeProduto': 'OI R$40',
                                'precocompraProduto': '38.60',
                                'precovendaProduto': '40.00',
                                'validadeProduto': '45',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '40.00',
                                'valorMaximoProduto': '40.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2016-03-24 09:20:38',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': '1021',
                                'nomeProduto': 'OI R$50',
                                'precocompraProduto': '48.25',
                                'precovendaProduto': '50.00',
                                'validadeProduto': '90',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '50.00',
                                'valorMaximoProduto': '50.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2013-05-13 09:06:51',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': '2069',
                                'nomeProduto': 'OI R$75',
                                'precocompraProduto': '72.38',
                                'precovendaProduto': '75.00',
                                'validadeProduto': '90',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '75.00',
                                'valorMaximoProduto': '75.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2016-03-24 09:21:37',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': '1629',
                                'nomeProduto': 'OI R$100',
                                'precocompraProduto': '96.50',
                                'precovendaProduto': '100.00',
                                'validadeProduto': '90',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '100.00',
                                'valorMaximoProduto': '100.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2015-01-26 16:05:20',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}}]}},
                {
                    'codigoOperadora': '17',
                    'nomeOperadora': 'ZUUM',
                    'ultimaAtualizacaoOperadora': '2013-11-04 11:43:42',
                    'estadosAtuantes': {
                        'qtdEstadosOperadora': '0'},
                    'produtos': {
                        'qtdProdutos': '1',
                        'produto': {
                            'codigoProduto': '1180',
                            'nomeProduto': 'RECARGA ZUUM',
                            'precocompraProduto': '0.00',
                            'precovendaProduto': '0.00',
                            'validadeProduto': '0',
                            'modeloRecarga': 'ONLINE',
                            'valorMinimoProduto': '40.00',
                            'valorMaximoProduto': '130.00',
                            'valorIncrementoProduto': '0.01',
                            'ultima_atualizacaoProduto': '2014-02-06 16:52:50',
                            'precoVariavelProduto': '1',
                            'estadosProdutoPin': {
                                'qtdEstadosProduto': '27',
                                'estadoProduto': [
                                    'AC',
                                    'AL',
                                    'AM',
                                    'AP',
                                    'BA',
                                    'CE',
                                    'DF',
                                    'ES',
                                    'GO',
                                    'MA',
                                    'MG',
                                    'MS',
                                    'MT',
                                    'PA',
                                    'PB',
                                    'PE',
                                    'PI',
                                    'PR',
                                    'RJ',
                                    'RN',
                                    'RO',
                                    'RR',
                                    'RS',
                                    'SC',
                                    'SE',
                                    'SP',
                                    'TO']}}}},
                {
                    'codigoOperadora': '31',
                    'nomeOperadora': 'EMBRATEL',
                    'ultimaAtualizacaoOperadora': '2012-04-23 08:55:31',
                    'estadosAtuantes': {
                        'qtdEstadosOperadora': '27',
                        'estadoOperadora': [
                            'TO',
                            'SP',
                            'SE',
                            'SC',
                            'RS',
                            'RR',
                            'RO',
                            'RN',
                            'RJ',
                            'PR',
                            'PI',
                            'PE',
                            'PB',
                            'PA',
                            'MT',
                            'MS',
                            'MG',
                            'MA',
                            'GO',
                            'ES',
                            'DF',
                            'CE',
                            'BA',
                            'AP',
                            'AM',
                            'AL',
                            'AC']},
                    'produtos': {
                        'qtdProdutos': '2',
                        'produto': [
                            {
                                'codigoProduto': '562',
                                'nomeProduto': 'EMBRATEL R$5',
                                'precocompraProduto': '4.83',
                                'precovendaProduto': '5.00',
                                'validadeProduto': '180',
                                'modeloRecarga': 'PIN',
                                'valorMinimoProduto': '5.00',
                                'valorMaximoProduto': '5.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2015-05-07 09:44:38',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '1',
                                    'estadoProduto': None}},
                            {
                                'codigoProduto': '657',
                                'nomeProduto': 'CTBC CEL R$50',
                                'precocompraProduto': '48.25',
                                'precovendaProduto': '50.00',
                                'validadeProduto': '90',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '50.00',
                                'valorMaximoProduto': '50.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2018-09-06 17:04:35',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '9',
                                    'estadoProduto': [
                                        'AC',
                                        'DF',
                                        'GO',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'RO',
                                        'SP',
                                        'TO']}}]}},
                {
                    'codigoOperadora': '32',
                    'nomeOperadora': 'ALGAR FIXA',
                    'ultimaAtualizacaoOperadora': '2014-03-19 10:36:36',
                    'estadosAtuantes': {
                        'qtdEstadosOperadora': '4',
                        'estadoOperadora': [
                            'MG',
                            'GO',
                            'CE',
                            'SP']},
                    'produtos': {
                        'qtdProdutos': '0'}},
                {
                    'codigoOperadora': '33',
                    'nomeOperadora': 'CLARO FIXO',
                    'ultimaAtualizacaoOperadora': '2012-03-15 09:38:21',
                    'estadosAtuantes': {
                        'qtdEstadosOperadora': '18',
                        'estadoOperadora': [
                            'AC',
                            'AL',
                            'AM',
                            'AP',
                            'BA',
                            'CE',
                            'ES',
                            'MA',
                            'MG',
                            'PA',
                            'PB',
                            'PE',
                            'PI',
                            'RJ',
                            'RN',
                            'RR',
                            'SE',
                            'SP']},
                    'produtos': {
                        'qtdProdutos': '7',
                        'produto': [
                            {
                                'codigoProduto': '151',
                                'nomeProduto': 'CLARO FIXO 15',
                                'precocompraProduto': '14.48',
                                'precovendaProduto': '15.00',
                                'validadeProduto': '30',
                                'modeloRecarga': 'PIN',
                                'valorMinimoProduto': '15.00',
                                'valorMaximoProduto': '15.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2012-03-15 09:40:11',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '1',
                                    'estadoProduto': None}},
                            {
                                'codigoProduto': '1099',
                                'nomeProduto': 'CLARO FIXO 19',
                                'precocompraProduto': '18.34',
                                'precovendaProduto': '19.00',
                                'validadeProduto': '30',
                                'modeloRecarga': 'PIN',
                                'valorMinimoProduto': '19.00',
                                'valorMaximoProduto': '19.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2013-08-06 14:23:52',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '1',
                                    'estadoProduto': None}},
                            {
                                'codigoProduto': '468',
                                'nomeProduto': 'CLARO FIXO 25',
                                'precocompraProduto': '24.13',
                                'precovendaProduto': '25.00',
                                'validadeProduto': '30',
                                'modeloRecarga': 'PIN',
                                'valorMinimoProduto': '25.00',
                                'valorMaximoProduto': '25.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2012-03-15 09:40:30',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '1',
                                    'estadoProduto': None}},
                            {
                                'codigoProduto': '245',
                                'nomeProduto': 'CLARO FIXO 35',
                                'precocompraProduto': '33.78',
                                'precovendaProduto': '35.00',
                                'validadeProduto': '30',
                                'modeloRecarga': 'PIN',
                                'valorMinimoProduto': '35.00',
                                'valorMaximoProduto': '35.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2012-03-15 09:40:45',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '1',
                                    'estadoProduto': None}},
                            {
                                'codigoProduto': '1188',
                                'nomeProduto': 'CLARO FIXO 45',
                                'precocompraProduto': '43.43',
                                'precovendaProduto': '45.00',
                                'validadeProduto': '30',
                                'modeloRecarga': 'PIN',
                                'valorMinimoProduto': '45.00',
                                'valorMaximoProduto': '45.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2013-11-19 14:44:05',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '1',
                                    'estadoProduto': None}},
                            {
                                'codigoProduto': '246',
                                'nomeProduto': 'CLARO FIXO 55',
                                'precocompraProduto': '53.08',
                                'precovendaProduto': '55.00',
                                'validadeProduto': '60',
                                'modeloRecarga': 'PIN',
                                'valorMinimoProduto': '55.00',
                                'valorMaximoProduto': '55.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2012-03-15 09:41:17',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '1',
                                    'estadoProduto': None}},
                            {
                                'codigoProduto': '361',
                                'nomeProduto': 'CLARO FIXO 80',
                                'precocompraProduto': '77.20',
                                'precovendaProduto': '80.00',
                                'validadeProduto': '60',
                                'modeloRecarga': 'PIN',
                                'valorMinimoProduto': '80.00',
                                'valorMaximoProduto': '80.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2012-03-15 09:41:34',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '1',
                                    'estadoProduto': None}}]}},
                {
                    'codigoOperadora': '56',
                    'nomeOperadora': 'VIVO FIXO',
                    'ultimaAtualizacaoOperadora': '2012-04-23 08:35:25',
                    'estadosAtuantes': {
                        'qtdEstadosOperadora': '1',
                        'estadoOperadora': 'SP'},
                    'produtos': {
                        'qtdProdutos': '5',
                        'produto': [
                            {
                                'codigoProduto': '551',
                                'nomeProduto': 'VIVO FIXO 10',
                                'precocompraProduto': '9.65',
                                'precovendaProduto': '10.00',
                                'validadeProduto': '360',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '10.00',
                                'valorMaximoProduto': '10.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2012-04-23 08:40:34',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '1',
                                    'estadoProduto': 'SP'}},
                            {
                                'codigoProduto': '203',
                                'nomeProduto': 'VIVO FIXO 15',
                                'precocompraProduto': '14.48',
                                'precovendaProduto': '15.00',
                                'validadeProduto': '360',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '15.00',
                                'valorMaximoProduto': '15.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2012-04-23 08:41:10',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '1',
                                    'estadoProduto': 'SP'}},
                            {
                                'codigoProduto': '204',
                                'nomeProduto': 'VIVO FIXO 20',
                                'precocompraProduto': '19.30',
                                'precovendaProduto': '20.00',
                                'validadeProduto': '360',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '20.00',
                                'valorMaximoProduto': '20.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2012-04-23 08:41:31',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '1',
                                    'estadoProduto': 'SP'}},
                            {
                                'codigoProduto': '321',
                                'nomeProduto': 'VIVO FIXO 25',
                                'precocompraProduto': '24.13',
                                'precovendaProduto': '25.00',
                                'validadeProduto': '360',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '25.00',
                                'valorMaximoProduto': '25.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2012-04-23 08:41:48',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '1',
                                    'estadoProduto': 'SP'}},
                            {
                                'codigoProduto': '205',
                                'nomeProduto': 'VIVO FIXO 30',
                                'precocompraProduto': '28.95',
                                'precovendaProduto': '30.00',
                                'validadeProduto': '360',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '30.00',
                                'valorMaximoProduto': '30.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2012-04-23 08:42:27',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '1',
                                    'estadoProduto': 'SP'}}]}},
                {
                    'codigoOperadora': '60',
                    'nomeOperadora': 'OI FIXO',
                    'ultimaAtualizacaoOperadora': '2008-05-20 11:29:10',
                    'estadosAtuantes': {
                        'qtdEstadosOperadora': '3',
                        'estadoOperadora': [
                            'RJ',
                            'PB',
                            'MG']},
                    'produtos': {
                        'qtdProdutos': '1',
                        'produto': {
                            'codigoProduto': '389',
                            'nomeProduto': 'OI FIXO',
                            'precocompraProduto': '0.00',
                            'precovendaProduto': '0.00',
                            'validadeProduto': '180',
                            'modeloRecarga': 'ONLINE',
                            'valorMinimoProduto': '5.00',
                            'valorMaximoProduto': '499.99',
                            'valorIncrementoProduto': '0.01',
                            'ultima_atualizacaoProduto': '2008-08-22 09:07:50',
                            'precoVariavelProduto': '1',
                            'estadosProdutoPin': {
                                'qtdEstadosProduto': '16',
                                'estadoProduto': [
                                    'AL',
                                    'AM',
                                    'AP',
                                    'BA',
                                    'CE',
                                    'ES',
                                    'MA',
                                    'MG',
                                    'PA',
                                    'PB',
                                    'PE',
                                    'PI',
                                    'RJ',
                                    'RN',
                                    'RR',
                                    'SE']}}}},
                {
                    'codigoOperadora': '73',
                    'nomeOperadora': 'NEXTEL',
                    'ultimaAtualizacaoOperadora': '2011-06-21 09:59:19',
                    'estadosAtuantes': {
                        'qtdEstadosOperadora': '11',
                        'estadoOperadora': [
                            'SP',
                            'SC',
                            'RS',
                            'RJ',
                            'PR',
                            'PE',
                            'MG',
                            'GO',
                            'ES',
                            'DF',
                            'BA']},
                    'produtos': {
                        'qtdProdutos': '7',
                        'produto': [
                            {
                                'codigoProduto': '2799',
                                'nomeProduto': 'NEXTEL R$10',
                                'precocompraProduto': '9.65',
                                'precovendaProduto': '10.00',
                                'validadeProduto': '30',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '10.00',
                                'valorMaximoProduto': '10.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2017-09-13 08:34:23',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': '1203',
                                'nomeProduto': 'NEXTEL R$15',
                                'precocompraProduto': '14.48',
                                'precovendaProduto': '15.00',
                                'validadeProduto': '15',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '15.00',
                                'valorMaximoProduto': '15.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2013-12-16 10:33:49',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': '469',
                                'nomeProduto': 'NEXTEL R$20',
                                'precocompraProduto': '19.30',
                                'precovendaProduto': '20.00',
                                'validadeProduto': '30',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '20.00',
                                'valorMaximoProduto': '20.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2013-12-16 10:34:45',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': '1204',
                                'nomeProduto': 'NEXTEL R$25',
                                'precocompraProduto': '24.13',
                                'precovendaProduto': '25.00',
                                'validadeProduto': '30',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '25.00',
                                'valorMaximoProduto': '25.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2013-12-16 10:34:12',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': '470',
                                'nomeProduto': 'NEXTEL R$30',
                                'precocompraProduto': '28.95',
                                'precovendaProduto': '30.00',
                                'validadeProduto': '30',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '30.00',
                                'valorMaximoProduto': '30.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2013-12-16 10:35:00',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': '471',
                                'nomeProduto': 'NEXTEL R$50',
                                'precocompraProduto': '48.25',
                                'precovendaProduto': '50.00',
                                'validadeProduto': '60',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '50.00',
                                'valorMaximoProduto': '50.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2009-08-12 16:08:03',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}},
                            {
                                'codigoProduto': '472',
                                'nomeProduto': 'NEXTEL R$100',
                                'precocompraProduto': '96.50',
                                'precovendaProduto': '100.00',
                                'validadeProduto': '90',
                                'modeloRecarga': 'ONLINE',
                                'valorMinimoProduto': '100.00',
                                'valorMaximoProduto': '100.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2009-08-12 16:08:23',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '27',
                                    'estadoProduto': [
                                        'AC',
                                        'AL',
                                        'AM',
                                        'AP',
                                        'BA',
                                        'CE',
                                        'DF',
                                        'ES',
                                        'GO',
                                        'MA',
                                        'MG',
                                        'MS',
                                        'MT',
                                        'PA',
                                        'PB',
                                        'PE',
                                        'PI',
                                        'PR',
                                        'RJ',
                                        'RN',
                                        'RO',
                                        'RR',
                                        'RS',
                                        'SC',
                                        'SE',
                                        'SP',
                                        'TO']}}]}},
                {
                    'codigoOperadora': '79',
                    'nomeOperadora': 'LEVEL UP',
                    'ultimaAtualizacaoOperadora': '2011-06-13 09:11:23',
                    'estadosAtuantes': {
                        'qtdEstadosOperadora': '1',
                        'estadoOperadora': 'RJ'},
                    'produtos': {
                        'qtdProdutos': '2',
                        'produto': [
                            {
                                'codigoProduto': '625',
                                'nomeProduto': 'LEVELUP 20',
                                'precocompraProduto': '19.30',
                                'precovendaProduto': '20.00',
                                'validadeProduto': '0',
                                'modeloRecarga': 'PIN',
                                'valorMinimoProduto': '20.00',
                                'valorMaximoProduto': '20.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2012-09-04 13:25:41',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '1',
                                    'estadoProduto': None}},
                            {
                                'codigoProduto': '785',
                                'nomeProduto': 'LEVELUP 40',
                                'precocompraProduto': '38.60',
                                'precovendaProduto': '40.00',
                                'validadeProduto': '0',
                                'modeloRecarga': 'PIN',
                                'valorMinimoProduto': '40.00',
                                'valorMaximoProduto': '40.00',
                                'valorIncrementoProduto': '0.00',
                                'ultima_atualizacaoProduto': '2012-09-04 13:25:58',
                                'precoVariavelProduto': '0',
                                'estadosProdutoPin': {
                                    'qtdEstadosProduto': '1',
                                    'estadoProduto': None}}]}}, {
                    'codigoOperadora': '226',
                    'nomeOperadora': 'GOOGLE PLAY DIGITAL',
                    'ultimaAtualizacaoOperadora': '2018-10-05 17:18:59',
                    'estadosAtuantes': {
                        'qtdEstadosOperadora': '0'
                    },
                    'produtos': {
                        'qtdProdutos': '1',
                        'produto': {
                            'codigoProduto': '2988',
                            'nomeProduto': 'GOOGLE PLAY DIGITAL',
                            'precocompraProduto': '0.00',
                            'precovendaProduto': '0.00',
                            'validadeProduto': '0',
                            'modeloRecarga': 'PIN',
                            'valorMinimoProduto': '30.00',
                            'valorMaximoProduto': '300.00',
                            'valorIncrementoProduto': '0.01',
                            'ultima_atualizacaoProduto': '2018-10-05 17:21:09',
                            'precoVariavelProduto': '1',
                            'estadosProdutoPin': {
                                'qtdEstadosProduto': '1',
                                'estadoProduto': None}}}}]}}}
