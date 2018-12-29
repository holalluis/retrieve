#!/usr/bin/env python3
'''
  Translation of "RETRIEVE.PAS" Pascal code to Python3.
  Created by Lluís Bosch (lbosch@icra.cat) on 2018-12-20. Requested by George Ekama

  The key on converting this has been dealing with the
  Turbo Pascal 48 bit "Real" type 
  found on: http://www.shikadi.net/moddingwiki/Turbo_Pascal_Real 
  While most languages use a 32-bit or 64-bit floating point decimal variable,
  usually called single or double, Turbo Pascal featured an uncommon 48-bit float
  called a real which served the same function as a float. 32 and 64-bit floats
  were introduced in Turbo Pascal version 5. Pascal's successor, Delphi, did not
  feature reals as a variable type.
  A Pascal real has a value range of 2.9 x 10-39 to 1.7 x 1038.
  The structure of a Pascal real is seen in the diagram below.

  Byte	0	        1	        2	        3	        4	        5
  Bit	  01234567	01234567	01234567	01234567	01234567	01234567
  Value	EEEEEEEE	MMMMMMMM	MMMMMMMM	MMMMMMMM	MMMMMMMM	SMMMMMMM

  E: exponent, M: mantissa, S: sign bit

  conversion tests (using the 'convert' function, see below)
  48 bit hex        | PRN file | computed          | syntax
  ------------------+----------+-------------------+----------
  8d 25 7c e2 9d 07 | 4339.736 | 4339.735588349402 | convert(0x8d257ce29d07)
  88 a9 f6 62 91 42 |  194.568 | 194.5679163134191 | convert(0x88a9f6629142)
  8c 17 8f 82 1d 1f | 2545.844 | 2545.844374742359 | convert(0x8c178f821d1f)
  8a 4f 07 d4 9f 1e |  634.497 | 634.4973161956295 | convert(0x8a4f07d49f1e)
  8a a2 63 10 73 1a |  617.798 | 617.7978753168136 | convert(0x8aa26310731a)
  84 2a 07 a6 9a 23 |   10.225 | 10.22525599287474 | convert(0x842a07a69a23)
  86 33 7d cd 34 25 |   41.302 | 41.30156512855319 | convert(0x86337dcd3425)
  81 ca e2 e4 04 41 |    1.508 | 1.507961855637404 | convert(0x81cae2e40441)
  84 8f 69 b8 9a 41 |   12.100 | 12.10027352556062 | convert(0x848f69b89a41)
  81 89 16 b8 1a 05 |    1.040 | 1.039877902034277 | convert(0x818916b81a05)
  81 f1 d2 3b 23 00 |    1.001 | 1.001075246809705 | convert(0x81f1d23b2300)
  83 82 a8 96 4e 47 |    6.228 | 6.22834332381899  | convert(0x8382a8964e47)
  86 b6 3b 77 87 44 |   49.132 | 49.13229077623691 | convert(0x86b63b778744)
  00 00 00 00 00 00 |    0.000 | 0                 | convert(0x000000000000)
  8d ed 24 81 27 30 | 5636.938 | 5636.938058711588 | convert(0x8ded24812730)
  84 78 70 65 4c 63 |   14.206 | 14.2061514275847  | convert(0x847870654c63)
  8d d5 63 c1 ab 07 | 4341.469 | 4341.469428695738 | convert(0x8dd563c1ab07)
'''
import sys

#convert a chunk of 48 bits (pascal type "real") to float
def convert(n):
  if(n==0): return 0
  #create byte array from n
  ba=bytearray([
    (n & 0xff0000000000) >> 8*5, #byte 1
    (n & 0x00ff00000000) >> 8*4, #byte 2
    (n & 0x0000ff000000) >> 8*3, #byte 3
    (n & 0x000000ff0000) >> 8*2, #byte 4
    (n & 0x00000000ff00) >> 8*1, #byte 5
    (n & 0x0000000000ff) >> 8*0, #byte 6
  ]);
  #float = (1+mantissa)*2^exponent
  exponent = ba[0] - 129
  mantissa = 0.0
  value    = 1.0
  #foreach byte (except the first)
  for i in range(5,0,-1):
    startbit=7
    if(i==5): startbit=6 #skip the sign bit
    #foreach bit
    for j in range(startbit,-1,-1):
      value=value/2 #each bit is worth half the next bit but we're going backwards.
      if((ba[i]>>j)&1): #if this bit is set add the value
        mantissa += value
  #test for null value
  if(mantissa==1.0 and ba[0]==0): return 0.0
  #sign bit check
  if(ba[5] & 0x80): mantissa = -mantissa
  #create the float number
  return (1+mantissa)*pow(2.0,exponent)
  '''tests
    print(convert(0x8d257ce29d07))
    print(convert(0x88a9f6629142))
    print(convert(0x8c178f821d1f))
    print(convert(0x8a4f07d49f1e))
    print(convert(0x8aa26310731a))
    print(convert(0x842a07a69a23))
    print(convert(0x86337dcd3425))
    print(convert(0x81cae2e40441))
    print(convert(0x848f69b89a41))
    print(convert(0x818916b81a05))
    print(convert(0x81f1d23b2300))
    print(convert(0x8382a8964e47))
    print(convert(0x86b63b778744))
    print(convert(0x000000000000))
    print(convert(0x8ded24812730))
    print(convert(0x847870654c63))
    print(convert(0x8dd563c1ab07))
    sys.exit()
  '''

#read a "file.did"
assert(len(sys.argv)>3), "Usage: ./retrieve.py file.did [data_interval:10,15,30] [NoDiVars:17,18]"
did_filename  = sys.argv[1]      #filename.did
data_interval = int(sys.argv[2]) #10, 15 or 30
NoDiVars      = int(sys.argv[3]) #17, 18 number of variables

#assert data_interval and NoDiVars
assert(
  data_interval==10 or
  data_interval==15 or
  data_interval==30), 'Data interval must be "10", "15" or "30"'
assert(
  type(NoDiVars)==int),'NoDiVars must be an integer number'

#calculate data per day and number of dimensions 'NoDiVars'
data_per_day=int(24*60.0/int(data_interval))

#write spreadsheet headers
print(did_filename, data_interval, NoDiVars)
print("REACTOR; Time; ",end='')
for i in range(NoDiVars): print("Var {}; ".format(i+1),end='')
print(""); #add a newline after the headers

#init reactor 1 and time 0
reactor=1
time=0

#open did file
with open(did_filename,"rb") as did_file:
  numbers_read = 0; #counter for total numbers read
  rows_printed = 0; #counter for total rows printed
  chunk = True      #initial value for starting to read the file

  #read the file by chunks of 48 bits (6 bytes)
  while chunk:
    #print current reactor and time. Then, next reactor after 'data_per_day' rows are printed
    if numbers_read % NoDiVars==0:
      print("{}; {};".format(reactor, time), end=" ")
      if rows_printed > data_per_day:
        time=0
        reactor += 1
        rows_printed=0
      else:
        time += data_interval/60.0;

    chunk = did_file.read(6)                    #read next chunk of 6 bytes
    n = int.from_bytes(chunk, byteorder='big'); #convert byte chunk to int number
    f = convert(n);                             #convert 48bit int to float
    numbers_read +=1                            #increase counter for numbers read

    #check if end of row to add a newline and increase row counter
    if numbers_read % NoDiVars==0:
      end='\n'
      rows_printed+=1
    else:
      end=' '

    #print the 48 bit number that has been read from the did file
    print("{:.3f};".format(f), end=end)
