import zlib
import base64
import argparse
import sys
import select

parser = argparse.ArgumentParser()
parser.add_argument('--encode', "-e", dest="encode", action='store_true', help="use to encode instead of decode")
parser.add_argument("--file", "-f", dest="file", default = "", help="file with content to encode/decode")
parser.add_argument("--value", "-v", dest="value", default = "", help="value to encode/decode")
parser.add_argument('--append-value', "-a", dest="append_value", action='store_true', help="append ' # <value>' after decoded/encoded value")


args = parser.parse_args()

"""
* Python: Inflate and Deflate implementations
https://stackoverflow.com/questions/1089662/python-inflate-and-deflate-implementations
* How do I check if stdin has some data?
https://stackoverflow.com/questions/3762881/how-do-i-check-if-stdin-has-some-data
"""

class ZipHelper(object):
   @staticmethod
   def FromBase64String(s):
      return base64.b64decode(s)

   @staticmethod
   def Compress(input):
      result = zlib.compress(input)
      return result[2:-4]

   @staticmethod
   def Decompress(input):
      return zlib.decompress(input, -15)

   @staticmethod
   def Zip(input):
      return base64.b64encode(ZipHelper.Compress(input))

   @staticmethod
   def Unzip(input):
       return ZipHelper.Decompress(ZipHelper.FromBase64String(input))

data = []
if (select.select([sys.stdin,],[],[],0.0)[0]):
   data = sys.stdin.readlines()
elif (len(args.file) > 0):
   with open(args.file, 'r') as f:
      data = f.readlines()
elif (len(args.value) > 0):
   data.append(args.value)
else:
   print("error: no input value to encode/decode")
   parser.print_help(sys.stderr)
   sys.exit(1)

for value in data:
   dencoded = ""
   if (not args.encode):
      dencoded = ZipHelper.Unzip(value.strip())
   else:
      dencoded = ZipHelper.Zip(value.strip())

   if (args.append_value):
      print("{}# {}".format(dencoded.strip(), value.strip()))
   else:
      print(dencoded.strip())
