#!/usr/bin/env python3
import serial
import csv
import time

def list_binary(num):
    binary = bin(num).replace("0b", "")
    list_bin = list(binary)
    list_binary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
    for i in range(0,len(list_bin)):
        list_binary[len(list_binary)-len(list_bin)+i] = int(list_bin[i])
    return list_binary

bms_flag_list = [ "P0A07 (Discharge Limit Enforcement Fault)",
"P0A08 (Charger Safety Relay Fault)",
"P0A09 (Internal Hardware Fault)",
"P0A0A (Internal Heatsink Thermistor Fault)",
"P0A0B (Internal Software Fault)",
"P0A0C (Highest Cell Voltage Too High Fault)",
"P0A0E (Lowest Cell Voltage Too Low Fault)",
"P0A10 (Pack Too Hot Fault)",
"P0A1F (Internal Communication Fault)",
"P0A12 (Cell Balancing Stuck Off Fault)",
"P0A80 (Weak Cell Fault)",
"P0AFA (Low Cell Voltage Fault)",
"P0A04 (Open Wiring Fault)",
"P0AC0 (Current Sensor Fault)",
"P0A0D (Highest Cell Voltage Over 5V Fault)",
"P0A0F (Cell ASIC Fault)",
"P0A02 (Weak Pack Fault)",
"P0A81 (Fan Monitor Fault)",
"P0A9C (Thermistor Fault)",
"U0100 (External Communication Fault)",
"P0560 (Redundant Power Supply Fault)",
"P0AA6 (High Voltage Isolation Fault)",
"P0A05 (Input Power Supply Fault)",
"P0A06 (Charge Limit Enforcement Fault)" ]

mc_fault_list = ["No faults", "Overvoltage", "Undervoltage", "DRV",
"ABS. Overcurrent",  "CTLR Overtemp", "Motor Overtemp", "Sensor wire fault",
"Sensor general fault", "CAN Command error", "Analog Input error"]

mc_limits= ["Capacitor Temp limit", "DC Current limit", "Drive Enable limit", "IGBT Acceleration limit", "IGBT Temp limit", "Input Voltage limit",
             "Motor Acceleration Temperature limit", "Motor Temp limit", "RPM min limit", "RPM max limit", "Power Limit", "Reserved", "Reserved", "Reserved", "Reserved", "Reserved",]

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()
    t = time.localtime()
    current_time=time.strftime("%d-%m%H:%M:%S", t)
    filename = "./DataLog/Log" + current_time + ".csv"
    file = open(filename,"a+")
    writer = csv.writer(file)
    writer.writerow(["Time", "Current", "InstVoltage", "SOC", "HighTemp", "LowTemp", "P0A07 (Discharge Limit Enforcement Fault)",
"P0A08 (Charger Safety Relay Fault)", "P0A09 (Internal Hardware Fault)", "P0A0A (Internal Heatsink Thermistor Fault)", "P0A0B (Internal Software Fault)",
"P0A0C (Highest Cell Voltage Too High Fault)", "P0A0E (Lowest Cell Voltage Too Low Fault)", "P0A10 (Pack Too Hot Fault)", "P0A1F (Internal Communication Fault)",
"P0A12 (Cell Balancing Stuck Off Fault)", "P0A80 (Weak Cell Fault)", "P0AFA (Low Cell Voltage Fault)", "P0A04 (Open Wiring Fault)",
"P0AC0 (Current Sensor Fault)", "P0A0D (Highest Cell Voltage Over 5V Fault)", "P0A0F (Cell ASIC Fault)", "P0A02 (Weak Pack Fault)",
"P0A81 (Fan Monitor Fault)", "P0A9C (Thermistor Fault)", "U0100 (External Communication Fault)", "P0560 (Redundant Power Supply Fault)",
"P0AA6 (High Voltage Isolation Fault)", "P0A05 (Input Power Supply Fault)", "P0A06 (Charge Limit Enforcement Fault)",
"InputSupp", "RPM", "Speed", "DutyCycle", "InputVol", "Ac_Curr", "Dc_Curr", "Cont_temp", "Motor_temp", "MC_Fault","Id", "Iq", "Throttle",
"Capacitor Temp limit", "DC Current limit", "Drive Enable limit", "IGBT Acceleration limit", "IGBT Temp limit", "Input Voltage limit",
"Motor Acceleration Temperature limit", "Motor Temp limit", "RPM min limit", "RPM max limit", "Power Limit" ,"BPS"])
    file.close()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            list_ard = line.split()
            if (list_ard[0]=="1"):
                #print(list_ard)
                t = time.localtime()
                current_time=time.strftime("%H:%M:%S", t)
                list_pi=[current_time]
                for i in range(1,len(list_ard)):
                    if ((i==6) or (i==7) or (i==21) or (i==22)):
                        binary =  list_binary(int(list_ard[i]))
                        if (i==6):
                            binary = binary[:8]
                        if (i==21):
                            binary = binary[8:]
                        if (i==22):
                            binary = binary[8:11]
                        for j in binary:
                            list_pi.append(j)
                    elif(i==17):
                        if (int(list_ard[i])==0):
                            list_pi.append(list_ard[i])
                        else:
                            list_pi.append(list_ard[i] + " : " + mc_fault_list[int(list_ard[i])])
                    else:
                        list_pi.append(float(list_ard[i]))
                print(list_pi)
                flag = list_pi[6:30]
                for i in range(0,len(flag)):
                    if flag[i]:
                        print("BMS Fault: ", bms_flag_list[i])
                print("MC Fault: ", mc_fault_list[int(list_ard[17])])
                mc_limit = list_pi[43:54]
                for i in range(0,len(mc_limit)):
                    if mc_limit[i]:
                        print(mc_limits[i])
                file = open(filename,"a+")
                writer = csv.writer(file)
                writer.writerow(list_pi)
                file.close()