import requests, re, argparse, os, sys
sys.setrecursionlimit(999999999)

class UnPipsomania:
   def __init__ ( self, options ):
      _, self.filename = os.path.split(options.filename)
      self.source = options.source
      self.output = options.output

   def decode_all_hex ( self ):
      rq = re.findall(r'\\x([a-fA-F0-9]{2})', self.source)
      print(f"[+] converting all hex.. {len(rq)}")
      for i in rq:
         j = "27" if i == "22" else i
         self.source = self.source.replace(f"\\x{i}", bytes.fromhex(j).decode("utf8"))

   def translate_globals ( self ):
      rq = re.findall(r'((\${"GLOBALS"}\["([a-z]+)"\])="(.*?)";)', self.source)
      print(f"[+] search for globals variable.. {len(rq)}")
      for i in rq:
         self.source = self.source.replace('${'+i[1]+'}', f"${i[3]}").replace(i[0], "")

   def translate_id ( self, msg ):
      rq = re.findall(r'(\$([a-z]+)="(.*?)";)',msg)
      for i in rq:
         if '${$'+i[1]+'}' in msg:
            msg = msg.replace('${$'+i[1]+'}', f"${i[2]}").replace(i[0], "")
      if "${$" in msg: return self.translate_id(msg)
      return msg

   def beautify ( self ):
      print("[+] formatting code.. ", end="")

      data = {
         'data': self.source, 'indentation_style': 'k&r',
         'indent_with': 'spaces', 'indentation_size': '4',
         'ArrayNested': 'ArrayNested', 'EqualsAlign': '',
         'Fluent': 'Fluent', 'KeepEmptyLines': 'KeepEmptyLines',
         'ListClassFunction': '', 'Lowercase': 'Lowercase',
      }
      
      try: 
         self.source = requests.post('https://beautifytools.com/pb.php', data=data).text
         print("done")
      except: print("\n[+] there was an error formatting... using original")

   def decode ( self ):
      self.decode_all_hex()
      self.translate_globals()

      print("[+] replacing fake variable..")
      self.source = self.translate_id(self.source).replace('"\\"', '"\\\\"')
      self.beautify()

      if self.source != "":
         file_output = f"dec_{self.filename}" if self.output == None else self.output
         open(file_output, "w").write(self.source)
         print(f"[+] saving file to : {file_output}")
      else: print("[-] error, empty result")

def getArgs ():
   arg	= argparse.ArgumentParser(description = "[+] Easy Decryptor For Pipsomania")
   arg.add_argument("filename", help="Source File")
   arg.add_argument("-o", "--output", help="")
   args = arg.parse_args()

   if not os.path.exists(args.filename):
      exit("[-] error file not found in path")
   
   args.source = open(args.filename, "r").read().replace("}as$", "} as $")
   return args

if __name__ == "__main__":
   print("""
█░█ █▄░█ █▀█ █ █▀█ █▀ ▄▀ █▀█ ▀▄
█▄█ █░▀█ █▀▀ █ █▀▀ ▄█ ▀▄ █▄█ ▄▀
github.com/nopebee7/unpipso
   """)

   options = getArgs()
   UnPipsomania(options).decode()