#!/usr/bin/env python3
#lwp3 characteristic: 00001624-1212-efde-1623-785feabcd123
#hub status led color change: 

import asyncio
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from bleak import BleakClient, BleakScanner

async def connect_to_device(address):
    client = BleakClient(address)
    await client.connect()
    return client

async def get_characteristics(client):
    services = await client.get_services()
    characteristics = []
    for service in services:
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

    index = int(input("Select device index to connect: "))
    address = devices[index].address

    client = await connect_to_device(address)
    print(f"Connected to {address}")

    characteristics = await get_characteristics(client)
    print("Available characteristics:")
    for i, (uuid, properties) in enumerate(characteristics):
        print(f"{i}: {uuid} (Properties: {', '.join(properties)})")

    while True:
        cmd = input("Enter command (read/write/exit): ").strip().lower()
        if cmd == "exit":
            break
        elif cmd == "read":
            char_index = int(input("Enter characteristic index to read: ").strip())
            characteristic_uuid = characteristics[char_index][0]
            data = await read_characteristic(client, characteristic_uuid)
            print(f"Data: {data}")
        elif cmd == "write":
            char_index = int(input("Enter characteristic index to write: ").strip())
            characteristic_uuid = characteristics[char_index][0]
            data = input("Enter data to write (in hex): ").strip()
            data_bytes = bytes.fromhex(data)
            await write_characteristic(client, characteristic_uuid, data_bytes)
            print("Data written")
        else:
            print("Unknown command")

    await client.disconnect()
    print("Disconnected")

if __name__ == "__main__":
    asyncio.run(run_terminal())
