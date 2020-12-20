Malware Analysis of SolarWinds backdoor (Sunburst)
Sample from https://app.any.run/tasks/4fc6b555-4f9b-4346-8df2-b59e5796eb88/

# decode/encode base64 value (Inflate and Deflate)
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

# Extract the base64 values
```
cat OrionImprovementBusinessLayer.cs | tr " " "\n" | grep -Eo 'Unzip\("(.+)"\)' | sed 's/Unzip("//g' | sed 's/")$//g' | tee OrionImprovementBusinessLayer.cs.Unzip.b64
```

Decode base64 and Decompress the values
```
cat OrionImprovementBusinessLayer.cs.Unzip.b64 | head -n 10 | python ../tools/dencode.py -a

Select * From Win32_NetworkAdapterConfiguration where IPEnabled=true# C07NSU0uUdBScCvKz1UIz8wzNor3Sy0pzy/KdkxJLChJLXLOz0vLTC8tSizJzM9TKM9ILUpV8AxwzUtMyklNsS0pKk0FAA==
Description# c0ktTi7KLCjJzM8DAA==
MACAddress# 83V0dkxJKUotLgYA
DHCPEnabled# c/FwDnDNS0zKSU0BAA==
DHCPServer# c/FwDghOLSpLLQIA
DNSHostName# c/EL9sgvLvFLzE0FAA==
DNSDomainSuffixSearchOrder# c/ELdsnPTczMCy5NS8usCE5NLErO8C9KSS0CAA==
DNSServerSearchOrder# c/ELDk4tKkstCk5NLErO8C9KSS0CAA==
IPAddress# 8wxwTEkpSi0uBgA=
IPSubnet# 8wwILk3KSy0BAA==
```
