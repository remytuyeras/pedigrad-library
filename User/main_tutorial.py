from Pedigrad import *

ribosome = read_alignment_file("ribosome.fa",READ_DNA)

indices = list()
transpose = list()
for i in range(len(ribosome[1][0])):
  column = list()
  for j in range(len(ribosome[1])):
    column.append(ribosome[1][j][i])
  if not(column_is_trivial(column,[])):
    transpose.append(column)
    indices.append(i)

Seg_rb = CategoryOfSegments("omega.yml",len(ribosome[1][0]))

unknown = read_alignment_file("unknown.fa",READ_DNA)
Seg_ukn = CategoryOfSegments("omega.yml",len(unknown[1][0]))

parse_coding = list()
for i in range(Seg_ukn.domain):
  if i % 3 ==0:
    parse_coding.append(Seg_ukn.segment([(i,3,1,'codr')]))

def print_parsing_method(list_of_segments):
  for i in range(len(list_of_segments)):
    print((list_of_segments[i].topology,list_of_segments[i].colors))

print_parsing_method(parse_coding)

parse_ncoding = list()
for i in range(Seg_ukn.domain):
  if i % 2 ==0 and (i+1 < Seg_ukn.domain):
    parse_ncoding.append(Seg_ukn.segment([(i,2,1,'ncdr')]))

print_parsing_method(parse_ncoding)

parse_ground0 = list()
parse_ground1 = list()
for i in range(Seg_ukn.domain):
  if i % 3 ==0 and (i+2 < Seg_ukn.domain):
    parse_ground0.append(Seg_ukn.segment([(i,2,1,'read'),(i+2,1,1,'read')]))
  if i % 3 == 0 and (i+2 < Seg_ukn.domain):
    parse_ground1.append(Seg_ukn.segment([(i,1,1,'read'),(i+1,2,1,'read')]))
parse_ground = parse_ground0 + parse_ground1

print_parsing_method(parse_ground)

Loc_rb = LocalAnalysis(NUCL_MODE,'read',"omega.yml",Seg_rb.domain)

for i in range(len(Loc_rb.base)):
  print("segment " + str(i+1) + ": " + str(Loc_rb.base[i].topology) + " " + str(Loc_rb.base[i].colors) + " ---> " + str(ID_to_EQ(Loc_rb.equiv[i])))

N01_EQ.extend([["ATA","GTG"],["CTA","TTG"],["TTA","CTG"]])

equiv_coding = list()
for i in range(len(parse_coding)):
  equiv_coding.append(N01_ID)

Loc_coding =LocalAnalysis(SEGM_MODE,parse_coding,equiv_coding,"omega.yml",Seg_ukn.domain)

for i in range(len(Loc_coding.base)):
  print("segment " + str(i+1) + ": " + str(Loc_coding.base[i].topology) + " " + str(Loc_coding.base[i].colors) + " ---> " + str(ID_to_EQ(Loc_coding.equiv[i])))

N02_EQ.extend([["CA","TG"]])

equiv_ncoding = list()
for i in range(len(parse_ncoding)):
  equiv_ncoding.append(N02_ID)

Loc_ncoding = LocalAnalysis(SEGM_MODE,parse_ncoding,equiv_ncoding,"omega.yml",Seg_ukn.domain)

for i in range(len(Loc_ncoding.base)):
  print("segment " + str(i+1) + ": " + str(Loc_ncoding.base[i].topology) + " " + str(Loc_ncoding.base[i].colors) + " ---> " + str(ID_to_EQ(Loc_ncoding.equiv[i])))

P_rb = Pedigrad("ribosome.fa",READ_DNA,NUCL_MODE,'read',"omega.yml")

for i in range(len(P_rb.local)):
  print("segment " + str(P_rb.base[i].topology) + " "+ str(P_rb.base[i].colors) + " ---> " +str(P_rb.local[i]))

print(P_rb.partition([(5,1,1,'read')],EXPR_MODE))
print(P_rb.partition([(5,1,1,'read'),(6,1,1,'read')],EXPR_MODE))
print(P_rb.partition([(5,1,1,'read'),(9,1,1,'read')],EXPR_MODE))

Q = P_rb.isolate(NEW,['C'])

for i in range(len(Q.local)):
  print("segment " + str(Q.base[i].topology)+ " "+ str(Q.base[i].colors) + " ---> " +str(Q.local[i]))

print(Q.partition([(5,1,1,'read')],EXPR_MODE))
print(Q.partition([(5,1,1,'read'),(6,1,1,'read')],EXPR_MODE))
print(Q.partition([(5,1,1,'read'),(9,1,1,'read')],EXPR_MODE))

P_codr = Pedigrad("unknown.fa",READ_DNA,SEGM_MODE,parse_coding,equiv_coding,"omega.yml")
P_ncdr = Pedigrad("unknown.fa",READ_DNA,SEGM_MODE,parse_ncoding,equiv_ncoding,"omega.yml")

for i in range(len(P_codr.local)):
  print("segment " + str(P_codr.base[i].topology) + " "+ str(P_codr.base[i].colors) + " ---> " +str(P_codr.local[i]))

for i in range(len(P_ncdr.local)):
  print("segment " + str(P_ncdr.base[i].topology) + " "+ str(P_ncdr.base[i].colors) + " ---> " +str(P_ncdr.local[i]))

print(P_codr.partition([(0,2,1,'read'),(2,1,1,'read')],EXPR_MODE))
print(P_ncdr.partition([(0,2,1,'read'),(2,1,1,'read')],EXPR_MODE))

print("\n{{Alignment}}\n")
for i in range(len(P_rb.local)):
  print("Segment "+str(P_rb.base[i].topology)+ " ---> " + str(preimage_of_partition(P_rb.local[i])))

p = list()
for i in range(len(P_rb.taxa)):
  p.append([[i]])
pgy = Phylogeny(p)

print("\n{{Mathematical phylogeny}}\n")
for i in range(len(pgy.phylogeneses)):
  print(P_rb.taxa[i] + " = " + str(pgy.phylogeneses[i].history))

keep_going = True

#if keep_going:
while(keep_going):

  print("\n{{Set up friendship}}\n")
  friendship =  pgy.set_up_friendships()
  for i in range(len(P_rb.taxa)):
    print("----->"+str(P_rb.taxa[i])+"'s network: ")
    for j in range(len(friendship[0][i])):
      print("> common ancestor with " + str(P_rb.taxa[friendship[0][i][j]]) + ": "+ str(friendship[1][i][j]))
      
  print("\n{{Score friendship}}\n")
  scores = pgy.score(P_rb.local,pgy.set_up_friendships())
  for i in range(len(scores)):
    print("----->"+ str(P_rb.taxa[i]))
    for j in range(len(scores[i])):
      print(">" + str(P_rb.taxa[scores[i][j][0]]) + ": L = "+str(8+scores[i][j][1]) + ", E = "+str(scores[i][j][2]))
      
  print("\n{{Choose friendship}}\n")
  choose_friends = pgy.choose(scores)
  for i in range(len(choose_friends)):
    print("----->"+ str(P_rb.taxa[i])+"'s closet relative(s): ")
    for j in range(len(choose_friends[i])):
      print(">" + str(P_rb.taxa[choose_friends[i][j]]))

  print("\n{{Set up competition}}\n")
  competition =  pgy.set_up_competition(choose_friends)
  for i in range(len(competition)):
    print("----->"+str(P_rb.taxa[i])+"'s team: ")
    for j in range(len(competition[i])):
      print(">" + str(P_rb.taxa[competition[i][j]]))
  adjusted_competition = ([range(len(competition))],[competition])  

  print("\n{{Score competition}}\n")
  scores = pgy.score(P_rb.local,adjusted_competition)
  #print(scores)
  for j in range(len(scores[0])):
    print(">" + str(P_rb.taxa[scores[0][j][0]]) + ": L = "+str(8+scores[0][j][1]) + ", E = "+str(scores[0][j][2]))
  
  print("\n{{Choose competition}}\n")
  choose_competitors = pgy.choose(scores)
  c = list()
  for i in range(len(choose_competitors[0])):
    c.append((choose_competitors[0][i],competition[choose_competitors[0][i]]))
    print("----->"+P_rb.taxa[choose_competitors[0][i]]+"'s winners: ")
    for j in range(len(competition[choose_competitors[0][i]])):
      print(">"+P_rb.taxa[competition[choose_competitors[0][i]][j]])
  
  print("\n{{Extension}}\n")
  keep_going = pgy.extend(c)
  print("CONTINUE: "+str(keep_going))

  #Display current phylogeny
  if keep_going == True:
    for i in range(len(pgy.phylogeneses)):
      print("\nTree for " + str(P_rb.taxa[pgy.phylogeneses[i].taxon])+":")
      try:
        pgy.phylogeneses[i].print_tree()
      except:
        {}

print("\n{{Phylogeny}}")
for i in range(len(pgy.phylogeneses)):
  print("\nTree for " + str(P_rb.taxa[pgy.phylogeneses[i].taxon])+":")
  pgy.phylogeneses[i].print_tree()

print("\n{{Mathematical phylogeny}}\n")
for i in range(len(pgy.phylogeneses)):
  print(P_rb.taxa[i] + " = " + str(pgy.phylogeneses[i].history))


print("\n{{Agreements}}\n")
for i in range(len(pgy.phylogeneses)):
  print("----->"+P_rb.taxa[i])
  print("Coding")
  for j in range(len(pgy.phylogeneses[i].history)):
    u = EquivalenceRelation([pgy.phylogeneses[i].history[j]],len(pgy.phylogeneses)-1)
    a = P_codr.agree(parse_ground,u.quotient())
    print(">" + str(pgy.phylogeneses[i].history[j]) + "(" + str(len(a))+")")
    #for k in range(len(a)):
    #  sys.stdout.write(str(a[k].topology)+" ")
    #sys.stdout.flush()
    #print("")
  print("Non-coding")
  for j in range(len(pgy.phylogeneses[i].history)):
    u = EquivalenceRelation([pgy.phylogeneses[i].history[j]],len(pgy.phylogeneses)-1)  
    b = P_ncdr.agree(parse_ground,u.quotient())
    print(">" + str(pgy.phylogeneses[i].history[j]) + "(" + str(len(b))+")")
    #for k in range(len(b)):
    #  sys.stdout.write(str(b[k].topology)+" ")
    #sys.stdout.flush()
    #print("")
      

