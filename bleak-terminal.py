#!/usr/bin/env python3
#lwp3 characteristic: 00001624-1212-efde-1623-785feabcd123
#hub status led color change command: 0800813F11510002

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

    index = int(input("Select device index to connect: "))
    address = devices[index].address

    client = await connect_to_device(address)
    print(f"Connected to {address}")

    characteristics = await get_characteristics(client)
    print("Available characteristics:")
    for i, (uuid, properties) in enumerate(characteristics):
        print(f"{i}: {uuid} (Properties: {', '.join(properties)})")

    current_characteristic_uuid = None

    while True:
        if current_characteristic_uuid is None:
            cmd = input("Enter command (read/write/exit): ").strip().lower()
        else:
            cmd = input(f"Enter data to write to {current_characteristic_uuid} or type 'switch' to change characteristic or 'exit' to quit: ").strip().lower()

        if cmd == "exit":
            break
        elif cmd == "read" and current_characteristic_uuid is None:
            char_index = int(input("Enter characteristic index to read: ").strip())
            characteristic_uuid = characteristics[char_index][0]
            data = await read_characteristic(client, characteristic_uuid)
            print(f"Data: {data}")
        elif cmd == "write" and current_characteristic_uuid is None:
            char_index = int(input("Enter characteristic index to write: ").strip())
            current_characteristic_uuid = characteristics[char_index][0]
            data = input("Enter data to write (in hex): ").strip()
            if data.lower() == "exit":
                break
            data_bytes = bytes.fromhex(data)
            await write_characteristic(client, current_characteristic_uuid, data_bytes)
            print("Data written")
        elif cmd == "switch":
            current_characteristic_uuid = None
        elif current_characteristic_uuid is not None:
            if cmd.lower() == "exit":
                break
            elif cmd.lower() == "switch":
                current_characteristic_uuid = None
            else:
                data_bytes = bytes.fromhex(cmd)
                await write_characteristic(client, current_characteristic_uuid, data_bytes)
                print("Data written")
        else:
            print("Unknown command")

    await client.disconnect()
    print("Disconnected")

if __name__ == "__main__":
    asyncio.run(run_terminal())

