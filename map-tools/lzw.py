charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

def encode(x):
  a = x // len(charset)
  b = x % len(charset)
  return charset[a] + charset[b]

def decode(x):
  return charset.index(x[0]) * len(charset) + charset.index(x[1])

def compress(text):
  d = {}
  for c in charset:
    d[c] = len(d.keys())
  
  res = []
  p = ""
  for c in text:
    pc = p + c
    if pc in d:
      p = pc
    else:
      d[pc] = len(d.keys())
      res.append(d[p])
      p = c
  
  if pc in d:
    res.append(d[p])
  
  return "".join(map(encode, res))

def decompress(text):
  text = [ decode(text[0+i:2+i]) for i in range(0, len(text), 2) ]
  
  d = {}
  for c in charset:
    d[len(d.keys())] = c
  
  res = d[text[0]]
  p = res
  for c in text[1:]:
    if c not in d:
      d[c] = p + p[0]
      res += d[c]
      p = d[c]
    else:
      res += d[c]
      d[len(d.keys())] = p + d[c][0]
      p = d[c]
  
  return res
