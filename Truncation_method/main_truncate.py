from Pedigrad import *

def read_tab_row(text):
  row = list()
  position = 0
  while position < len(text):
    save = position
    while position < len(text) and not(text[position] in ['\t', ' ']):
      position = position + 1
    row.append(text[save:position])
    position = position + 1
  return row

def read_tab_row_int(text):
  row = list()
  position = 0
  while position < len(text):
    save = position
    while position < len(text) and not(text[position] in ['\t', ' ']):
      position = position + 1
    if text[save:position] !='':
       row.append(int(float(text[save:position])))
    else:
       row.append(text[save:position])
    position = position + 1
  return row

def read_tab_stat(name_of_file):
  the_file = open(name_of_file,"r")
  text = str(the_file.read())
  the_file.close()
  labels = list()
  position = 0
  while position < len(text) and not(text[position] in ['\t',' ']) :
    position = position + 1
  position = position + 1
  save = position
  while position < len(text) and not(text[position] in ['\n','\r']):
    position = position + 1
  labels = read_tab_row(text[save:position])
  position = position + 1
  table = list()
  while position < len(text):
    while position < len(text) and not(text[position] in ['\t',' ']):
      position = position + 1
    position = position + 1
    save = position
    while position < len(text) and not(text[position] in ['\n','\r']):
      position = position + 1
    row = read_tab_row(text[save:position])
    if position < len(text):
      #This may happen in triangular tables:
      if len(row) < len(labels):
        for i in range(len(row),len(labels)):
          row.append('')
      table.append(row)
    position = position + 1
  return (labels,table)

def symmetric((labels,table)):
  for i in range(len(table)):
    for j in range(len(table[i])):
      if i ==i:
        table[i][i] = -1
      if i > j:
        table[j][i] = table[i][j]
  return (labels,table)

def convert_int_into_eqrel((labels,table),threshold):
  for i in range(len(table)):
    for j in range(len(table[i])):
      t = int(table[i][j])
      if t>=threshold:
        table[i][j] = 1
      else:
        table[i][j] = ''
  for i in range(len(table)):
    print(table[i])
  if len(table) == 1:
    return (labels,table)
  else:
    product = table[0]
    for i in range(len(table)-1):
      product = product_of_partitions(product,table[i+1])
    return (labels,product)

def convert_float_into_eqrel((labels,table),threshold):
  for i in range(len(table)):
    for j in range(len(table[i])):
      t = float(table[i][j])
      if t>=threshold:
        table[i][j] = 1
      else:
        table[i][j] = ''
  for i in range(len(table)):
    print(table[i])
  if len(table) == 1:
    return (labels,table)
  else:
    product = table[0]
    for i in range(len(table)-1):
      product = product_of_partitions(product,table[i+1])
    return (labels,product)

def labeled_preimage((labels,partition)):
  the_preimage = preimage_of_partition(partition)
  #print("Preimage",the_preimage)
  equiv_classes = list()
  for i in range(len(the_preimage)-1):
    if len(the_preimage[i+1]) > 1 :
      l = list()
      for j in range(len(the_preimage[i+1])):
        l.append(labels[the_preimage[i+1][j]])
      equiv_classes.append(l)
  return equiv_classes

tncod = convert_float_into_eqrel(symmetric(read_tab_stat("Mammal_noncodingRatio.tab")),18)
tnc = labeled_preimage(tncod)
#print(tncod[0])
#print(tncod[1])
print(tnc)

tcod = convert_float_into_eqrel(symmetric(read_tab_stat("Mammal_codingRatio.tab")),18)
tc = labeled_preimage(tcod)
#print(tcod[0])
#print(tcod[1])
print(tc)
