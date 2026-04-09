# funcao para o calculo de f(x)
def funcao(x):
    return 6*(x**5) - 14*(x**4) + 21*(x**3) - 49*(x**2) - 12*x + 28

# funcao para o calculo de f'(x)
def funcao_der(x):
    return 30*(x**4) - 56*(x**3) + 63*(x**2) - 98*x - 12

# maxiter = numero maximo de iteracoes
maxiter = 30

# abre o arquivo de texto para gravar as saidas
f = open('newton_output1.txt', 'w')

ctn = (str(input('Escrever novos resultados? y/n :')))
while (ctn == 'y'):

    # escreve o cabecalho no arquivo de texto de forma tabulada
    f.write("{:<25}{:<25}{:<25}{:<25}{:<25}\n".format("Iteracao k", "xk", "f(xk)", "f'(xk)","ek"))

    # Define o intervalo e raiz almejada
    a = float(input('Defina: a = '))
    b = float(input('Defina: b = '))
    raiz = float(input('Defina: Raiz = '))

    # i = contador de iteraçoes
    i = 0

    erro = 1.0

    #define xk inicial como ponto medio
    xk = a+b/2

    # tmp = variavel temporavel para guardar xk-1
    tmp = 0.0

    # implementacao do loop condicional usando erro relativo (Aula 2)
    while(abs(xk-tmp) >= 0.000001*max(1,abs(xk)) and i<maxiter):
        tmp = xk
        xk = tmp - funcao(tmp)/funcao_der(tmp)
        erro = abs(xk-raiz)

        # escreve os resultados no arquivo de texto de forma tabulada
        f.write("{:<25}{:<25}{:<25}{:<25}{:<25}\n".format(i,xk,funcao(xk),funcao_der(xk),erro))

        i+=1
    ctn = (str(input('Continuar? y/n :')))

f.close()
quit()
