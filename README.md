Malware Analysis of SolarWinds backdoor (Sunburst)

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

cat ../data/data.b64 | head -n 2 | python dencode.py -a
Select * From Win32_NetworkAdapterConfiguration where IPEnabled=true# C07NSU0uUdBScCvKz1UIz8wzNor3Sy0pzy/KdkxJLChJLXLOz0vLTC8tSizJzM9TKM9ILUpV8AxwzUtMyklNsS0pKk0FAA==
Description# c0ktTi7KLCjJzM8DAA==
```
