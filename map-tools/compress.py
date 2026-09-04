import zlib
import csv
import re
import math
import lzw
import json

map_name = "botr1.txt"
output_name = "output.txt"

N = 23

column_sets = [ set() for i in range(N) ]
rows = []

with open(map_name) as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  for row in reader:
    row = list(row)
    if len(row) > N:
      row[N - 1] = ",".join(row[N-1:])
      row = row[:N]
    elif len(row) < N:
      print(len(row))
      continue
      
    rows.append(row)
    for i, col in enumerate(row):
      column_sets[i].add(col)

column_order = sorted([ i for i in range(N) ], key=lambda x: len(column_sets[x]))
rows.sort(key=lambda x : [ x[k] for k in column_order ] )
columns = [ [row[i] for row in rows] for i in range(N) ]

def compress_column_rle(column):
  res = []
  
  a = column[0]
  count = 1
  
  for b in column[1:]:
    if a == b:
      count += 1
    else:
      res.append((a, count))
      a = b
      count = 1
  
  res.append((a, count))
  res = ",".join(f"{x[1]},{x[0]}" for x in res)
  res = lzw.compress(res)
  
  return res

def compress_column(column):
  text = ",".join(column)
  res = lzw.compress(text)
  return res

c_type = ""
data = []

total = 0
for i in range(N):
  M = len(column_sets[i])
  if M < 256:
    c_type += "0"
    data.append("string:" + compress_column_rle(columns[i]))
  else:
    c_type += "1"
    data.append("string:" + compress_column(columns[i]))

result = {
  "n": "int:" + str(len(columns[0])),
  "t": "string:" + c_type,
}

for i, column in enumerate(data):
  result[str(i)] = column

compressed = json.dumps(result)

with open(output_name, "w") as f:
  f.write(compressed)
  
with open(map_name) as f:
  print("Original Size:", len(f.read()))

print("Compressed Size:", len(compressed))
