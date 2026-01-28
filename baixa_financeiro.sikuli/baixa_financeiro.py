# coding=utf-8
import random


def entrar_erp():
    if find("logo_erp.png"):
        if exists(Pattern("pesquisa_rotina.png").similar(0.80).targetOffset(31,-4)): return
        click(Region(0,1139,1920,61).find("logo_erp.png"))
        if exists(Pattern("pesquisa_rotina.png").similar(0.80).targetOffset(31,-4)): return
        inform_dados_usuario()    
    
    else:    
        type(Key.WIN)
        type("erpmts")
        type(Key.ENTER)
        inform_dados_usuario()


def inform_dados_usuario():
    wait(Pattern("input_usuario.png").targetOffset(-48,3), 15)
    type(Pattern("input_usuario.png").targetOffset(-48,3), "mitis")
    type(Key.TAB)
    type("mitis01")
    type(Key.TAB)
    type("109")
    type(Key.TAB)
    type(Key.ENTER)
    if exists("botao_nao.png"): click("botao_nao.png")


def inform_rotina(codigo):
    wait(Pattern("pesquisa_rotina.png").similar(0.80).targetOffset(31,-4), 15)
    click(Pattern("pesquisa_rotina.png").similar(0.80).targetOffset(31,-4))
    wait(1)
    type(codigo)
    type(Key.ENTER)
    wait(1)


def criacao_conta_1():
    wait("contas_pagar.png")
    type(Key.F8)
    wait("botao_novo.png", 5)
    click("botao_novo.png")
    type("teste baixa financeiro - gap")
    type(Key.TAB)
    type(Key.TAB)
    type("11")
    type(Key.TAB)


def entrada_n_doc():
    valido = False
    
    while not valido:
        numero_1 = random.randint(0, 1000000)
        numero_2 = random.randint(0, 999)

        click(Pattern("input_documento.png").targetOffset(32,-1))
        type(str(numero_1))
        type(Key.TAB)
        type(str(numero_2))
        type(Key.TAB)
        if exists("alerta_usado.png"): 
            type(Key.ENTER)
        else: valido = True    


def criacao_conta_2():
    click(Pattern("data_entrada.png").similar(0.89).targetOffset(-43,-1))
    click(Pattern("data_emissao.png").similar(0.86).targetOffset(-47,-1))
    valor = str(random.randint(1,9))
    type("input_valor.png", valor)
    type(Key.TAB)
    type(Key.TAB)
    type("11")
    type(Pattern("input_rateio.png").targetOffset(-27,11), "1")
    type(Key.TAB)
    type(valor)
    click("botao_mais.png")
    wait(0.2)
    type("s", Key.CTRL)
    wait("botao_ok.png")
    type(Key.ENTER)
    wait(0.2)
    click(Pattern("botao_sair.png").similar(0.79).targetOffset(-1,30))
    wait(2)


def verifica_filtros():
    if exists(Pattern("ultima_conta.png").similar(0.89).targetOffset(5,-13)): return
    
    if exists("pesquisa_avancada.png"): type("p", Key.ALT)
    
    regiao = find("filtros_tipos.png")

    while regiao.has("botao_check_true.png"):
        click(regiao.find("botao_check_true.png"))

    aberto = regiao.find("filtro_aberto.png")
    if aberto.has("botao_check_false.png"): click(aberto.find("botao_check_false.png"))
    click("botao_procurar.png")

    wait(1)
    if not exists(Pattern("ultima_conta.png").similar(0.89).targetOffset(5,-13)): 
        click(Pattern("qualquer_data.png").similar(0.88).targetOffset(-48,-2))
        click("botao_procurar.png")
        wait(1)

    click("ocultar.png")
    

def baixa_conta():
    wait(2)
    doubleClick(findBest(Pattern("ultima_conta.png").similar(0.89).targetOffset(5,-13)))
    wait(0.5)
    click(Pattern("situacao_aberto.png").targetOffset(64,10))
    click(Pattern("situacoes.png").targetOffset(-47,51))
    type(Pattern("baixa.png").targetOffset(32,1), "11")
    type(Key.TAB)

    escolhe_conta_e_salva()
    
    wait(Pattern("botao_sair.png").similar(0.83).targetOffset(-2,30))
    click(Pattern("botao_sair.png").similar(0.83).targetOffset(-2,30))


def escolhe_conta_e_salva():
    linha = 0
    valido = False

    # Escolhe uma conta bancaria para a baixa, 
    # porque uma mesma conta nao pode ter duas
    # "vistas" no mesmo dia
    while not valido and linha < 30:
        click(Pattern("lupa_contas.png").targetOffset(-2,39))
        wait("procurar_conta.png")
        type(Key.ENTER)
        wait(1)
        click("codigo.png")
        for _ in range(linha): type(Key.DOWN)
        type(Key.ENTER)

        wait(0.2)
        type("s", Key.CTRL)
        wait("botao_ok.png", 6)
        if exists("sucesso.png"): valido = True
        type(Key.ENTER)


def vistar_conta():
    click("botao_procurar.png")
    wait(0.8)
    click(Pattern("tipo_financeiro.png").targetOffset(0,25))
    click("vistar_conta.png")
    type("11")
    type("v", Key.ALT)
    wait(2)
    type(Key.ENTER) 


def sair():
    type(Key.ESC)
    type(Key.ENTER)
    wait(0.2)
    type(Key.ESC)
    type(Key.ENTER)


def main():
    entrar_erp()
    inform_rotina("155")
    
    # Criacao da conta
    criacao_conta_1()
    entrada_n_doc()
    criacao_conta_2()

    # Baixa da conta
    verifica_filtros()
    baixa_conta()

    # Vistar conta
    inform_rotina("254")
    vistar_conta()

    sair()


if __name__ == "__main__":
    main()