import obd

ports = obd.scanSerial() # return list of valid USB or RF ports
print(ports)