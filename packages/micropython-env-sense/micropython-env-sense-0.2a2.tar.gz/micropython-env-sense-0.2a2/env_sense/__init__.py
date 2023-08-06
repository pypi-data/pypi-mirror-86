# https://opensource.org/licenses/GPL-3.0

# import esp
import gc
import machine
import ntptime
import time
import utime
from common import led

from env_sense import bme280_int as bme280
from env_sense import pms7003
from env_sense import aqi
from env_sense import publishThingspeak

SECONDS_BETWEEN_READINGS = 1
SAMPLES = 1
FREQUENCY_BME_MINS = 10
FREQUENCY_AIR_MINS = 20

# assumes BME < AIR; AIR is a multiple of BME

# Thingspeak:
TS_CHANNEL_ID = b'1229949'
TS_CHANNEL_WRITE_API_KEY = b'MD2BOTGRJ8JE8J6U'


# https://cfpub.epa.gov/si/si_public_record_report.cfm?dirEntryId=349513&Lab=CEMM
# https://cfpub.epa.gov/si/si_public_file_download.cfm?p_download_id=540979&Lab=CEMM
def us_epa_correction(pm2_5cf1, rel_humi):
    return (0.52 * pm2_5cf1) - (0.085 * rel_humi) + 5.71


def ts_publish(ts, reading_bme, reading_air):
    if reading_air:
        pm2_5_corr = us_epa_correction(reading_air['pm2_5cf1'], rel_humi=reading_bme[2])
        aqi25_instant = aqi.AQI.PM2_5(pm2_5_corr)
        data = {'field1': aqi25_instant,
                'field2': reading_air['pm1_0'],
                'field3': reading_air['pm2_5'],
                'field4': reading_air['pm2_5cf1'],
                'field5': reading_air['pm10'],
                'field6': reading_bme[0],  # temp
                'field7': reading_bme[1],  # pressure
                'field8': reading_bme[2],  # humidity
                }
    else:
        data = {'field6': reading_bme[0],  # temp
                'field7': reading_bme[1],  # pressure
                'field8': reading_bme[2],  # humidity
                }
    ts.publish(data)


# -----------------------------------------------------------------------------------------------------------
# Init / read sensors
# -----------------------------------------------------------------------------------------------------------
class Sensor:
    def read(self):
        return {}


class SensorAir(Sensor):
    pass  # TODO
    # WARMUP_SECONDS = 30
    # def __init__(self):
    #     self.sensor = pms7003.PassivePms7003Sensor(uart=0)
    #     self.sensor.wakeup()
    #     time.sleep(SensorAir.WARMUP_SECONDS)

    # def read(self):
    #     return self.sensor.read()

    def read(self):
        return {'pm1_0': -1,
                'pm2_5': -1,
                'pm2_5cf1': -1,
                'pm10': -1}


class SensorBME(Sensor):
    pass  # TODO
    # def __init__(self):
    #     i2c = machine.I2C()
    #     self.bme = bme280.BME280(i2c=i2c)

    # def read(self):
    #     t, p, h = self.read_compensated_data()
    #     p >>= 8
    #     h >>= 10
    #     return [t, p, h]
    def read(self):
        return [-1, -1, -1]


def read_sensors_and_publish(air=False):
    air = SensorAir() if air else Sensor()
    bme = SensorBME()

    for i in range(SAMPLES):
        ts_publish(ts, bme.read(), air.read())
        time.sleep(SECONDS_BETWEEN_READINGS)
    # air.sensor.sleep()  # TODO


def main_loop():
    while True:
        # read air sensor every 20mins, BME every 10mins
        air = utime.localtime()[4] % 20 == 0
        print('Main loop called: {}. Sensing air: {}'.format(utime.localtime(), air))
        read_sensors_and_publish(air=air)
        led.flash(2)

        # sleep until next wake up time
        ntptime.settime()
        now = utime.localtime()
        secs_until_next = (FREQUENCY_BME_MINS - (now[4] % FREQUENCY_BME_MINS))*60 - now[5]
        print("Sleeping for {} seconds. Free mem: {}".format(secs_until_next, gc.mem_free()))
        time.sleep(secs_until_next)


# -----------------------------------------------------------------------------------------------------------
# main loop
# -----------------------------------------------------------------------------------------------------------
# TODO:
# - disable UART so it's sensor only
# - watchdog to sleep sensor and reboot
# - security: webrepl password? separate wifi network, mac protected?

# TODO:
# if machine.reset_cause() == machine.DEEPSLEEP_RESET:
#     print('Woke from deep sleep')
# else:
#     print('Cold boot')
# doesn't come back up. Probably need to jumper connect RST and D0:
# https://www.reddit.com/r/esp8266/comments/7gmzn1/wemos_d1_mini_sleep/
# esp.deepsleep(SLEEP_SECONDS * 1000000)

ts = publishThingspeak.ThingspeakMqtt(TS_CHANNEL_ID, TS_CHANNEL_WRITE_API_KEY)
main_loop()
