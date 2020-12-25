# Malware Analysis of SolarWinds backdoor (Sunburst)
## Notes
### Sample
OrionImprovementBusinessLayer.cs was extracted from sample available at https://app.any.run/tasks/4fc6b555-4f9b-4346-8df2-b59e5796eb88/

### Cracked Hashes
hashes/hashcat_team.cracked_hashes.txt contains all recovered strings by the Hashcat team available at:<br>
https://docs.google.com/spreadsheets/d/1u0_Df5OMsdzZcTkBDiaAtObbIOkMa5xbeXdKk_k0vWs/edit#gid=0

## Tools
### Python script (dencode.py) usage
Custom python script to decode & encode compressed base64 value and generate 'FNV-1a 64bit XOR' hash from value.
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
$ python3 dencode.py -v "C07NSU0uUdBScCvKz1UIz8wzNor3Sy0pzy/KdkxJLChJLXLOz0vLTC8tSizJzM9TKM9ILUpV8AxwzUtMyklNsS0pKk0FAA=="
Select * From Win32_NetworkAdapterConfiguration where IPEnabled=true

$ cat base64_list.txt | python3 dencode.py
```
Encode value(s)
```
$ python3 dencode.py -v "Select * From Win32_NetworkAdapterConfiguration where IPEnabled=true" -e
C07NSU0uUdBScCvKz1UIz8wzNor3Sy0pzy/KdkxJLChJLXLOz0vLTC8tSizJzM9TKM9ILUpV8AxwzUtMyklNsS0pKk0FAA==

$ cat values.txt | python3 dencode.py -e
```

#### Get hash for string
```
$ python3 dencode.py -v "pexplorer" -H
9903758755917170407

$ echo pexplorer | python3 dencode.py -H -a -s " " 
9903758755917170407 pexplorer

$ echo pexplorer | python3 dencode.py -H -A -s " " 
pexplorer 9903758755917170407

$ echo "procexp,procexp64" | tr "," "\n" | python3 dencode.py -H -a -s " "
6491986958834001955 procexp
27407921587843457 procexp64

$ cat values.txt | python3 dencode.py -H -a -s " "
```

### Quick scripts
#### Decode compressed base64 string
```
$ tools/decode_b64.sh C07NSU0uUdBScCvKz1UIz8wzNor3Sy0pzy/KdkxJLChJLXLOz0vLTC8tSizJzM9TKM9ILUpV8AxwzUtMyklNsS0pKk0FAA==
Select * From Win32_NetworkAdapterConfiguration where IPEnabled=true
```

#### Hash a string in 'FNV-1a 64bit XOR' format
```
$ tools/hash_value.sh Test
9212244707478111842 Test

$ tools/hash_value.sh test
11694290038524490306 test
```

#### Get result from cracked hashes based on string
```
$ tools/get_hash.sh accept
2734787258623754862 accept

$ tools/get_hash.sh Accept
2734787258623754862 accept
```

#### Get result from cracked hashes based on hash
```
$ tools/lookup_hash.sh 2734787258623754862
2734787258623754862 accept
```

#### Get result from cracked hashes based on matching "string"
```
$ tools/find_match.sh ui
607197993339007484 egui
9149947745824492274 jd-gui
11818825521849580123 avastui
12709986806548166638 avgui
13581776705111912829 ksdeui
13655261125244647696 f-secure webui daemon
14513577387099045298 eguiproxy
14971809093655817917 fswebuid
18147627057830191163 avpui

$ tools/find_match.sh mon
397780960855462669 hexisfsmonitor.sys
2128122064571842954 procmon
2597124982561782591 apimonitor-x64
2600364143812063535 apimonitor-x86
3538022140597504361 sysmon64
7810436520414958497 diskmon
12343334044036541897 sentinelmonitor.sys
13655261125244647696 f-secure webui daemon
14111374107076822891 sysmon
15587050164583443069 eamonm
18294908219222222902 regmon

$ tools/find_match.sh 123
7412338704062093516 ffdec
8760312338504300643 task explorer-64
10374841591685794123 win64_remotex64
10501212300031893463 microsoft.tri.sensor
11818825521849580123 avastui
12343334044036541897 sentinelmonitor.sys
```

## Output
### Extract sample data
#### Extract printable characters from sample binary
```
strings 32519b85c0b422e4656de6e6c41878e95fd95026267daab4215ee59c107d6c77.bin | strings | tee sample.bin.strings
cat sample.bin.strings | tr '[:upper:]' '[:lower:]' | tee sample.bin.strings.lowercase
```
#### Extract hardcoded base64 values from source
```
cat OrionImprovementBusinessLayer.cs | tr " " "\n" | grep -Eo 'Unzip\("(.+)"\)' | sed 's/Unzip("//g' | sed 's/")$//g' | tee OIBL.Unzip.b64

tools/extract_b64.sh OrionImprovementBusinessLayer.cs | tee OIBL.Unzip.b64
cat OrionImprovementBusinessLayer.cs | tools/extract_b64.sh | tee OIBL.Unzip.b64
```
#### Extract hardcoded 'FNV-1a 64bit XOR' hashes from source
```
cat OrionImprovementBusinessLayer.cs | grep -Eo "[0-9]+UL" | sed 's/UL$//g' | tee hashes/OIBL.hardcoded_hashes.txt
```

### Decode extracted data
#### Decode decompressed base64 values
```
cat OIBL.Unzip.b64 | python3 dencode.py -a -s " # " | tee OIBL.Unzip.b64.decoded
cat OIBL.Unzip.b64 | python3 dencode.py | tee OIBL.Unzip.b64.decompressed
```
#### Hash decompressed base64 values
```
cat OIBL.Unzip.b64.decompressed | python3 dencode.py -H -a -s " " | tee hashes/OIBL.Unzip.b64.decompressed.hashed
```

### Find known hashed "strings" matching hardcoded hashes
file format: hash string
```
$ cat hashed/sample.bin.strings.lowercase.hashes_only hashed/OIBL.Unzip.b64.decompressed.lowercase.hashed | sort -u > hashed/known_unique_hashes_only.txt
$ cat hashed/known_unique_hashes_only.txt hashed/OIBL.hardcoded_hashes.txt | sort | uniq -cd | sed 's/^[ \t]*//g' | cut -d " " -f 2
11266044540366291518
12445177985737237804
14710585101020280896
15695338751700748390
3200333496547938354
6116246686670134098
8698326794961817906
8873858923435176895
  
// find files with <hash>
$ grep -R --color=always <hash> *
```
