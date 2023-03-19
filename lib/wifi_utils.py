from wifi_secrets import networks
import network
import time


def wlan_connect():

    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            for net in networks:
                wlan.connect(net['ssid'], net['psk'])
                print(f"Waiting for connection {net['ssid']}...")
                for _retry in range(10):
                    if wlan.isconnected():
                        break
                    time.sleep(0.5)
                if wlan.isconnected():
                    print('Connected')
                    break
        print(wlan.ifconfig())
        return wlan

    except OSError as e:
        print(f"Exception during wifi connection {e}")
        exit(1)
