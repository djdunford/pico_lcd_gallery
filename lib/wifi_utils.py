from wifi_secrets import networks
import network
import time
from sys import exit


def wlan_connect():

    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            for net in networks:
                wlan.connect(net['ssid'], net['psk'])
                print(f"Waiting for connection {net['ssid']}...")
                for _retry in range(20):
                    if wlan.isconnected():
                        break
                    time.sleep(0.5)
                if wlan.isconnected():
                    print('Connected')
                    break
        if not wlan.isconnected():
            print('Unable to find any network')
            exit(1)

        print(wlan.ifconfig())
        return wlan

    except OSError as e:
        print(f"Exception during wifi connection {e}")
        exit(1)


def wlan_disconnect():

    try:
        wlan = network.WLAN(network.STA_IF)
        if wlan.isconnected():
            wlan.disconnect()
        if wlan.active():
            wlan.active(False)

    except OSError as e:
        print(f"Exception during wifi connection {e}")
        exit(1)
