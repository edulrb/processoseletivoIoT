from machine import Pin, I2C
import mpu6050
import time

LIMITE_TEMPO_X = 5000
LIMITE_VARIACAO_Y = 3

estado_botao = 1
alerta_porta_aberta = False
tempo_porta_aberta = 0
variacao_alertada = False
temperatura_porta_fechada = 0.0

i2c = I2C(0, scl=Pin(21), sda=Pin(22))
sensor = mpu6050.accel(i2c)
botao = Pin(27, Pin.IN, Pin.PULL_UP)

def alertar(tipo_de_alerta):
  global alerta_porta_aberta, variacao_alertada
  if tipo_de_alerta == "tempo_porta_aberta":
    print("ALERTA: Porta aberta por muito tempo!")
    alerta_porta_aberta = False
  
  elif tipo_de_alerta == "variacao_termica":
    print("ALERTA: Degradacao termica detectada!")
    variacao_alertada = True

def trocou_de_estado(anterior, atual):
    global alerta_porta_aberta, tempo_porta_aberta, temperatura_atual, temperatura_porta_fechada, variacao_alertada
    if anterior == 1:
      temperatura_porta_fechada = temperatura_atual
      print("Porta Aberta")
      alerta_porta_aberta = True
      tempo_porta_aberta = time.ticks_ms()
    else:
      print("Porta Fechada")
      alerta_porta_aberta = False
      tempo_porta_aberta = 0
      variacao_alertada = False

print("Sistema de Monitoramento Inicializado")

while True:
  temperatura_atual = sensor.get_values()["Tmp"]
  tempo_atual = time.ticks_ms()
  checagem_anterior = estado_botao
  estado_botao = botao.value()

  if estado_botao != checagem_anterior:
    trocou_de_estado(checagem_anterior, estado_botao)

  #CHECANDO SE O ALERTA ESTÁ ATIVO E PASSOU DOS 5000ms
  tempo_decorrido = time.ticks_diff(tempo_atual, tempo_porta_aberta)
  if tempo_decorrido >= LIMITE_TEMPO_X and alerta_porta_aberta:
    alertar("tempo_porta_aberta")

  #CHECANDO VARIAÇÃO TERMICA SOMENTE SE A PORTA ESTIVER ABERTA
  variacao_termica = temperatura_atual - temperatura_porta_fechada
  if variacao_termica >= LIMITE_VARIACAO_Y and not variacao_alertada and alerta_porta_aberta:
    alertar("variacao_termica")

  #DELAY PARA EVITAR DEBOUNCE
  time.sleep_ms(10)