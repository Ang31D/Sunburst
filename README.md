# Malware Analysis of SolarWinds backdoor (Sunburst)<br/>
Sample from https://app.any.run/tasks/4fc6b555-4f9b-4346-8df2-b59e5796eb88/

## decode/encode base64 value (Inflate and Deflate)
```
usage: dencode.py [-h] [--encode] [--file FILE] [--value VALUE]
                  [--append-value]

optional arguments:
  -h, --help            show this help message and exit
  --encode, -e          use to encode instead of decode
  --file FILE, -f FILE  file with content to encode/decode
  --value VALUE, -v VALUE
                        value to encode/decode
  --append-value, -a    append ' # <value>' after decoded/encoded value
```

```
python dencode.py -v "C07NSU0uUdBScCvKz1UIz8wzNor3Sy0pzy/KdkxJLChJLXLOz0vLTC8tSizJzM9TKM9ILUpV8AxwzUtMyklNsS0pKk0FAA=="
Select * From Win32_NetworkAdapterConfiguration where IPEnabled=true

python dencode.py -v "Select * From Win32_NetworkAdapterConfiguration where IPEnabled=true" -e
C07NSU0uUdBScCvKz1UIz8wzNor3Sy0pzy/KdkxJLChJLXLOz0vLTC8tSizJzM9TKM9ILUpV8AxwzUtMyklNsS0pKk0FAA==
```

## Extract the base64 values
```
cat OrionImprovementBusinessLayer.cs | tr " " "\n" | grep -Eo 'Unzip\("(.+)"\)' | sed 's/Unzip("//g' | sed 's/")$//g' | tee OIBL.Unzip.b64
```

## Decode base64 and Decompress the values
```
cat OIBL.Unzip.b64 | while read b64; do decoded=$(echo $b64 | python ../tools/dencode.py); echo "$decoded # $b64"; done | tee OIBL.Unzip.b64.translated
```
