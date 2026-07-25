from machine import Pin, I2C
import mpu6050
import time

i2c = I2C(0, scl=Pin(21), sda=Pin(22))
sensor_de_temperatura = mpu6050.accel(i2c)
botao = Pin(27, Pin.IN, Pin.PULL_UP)

print("Sistema de Monitoramento Inicializado")

while True:
  pass