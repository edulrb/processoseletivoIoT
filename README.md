# Relatório do Candidato

## Identificação do Candidato

- **Nome completo:** Eduardo Lustosa Ribeiro
- **GitHub:** https://github.com/edulrb

---

## Visão Geral da Solução

O projeto é um sistema de monitoramento ambiental simulado. O código (firmware) monitora o estado de uma porta e a temperatura do ambiente. Ele envia alertas pelo terminal serial caso a porta fique aberta por mais de 5 segundos ou se a temperatura subir rápido demais (uma variação de 3.0°C ou mais). A interação acontece clicando no botão do simulador (que faz o papel da porta) e mudando a temperatura direto no sensor do Wokwi.

---

## Arquitetura do Sistema Embarcado

A arquitetura lógica no main.py funciona em um loop contínuo (polling) não-bloqueante. O ESP32 lê os estados do botão e do sensor MPU6050 a cada 10ms, o que também serve como um debounce simples para o hardware. A passagem do tempo é controlada em segundo plano usando time.ticks_ms() e time.ticks_diff(), sem pausar a placa. O ESP32 processa os dados físicos e os cruza com variáveis de estado, decidindo o momento exato de enviar as mensagens para a porta serial, o que garante respostas em tempo real e evita sobrecarregar o terminal.

---

## Componentes Utilizados na Simulação

Liste os principais componentes definidos no `diagram.json`, por exemplo:

O sistema utiliza um ESP32 como placa principal para rodar o MicroPython, processar a lógica central e gerenciar a comunicação serial. Conectado a ele via I2C, um sensor MPU6050 é usado para ler a temperatura ambiente e detectar os picos de calor. Por fim, um botão (Push Button) ligado a um pino com resistor de Pull-Up interno atua como o sensor magnético da porta, indicando estado alto (1) quando fechada e baixo (0) quando aberta.

---

## Decisões Técnicas Relevantes

A principal decisão foi manter o código não-bloqueante para que o ESP32 registre imediatamente qualquer estímulo do simulador. Para contornar a latência do robô de testes do Wokwi CI, adicionei um delay estratégico de 600ms exclusivamente no momento de normalizar o sistema, garantindo que o simulador esteja pronto para ler a string final. Além disso, isolei as regras de acionamento em funções específicas, como trocou_de_estado e alertar, para manter o loop principal limpo e facilitar a manutenção.

---

## Resultados Obtidos

O projeto cumpriu todos os requisitos do desafio, respondendo em tempo real às aberturas da porta e elevações de temperatura. O código passou em todos os cenários dos testes automatizados (GitHub Actions e Wokwi CI), validando as strings exatas exigidas pela documentação sem apresentar erros de timeout na execução.

---

## Comentários Adicionais (Opcional)

Durante o desenvolvimento, houve dificuldade com a confiabilidade das bibliotecas nativas para o sensor MPU6050 no ambiente do simulador durante o CI. Para resolver isso, decidi baixar o arquivo da biblioteca (mpu6050.py) de uma fonte externa e incluí-lo diretamente na pasta do projeto. Isso evitou a dependência de instalações durante o build e garantiu estabilidade para os testes passarem sem quebrar.
