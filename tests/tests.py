import random
from decimal import Decimal

import pendulum

from rv_schubert_sdk import RVapi, \
    Transacao1, \
    Transacao3, \
    Transacao5, \
    Transacao7, \
    Transacao9, \
    Recarga, ErroRV, Produto, Operadora, Comprovante
from .test_mockups import Transacao1Mock, Transacao3Mock, ErrosMock, Transacao5Mock, Transacao9Mock, Transacao7Mock

from rv_schubert_sdk import FoneIncompletoInvalido, LimiteCreditoInsuficiente, EstoqueInsuficiente, \
    TelefoneNaoAutorizado, SenhaInvalida, MaximoNumeroConexoesAtingida, SistemaEmManutencao, \
    OperadoraProdutoNaoEncontrado, CodigoInvalido, ValorInvalido, Timeout, CompraExpirada, CompraInexistente, \
    UsuarioLojaNaoEncontrado, ParametrosInsuficientes, CompraJaConfirmada, BoletoNaoEncontrado, \
    ParametrosNaoEnviadosViaPOST, CodigoTransacaoNaoInformado, VersaoNaoInformada, UsuarioSemNivelDeAcesso, \
    CobrancaAindaNaoVisualizada, TransacaoNaoPermitida

from unittest import TestCase

RODAR_HOMOL = True


if RODAR_HOMOL is False:
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

            res = self.transacao_1.execute(mock=Transacao1Mock().get())
            print(res)
            # self.assertIsInstance(self.transacao_1.OPERADORAS, Operadora)


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
            self.assertEqual(result.DATA_RV,
                             pendulum.datetime(year=2019, month=3, day=19, hour=14, minute=5, second=23))


    class Transacao7TestCase(TestCase):

        def setUp(self):
            self.transacao_7 = Transacao7()

        def test_execute(self):
            self.transacao_7.execute(compra=5, mock=Transacao7Mock().get_confirmada())
            self.assertEqual(self.transacao_7.CONFIRMADO, True)
            self.assertEqual(self.transacao_7.CANCELADO, False)

            self.transacao_7.execute(compra=6, cod_retorno=1, mock=Transacao7Mock().get_cancelada())
            self.assertEqual(self.transacao_7.CONFIRMADO, False)
            self.assertEqual(self.transacao_7.CANCELADO, True)


    class Transacao9TestCase(TestCase):

        def setUp(self):
            self.transacao_9 = Transacao9()

        def test_execute(self):
            self.transacao_9.execute(Transacao9Mock().get())

            self.assertEqual(self.transacao_9.LIMITE_CREDITO, Decimal("100000"))
            self.assertEqual(self.transacao_9.LIMITE_DISPONIVEL, Decimal("71936.28"))
            self.assertEqual(self.transacao_9.ANTECIPADO, Decimal("0.18"))
            self.assertEqual(self.transacao_9.VALOR_ABERTO, Decimal("196819.21"))


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
            self.assertEqual(recarga.DATA_RV,
                             pendulum.datetime(year=2019, month=3, day=13, hour=18, minute=13, second=51))
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
            self.assertEqual(produto.PRECO_COMPRA_PRODUTO,
                             Decimal(Transacao1Mock().get_produto_dict()['precocompraProduto']))
            self.assertEqual(produto.PRECO_VENDA_PRODUTO,
                             Decimal(Transacao1Mock().get_produto_dict()['precovendaProduto']))
            self.assertEqual(produto.VALIDADE_PRODUTO, Transacao1Mock().get_produto_dict()['validadeProduto'])
            self.assertEqual(produto.MODELO_RECARGA, Transacao1Mock().get_produto_dict()['modeloRecarga'])
            self.assertEqual(produto.VALOR_MINIMO_PRODUTO,
                             Decimal(Transacao1Mock().get_produto_dict()['valorMinimoProduto']))
            self.assertEqual(produto.VALOR_MAXIMO_PRODUTO,
                             Decimal(Transacao1Mock().get_produto_dict()['valorMaximoProduto']))
            self.assertEqual(produto.VALOR_INCREMENTO_PRODUTO,
                             Decimal(Transacao1Mock().get_produto_dict()['valorIncrementoProduto']))
            self.assertEqual(produto.ULTIMA_ATUALIZACAO_PRODUTO,
                             pendulum.parse(Transacao1Mock().get_produto_dict()['ultima_atualizacaoProduto']))
            self.assertEqual(produto.PRECO_VARIAVEL_PRODUTO,
                             Decimal(Transacao1Mock().get_produto_dict()['precoVariavelProduto']))
            self.assertEqual(produto.ESTADOS_PRODUTO_PIN,
                             Transacao1Mock().get_produto_dict()['estadosProdutoPin']['estadoProduto'])


    class OperadoraObjectTestCase(TestCase):

        def test_build_operadora_from_dict(self):
            operadora = Operadora().build_from_dict(Transacao1Mock().get_operadora_dict())

            self.assertEqual(operadora.CODIGO_OPERADORA, Transacao1Mock().get_operadora_dict()['codigoOperadora'])
            self.assertEqual(operadora.NOME_OPERADORA, Transacao1Mock().get_operadora_dict()['nomeOperadora'])
            self.assertEqual(operadora.ULTIMA_ATUALIZACAO_OPERADORA,
                             pendulum.parse(Transacao1Mock().get_operadora_dict()['ultimaAtualizacaoOperadora']))
            self.assertEqual(operadora.ESTADOS_ATUANTES,
                             Transacao1Mock().get_operadora_dict()['estadosAtuantes']['estadoOperadora'])
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
                RVapi().convert_xml_to_dict(
                    self.error_builder.build_error_xml(6, "Máximo número de conexões atingida"))
            with self.assertRaises(ErroRV):
                self.assertTrue(issubclass(SistemaEmManutencao, ErroRV))
                RVapi().convert_xml_to_dict(self.error_builder.build_error_xml(7, "Sistema em Manutenção"))
            with self.assertRaises(ErroRV):
                self.assertTrue(issubclass(OperadoraProdutoNaoEncontrado, ErroRV))
                RVapi().convert_xml_to_dict(
                    self.error_builder.build_error_xml(8, "Operadora / Produto não encontrado"))
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
                RVapi().convert_xml_to_dict(
                    self.error_builder.build_error_xml(20, "Codigo de Transacao não informado"))
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

    class ComprovanteTestCase(TestCase):

        def setUp(self):
            self.comprovante = Comprovante()

        def test_generate_online(self):
            self.comprovante.generate_for_online(
                data_hora=pendulum.now(),
                loja="LOJA TESTE",
                cod_online="00001",
                operadora="TIM",
                valor=Decimal("10"),
                telefone="47 99999-9999",
                mensagem="Mensagem de teste",
                nsu="123"
            )

        def test_generate_pin(self):
            self.comprovante.generate_for_pin(
                data_hora=pendulum.now(),
                loja="LOJA TESTE",
                cod_online="00001",
                operadora="TIM",
                valor=Decimal("10"),
                pin="909090",
                lote_serie="1357623",
                mensagem="Mensagem de teste"
            )


if RODAR_HOMOL is True:
    class HomologacaoUnitTest(TestCase):
        """
        Unit tests relacionados a homologacao juntamente a RV TEcnologia

        Os resultados dos testes abaixo sao printados no console para poder ser enviados para a RV
        """

        def test_1_consulta_valores(self):
            print("##################################################")
            print("CONSULTA DE VALORES")
            print("##################################################")
            result = Transacao9().execute()
            print("versao: ", result['cellcard']['versao'])
            print("codigoTransacao: ", result['cellcard']['codigoTransacao'])
            print("limite_credito: ", result['cellcard']['limite_credito'])
            print("limite_disponivel: ", result['cellcard']['limite_disponivel'])
            print("antecipado: ", result['cellcard']['antecipado'])
            print("valor_aberto: ", result['cellcard']['valor_aberto'])
            print("##################################################")

        def test_5_transacoes_pin_confirmadas(self):
            print("##################################################")
            print("5 TRANSACOES PIN - CONFIRMADAS")
            print("##################################################")
            id_interno = random.randint(10000, 20000)

            print("id_interno: ", id_interno + 1,  "| cod_online: ", Transacao3(homologacao=True).execute(
                compra=id_interno + 1,
                produto="2078"
            ).RAW_DATA['cod_online'])  # steam $50
            print("id_interno: ", id_interno + 2,  "| cod_online: ", Transacao3(homologacao=True).execute(
                compra=id_interno + 2,
                produto="1949"
            ).RAW_DATA['cod_online'])  # google $15
            print("id_interno: ", id_interno + 3,  "| cod_online: ", Transacao3(homologacao=True).execute(
                compra=id_interno + 3,
                produto="2078"
            ).RAW_DATA['cod_online'])  # steam $50
            print("id_interno: ", id_interno + 4,  "| cod_online: ", Transacao3(homologacao=True).execute(
                compra=id_interno + 4,
                produto="775"
            ).RAW_DATA['cod_online'])  # paymentz $45

            transacao = Transacao3(homologacao=True).execute(
                compra=id_interno + 5,
                produto="1952"
            )
            print("id_interno: ", id_interno + 5,  "| cod_online: ", transacao.RAW_DATA['cod_online'])  # google $100

            print(Transacao7().execute(compra=id_interno + 1))
            print(Transacao7().execute(compra=id_interno + 2))
            print(Transacao7().execute(compra=id_interno + 3))
            print(Transacao7().execute(compra=id_interno + 4))
            print(Transacao7().execute(compra=id_interno + 5))

            Comprovante().generate_for_pin(
                data_hora=transacao.DATA_RV,
                loja="LOJA TESTE",
                cod_online=transacao.COD_ONLINE,
                operadora="PAYMENTEZ",
                valor=transacao.FACE,
                pin=transacao.PIN,
                lote_serie=transacao.LOTE,
                mensagem=transacao.MENSAGEM
            )
            print("##################################################")

        def test_5_transacoes_online_confirmadas(self):
            print("##################################################")
            print("5 TRANSACOES ONLINE - CONFIRMADA")
            print("##################################################")
            id_interno = random.randint(20010, 30000)

            transacao_5 = Transacao5()

            print("id_interno: ", id_interno + 1,  "| cod_online: ", transacao_5.execute(
                compra=id_interno + 1,
                produto='470',
                ddd='47',
                fone='99999999'
            ).RAW_DATA['cod_online'])  # nextel $30
            print("id_interno: ", id_interno + 2,  "| cod_online: ", transacao_5.execute(
                compra=id_interno + 2,
                produto='205',
                ddd='47',
                fone='99999999'
            ).RAW_DATA['cod_online'])  # vivo fixo $30
            print("id_interno: ", id_interno + 3,  "| cod_online: ", transacao_5.execute(
                compra=id_interno + 3,
                produto='1629',
                ddd='47',
                fone='99999999'
            ).RAW_DATA['cod_online'])  # oi $100
            print("id_interno: ", id_interno + 4,  "| cod_online: ", transacao_5.execute(
                compra=id_interno + 4,
                produto='1628',
                ddd='47',
                fone='99999999'
            ).RAW_DATA['cod_online'])  # oi $35
            print("id_interno: ", id_interno + 5,  "| cod_online: ", transacao_5.execute(
                compra=id_interno + 5,
                produto='M5',
                ddd='47',
                fone='99999999'
            ).RAW_DATA['cod_online'])  # claro $30

            print(Transacao7().execute(compra=id_interno + 1))
            print(Transacao7().execute(compra=id_interno + 2))
            print(Transacao7().execute(compra=id_interno + 3))
            print(Transacao7().execute(compra=id_interno + 4))
            print(Transacao7().execute(compra=id_interno + 5))
            print("##################################################")

        def test_5_transacoes_online_canceladas(self):
            print("##################################################")
            print("5 TRANSACOES ONLINE - CANCELADA")
            print("##################################################")
            id_interno = random.randint(30010, 40000)

            print("id_interno: ", id_interno + 1,  "| cod_online: ", Transacao5().execute(
                compra=id_interno + 1,
                produto='470',
                ddd='47',
                fone='99999999'
            ).RAW_DATA['cod_online'])  # nextel $30
            print("id_interno: ", id_interno + 2,  "| cod_online: ", Transacao5().execute(
                compra=id_interno + 2,
                produto='205',
                ddd='47',
                fone='99999999'
            ).RAW_DATA['cod_online'])  # vivo fixo $30
            print("id_interno: ", id_interno + 3,  "| cod_online: ", Transacao5().execute(
                compra=id_interno + 3,
                produto='1629',
                ddd='47',
                fone='99999999'
            ).RAW_DATA['cod_online'])  # oi $100
            print("id_interno: ", id_interno + 4,  "| cod_online: ", Transacao5().execute(
                compra=id_interno + 4,
                produto='1628',
                ddd='47',
                fone='99999999'
            ).RAW_DATA['cod_online'])  # oi $35
            print("id_interno: ", id_interno + 5,  "| cod_online: ", Transacao5().execute(
                compra=id_interno + 5,
                produto='M5',
                ddd='47',
                fone='99999999'
            ).RAW_DATA['cod_online'])  # claro $30

            print(Transacao7().execute(compra=id_interno + 1, cod_retorno=1))
            print(Transacao7().execute(compra=id_interno + 2, cod_retorno=1))
            print(Transacao7().execute(compra=id_interno + 3, cod_retorno=1))
            print(Transacao7().execute(compra=id_interno + 4, cod_retorno=1))
            print(Transacao7().execute(compra=id_interno + 5, cod_retorno=1))
            print("##################################################")

        def test_1_transacao_online_confirmada_valor_variavel_prod_1180(self):
            print("##################################################")
            print("1 TRANSACAO ONLINE - CONFIRMADA - VALOR VARIAVEL PROD 1180")
            print("##################################################")
            id_interno = random.randint(40010, 50000)

            transacao = Transacao5().execute(
                compra=id_interno,
                produto='1180', valor="40.0",
                codigo_assinante="1234",
                ddd='47',
                fone='99999999'
            )

            print("id_interno: ", id_interno,  "| cod_online: ", transacao.RAW_DATA['cod_online'])

            result = Transacao7().execute(compra=id_interno)
            print(result, transacao)

            Comprovante().generate_for_online(
                data_hora=transacao.DATA_RV,
                loja="LOJA TESTE",
                cod_online=transacao.COD_ONLINE,
                operadora="ZUUM",
                valor=transacao.FACE,
                telefone=transacao.FONE,
                mensagem=transacao.MENSAGEM,
                nsu=transacao.NSU
            )
            print("##################################################")
