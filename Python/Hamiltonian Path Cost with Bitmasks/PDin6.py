def costMinHamilton(n,adj,start):
    
    infinite = float('inf')

    # Tabela de programação dinâmica onde dp[mask][i] é o custo de chegar a cidade i, percorrendo caminho correspondente a máscara mask
    dp = [[infinite] * n for _ in range(1 << n)]

    # Caso base começando na cidade especificado
    dp[1 << start][start] = 0
    
    # Populando tabela de programação dinâmica
    for mask in range(1 << n):
        for i in range(n):
            if dp[mask][i] < infinite:
                for j in range(n):
                    if (mask & (1 << j)) == 0:                                              # Se j não é visitado
                        new_mask = mask | (1 << j)                                          # Inclui j no caminho
                        dp[new_mask][j] = min(dp[new_mask][j], dp[mask][i] + adj[i][j])     # Custo de incluir j no caminho = menor entre incluir o caminho i->j ou o menor caminho já encontrado


    # Máscara que visita todas cidades
    complete_mask = (1 << n) - 1
    costMin = infinite

    # Compara todos os finais/começos para o caminho, escolhendo o menor
    for i in range(n):
        costMin = min(costMin, dp[complete_mask][i] + adj[i][start])

    return costMin


n = int(input())
start = int(input())
adj = []

for i in range(n):
    row = list(map(int, input().strip().split()))
    adj.append(row)

cost = costMinHamilton(n,adj,start)
print(cost)
