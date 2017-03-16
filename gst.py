import sys
import time
import random
import argparse

from interop import Client
from interop import Target
from interop import Telemetry

from proxy_mavlink import proxy_mavlink


def generate_random_data(lat, lon, num_rows):
    latlong=[]
    for _ in xrange(num_rows):
        hex1 = '%012x' % random.randrange(16**12) # 12 char random string
        flt = float(random.randint(0,100))
        dec_lat = random.random()/100
        dec_lon = random.random()/100
        #print '%s %.1f %.6f %.6f \n' % (hex1.lower(), flt, lon+dec_lon, lat+dec_lat)
        latlong.append({'latitude':lat+dec_lat,'longitude':lon+dec_lon})
    return latlong


def testWaypoints(client,mission):
    for w in mission.mission_waypoints:
        telemetry = Telemetry(w.latitude,w.longitude,w.altitude_msl,90)
        client.post_telemetry(telemetry)


def testTelemtry(client):
    rand=generate_random_data(38.142544,-76.434088,10000)
    for w in rand:
        telemetry = Telemetry(w['latitude'],w['longitude'],200,90)
        client.post_telemetry(telemetry)
        time.sleep(0.5)


def testTarget(client,mission):
    target_pos = mission.off_axis_target_pos
    target = Target(type='standard',
                    latitude=38.145215,
                    longitude=-76.427942,
                    orientation='n',
                    shape='square',
                    background_color='green',
                    alphanumeric='A',
                    alphanumeric_color='white')
    target=client.post_target(target)
    print target

def getActiveMission(client):
    missions=client.get_missions()
    for m in missions:
        if m.active == True:
            return m

def spoofTelem(client):
    print('Spoofing Telemetry')
    while True:
        if raw_input():
            break
        else:
            testTelemtry(client)


def main():

    parser = argparse.ArgumentParser(description='ABES-AART AUVSI Ground Station')
    parser.add_argument('--url',
                        required=True,
                        help='URL for interoperability.')
    parser.add_argument('--username',
                        required=True,
                        help='Username for interoperability.')
    parser.add_argument('--password',
                         required=True,
                         help='Password for interoperability.')
    parser.add_argument('--spoofTelem')
    parser.add_argument('--mavlink',
                        help='Required argument for accessing and forwarding telemetry data')
    args=parser.parse_args()
    print(args)
    client = Client(args.url,args.username,args.password) #TODO : CREATE ARGS BASED

    activeMission=getActiveMission(client)
    print activeMission

    if args.spoofTelem:
        spoofTelem(client)
    #else:
    #    proxy_mavlink(args.mavlink, client)

    while True:
        if raw_input():
            break
        else:
            #testWaypoints(client,activeMission)
            testTelemtry(client)
            #testTarget(client,activeMission)

if __name__ == '__main__':
    main()
