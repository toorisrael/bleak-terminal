#!/usr/bin/env python3
#lwp3 characteristic: 00001624-1212-efde-1623-785feabcd123
#hub status led color change command: 0800813F11510002
#08 00 81 3F 11 51 00 02
#08 00 81					- beginning of the lwp3 command
#         3F				- port
#            11 			- set?? I've seen 11 or 01 in other command found on the internet
#               51			- data format, int??
#                  00 		- mode??
#                     02	- color
#run engine on port 51 (0x33() at 100% (0x64) power mode (0x00): 0800813301510064
#engine 1 25% power: 0800813201510019
#engine 2 25% power: 0800813301510019
#steer: 0800813401510301 - this is wrong
#leds: 0800813511510100 - this is also wrong
#request hardware version: 	0500010405
#request battery voltage: 	0500010605 (percentage)
#request firmware version: 	0500010305


import asyncio
from bleak import BleakClient, BleakScanner

async def connect_to_device(address):
    client = BleakClient(address)
    await client.connect()
    return client

async def get_characteristics(client):
    await client.get_services()  # Ensure services are loaded
    characteristics = []
    for service in client.services:
        for char in service.characteristics:
            characteristics.append((char.uuid, char.properties))
    return characteristics

async def read_characteristic(client, characteristic_uuid):
    data = await client.read_gatt_char(characteristic_uuid)
    return data

async def write_characteristic(client, characteristic_uuid, data):
    await client.write_gatt_char(characteristic_uuid, data)

async def run_terminal():
    devices = await BleakScanner.discover()
    print("Found devices:")
    for i, device in enumerate(devices):
        print(f"{i}: {device.name} ({device.address})")

    index = int(input("\nSelect device index to connect:\n"))
    address = devices[index].address

    client = await connect_to_device(address)
    print(f"\nConnected to {address}")

    characteristics = await get_characteristics(client)
    print("\nAvailable characteristics:")
    for i, (uuid, properties) in enumerate(characteristics):
        print(f"{i}: {uuid} (Properties: {', '.join(properties)})")

    current_characteristic_uuid = None

    while True:
        if current_characteristic_uuid is None:
            cmd = input("\nEnter command (read/write/exit):\n").strip().lower()

            if cmd == "exit":
                break
            elif cmd == "read":
                char_index = int(input("\nEnter characteristic index to read:\n").strip())
                current_characteristic_uuid = characteristics[char_index][0]
                data = await read_characteristic(client, current_characteristic_uuid)
                print(f"\nData: {data}")
            elif cmd == "write":
                char_index = int(input("\nEnter characteristic index to write:\n").strip())
                current_characteristic_uuid = characteristics[char_index][0]
                data = input("\nEnter data to write (in hex):\n").strip()
                if data.lower() == "exit":
                    break
                data_bytes = bytes.fromhex(data)
                await write_characteristic(client, current_characteristic_uuid, data_bytes)
                print("\nData written")
            else:
                print("\nUnknown command")
        else:
            cmd = input(f"\nEnter data to write to {current_characteristic_uuid} or type 'read' to read from this characteristic, 'switch' to change characteristic, or 'exit' to quit:\n").strip().lower()

            if cmd == "exit":
                break
            elif cmd == "read":
                data = await read_characteristic(client, current_characteristic_uuid)
                print(f"\nData: {data}")
            elif cmd == "switch":
                current_characteristic_uuid = None
            else:
                try:
                    data_bytes = bytes.fromhex(cmd)
                    await write_characteristic(client, current_characteristic_uuid, data_bytes)
                    print("\nData written")
                except ValueError:
                    print("\nInvalid hex data format")

    await client.disconnect()
    print("\nDisconnected")

if __name__ == "__main__":
    asyncio.run(run_terminal())
