from functools import lru_cache 
cut="S"
@lru_cache(maxsize=10)
def encpass(pas):
  num = sum([ord(x) for x in pas])
  return sum([ord(x)*num for x in pas])

def encrypt(sdata,password):
  pas = encpass(password)
  return cut.join([str(ord(x)*pas) for x in sdata])

def decrypt(edata,password):
  pas = encpass(password)
  return "".join([chr(int(int(x)/pas)) for x in edata.split(cut)])

