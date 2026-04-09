#Funcao para o calculo de f(x)
def funcao(x):
    return 6*(x**5) - 14*(x**4) + 21*(x**3) - 49*(x**2) - 12*x + 28

fa = fb = 0.0

# maxiter = numero maximo de iteracoes
maxiter = 30

# abre o arquivo de texto para gravar as saidas
f = open('biseccao_output1.txt', 'w')

ctn = (str(input('Escrever novos resultados? y/n :')))
while (ctn == 'y'):

    # escreve o cabecalho no arquivo de texto de forma tabulada
    f.write("{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}\n".format("Iteracao k", "a", "b", "xk", "f(xk)", "ek"))

    # Define o intervalo e raiz almejada
    a = float(input('Defina: a = '))
    b = float(input('Defina: b = '))
    raiz = float(input('Defina: Raiz = '))

    # i = contador de iteraçoes
    i = 0

    erro = 1.0
    fa = funcao(a)
    fb = funcao(b)
    fxk = xk = 1.0
    tmp = 0

    # Condicao base para raiz
    if (fb * fa < 0):

        # implementacao do loop condicional usando erro relativo (Aula 2)
        while (abs(xk-tmp) >= 0.000001*max(1,abs(xk-tmp)) and i<maxiter):

            # tmp = variavel temporavel para guardar xk-1
            tmp = xk
            xk = (a + b)/2
            fxk = funcao(xk)
            erro = abs(xk - raiz)

            # escreve os resultados no arquivo de texto de forma tabulada
            f.write("{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}\n".format(i, a, b, xk, fxk, erro))

            # caso a funcao encontre o caso perfeito
            if (fxk == 0):
                break
            else:

                # condicionais para determinar qual intervalo escolher
                if (fa * fxk < 0):
                    b = xk
                    fb = fxk

                else:
                    if (fxk * fb < 0):
                        a = xk
                        fa = fxk
                    else:
                        break
            i += 1
    else:
        print("Nao ha raiz nesse intervalo")
    ctn = (str(input('Continuar? y/n :')))
f.close()
quit()
