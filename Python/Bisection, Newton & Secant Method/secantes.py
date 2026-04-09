def funcao(x):
    return 6*(x**5) - 14*(x**4) + 21*(x**3) - 49*(x**2) - 12*x + 28

# numero maximo de iteracoes
maxiter = 30

ctn = (str(input('Escrever novos resultados? y/n :')))
while (ctn == 'y'):

    # Abre e escreve o cabecalho no arquivo de texto na forma tabulada
    f = open('secantes_output1.txt', 'w')
    f.write("{:<25}{:<25}{:<25}{:<25}\n".format("Iteracao k", "xk", "f(xk)","ek"))

    a = float(input('Defina: a = '))
    b = float(input('Defina: b = '))
    raiz = float(input('Defina: Raiz = '))

    # i = contador de iteraçoes, comeca no 2 devido a x0 e x1 serem os intervalos
    i = 2
    erro = 0.0

    #cria um array de 30 posiçoes para guardar xk
    x = [0.0] * 30

    # entre com intervalos no array e grava as iteracoes iniciais no arquivo
    x[0] = a
    f.write("{:<25}{:<25}{:<25}{:<25}\n".format(0, x[0], funcao(x[0]), abs(x[0]-raiz)))
    x[1] = b
    f.write("{:<25}{:<25}{:<25}{:<25}\n".format(1, x[1], funcao(x[1]), abs(x[1]-raiz)))

    # ??? encontrar um jeito de comparar os xk consecutivos sem quebrar a condicao do erro relativo
    while(abs(x[i-1]-x[i-2]) >= 0.000001*max(1,abs(x[i-1])) and i<maxiter):
        f1 = funcao(x[i-1])
        f2 = funcao(x[i-2])
        xk = ((f1*x[i-2]) - (f2*x[i-1]))/(f1-f2)
        erro = abs(xk-erro)
        f.write("{:<25}{:<25}{:<25}{:<25}\n".format(i, x[i], funcao(x[i]), erro))
        i+=1
    ctn = (str(input('Continuar? y/n :')))

f.close()
quit()
