# Malware Analysis of SolarWinds backdoor (Sunburst)<br/>
OrionImprovementBusinessLayer.cs extracted from sample at https://app.any.run/tasks/4fc6b555-4f9b-4346-8df2-b59e5796eb88/

## python3 dencode.py -h
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

## decode/encode base64 value (Inflate and Deflate)
```
python3 dencode.py -v "C07NSU0uUdBScCvKz1UIz8wzNor3Sy0pzy/KdkxJLChJLXLOz0vLTC8tSizJzM9TKM9ILUpV8AxwzUtMyklNsS0pKk0FAA=="
Select * From Win32_NetworkAdapterConfiguration where IPEnabled=true

python3 dencode.py -v "Select * From Win32_NetworkAdapterConfiguration where IPEnabled=true" -e
C07NSU0uUdBScCvKz1UIz8wzNor3Sy0pzy/KdkxJLChJLXLOz0vLTC8tSizJzM9TKM9ILUpV8AxwzUtMyklNsS0pKk0FAA==
```

## get hash of string
```
python3 dencode.py -v "pexplorer" -H
9903758755917170407

echo pexplorer | python3 dencode.py -H -a
14549110565813358105# pexplorer
echo pexplorer | python3 dencode.py -H -a -s " " 
14549110565813358105 pexplorer
echo pexplorer | python3 dencode.py -H -A -s " " 
pexplorer 9903758755917170407

echo "procexp,procexp64" | tr "," "\n" | python3 dencode.py -H -a -s " "
6491986958834001955 procexp
27407921587843457 procexp64
```

## Extract the base64 values
```
cat OrionImprovementBusinessLayer.cs | tr " " "\n" | grep -Eo 'Unzip\("(.+)"\)' | sed 's/Unzip("//g' | sed 's/")$//g' | tee OIBL.Unzip.b64
```

## Decode base64 and Decompress the values
```
cat OIBL.Unzip.b64 | while read b64; do decoded=$(echo $b64 | python3 dencode.py); echo "$decoded # $b64"; done | tee OIBL.Unzip.b64.translated
```
