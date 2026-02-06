# coding=utf-8
Settings.ActionLogs=0
import random
import time
import datetime
import traceback
from abc import abstractmethod

# Isso serve apenas para garantir que uma IDE como o VS code apague os alertas 
# desnecessários e aponte só o que pode ser útil para quem escreve o teste
# from dummy import *


# ===================================================================================================================================
# Escolha os testes
# ===================================================================================================================================
def main():
    # Preciso de uma forma para garantir que o teste funcionou
    FuncoesAuxiliares.iniciar()

    BaixaFinanceiro.executar(vezes=1)
    CadastroCliente.executar()
    CadastroFornecedor.executar()
    CadastroProduto.executar()
    CriacaoBoleto.executar()
    CriacaoContrato.executar()
    EntradaNf.executar()
    EntradaNfXml.executar()
    FaturamentoContrato.executar()
    GeracaoRemessa.executar()
    Ocorrencia.executar()
    PagamentoNota.executar()

    FuncoesAuxiliares.finalizar()


class Configs:
    SPEED = 1
    DEBUG = False


# ===================================================================================================================================
# Auxiliares
# ===================================================================================================================================
class Constantes:                # Imagens e padroes reutilizaveis
    BOTAO_NOVO = Pattern("constantes_botao_novo.png").similar(0.82)
    BOTAO_PROCURAR = "constantes_botao_procurar.png"
    BOTAO_SIM = "constantes_botao_sim.png"
    BOTAO_NAO = "constantes_botao_nao.png"
    BOTAO_MAIS = Pattern("constantes_botao_mais.png").similar(0.80)
    BOTAO_OK = "constantes_botao_ok.png"
    BOTAO_SALVAR = "constantes_botao_salvar.png"
    BOTAO_EXCLUIR = "constantes_botao_excluir.png"
    BOTAO_SAIR = "constantes_botao_sair.png"

    CHECKBOX_TRUE = "constantes_checkbox_true.png"
    CHECKBOX_FuncoesAuxiliaresLSE = "constantes_checkbox_false.png"

    LOGO_ERP = Pattern("constantes_logo_erp.png").similar(0.80)
    PESQUISA_ROTINA = Pattern("constantes_pesquisa_rotina.png").similar(0.85).targetOffset(24,-1)
    INPUT_USERNAME = Pattern("INPUT_USERNAME.png").targetOffset(-5,21)
    
    PESQUISA_AVANCADA = "constantes_pesquisa_avancada.png"
    OCULTAR = "constantes_ocultar.png"


class T:
    # Substitui os métodos padrões do Sikuli por metodos próprios,
    # capazes de diminuir a velocidade de execucao com uma unica variavel 

    @classmethod
    def clique(cls, imagem):
        wait(0.5 / Configs.SPEED)
        click(imagem)

    @classmethod
    def duplo_clique(cls, imagem):
        wait(0.5 / Configs.SPEED)       
        doubleClick(imagem)

    @staticmethod
    def espere(*args):
        timeout = None
        imagem = None

        if len(args) > 2:
            raise ValueError("A funcao espere recebe no maximo 2 parametros, porem {} foram passados".format(len(args)))

        if len(args) > 0:
            if len(args) == 2:
                imagem, timeout = args
            elif isinstance(args[0], int) or isinstance(args[0], float):
                timeout = args[0]
            else: 
                imagem = args[0]
                
        else:
            raise ValueError("Nenhum valor passado para a funcao espere")

        if not timeout: timeout = 3

        timeout *= (1.0 / Configs.SPEED)
        
        if imagem:
            wait(imagem, timeout)
        else:
            wait(timeout)

    @classmethod
    def espere_e_clique(cls, imagem, timeout=None):
        cls.espere(imagem, timeout)
        cls.clique(imagem)


class FuncoesAuxiliares:

    _hora_inicio = 0

    @classmethod
    def iniciar(cls):
        print("INICIO DO SUITE")
        cls._hora_inicio = time.time()
        cls.entrar_erp()

    @classmethod
    def finalizar(cls):
        hora_final = time.time()
        tempo_exec = hora_final - cls._hora_inicio

        if tempo_exec > 60:
            minutos = tempo_exec // 60
            segundos = tempo_exec % 60
            print("\nTempo de execucao: %.0f min e %.1f seg" % (minutos, segundos))
        else:
            print("\nTempo de execucao: %.2f seg" % tempo_exec)

        print("Quantidade de testes: {}".format(TesteAbstrato.cont_testes))
        print("Quantidade de falhas: {}".format(TesteAbstrato.cont_falhas))

        if TesteAbstrato.cont_falhas == 0 or TesteAbstrato.cont_testes == 0: porcentagem = 100
        else: porcentagem = (float(TesteAbstrato.cont_testes - TesteAbstrato.cont_falhas) / float(TesteAbstrato.cont_testes)) * 100.0
        print("Porcentagem de acertos: {}%".format('%.1f' % porcentagem))
        print("FIM DO SUITE")
    
    @classmethod
    def entrar_erp(cls):
        print("Entrando no ERP...\n")
        if exists(Constantes.LOGO_ERP):
            if exists(Constantes.PESQUISA_ROTINA): cls.prepara(); return
            T.clique(Region(0,913,1536,47).find(Constantes.LOGO_ERP))
            if exists(Constantes.PESQUISA_ROTINA): cls.prepara(); return
            cls.inform_dados_usuario()    
        
        else:    
            type(Key.WIN)
            type('erpmts')
            type(Key.ENTER)
            cls.inform_dados_usuario()

    @classmethod
    def prepara(cls):
        if Configs.DEBUG:
            T.clique(Constantes.PESQUISA_ROTINA)
            cls.sair(5)

    @staticmethod
    def inform_dados_usuario():
        T.espere(Constantes.INPUT_USERNAME, 15)
        type(Constantes.INPUT_USERNAME, 'mitis')
        type(Key.TAB)
        type('mitis01')
        type(Key.TAB)
        type('109')
        type(Key.TAB)
        type(Key.ENTER)
        if exists(Constantes.BOTAO_NAO): T.clique(Constantes.BOTAO_NAO)

    @classmethod
    def inform_rotina(cls, codigo):
        T.espere_e_clique(Constantes.PESQUISA_ROTINA)
        T.espere(1)
        type(codigo)
        type(Key.ENTER)
        T.espere(1)

    @staticmethod
    def sair(qtdd):
        for _ in range(qtdd):
            type(Key.ESC)
            type(Key.ESC)
            type(Key.ENTER)
            T.espere(0.2)

    @classmethod
    def insere_cnpj(cls, regiao=None):
        T.espere(2)
        if not regiao: regiao = Region(0,0,1536,960)
            
        resultado = False
        tentativas = 10
        
        while not resultado and tentativas > 0:
            cnpj = cls._gera_cnpj()
            resultado = cls._tentativa_inserir(cnpj, regiao)
            tentativas -= 1

        if tentativas == 0: raise RuntimeError("Varias tentativas falhas de inserir CNPJ")
        return resultado
    
    @classmethod
    def _tentativa_inserir(cls, cnpj, regiao=None):
        T.espere(0.7)
        T.clique(regiao.find(Pattern("aux_simbolo_receita_to_left.png").targetOffset(-13,2)))
        type(Key.HOME)
        type("a", Key.CTRL)
        type(cnpj)
        T.clique("aux_receita.png")
        T.espere(0.5)
        if cls.aviso_contem("conflitantes"): type(Key.ENTER)
        T.espere(0.1)
    
        if cls.aviso_contem("invalido"):
            type(Key.ENTER)
            return False
        
        elif regiao.has(Pattern("aux_cnpj_vazio.png").similar(0.80)) or regiao.has(Pattern("aux_razao_social_vazio.png").similar(0.85)): return False
        
        elif cls.aviso_contem("Cliente ja cadastro"):
            type(Key.ENTER)
            return False
        else:
            return True
    
    @classmethod
    def _gera_cnpj(cls):
        cnpj = ''
        for _ in range(8): cnpj += str(random.randint(0, 9))
        cnpj += '0001'
    
        cnpj += cls._gera_digito_verific(cnpj)
        cnpj += cls._gera_digito_verific(cnpj)
    
        return cnpj   
    
    @classmethod
    def _gera_digito_verific(cls, cnpj):
        cnpj = cnpj[::-1]
    
        soma = 0
        
        for i in range(len(cnpj)):
            soma += int(cnpj[i]) * cls._gera_fator(i)
    
        digito = soma % 11
        digito = 11 - digito
        if digito == 10: digito = 0
    
        return str(digito)
    
    @staticmethod
    def _gera_fator(i): return range(2, 10)[i % 8]

    @staticmethod
    def multiplos_tabs(qtdd):
        for _ in range(qtdd): type(Key.TAB)

    @classmethod
    def aviso_contem(cls, conteudo, centralizado=None, compreensivo=None):
        if centralizado is None: centralizado = True
        if compreensivo is None: compreensivo = False
        if not centralizado: regiao = Region(472,312,621,333)
        else: regiao = Region(0,0,1181,684)

        texto_aviso = regiao.text().lower()
        conteudo = conteudo.lower()
        
        if conteudo in texto_aviso: return True
        elif not compreensivo: return False
    
        conteudo_em_lista = conteudo.split()
        if conteudo_em_lista[0] in texto_aviso or conteudo_em_lista[-1] in texto_aviso: return True

        return False
        
    @classmethod
    def espere_aviso_conter(cls, conteudo, centralizado=None, compreensivo=None, timeout=3):
        while not cls.aviso_contem(conteudo, centralizado, compreensivo) and timeout > 0:
            T.espere(1)
            timeout -= 1
            
        if timeout == 0: 
            raise FindFailed("O conteudo esperedo ({}) nao apareceu em aviso".format(conteudo))


# ===================================================================================================================================
# Testes
# ===================================================================================================================================
class TesteAbstrato():

    cont_falhas = 0

    cont_testes = 0
    _hora_ultimo_teste = time.time()
    _qtdd_testes_sequenciais_falhos = 0

    _QTDD_SEPARADORES = 80

    @classmethod
    def imprime_separador(cls, caractere=None, paragrafo=False):
        if not caractere: caractere = '='

        print(caractere * cls._QTDD_SEPARADORES)
        if paragrafo: print()

    @classmethod
    def retorna_pontos(cls, mensagem1='', mensagem2=''):
        return '.' * (cls._QTDD_SEPARADORES - len(mensagem1) - len(mensagem2))

    @classmethod
    def dados_inicio_execucao(cls):
        TesteAbstrato.cont_testes += 1

        cls.imprime_separador('=')
        print("TESTE {}: {}".format(cls.cont_testes, cls.__str__()))
        cls.imprime_separador('=')

    @classmethod
    def dados_final_execucao(cls, passou=False, exception=None):
        tempo_exec = str(round(time.time() - TesteAbstrato._hora_ultimo_teste, 2)) + " segundos"
        now = datetime.datetime.now()
        hora_resultado = '{}:{}:{}'.format(now.hour, now.minute, now.second)

        if passou: passou = 'PASSOU'
        else: passou = 'FuncoesAuxiliaresLHOU'

        mensagem_resultado_exec = "Situacao do teste {} - {}".format(cls.cont_testes, cls.__str__())
        print('{}{}{}'.format(mensagem_resultado_exec, cls.retorna_pontos(mensagem_resultado_exec, passou), passou))

        mensagem_hora_resultado = "Hora do resultado"
        print("{}{}{}".format(mensagem_hora_resultado, cls.retorna_pontos(mensagem_hora_resultado, hora_resultado), hora_resultado))

        mensagem_tempo_exec = "Tempo de execucao"
        print("{}{}{}\n".format(mensagem_tempo_exec, cls.retorna_pontos(mensagem_tempo_exec, str(tempo_exec)), tempo_exec))

        if not passou or exception: 
            print(repr(exception))
            print('\n')

    # Principal método do teste
    @classmethod
    def executar(cls, vezes=1):
        for _ in range(vezes):
            if TesteAbstrato._qtdd_testes_sequenciais_falhos >= 3:
                raise RuntimeError(
                        "Parece haver algum erro impedindo varios testes de executar..."
                        )
            
            cls.dados_inicio_execucao()
            TesteAbstrato._hora_ultimo_teste = time.time()
    
            try:
                cls._executar()
    
            except (Exception, FindFailed) as exception:
                cls.dados_final_execucao(passou=False, exception=exception)
    
                TesteAbstrato._qtdd_testes_sequenciais_falhos += 1
                TesteAbstrato.cont_falhas += 1
                # traceback.print_exception(e)
    
                if Configs.DEBUG: raise
                else: FuncoesAuxiliares.sair(5)
    
            else:
                cls.dados_final_execucao(passou=True)
                TesteAbstrato._qtdd_testes_sequenciais_falhos = 0

    # Esse método é privado e é o que realmente executa o teste, mas ele só deve ser chamado pelo def executar()
    # (sem o '_' no início), para que os dados da execução apareçam no terminal
    @abstractmethod
    def _executar(cls): pass

# ---------------------------------------------------------------------------------------------------------------------------
# Baixa financeiro
# ---------------------------------------------------------------------------------------------------------------------------
class BaixaFinanceiro(TesteAbstrato):

    @staticmethod
    def __str__(): return 'BaixaFinanceiro'
    
    @classmethod
    def _executar(cls):
        FuncoesAuxiliares.inform_rotina('155')
        
        # Criacao da conta
        cls.criacao_conta_1()
        cls.entrada_n_doc()
        cls.criacao_conta_2()
        
        # Baixa da conta
        cls.verifica_filtros()
        cls.baixa_conta()
        
        # Vistar conta
        FuncoesAuxiliares.inform_rotina('254')
        cls.vistar_conta()
    
        FuncoesAuxiliares.sair(2)
        
    @staticmethod
    def criacao_conta_1():
        T.espere(Constantes.PESQUISA_AVANCADA, 5)
        type(Key.F8)
        T.espere(Constantes.BOTAO_NOVO, 5)
        type("teste baixa financeiro - gap")
        type(Key.TAB)
        type(Key.TAB)
        type('11')
        type(Key.TAB)

    @staticmethod
    def entrada_n_doc():
        valido = False
        
        while not valido:
            numero_1 = random.randint(0, 1000000)
            numero_2 = random.randint(0, 999)
    
            T.clique(Pattern("baixa_financeiro_input_documento.png").similar(0.85).targetOffset(100,-1))
            type(str(numero_1))
            type(Key.TAB)
            type(str(numero_2))
            type(Key.TAB)
            if FuncoesAuxiliares.aviso_contem("Documento sendo usado", compreensivo=False):         # exists("baixa_financeiro_alerta_usado.png"): 
                T.espere(3)
                type(Key.ENTER)
            else: valido = True    

    @staticmethod
    def criacao_conta_2():
        T.clique(Pattern("baixa_financeiro_data_entrada.png").similar(0.92).targetOffset(-35,0))
        T.clique(Pattern("baixa_financeiro_data_emissao.png").similar(0.92).targetOffset(-36,0))
        valor = str(random.randint(1,9))
        type(Pattern("baixa_financeiro_input_valor.png").similar(0.80), valor)
        type(Key.TAB)
        type(Key.TAB)
        type('11')
        type(Pattern("baixa_financeiro_input_rateio.png").similar(0.80).targetOffset(-1,7), "1")
        type(Key.TAB)
        type(valor)
        T.clique(Constantes.BOTAO_MAIS)
        T.espere(0.2)
        type('s', Key.CTRL)
        T.espere(Constantes.BOTAO_OK)
        if FuncoesAuxiliares.aviso_contem("periodo ja fechado", compreensivo=False):
            type(Key.ENTER)
            type(Pattern("baixa_financeiro_data_entrada_true.png").similar(0.90).targetOffset(110,1), '3000')
            type('s', Key.CTRL)
            
        type(Key.ENTER)
        T.espere(0.2)
        FuncoesAuxiliares.sair(1)
        T.espere(2)

    @staticmethod
    def verifica_filtros():
        if exists("baixa_financeiro_conta_aberta.png"): return
        
        if exists(Constantes.PESQUISA_AVANCADA): T.clique(Constantes.PESQUISA_AVANCADA)

        T.espere(0.2)
        if find(Pattern("baixa_financeiro_filtro_aberto.png").similar(0.80).targetOffset(-16,0)).has(Constantes.CHECKBOX_FuncoesAuxiliaresLSE): 
            T.clique(Pattern("baixa_financeiro_filtro_aberto.png").similar(0.80).targetOffset(-16,0))
            T.clique(Constantes.BOTAO_PROCURAR)
    
        T.espere(1)
        if not exists("baixa_financeiro_conta_aberta.png"): 
            T.clique(Pattern("baixa_financeiro_qualquer_data.png").similar(0.85))
            T.clique(Constantes.BOTAO_PROCURAR)
            T.espere(1)
    
        type('o', Key.ALT)

    @classmethod
    def baixa_conta(cls):
        T.espere(2)
        T.duplo_clique("baixa_financeiro_conta_aberta.png")
        T.espere(0.5)
        T.clique(Pattern("baixa_financeiro_situacao_aberto.png").targetOffset(49,4))
        T.espere(0.1)
        for _ in range(3): type(Key.DOWN)
        type(Key.ENTER)
        type(Pattern("baixa_financeiro_input_baixa.png").similar(0.80).targetOffset(21,0), '11')
        type(Key.TAB)
        type('8')
        type('s', Key.CTRL)
        T.espere(Constantes.BOTAO_OK, 6)
        if FuncoesAuxiliares.aviso_contem("Sucesso"): valido = True            # exists("baixa_financeiro_sucesso.png")
        type(Key.ENTER)
    
        # cls.escolhe_conta_e_salva()
        
        FuncoesAuxiliares.sair(1)

    @staticmethod
    def escolhe_conta_e_salva():
        linha = 0
        valido = False
    
        # Escolhe uma conta bancaria para a baixa, 
        # porque uma mesma conta nao pode ter duas
        # "vistas" no mesmo dia
        while not valido and linha < 30:
            T.clique("1770063257886.png")
            T.espere("baixa_financeiro_procurar_conta.png")
            type(Key.ENTER)
            T.espere(1)
            T.clique("baixa_financeiro_codigo.png")
            for _ in range(linha): type(Key.DOWN)
            type(Key.ENTER)
    
            T.espere(0.2)
            type('s', Key.CTRL)
            T.espere(Constantes.BOTAO_OK, 6)
            if FuncoesAuxiliares.aviso_contem("Sucesso"): valido = True
            type(Key.ENTER)
    
    @staticmethod
    def vistar_conta():
        T.espere_e_clique(Constantes.BOTAO_PROCURAR)
        T.espere(0.8)
        T.clique("baixa_financeiro_contas_a_pagar.png")
        T.clique(Pattern("baixa_financeiro_vistar_conta.png").similar(0.80))
        type('11')
        type('v', Key.ALT)
        T.espere(2)
        type(Key.ENTER) 

    @staticmethod
    def fechar_janelas(qtdd): FuncoesAuxiliares.sair(qtdd)

# ---------------------------------------------------------------------------------------------------------------------------
# Cadastro cliente
# ---------------------------------------------------------------------------------------------------------------------------
class CadastroCliente(TesteAbstrato):

    @staticmethod
    def __str__(): return 'CadastroCliente'
    
    @classmethod
    def _executar(cls):
        FuncoesAuxiliares.inform_rotina('1')

        cls.entrada_dados_1()

        # Reduz a área de busca de algumas imagens, portanto também o tempo de execução
        regiao = Region(1,91,388,516)
        
        FuncoesAuxiliares.insere_cnpj(regiao)
        cls.entrada_dados_2()

    @staticmethod
    def entrada_dados_1():
        T.espere(2)
        if exists(Constantes.BOTAO_OK): type(Key.ENTER)
        T.espere(Constantes.BOTAO_NOVO)
        type(Key.F8)

    @staticmethod
    def entrada_dados_2():
        if exists(Pattern("cadastro_cliente_input_email.png").similar(0.90).targetOffset(-2,5)): type(Pattern("cadastro_cliente_input_email.png").similar(0.90).targetOffset(-2,5), 'testecliente.gap@gmail.com')
        if exists(Pattern("cadastro_cliente_input_telefone.png").similar(0.85).targetOffset(-12,7)): type(Pattern("cadastro_cliente_input_telefone.png").similar(0.85).targetOffset(-12,7), ('7'*11))
        
        T.clique(Pattern("cadastro_cliente_vendedor.png").similar(0.80))
        T.espere(0.2)
        T.clique(Pattern("cadastro_cliente_input_vendedor.png").similar(0.80).targetOffset(-21,6))
        type('1')
        type(Key.TAB)
        type('1')
        type(Key.TAB)
        type(Key.TAB)
        type('17')
        T.clique(Constantes.BOTAO_MAIS)
        type('s', Key.CTRL)
        T.espere(3)
        type(Key.ENTER)
        T.espere(0.2)
        FuncoesAuxiliares.sair(2)

# ---------------------------------------------------------------------------------------------------------------------------
# Cadastro fornecedor
# ---------------------------------------------------------------------------------------------------------------------------
class CadastroFornecedor(TesteAbstrato):

    @staticmethod
    def __str__(): return 'CadastroFornecedor'

    @classmethod
    def _executar(cls):
        FuncoesAuxiliares.inform_rotina('32')
        cls.entrada_dados_1()
    
        # Reduz a área de busca de algumas imagens, portanto também o tempo de execução
        regiao = Region(0,66,435,300)
        
        FuncoesAuxiliares.insere_cnpj(regiao)
        cls.entrada_dados_2()

    @staticmethod
    def entrada_dados_1():
        T.espere(0.9)
        if FuncoesAuxiliares.aviso_contem('Este cliente possui'): type(Key.ENTER)
        T.espere(Constantes.BOTAO_NOVO)
        type(Key.F8)

    @staticmethod
    def entrada_dados_2():    
        T.espere(0.4)
        T.clique(Pattern("cadastro_fornecedor_input_tipo_fiscal.png").similar(0.80).targetOffset(-23,8))
        type('a', Key.CTRL)
        type('1')
       
        type('s', Key.CTRL)
        FuncoesAuxiliares.espere_aviso_conter("Sucesso")
        type(Key.ENTER)
        T.espere(0.5)
        FuncoesAuxiliares.sair(1)

# ---------------------------------------------------------------------------------------------------------------------------
# Cadastro produto
# ---------------------------------------------------------------------------------------------------------------------------
class CadastroProduto(TesteAbstrato):

    @staticmethod
    def __str__(): return 'CadastroProduto'

    @classmethod
    def _executar(cls):
        FuncoesAuxiliares.inform_rotina('2')
        cls.entrada_dados()
        cls.salvar()

    @staticmethod
    def entrada_dados():
        T.espere(Constantes.BOTAO_NOVO)
        type(Key.F8)
        T.espere(0.5)
        FuncoesAuxiliares.multiplos_tabs(2)    
        type('1')                        # Sub-grupo
        FuncoesAuxiliares.multiplos_tabs(2)    
        type('1')                        # Grupo
        type(Key.TAB) 
        type('1')                        # Fornecedor
        FuncoesAuxiliares.multiplos_tabs(5)
        type('teste cadastro produto')
        type(Key.TAB)
        type('gap')
        type(Pattern("cadastro_produto_input_calc_fiscal.png").similar(0.80), "1")
        T.clique(Pattern("cadastro_produto_input_preco_final.png").similar(0.80).targetOffset(116,-22))
        type(Key.TAB)
        type('1')
        type(Key.TAB)
        type('1')

    @staticmethod
    def salvar():
        T.espere(0.2)
        type('s', Key.CTRL)
        FuncoesAuxiliares.espere_aviso_conter("Deseja que seja gerado?", compreensivo=True)
        type(Key.ENTER)
        T.espere(0.3)
        type(Key.ENTER)
        T.espere(1.8)
        type(Key.ENTER)
        FuncoesAuxiliares.sair(1)

# ---------------------------------------------------------------------------------------------------------------------------
# Criacao boleto
# ---------------------------------------------------------------------------------------------------------------------------
class CriacaoBoleto(TesteAbstrato):

    @staticmethod
    def __str__(): return 'CriacaoBoleto'

    @classmethod
    def _executar(cls):
        FuncoesAuxiliares.inform_rotina('96')
        cls.entrada_dados_1()
        cls.entrada_n_doc()
        cls.entrada_dados_2()
        cls.cobranca_bancaria()
        FuncoesAuxiliares.sair(3)

    @staticmethod
    def entrada_dados_1():
        T.espere(1.5)
        type(Key.F8)
        T.espere(Constantes.BOTAO_SALVAR, 8)
        type(Pattern("criacao_boleto_input_financeiro.png").similar(0.85).targetOffset(10,-11), "teste criacao boleto - gap")

    @staticmethod
    def entrada_n_doc():
        valido = False
        cont = 0
        
        while not valido and cont < 10:
            cont += 1
            numero_1 = random.randint(0, 1000000)
            numero_2 = random.randint(0, 999)
    
            T.clique(Pattern("criacao_boleto_input_documento.png").targetOffset(59,0))
            type(str(numero_1))
            type(Key.TAB)
            type(str(numero_2))
            type(Key.TAB)
            type(Key.TAB)
            if exists(Pattern("criacao_boleto_input_documento.png").similar(0.85)): 
                type(Key.ENTER)
            else: valido = True    

    @staticmethod
    def entrada_dados_2():
        type('11')
        T.clique("criacao_boleto_editar_conta.png")
        T.clique(Pattern("criacao_boleto_situacao.png").targetOffset(64,2))
        type(Key.DOWN)
        type(Key.DOWN)
        type(Key.ENTER)
        type(Pattern("criacao_boleto_input_valor.png").similar(0.86).targetOffset(22,-1), str(random.randint(1, 9)))
        type(Key.TAB)    
        type(Key.TAB)
        type('12')
        T.clique(Constantes.BOTAO_MAIS)
        T.espere(0.5)
        type('s', Key.CTRL)
        T.espere(Constantes.BOTAO_OK, 5)
        type(Key.ENTER)
        T.espere(0.2)

    @staticmethod
    def cobranca_bancaria():
        type('m', Key.ALT)
        for _ in range(2): type(Key.DOWN)
        type(Key.ENTER)
        T.espere(0.2)
        T.espere(Constantes.BOTAO_SIM)
        type(Key.ENTER)
        T.espere(0.5)
        type(Pattern("criacao_boleto_input_cobranca.png").similar(0.85).targetOffset(10,11), "11")
        type(Key.TAB)
        type('32')
        type('g', Key.ALT)
        T.espere(Constantes.BOTAO_SIM)
        type(Key.ENTER)
        T.espere(1)
        type(Key.ESC)

# ---------------------------------------------------------------------------------------------------------------------------
# Criacao contrato
# ---------------------------------------------------------------------------------------------------------------------------
class CriacaoContrato(TesteAbstrato):

    @staticmethod
    def __str__(): return 'CriacaoContrato'

    @classmethod
    def _executar(cls):
        FuncoesAuxiliares.inform_rotina('221')
        cls.entrada_dados()
        cls.inserir_item()
        FuncoesAuxiliares.sair(1)

    @staticmethod
    def entrada_dados():
        T.espere(Constantes.BOTAO_NOVO)
        T.clique(Constantes.BOTAO_NOVO)
        T.espere(1)
        FuncoesAuxiliares.multiplos_tabs(3)
        type('11')
        type(Key.TAB)
        type(Key.TAB)
        type('11')
        FuncoesAuxiliares.multiplos_tabs(9)
        type('714')
        T.espere(1)

    @staticmethod
    def inserir_item():
        T.clique("criacao_contrato_botao_inserir_item.png")
        T.espere(1)
        if exists("criacao_contrato_botao_tirar_item.png"):
            T.clique("criacao_contrato_botao_tirar_item.png")
            type('s', Key.ALT)
            type(Key.ENTER)
        T.clique(Pattern("criacao_contrato_input_produto.png").similar(0.85).targetOffset(-22,9))
        type('1')
        type(Key.TAB)
        type(Key.TAB)
        type('100')
        T.clique(Constantes.BOTAO_MAIS)
        if FuncoesAuxiliares.aviso_contem("maximo de rateio possivel"): type(Key.ENTER)       # exists("criacao_contrato_maximo_rateio.png"): type(Key.ENTER)
        T.clique(Pattern("criacao_contrato_botao_fechar.png").similar(0.83))

        T.espere(2)
        type('o', Key.ALT)
        T.espere(1)

# ---------------------------------------------------------------------------------------------------------------------------
# Entrada de nota fiscal abstrato
# ---------------------------------------------------------------------------------------------------------------------------
class EntradaNfAbstrato(TesteAbstrato):            # Reutilizar código entre ambas as classes de entrada de nota fiscal

    # Se der o aviso "data de entrada contempla o período já fechado", a data de entrada vai ser trocada para 3000
    @classmethod
    def troca_data_3000(cls):
        if FuncoesAuxiliares.aviso_contem("periodo ja fechado"):         # exists("entrada_nf_aviso_periodo_entrada_fechado.png"):
            type(Key.ENTER)
            T.clique(Pattern("entrada_nf_aba_calculo.png").similar(0.87))
            type(Pattern("entrada_nf_aba_data_entrada.png").similar(0.80).targetOffset(121,-1), '3000')
            return cls.finalizar()

    @staticmethod
    def insere_produto():
        T.clique(Pattern("entrada_nf_dados_produtos.png").similar(0.85))
        T.espere(1)
        FuncoesAuxiliares.multiplos_tabs(2)
        type('1')
        FuncoesAuxiliares.multiplos_tabs(2)
        type('4')
        type(Key.TAB)
        type('1')
        FuncoesAuxiliares.multiplos_tabs(2)
        type('1')
        T.clique(Constantes.BOTAO_MAIS)

# ---------------------------------------------------------------------------------------------------------------------------
# Entrada de nota fiscal 
# ---------------------------------------------------------------------------------------------------------------------------
class EntradaNf(EntradaNfAbstrato):

    @staticmethod
    def __str__(): return 'EntradaNf'

    @classmethod
    def _executar(cls):
        FuncoesAuxiliares.inform_rotina('152')
        cls.entrada_dados_1()
        cls.entrada_n_doc()
        cls.entrada_dados_2()
        cls.finalizar()
        FuncoesAuxiliares.sair(1)

    @staticmethod
    def entrada_dados_1():
        T.espere(Constantes.BOTAO_NOVO)
        type(Key.F8)
        T.espere(Constantes.BOTAO_SALVAR)
        type(Key.TAB)
        type('1')
    
    @staticmethod   
    def entrada_n_doc():
        valido = False
        
        while not valido:
            numero_1 = random.randint(0, 1000000)
            numero_2 = random.randint(0, 1000000)
            type(Pattern("entrada_nf_input_n_doc.png").targetOffset(-6,0), str(numero_1))
            type(Key.TAB)
            type(str(numero_2))
            type(Key.TAB)
            T.espere(0.2)
    
            if FuncoesAuxiliares.aviso_contem("Documento sendo usado"):        # exists("entrada_nf_aviso_documento_usado.png"): 
                type(Key.ENTER)
            else: valido = True
            
    @classmethod
    def entrada_dados_2(cls):
        type('1')
        FuncoesAuxiliares.multiplos_tabs(5)
        type('4')
        FuncoesAuxiliares.multiplos_tabs(19)
        type('01')
        cls.insere_produto()        
    
    @classmethod
    def finalizar(cls):
        T.espere(0.5)
        type('f', Key.ALT)
        T.espere(0.5)
        type(Key.ENTER)
        T.espere(Constantes.BOTAO_NAO, 5)
        T.clique(Constantes.BOTAO_NAO)
        T.espere(Constantes.BOTAO_OK, 5)

        cls.troca_data_3000()
            
        type(Key.ENTER)
        T.espere(0.3)
        if exists(Constantes.BOTAO_NAO): T.clique(Constantes.BOTAO_NAO)
        T.espere(0.2)
        if exists(Constantes.BOTAO_NAO): T.clique(Constantes.BOTAO_NAO)
        T.espere(0.2)

# ---------------------------------------------------------------------------------------------------------------------------
# Entrada de nota fiscal por XML
# ---------------------------------------------------------------------------------------------------------------------------
class EntradaNfXml(EntradaNfAbstrato):

    @staticmethod
    def __str__(): return 'EntradaNfXml'

    @classmethod
    def _executar(cls):
        FuncoesAuxiliares.inform_rotina('152')
        cls.entrada_dados_1()
        cls.opta_por_xml()
        cls.encontra_xml()
        cls.entrada_dados_2()
        cls.finalizar()  
        cls.excluir()
        FuncoesAuxiliares.sair(1)
        
    @staticmethod
    def entrada_dados_1():
        T.espere(Constantes.BOTAO_NOVO, 5)
        type(Key.F8)
        T.espere(0.5)
    
    @staticmethod 
    def opta_por_xml():
        T.espere(0.5)
        type('m', Key.ALT)
        T.espere(0.5)
        type(Key.DOWN)
        type(Key.ENTER)
        type(Key.ENTER)
        T.espere(2)
    
    @classmethod
    def encontra_xml(cls):
        # Aparece no início
        if cls.tentativa_busca_xml(): return
    
        # Aparece em um dos lugares mais prováveis
        lugares_possives = [Pattern("entrada_nf_xml_area_de_trabalho.png").similar(0.90), Pattern("entrada_nf_xml_documentos.png").similar(0.90), Pattern("entrada_nf_xml_downloads.png").similar(0.90), Pattern("entrada_nf_xml_imagens.png").similar(0.90)]
    
        for lugar in lugares_possives:
            if exists(lugar):
                T.clique(lugar)
                if cls.tentativa_busca_xml(): return
    
        raise FindFailed ("Nao foi possivel encontrar nenhum arquivo XML")
    
    @classmethod
    def tentativa_busca_xml(cls):
        T.espere(0.8)
        if exists(Pattern("entrada_nf_xml_icone_edge.png").similar(0.80)):
            T.duplo_clique(Pattern("entrada_nf_xml_icone_edge.png").similar(0.80).targetOffset(41,-1))
            T.espere(0.5)
            if FuncoesAuxiliares.aviso_contem("Confirma", centralizado=False, compreensivo=True): return True
            else: 
                raise RuntimeError("Ocorreu um erro durante a importacao da nota")
    
        return False
    
    @classmethod
    def entrada_dados_2(cls):
        T.espere(0.2)
        type(Key.ENTER)
        T.espere("entrada_nf_xml_botao_ok.png", 5)
        T.espere(1)
        T.clique("entrada_nf_xml_botao_ok.png")
        T.espere(0.5)
        type(Key.ENTER)
        T.espere(1)
        if exists(Constantes.BOTAO_OK): type(Key.ENTER)
        T.espere(1)
        if not exists(Pattern("entrada_nf_xml_item_1.png").similar(0.90)): cls.insere_produto()
            
    
    @classmethod
    def finalizar(cls):
        type('f', Key.ALT)
        T.espere(0.5)

        if exists("entrada_nf_xml_doc_usado.png"):
            numero_doc = find("entrada_nf_xml_doc_usado.png").text()[-14:]
            type(Key.ENTER)
            T.espere(0.1)
            type(Key.F8)
            type(Pattern("entrada_nf_xml_input_n_mov.png").targetOffset(43,-1), numero_doc)
            type(Key.TAB)
            cls.excluir()
            return cls._executar()

        cls.troca_data_3000()
        
        type(Key.ENTER)
        T.espere(0.5)
        if exists(Constantes.BOTAO_NAO): T.clique(Constantes.BOTAO_NAO)
        if exists(Constantes.BOTAO_NAO): T.clique(Constantes.BOTAO_NAO)
        T.espere(0.2)
        if exists(Constantes.BOTAO_OK): T.clique(Constantes.BOTAO_OK)
        T.espere(0.2)
        if exists(Constantes.BOTAO_NAO): T.clique(Constantes.BOTAO_NAO)
        T.espere(0.2)
        if exists(Constantes.BOTAO_NAO): T.clique(Constantes.BOTAO_NAO)
        T.espere(0.2)
    
    @staticmethod
    def excluir():
        T.clique(Constantes.BOTAO_EXCLUIR)
        T.espere(Constantes.BOTAO_SIM)
        type(Key.ENTER)
        T.espere(Constantes.BOTAO_OK, 7)
        type(Key.ENTER)
        T.espere(0.5)

# ---------------------------------------------------------------------------------------------------------------------------
# Faturamento contrato
# ---------------------------------------------------------------------------------------------------------------------------
class FaturamentoContrato(TesteAbstrato):

    @staticmethod
    def __str__(): return 'FaturamentoContrato'

    @classmethod
    def _executar(cls):
        FuncoesAuxiliares.inform_rotina("221")
        cls.gera_nf()
        
        FuncoesAuxiliares.inform_rotina("133")
        cls.integra_contrato()

        FuncoesAuxiliares.sair(2)

    @staticmethod
    def gera_nf():
        # if FuncoesAuxiliares.aviso_contem("Selecione os contratos"): type(Key.ENTER)
        # Ordem decrescente
        T.espere(Constantes.BOTAO_NOVO, 7)
        if exists(Pattern("faturamento_contrato_contratos_todos.png").similar(0.90).targetOffset(30,1)):
            T.clique(Pattern("faturamento_contrato_contratos_todos.png").similar(0.90).targetOffset(30,1))
            for _ in range(2): type(Key.DOWN)
            type(Key.ENTER)
            T.clique(Constantes.BOTAO_PROCURAR)
            T.espere(0.3)
            
        regiao = find(Pattern("faturamento_contrato_id_decrescente.png").similar(0.80))
        
        while not regiao.has(Pattern("faturamento_contrato_id_dec_seta.png").similar(0.80)): 
            T.clique(regiao)
            T.espere(1)
    
        T.clique("faturamento_contrato_desmarcar_todos.png")
        
        if not exists(Pattern("faturamento_contrato_sel_contrato.png").similar(0.85)): raise RuntimeError ("Nao ha contratos para gerar NF")
        
        T.clique(Pattern("faturamento_contrato_sel_contrato.png").similar(0.85))
        type("n", Key.ALT)
        T.espere(0.7)
            
        T.espere_e_clique(Pattern("faturamento_contrato_botao_ok_upper.png").similar(0.80), 8)
        T.espere(0.5)
        if FuncoesAuxiliares.aviso_contem("possuem NF gerada"): type(Key.ENTER)
        if exists(Pattern("faturamento_contrato_botao_ok_capital.png").similar(0.85)): T.clique(Pattern("faturamento_contrato_botao_ok_capital.png").similar(0.85)) 
        else: T.clique(Pattern("faturamento_contrato_botao_ok_capital_subl.png").similar(0.85))
    
        FuncoesAuxiliares.espere_aviso_conter("Gerando", compreensivo=True, centralizado=True)
        type(Key.ENTER)

    @staticmethod
    def integra_contrato():
        T.espere("faturamento_contrato_botao_desmarcar.png", 8)
        type('d', Key.ALT)
        T.clique(Pattern("faturamento_contrato_sel_contrato_pedido.png").similar(0.90).targetOffset(1,33))
        T.clique(Pattern("faturamento_contrato_botao_integrar_nf.png").similar(0.85))
        T.espere_e_clique(Pattern("faturamento_contrato_botao_integrar.png").similar(0.90))
        T.espere(0.2)
    
        if FuncoesAuxiliares.aviso_contem("Existem pedidos que ja estao sendo faturados", compreensivo=False):
            raise RuntimeError(
                    'O teste nao pode ser concluido: "Existem pedidos que ja estao sendo faturados ou nao estao em faturamento mais"'
                    )
        T.espere(2)

# ---------------------------------------------------------------------------------------------------------------------------
# Geracao remessa
# ---------------------------------------------------------------------------------------------------------------------------
class GeracaoRemessa(TesteAbstrato):

    @staticmethod
    def __str__(): return 'GeracaoRemessa'

    @classmethod
    def _executar(cls):
        FuncoesAuxiliares.inform_rotina('150')
        cls.entrada_dados_1()

    @staticmethod
    def entrada_dados_1():
        type(Key.F8)
        T.espere(1)
        type('748')
        type(Key.TAB)
        type('32')
        type(Key.TAB)
        type(Key.ENTER)
        T.espere(0.8)
        type('g', Key.ALT)
        T.espere(1.5)
        if FuncoesAuxiliares.aviso_contem("Nao ha item selecionado"): 
            raise RuntimeError("Nao ha boletos gerados \nrode CriacaoBoleto._executar() para criar um boleto")       # exists("gerar_remessa_aviso_nenhum_item_sel.png"): 
        type(Key.ENTER)
        T.espere(0.3)
        FuncoesAuxiliares.sair(1)

# ---------------------------------------------------------------------------------------------------------------------------
# Geracao ocorrencia
# ---------------------------------------------------------------------------------------------------------------------------
class Ocorrencia(TesteAbstrato):

    @staticmethod
    def __str__(): return 'Ocorrencia'

    @classmethod
    def _executar(cls):
        FuncoesAuxiliares.inform_rotina('407')
        cls.cria_ocorrencia()
        
        FuncoesAuxiliares.inform_rotina('133')
        cls.integra_pedido()
        
        FuncoesAuxiliares.sair(2)

    @staticmethod
    def cria_ocorrencia():
        T.espere(Constantes.BOTAO_NOVO, 8)
        type(Key.F8)
        T.espere(Constantes.BOTAO_EXCLUIR, 5)
    
        # Dados de texto
        type('1')
        type(Key.TAB)
        type('2')
        FuncoesAuxiliares.multiplos_tabs(4)
        type('2')
        FuncoesAuxiliares.multiplos_tabs(10)
        type("teste ocorrencia - gap")
        type(Key.TAB)
        type('11')

        # Insere item
        T.clique(Pattern("ocorrencia_aba_itens.png").similar(0.85))
        T.espere(0.2)
        FuncoesAuxiliares.multiplos_tabs(2)
        type('1')
        type(Key.TAB)
        T.clique(Constantes.BOTAO_MAIS)        
    
        # Pedido de venda
        T.espere(0.5)
        type('m', Key.ALT)
        T.espere(0.5)
        for _ in range(6): type(Key.UP)
        type(Key.ENTER)
        T.espere(1)
        FuncoesAuxiliares.sair(1)
        T.espere(0.5)
    
    @staticmethod
    def integra_pedido():
        T.espere(Constantes.BOTAO_SAIR, 8)
        type('d', Key.ALT)
        T.clique(Pattern("ocorrencia_selecionar.png").similar(0.90).targetOffset(1,33))
        T.clique("ocorrencia_integrar_nf.png")
        T.espere_e_clique(Pattern("ocorrencia_integrar.png").similar(0.85))
    
        if FuncoesAuxiliares.aviso_contem("Nao ha item selecionado", compreensivo=False):
            raise RuntimeError(
                    'O teste nao pode ser concluido: "Existem pedidos que ja estao sendo faturados ou nao estao em faturamento mais"'
                    )

# ---------------------------------------------------------------------------------------------------------------------------
# Pagamento de nota
# ---------------------------------------------------------------------------------------------------------------------------
class PagamentoNota(TesteAbstrato):

    @staticmethod
    def __str__(): return 'PagamentoNota'

    @classmethod
    def _executar(cls):
        FuncoesAuxiliares.inform_rotina("155")
        cls.filtrando()
        cls.entrada_dados_1()
        cls.salvando()

    @staticmethod
    def filtrando():
        if exists(Constantes.PESQUISA_AVANCADA): T.clique(Constantes.PESQUISA_AVANCADA)
        T.espere(1)

        if find(Pattern("pagamento_nota_todos_os_vencidos.png").similar(0.85)).has(Constantes.CHECKBOX_FuncoesAuxiliaresLSE): T.clique(Pattern("pagamento_nota_todos_os_vencidos.png").similar(0.85).targetOffset(-47,0))
    
        if exists(Constantes.OCULTAR): T.clique(Constantes.OCULTAR)
        T.clique(Constantes.BOTAO_PROCURAR)            
        T.espere(Pattern("pagamento_nota_sel_conta.png").targetOffset(36,1), 5)
        T.espere(2)
        T.clique(Pattern("pagamento_nota_emissao.png").similar(0.90))
        T.espere(0.5)
        T.clique(Pattern("pagamento_nota_emissao.png").similar(0.90))
        T.espere(0.5)
    
    @staticmethod 
    def entrada_dados_1():
        T.duplo_clique(Pattern("pagamento_nota_sel_conta.png").targetOffset(36,1))
        T.espere(Constantes.BOTAO_SALVAR)
        for _ in range(4): type(Key.DOWN)
        type(Key.ENTER)
        
        T.clique(Pattern("pagamento_nota_alterar.png").similar(0.85))
        dragDrop(Pattern("pagamento_nota_input_cobranca.png").similar(0.85).targetOffset(44,0), Pattern("pagamento_nota_input_cobranca.png").similar(0.85).targetOffset(25,0))
        type('c', Key.CTRL)
        T.clique(Pattern("pagamento_nota_alterar.png").similar(0.78).targetOffset(-28,1))
        T.clique(Pattern("pagamento_nota_input_baixa.png").similar(0.85).targetOffset(24,0))
        type('a', Key.CTRL)
        type('v', Key.CTRL)
        type(Key.TAB)
        type('8')
        FuncoesAuxiliares.multiplos_tabs(16)
        type(Key.ENTER)
        T.espere(Pattern("pagamento_nota_pesquisar_em_negrito.png").similar(0.80))
        type(Key.ENTER)
        T.espere(2)
        type(Key.ENTER)
        T.espere(0.5)
    
    @staticmethod
    def salvando():
        type('s', Key.CTRL)
        T.espere(2)
        type(Key.ENTER)
        FuncoesAuxiliares.sair(2)


if __name__ == '__main__':
    main()