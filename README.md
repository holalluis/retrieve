# requirements
- python3 (https://www.python.org/)

# how to use
Usage:   
```
./retrieve.py [filename.did] [data-interval] [NoDiVars] > [filename.csv]
```
Example: 
```
./retrieve.py DP16SETP.DID 15 23 > DP16SETP.CSV
```

# retrieve
Translation of "RETRIEVE.PAS" (Pascal programming language) to Python3 ("retrieve.py")

Created by Lluís Bosch (lbosch@icra.cat) on 2018-12-20.

Request by George Ekama:
```
There are 2 old programs (UCTOLD and UCTPHO) that run as “UCTOLD.exe” and
“UCTPHO.exe” files which were generated (~1990) by compiling TurboPascal 4.0
files.

These programs both generate output files with an 8 character alphanumeric
string of user choice and a “did” extension  e.g.  “CTWWTP05.did”.

This .did output file is then converted to a print (.prn)  file with another
TurboPascal 4.0 program called “RETRIEVE.exe”, which reads the e.g.
“CTWWTP05.did” file and converts it to a “CTWWTP05.prn” file, that can be
imported into spreadsheets to work with the output results.

The UCTOLD is for simulating biological N removal plants and UCTPHO is for
simulating biological N and P removal plants.

The only “RETRIEVE.exe” file I have (dated 1991/08/15 1:13pm) works only for “
.did” files generated by UCTOLD, not for “ .did” files generated by UCTPHO.

I suspect there was a second RETRIEVE.exe file that worked for UCTPHO but it
seems I have lost it.

As a result last year (2017) I could give the Postgraduate (PG) class only
simulation exercises with UCTOLD, not UCTPHO because the UCTPHO output could
not be imported into Excel.

I would like the “RETRIEVE.exe” code to work for both UCTOLD and UCTPHO so that
next year (2019) I can give the PG class simulation exercises with both UCTOLD
and UCTPHO.

I have four Retrieve.pas files and I attach the youngest RETRIEVE.pas (dated
1991/06/03 9:56am) file that presumably generated the RETRIEVE.exe  file.

Do you think the RETRIEVE.pas code can be translated to some new software like
Python so that I can use the RETRIEVE code for both UCTOLD and UCTPHO?
```

The specification of the Turbo Pascal 48 bit "Real" type was found on: http://www.shikadi.net/moddingwiki/Turbo_Pascal_Real 

While most languages use a 32-bit or 64-bit floating point decimal variable,
usually called single or double, Turbo Pascal featured an uncommon 48-bit float
called a real which served the same function as a float. 32 and 64-bit floats
were introduced in Turbo Pascal version 5. Pascal's successor, Delphi, did not
feature reals as a variable type.

A Pascal real has a value range of 2.9 x 10-39 to 1.7 x 1038.

The structure of a Pascal real is seen in the diagram below.

```
Byte  0        1        2        3        4        5
Bit   01234567 01234567 01234567 01234567 01234567 01234567
Value EEEEEEEE MMMMMMMM MMMMMMMM MMMMMMMM MMMMMMMM SMMMMMMM
```

E: exponent, M: mantissa, S: sign bit

float conversion tests

```
48 bit hex        | PRN file | computed          | syntax
------------------+----------+-------------------+------------------------
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
```
