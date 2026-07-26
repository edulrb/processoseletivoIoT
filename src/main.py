from machine import Pin, I2C
import mpu6050
import time

LIMITE_TEMPO_X = 5000

estado_botao = 1
alerta_acionado = False
inicio_do_alerta = 0

def alertar():
  global alerta_acionado
  print("ALERTA: Porta aberta por muito tempo!")
  alerta_acionado = False

def trocou_de_estado(anterior, atual):
    global alerta_acionado, inicio_do_alerta
    if anterior == 1:
      print("Botao clicado")
      alerta_acionado = True
      inicio_do_alerta = time.ticks_ms()
    else:
      print("Botao solto")
      alerta_acionado = False
      inicio_do_alerta = 0

i2c = I2C(0, scl=Pin(21), sda=Pin(22))
sensor_de_temperatura = mpu6050.accel(i2c)
botao = Pin(27, Pin.IN, Pin.PULL_UP)

print("Sistema de Monitoramento Inicializado")

while True:
  tempo_atual = time.ticks_ms()
  checagem_anterior = estado_botao
  estado_botao = botao.value()
  if estado_botao != checagem_anterior:
    trocou_de_estado(checagem_anterior, estado_botao)

  #CHECANDO SE O ALERTA ESTÁ ATIVO E PASSOU DOS 5000ms
  tempo_decorrido = time.ticks_diff(tempo_atual, inicio_do_alerta)
  if tempo_decorrido >= LIMITE_TEMPO_X and alerta_acionado:
    alertar()
  time.sleep_ms(10)