% Treinamento para o dígito 0 utilizando o método GDE

clear all
clc

% Entradas em forma de matrizes 1x7 para cada um dos dígitos possíveis 
X = [1 1 1 1 1 1 0;
     0 1 1 0 0 0 0;
     1 1 0 1 1 1 1;
     1 1 1 1 0 0 1;
     0 1 1 0 0 1 1;
     1 0 1 1 0 1 1;
     1 0 1 1 1 1 1;
     1 1 1 0 0 0 0;
     1 1 1 1 1 1 1;
     1 1 1 1 0 1 1];
 
% Saídas desejadas, nível alto apenas para o dígito 0
D = [0; 0; 0; 0; 0; 0; 0; 0; 0; 1];

W = 2*rand(1, 7) - 1;   % Inicialização dos sete pesos

% Treinamento (ajuste de pesos):
for epoch = 1:10000
    W = DeltaSGD(W, X, D);
end

% Inferência:
N = 10;
y = zeros(N,1);
for k = 1:N
x = X(k, :)';
v = W*x;
y(k) = Sigmoid(v);  %saída desejada
end

disp('Results:');
disp('   [desired   neuron_output]');
disp([D y]);
disp(W)
