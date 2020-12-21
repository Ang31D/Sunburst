import zlib
import base64
import argparse
import sys
import select

parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", dest="file", default = "", help="file with content to encode/decode")
parser.add_argument("--value", "-v", dest="value", default = "", help="value to encode/decode")
parser.add_argument('--append-value', "-a", dest="append_value", action='store_true', help="append ' # <value>' after decoded/encoded value")
parser.add_argument("--separator", "-s", dest="separator", default = "# ", help="value to separate the appending (default: '# ')")
parser.add_argument('--encode', "-e", dest="encode", action='store_true', help="use to encode instead of decode")
parser.add_argument('--hash', "-H", dest="hash", action='store_true', help="hash the value")

args = parser.parse_args()

"""
* Python: Inflate and Deflate implementations
https://stackoverflow.com/questions/1089662/python-inflate-and-deflate-implementations
* How do I check if stdin has some data?
https://stackoverflow.com/questions/3762881/how-do-i-check-if-stdin-has-some-data
"""


"""
// Token: 0x06000057 RID: 87 RVA: 0x00004E7C File Offset: 0x0000307C
private static ulong GetHash(string s)
{
   ulong num = 14695981039346656037UL;
   try
   {
      foreach (byte b in Encoding.UTF8.GetBytes(s))
      {
         num ^= (ulong)b;
         num *= 1099511628211UL;
      }
   }
   catch
   {
   }
   return num ^ 6605813339339102567UL;
}
"""
"""
def GetHash(s):
   num = 14695981039346656037
   for b in s.encode():
      num = (num^int(b)) * 1099511628211
   return int(bin(num ^ 6605813339339102567)[-64:], 2)
"""
def GetHash(input):
    overflow = lambda num : num & ~(-1 << 64)
    num = 14695981039346656037
    for b in input.encode():
        num = overflow((num^b) * 1099511628211)
    return overflow(num ^ 6605813339339102567)
"""
// Token: 0x020000DA RID: 218
private static class ZipHelper
{
   ...
}
"""
class ZipHelper(object):
   @staticmethod
   def FromBase64String(s):
      return base64.b64decode(s)

   """
   // Token: 0x060009C3 RID: 2499 RVA: 0x000468FC File Offset: 0x00044AFC
   public static byte[] Compress(byte[] input)
   {
      byte[] result;
      using (MemoryStream memoryStream = new MemoryStream(input))
      {
         using (MemoryStream memoryStream2 = new MemoryStream())
         {
            using (DeflateStream deflateStream = new DeflateStream(memoryStream2, CompressionMode.Compress))
            {
               memoryStream.CopyTo(deflateStream);
            }
            result = memoryStream2.ToArray();
         }
      }
      return result;
   }
   """
   @staticmethod
   def Compress(input):
      result = zlib.compress(input.encode())
      return result[2:-4]

   """
   // Token: 0x060009C4 RID: 2500 RVA: 0x00046978 File Offset: 0x00044B78
   public static byte[] Decompress(byte[] input)
   {
      byte[] result;
      using (MemoryStream memoryStream = new MemoryStream(input))
      {
         using (MemoryStream memoryStream2 = new MemoryStream())
         {
            using (DeflateStream deflateStream = new DeflateStream(memoryStream, CompressionMode.Decompress))
            {
               deflateStream.CopyTo(memoryStream2);
            }
            result = memoryStream2.ToArray();
         }
      }
      return result;
   }
   """
   @staticmethod
   def Decompress(input):
      return zlib.decompress(input, -15)

   """
   // Token: 0x060009C5 RID: 2501 RVA: 0x000469F4 File Offset: 0x00044BF4
   public static string Zip(string input)
   {
      if (string.IsNullOrEmpty(input))
      {
         return input;
      }
      string result;
      try
      {
         result = Convert.ToBase64String(OrionImprovementBusinessLayer.ZipHelper.Compress(Encoding.UTF8.GetBytes(input)));
      }
      catch (Exception)
      {
         result = "";
      }
      return result;
   }
   """
   @staticmethod
   def Zip(input):
      return base64.b64encode(ZipHelper.Compress(input)).decode()

   """
   // Token: 0x060009C6 RID: 2502 RVA: 0x00046A40 File Offset: 0x00044C40
   public static string Unzip(string input)
   {
      if (string.IsNullOrEmpty(input))
      {
         return input;
      }
      string result;
      try
      {
         byte[] bytes = OrionImprovementBusinessLayer.ZipHelper.Decompress(Convert.FromBase64String(input));
         result = Encoding.UTF8.GetString(bytes);
      }
      catch (Exception)
      {
         result = input;
      }
      return result;
   }
   """
   @staticmethod
   def Unzip(input):
      return ZipHelper.Decompress(ZipHelper.FromBase64String(input)).decode()

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
   if (args.hash):
      dencoded = GetHash(value.strip())
   elif (not args.encode):
      dencoded = ZipHelper.Unzip(value.strip()).strip()
   else:
      dencoded = ZipHelper.Zip(value.strip()).strip()

   if (args.append_value):
      print("{}{}{}".format(dencoded, args.separator, value.strip()))
   else:
      print(dencoded)
