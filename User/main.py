from Pedigrad import *

Omega = PreOrder("omega.yml")
print Omega.relations
print Omega.mask
print Omega.cartesian
Omega.closure()
print "--after:"
print Omega.relations
print "--relation:"
print Omega.geq('1','2')
print Omega.geq('2','1')
print Omega.geq('4','3')
print Omega.geq('?','3')
print Omega.geq('?','?')
print "--infimum:"
print Omega.inf('2','3')
print Omega.inf('1','2')
print Omega.inf('?','3')
print "--presence test:"
print Omega.presence('3')
print Omega.presence('1')
print Omega.presence('?')

print "\n------------------------\n"

t = list()
c = list()
for i in range(0,20):
  t = t + [(i,i)]
  if i%15 in [11]:
    c = c + ['?']
  elif i%2 in [0]:
    c = c + ['1']
  elif i%2 in [1]:
    c = c + ['2'] 
s = SegmentObject(20,t,c)
sys.stdout.write("s = ")
s.display()
print "colors = "+str(s.colors)

s1 = s.merge([(0,3,9),(10,2,14),(15,3,19)],Omega.inf)
sys.stdout.write("s1 = ")
s1.display()
print "topology = "+str(s1.topology)
print "colors = "+str(s1.colors)

s2 = s.merge([(0,3,9),(10,2,14)],Omega.inf)
sys.stdout.write("s2 = ")
s2.display()

s2 = s2.remove([5,23])
sys.stdout.write("s2 = ")
s2.display()

s2.domain = s2.domain+4
sys.stdout.write("s2 = ")
s2.display()
print "colors = "+str(s2.colors)

s3 = s.merge([(0,3,9),(10,2,14)],Omega.inf)
sys.stdout.write("s3 = ")
s3.display()
s3 = s3.remove([1,5,6,8,10])
sys.stdout.write("s3 = ")
s3.display()
s3.topology = s3.topology+[(24,24)]
s3.colors = s3.colors+['5']

s3.domain = s3.domain+5
sys.stdout.write("s3 = ")
s3.display()
print "colors= "+str(s3.colors)

m = MorphismOfSegments(s2,s3,'id',Omega.geq)
print m.defined
sys.stdout.write("s = ")
m.source.display()
sys.stdout.write("t = ")
m.target.display()
print "f0 = "+str(m.f0)

print "\n------------------------\n"

Seg = CategoryOfSegments(Omega)

s = Seg.initial(18,'1')
s = s.merge([(2,2,8)],Omega.inf)

print Seg.identity(s,s)

t = Seg.initial(20,'1')
t = t.merge([(2,3,10),(15,2,18)],Omega.inf)

print Seg.identity(s,t)

sys.stdout.write("s = ")
s.display()
sys.stdout.write("t = ")
t.display()

h = Seg.homset(s,t)
for i in range(len(h)):
  print str(i)+") well-defined = "+str(h[i].defined)
  print "f1 = "+str(h[i].f1)
  print "f0 = "+str(h[i].f0)

print "\n------------------------\n"

E = PointedSet(['-','A','C','G','T'],0)

Env = Environment(Seg,E,5,['4']*5) #[] = white nodes
print Env.Seg.preorder.relations
print Env.pset.symbols
print Env.pset.point()
print Env.spec
print Env.b

s4 = Env.segment(['A','C','G','T','T','P','C','A','-','C','T'],'1')
s4.display()

print "\n------------------------\n"

Seqali = Env.seqali("align.fa")

print "\nDatabase\n" 

print Seqali.indiv
for i in range(len(Seqali.base)):
  print str(i)+") color: "+str(Seqali.base[i].colors[Seqali.base[i].parse])
  Seqali.base[i].display()
  for j in range(len(Seqali.database[i])):
    for k in range(len(Seqali.database[i][j])):
      print Seqali.database[i][j][k]
    print ""

print "\nImage\n" 
for i in range(len(Seqali.base)):
  print "base["+str(i)+"]"
  Seqali.base[i].display()
  sal = Seqali.eval(Seqali.base[i])
  for j in range(len(sal)):
    for k in range(len(sal[j])):
      print sal[j][k]
    print ""

print "\nExtending category\n" 
l= Seqali.extending_category(Seqali.base[0])
for i,m in l:
  print i
  print m.f1
  print m.f0
  
print "\nExtending category\n" 
l= Seqali.extending_category(Seqali.base[1])
for i,m in l:
  print i
  print m.f1
  print m.f0

print "\n------------------------\n"

a = list('AGCTAGCTGA')
b = list('GTGGATCGATGA')

A = Sequence('a',a,'1')
B = Sequence('b',b,'1')

table = Table(A,B)
print "\nincidence"
table.incidence()
table.stdout()
print "\nfillout"
table.fillout() 
table.stdout()
table.dynamic_programming("dprog.fa",option = "w",debug = False,display = True)

print "\n------------------------\n"

E = PointedSet(['-','A','C','G','T'],0)

Env = Environment(Seg,E,2,['1']*2) #[] = white nodes
Seqali = Env.seqali("dprog.fa")

print "\nImage\n" 

print Seqali.indiv
Seqali.base[0].display()
sal= Seqali.eval(Seqali.base[0])
for j in range(len(sal)):
  for k in range(len(sal[j])):
    print sal[j][k]
  print ""
