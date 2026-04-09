function W = DeltaBatch(W, X, D)

    alpha = 0.9;
    
    dWsum = zeros(7, 1);
    
    N = 10;
    for k = 1:N
        x = X(k, :)';         % Entradas
        d = D(k);             % Saídas desejadas
        v = W*x;
        y = Sigmoid(v);       % Saídas obtidas
        e = d - y;
        delta = y*(1-y)*e;
        dW = alpha*delta*x; 
        dWsum = dWsum + dW; 
    end
    dWavg = dWsum/N;        % Cálculo da média dos ajustes de peso
    W(1) = W(1) + dWavg(1);   
    W(2) = W(2) + dWavg(2);
    W(3) = W(3) + dWavg(3);
    W(4) = W(4) + dWavg(4);
    W(5) = W(5) + dWavg(5);
    W(6) = W(6) + dWavg(6);
    W(7) = W(7) + dWavg(7);
end
