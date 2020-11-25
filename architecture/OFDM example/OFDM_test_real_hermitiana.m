#### OFDM_test_real_hermitiana

pkg load communications

close all
clear all
clc

% Número de níveis do QAM (índice de modulação) -- Quantidade de pontos/símbolos no diagrama de constelação
M_QAM = 4;
% número de bits por símbolo de subportadora de dados
m = log2(M_QAM);

% valor do SNR
SNR = 15;

% quantidade de pontos da IFFT (para multiplexação)
N_IFFT = 1024;

% Números de subportadoras de dados (seerão incusas subportadoras com zeros para poder visualizar os dados)
N = 1002;
N = 902;

% subportadoras a serem multiplicadas
Ns = N/2-1;

% Quantidade de amostras do prefixo cíclico (intervalor de guarda)
N_CP = 11;

% Número de bits no bitstream de entrada
% N_BITS = Ns*m;
N_BITS = Ns;


% 
indice = 0:N_BITS-1;

% Gera os dados entrada
tx = floor(rand(1,N_BITS)*(M_QAM));
tx = randi(M_QAM, 1, N_BITS)-1;
% tx = [0 1 2 3 0 1 2 3 0 1]

% figure(1)
% plot(indice,x,'o')
% hold on


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TRANSMISSÃO <------------------
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Conversão Série-Paralelo
x = tx';


% Mapeamento
Y = qammod(x,M_QAM);

% plot da constelação de entrada
figure(1)
plot(Y,'o')
xlim([min(real(Y))-1 max(real(Y))+1])
ylim([min(imag(Y))-1 max(imag(Y))+1])
grid on


% Simetria Hermitiana
Y_hermit = [0;Y;0;flipud(conj(Y))];
% Simetria Hermitiana
tam_hermit = size(Y_hermit);



% [Essa parte é importante: pois o matlab coloaca a parte positiva do espectro na esquerda, e a parte negativa na direita]
% Interpolação para poder vizualizar o espectro (para centralização do espectro)
y_tx = zeros(N_IFFT,1);
y_tx(1:N_BITS+1) = Y_hermit(1:N_BITS+1);
y_tx(N_IFFT-(N_BITS):N_IFFT) = Y_hermit(N_BITS+2:end);

figure(5)
% plot(abs(y_tx), 'o')
% hold on 
plot(angle(y_tx), '-r')

% "Modulação" via IDFT
y = ifft(y_tx);


% plot(y,'o')

% Insere Intervalo de Guarda (CP)
y_ig = [y(end-(N_CP-1):end); y];


% Conversão paralelo-Série
y_ig = y_ig.';


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CANAL <---------------------
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


y_ig2 = conv(y_ig,1)

% Gera o perfil de potência do canal (taps no domínio do tempo)
h = [(randn+j*randn) (randn+j*randn)/2 (randn+j*randn)/4];
% Convolução com o canal
y_ig2 = conv(y_ig, h);
% Retira as amostras excedentes devido à convolução
y_ig2 = y_ig2(1:length(y_ig));

% inclui ruído branco
y_ruido = awgn(y_ig, SNR, 'measured');
%y_ruido = awgn(y_ig2, SNR, 'measured');
% y_ig = y_ig + rand(1,N_IFFT+N_CP)*max(abs(y_ig))/5;

% se for de potencia 10*log
OFDM_freq = fft(y_ruido);


figure(2)
% fftshift é para inverter a ordem do espectro OFDM
plot(fftshift(10*log10(abs(OFDM_freq)))); grid on;


figure(3)
% tempo discreto
t_discreto = [1:N_IFFT+N_CP];
% plot do símbolo OFDM
plot(t_discreto,y_ruido)


% 
% r_y_ig = real(y_ig);
% i_y_ig = imag(y_ig);

% central_freq = 1e6;
% soma = r_y_ig*cos(2*pi*central_freq) + ...
% 	i_y_ig*sin(2*pi*central_freq);

% figure(3)
% plot(soma)
% % plot(r_y_ig)
% % hold on
% % plot(i_y_ig,'r')
% % xlim([min(real(Z))-1 max(real(Z))+1])
% % ylim([min(imag(Z))-1 max(imag(Z))+1])
% grid on


% figure(3)
% plot(Z,'o')
% xlim([min(real(Z))-1 max(real(Z))+1])
% ylim([min(imag(Z))-1 max(imag(Z))+1])
% grid on


% plot(r_y_ig,i_y_ig,'o')


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% RECEPÇÃO <---------------------
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Conversão Série-Paralelo
z_ig = y_ruido.';


% Remove o prefixo cíclico (primeiros N_CP posições)
z = [z_ig(N_CP+1:end)];


% "Demodulação" via DFT. 'z_rx' contém as subportadoras
z_rx = fft(z);

% Faz um shift do resultado do FFT para a esquerda (ou pra cima) circularmente
% z_rx = round(shift(z_rx,-1));

% round([y_tx z_rx])

% lugar onde deve ser feita a interpolação ao contrário
% Z = z_rx;
Z_hermit(1:N_BITS+1,1) = z_rx(1:N_BITS+1,1);
%Z_hermit(N_BITS+2:tam_hermit,1) = z_rx(N_IFFT-(N_BITS):N_IFFT,1);
Z_hermit(N_BITS+2:N,1) = z_rx(N_IFFT-(N_BITS):N_IFFT,1);


% Simetria Hermitiana
Z = Z_hermit(2:N_BITS+1);


% y_tx(1:N_BITS+1) = Y_hermit(1:N_BITS+1);
% y_tx(N_IFFT-(N_BITS):N_IFFT) = Y_hermit(N_BITS+2:end);
% Z = Z';

[Y Z];

figure(4)
plot(Z,'o')
xlim([min(real(Z))-1 max(real(Z))+1])
ylim([min(imag(Z))-1 max(imag(Z))+1])
grid on

% j
% Mapeamento de volta para a sequência de bits
rx = qamdemod(Z,M_QAM);

% Conversão paralelo-Série
rx = rx.';

% problema 
% sum(abs(tx-rx))
norm(abs(tx-rx))



BW = 20e6

% M_QAM = 16
delta_CP = 1/4;
Ns = 48;
delta_f = 312.5e3;
% taxa de bits
Rb = delta_f*Ns*log2(M_QAM)/(1+delta_CP)
