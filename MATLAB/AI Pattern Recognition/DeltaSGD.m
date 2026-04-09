function W = DeltaSGD(W, X, D)

    alpha = 0.9;
    
    N = 10;
    for k = 1:N
        x = X(k, :)';   % Entradas
        d = D(k);       % Saídas desejadas
        
        v = W*x;
        y = Sigmoid(v); % Saídas obtidas
        
        e = d - y;
        delta = y*(1-y)*e;
        
        dW = alpha*delta*x; % Regra delta
        
% Atualização para cada um dos 7 pesos
        W(1) = W(1) + dW(1);
        W(2) = W(2) + dW(2);
        W(3) = W(3) + dW(3);
        W(4) = W(4) + dW(4);
        W(5) = W(5) + dW(5);
        W(6) = W(6) + dW(6);
        W(7) = W(7) + dW(7);

    end
end
