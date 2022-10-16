from contextlib import nullcontext
import os
import psycopg2
import serial
import time

conn = psycopg2.connect("postgresql://theDucks:<password>@free-tier11.gcp-us-east1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dkenthackenough-2373"); 

ser = serial.Serial(
    port='/dev/cu.usbserial-14210',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    xonxoff = False,
    timeout=0)

print("connected to: " + ser.portstr)
count=1

pretag = []; 
while True:
    for line in ser.read():
        pretag.append(chr(line))
        if (chr(line) == '\n' ) :
            pretag.pop()
            pretag.pop()
            tag = ''.join(pretag)
            print(tag)
            pretag.clear()
            with conn.cursor() as cur:
                cur.execute("select firstname, lastname, email from person where person_id='" + str(tag) + "';"); 
                res = cur.fetchall()
                if (len(res) == 0) :
                    test = str('fail\n\r')
                else :
                    test = str('pass\n\r')
                    cur.execute("insert into scan values (((select max(scan_id) from scan) + 1), now(), 100, '" + str(tag) + "');")
                conn.commit()
                print(res)
                val = ser.write(test.encode())
                ser.flushOutput()
ser.close()
