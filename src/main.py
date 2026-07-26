from machine import Pin, I2C
import mpu6050
import time

LIMITE_TEMPO_X = 5000
LIMITE_VARIACAO_Y = 3.0

estado_botao = 1 
porta_aberta = False
alertado_porta_aberta = False
tempo_porta_aberta = 0
variacao_alertada = False
temperatura_porta_fechada = 0.0
erro_ativo = False

i2c = I2C(0, scl=Pin(21), sda=Pin(22))
sensor = mpu6050.accel(i2c)
botao = Pin(27, Pin.IN, Pin.PULL_UP)

time.sleep_ms(10)
temperatura_porta_fechada = sensor.get_values()["Tmp"]

def alertar(tipo_de_alerta):
    global variacao_alertada, erro_ativo, alertado_porta_aberta
    erro_ativo = True
    if tipo_de_alerta == "tempo_porta_aberta":
        print("ALERTA: Porta aberta por muito tempo!")
        alertado_porta_aberta = True
    
    elif tipo_de_alerta == "variacao_termica":
        print("ALERTA: Degradacao termica detectada!")
        variacao_alertada = True

def trocou_de_estado(anterior, atual):
    global porta_aberta, tempo_porta_aberta, temperatura_atual, temperatura_porta_fechada
    
    if anterior == 1 and atual == 0:
        temperatura_porta_fechada = temperatura_atual
        porta_aberta = True
        tempo_porta_aberta = time.ticks_ms()
        
    elif anterior == 0 and atual == 1:
        porta_aberta = False
        tempo_porta_aberta = 0

print("Sistema de Monitoramento Inicializado")

while True:
    temperatura_atual = sensor.get_values()["Tmp"]
    tempo_atual = time.ticks_ms()
    
    checagem_anterior = estado_botao
    estado_botao = int(not botao.value()) 

    if estado_botao != checagem_anterior:
        trocou_de_estado(checagem_anterior, estado_botao)

    if not porta_aberta and temperatura_atual < temperatura_porta_fechada:
        temperatura_porta_fechada = temperatura_atual

    #CHECANDO SE O ALERTA ESTÁ ATIVO E PASSOU DOS 5000ms
    tempo_decorrido = time.ticks_diff(tempo_atual, tempo_porta_aberta)
    if porta_aberta and tempo_decorrido >= LIMITE_TEMPO_X and not alertado_porta_aberta:
        alertar("tempo_porta_aberta")

    #CHECANDO VARIAÇÃO TERMICA
    variacao_termica = temperatura_atual - temperatura_porta_fechada
    if variacao_termica >= LIMITE_VARIACAO_Y and not variacao_alertada:
        alertar("variacao_termica")

    condicoes_seguras = not porta_aberta and (variacao_termica < LIMITE_VARIACAO_Y)
    
    if erro_ativo and condicoes_seguras:
        time.sleep_ms(600)
        print("Status: Sistema Normalizado.")
        
        erro_ativo = False
        alertado_porta_aberta = False
        variacao_alertada = False

    #DELAY PARA EVITAR DEBOUNCE
    time.sleep_ms(10)