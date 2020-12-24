# Malware Analysis of SolarWinds backdoor (Sunburst)<br/><br/>
## Notes
### Sample
OrionImprovementBusinessLayer.cs was extracted from sample available at https://app.any.run/tasks/4fc6b555-4f9b-4346-8df2-b59e5796eb88/
### Cracked Hashes
hashes/hashcat_team.cracked_hashes.txt contains all recovered strings by the Hashcat team available at:<br>
https://docs.google.com/spreadsheets/d/1u0_Df5OMsdzZcTkBDiaAtObbIOkMa5xbeXdKk_k0vWs/edit#gid=0

## Tools
### Python script (dencode.py) usage
Custom python script to decode & encode base64 value and generate 'FNV-1a 64bit XOR' hash from value.
```
usage: dencode.py [-h] [--file FILE] [--value VALUE] [--append-value] [--reverse-append] [--separator SEPARATOR] [--encode] [--hash]

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  file with content to encode/decode
  --value VALUE, -v VALUE
                        value to encode/decode
  --append-value, -a    append ' # <value>' after decoded/encoded value
  --reverse-append, -A  prefix '<value># ' before decoded/encoded value
  --separator SEPARATOR, -s SEPARATOR
                        value to separate the appending (default: '# ')
  --encode, -e          use to encode instead of decode
  --hash, -H            hash the value
```

#### Decode/encode base64 value (Inflate and Deflate)
Decode value(s)
```
python3 dencode.py -v "C07NSU0uUdBScCvKz1UIz8wzNor3Sy0pzy/KdkxJLChJLXLOz0vLTC8tSizJzM9TKM9ILUpV8AxwzUtMyklNsS0pKk0FAA=="
Select * From Win32_NetworkAdapterConfiguration where IPEnabled=true

cat base64_list.txt | python3 dencode.py
```
Encode value(s)
```
python3 dencode.py -v "Select * From Win32_NetworkAdapterConfiguration where IPEnabled=true" -e
C07NSU0uUdBScCvKz1UIz8wzNor3Sy0pzy/KdkxJLChJLXLOz0vLTC8tSizJzM9TKM9ILUpV8AxwzUtMyklNsS0pKk0FAA==

cat values.txt | python3 dencode.py -e
```

#### Get hash for string
```
python3 dencode.py -v "pexplorer" -H
9903758755917170407

echo pexplorer | python3 dencode.py -H -a -s " " 
9903758755917170407 pexplorer

echo pexplorer | python3 dencode.py -H -A -s " " 
pexplorer 9903758755917170407

echo "procexp,procexp64" | tr "," "\n" | python3 dencode.py -H -a -s " "
6491986958834001955 procexp
27407921587843457 procexp64

cat values.txt | python3 dencode.py -H -a -s " "
```

## Extract the base64 values
```
cat OrionImprovementBusinessLayer.cs | tr " " "\n" | grep -Eo 'Unzip\("(.+)"\)' | sed 's/Unzip("//g' | sed 's/")$//g' | tee OIBL.Unzip.b64
```

## Decode & Decompress base64 values
```
cat OIBL.Unzip.b64 | python3 dencode.py -a -s " # " | tee OIBL.Unzip.b64.translate
cat OIBL.Unzip.b64 | python3 dencode.py | tee OIBL.Unzip.b64.decompressed
```
## Hash Decompress base64 values
```
cat OIBL.Unzip.b64.decompressed | python3 dencode.py -H -a -s " " | tee OIBL.Unzip.b64.decompressed.hashed
```

## Extract hardcoded hashes
```
cat OrionImprovementBusinessLayer.cs | grep -Eo "[0-9]+UL" | sed 's/UL$//g' | tee hashes/OIBL.hardcoded_hashes.txt
```

## Extract printable characters from sample binary
```
strings 32519b85c0b422e4656de6e6c41878e95fd95026267daab4215ee59c107d6c77.bin | strings | tee sample.bin.strings
cat sample.bin.strings | tr '[:upper:]' '[:lower:]' | tee sample.bin.strings.lowercase
```
