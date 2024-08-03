# bleak-terminal
Python bleak terminal

Python script made to interact with LEGO Technic Move hub. Credits goes to Chat GPT.

Example usage - changing hub LED status light color:
python bleak-terminal.py
Found devices:
0: Technic Move   (34:68:B5:1C:BD:3E)
Select device index to connect: 0
Connected to 34:68:B5:1C:BD:3E
Available characteristics:
0: 00002a00-0000-1000-8000-00805f9b34fb (Properties: read, write)
1: 00002a01-0000-1000-8000-00805f9b34fb (Properties: read, write)
2: 00002a04-0000-1000-8000-00805f9b34fb (Properties: read)
3: 00002aa6-0000-1000-8000-00805f9b34fb (Properties: read)
4: 00002ac9-0000-1000-8000-00805f9b34fb (Properties: read)
5: 00002a05-0000-1000-8000-00805f9b34fb (Properties: indicate)
6: 00001624-1212-efde-1623-785feabcd123 (Properties: write-without-response, write, notify)
7: f000ffc1-0451-4000-b000-000000000000 (Properties: write-without-response, write, notify)
8: f000ffc2-0451-4000-b000-000000000000 (Properties: write-without-response, write, notify)
9: f000ffc5-0451-4000-b000-000000000000 (Properties: write-without-response, notify)
Enter command (read/write/exit): write
Enter characteristic index to write: 6
Enter data to write (in hex): 0800813F11510002
Data written
Enter command (read/write/exit): exit
Disconnected
