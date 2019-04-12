#------------------------------------------------------------------------------
#Phylogeny: .phylogeneses, .coalescent, .extend, .make_friends, .score, 
#.choose, .set_up_competition, .compute
#------------------------------------------------------------------------------
'''
This class possesses one object, namely
- .phylogeneses (Phylogenesis item)
and ten methods, namely
- .__init__ (constructor)
- .coalescent
- .extend
- .count_uniformity
- .boolean_partition
- .make_friends
- .set_up_friendships
- .score
- .choose_friends
- .set_up_competition
- .score_dominance
- .choose_dominants



The object .phylogenesis is supposed to contained a list of Phylogenesis items.
The taxon associated with the i-th phylogenesis should be indexed by the interger i itself and any label appearing in the Phylogenesis items of the list should have its own Phylogenesis item in the list.



The constructor .__init__ takes a list of lists of lists containing indices and use every internal list of the input to create a Phylogenesis item, which is stored in the object .phylogeneses.



The method .coalescent() returns the list of the first generations (i.e the last lists) of the objects .history of each of the Phylogenesis item contained in the object .phylogeneses. The k-th list of the output is the first generation of the history of taxon k. 



The method .extend takes a list of pairs of the form (t,l) where t is the label of a taxon and l is a list of taxa and updates the object .phylogeneses as follows:
--> for all pairs (t,l) contained in the input passed to .extend:
1) if every list l contains the last list of self.phylogeneses[t].history and if at least one of the lists l strictly contains the last list of
self.phylogeneses[t].history, then every list l is appended to the list self.phylogeneses[t].history and the value True is returned;
  2) if there is no strict inclusion of the last list of self.phylogeneses[t].history into l, then the object .phylogeneses is not modified and the value False is returned;
  3) otherwise, an error message is returned and the procedure exit the program;
--> in any terminating case, for all other taxa t of the phylogeny that do not appear in the input of .extend, the last list of self.phylogeneses[t].history (i.e. the first generation of the history of the phylogenesis of t) is again repeated (i.e. appended again) in the list self.phylogeneses[t].history.



The method .make_friends takes the label of a taxon (i.e. a non-negative integer) and returns a pair of lists (friends,hypothesis). The list 'friends' contains all those taxa that have not coalesced with the input taxon, which means that there are not in the first generation of phylogenesis of the taxon. while the list 'hypothesis' contains the lists obtained by making the union of the first generation of the input taxon with the first generation of one of the taxon in 'friends'.



The method .set_up_friendships() returns a pair of lists (friendships,hypotheses) containing the lists of the two different outputs of the method .make_friends for every taxon of the phylogeny. More specifically, 
  - 'friendships' is the list of lists whose i-th list contains the first output of the procedure self.make_friends for taxon i;
  - 'hypotheses'  is the list of lists whose i-th list contains the second output of the procedure self.make_friends for taxon i;




The method .score takes a list of lists of non-negative integers (i.e. partitions) and a pair of lists, say (friendships,hypotheses), where
  - friendships is a list of lists;
  - hypotheses is a list of lenght len(friendships) whose t-th element is a
    list of length len(friendships[t]) whose elements are lists of integers
    ranging from 0 to len(self.phylogeneses)-1 (preferrably sorted from
    smallest to greatest);
and returns a list of length len(friendships) whose t-th element is a list of triples of the form (r,large,exact) where
  - r runs over the elements of friendships[t],
  - 'large' is the large score [4] of the hypothetical ancestor 
    hypotheses[t][r] within the set of ancestors contained in 
    hypotheses[t] for the list of partitions given in the input,
  - 'exact' is the exact score [4] of the hypothetical ancestor 
    hypotheses[t][r] within the set of ancestors contained in 
    hypotheses[t] for the list of partitions given in the input.

This means that 'large' is the number of partitions belonging to the first input list for which there is a morphism of partition x.quotient() -> partitions[i]
where we take

x = EquivalenceRelation([hypotheses[t][r]],len(self.phylogeneses)-1)

and 'exact' is the number of partitions that were counted in the large score of r such that if these partitions belong to the large score of any other element s in friendships[t], then either the equality hypotheses[t][r] = hypotheses[t][s] holds or the intersection of hypotheses[t][r] with hypotheses[t][s] is empty.
The second input of the method .score can, for instance, be taken to be the output of the procedure self.set_up_friendships().


The method .choose takes a list of lists of triples (r,l,e) where l and e are non-negative integers and returns a list of lists whose i-th list is the list of element r of the i-th internal list of the input list for which the associated pairs (l,e) are equal to the greatest local maxima of the function (e,l) -> (l,e) ordered by the lexicographical order and relative to the pairs of the i-th internal list of the input list.


The method .set_up_competition takes a list of lists of integers whose length must be equal to the length of self.phylogeneses (i.e. the number of taxa of the phylogeny) and returns a list of lists of integers whose length is also equal to the length of self.phylogeneses and whose t-th internal list is the union of the t-th list of self.coalescent() with the r-th lists of self.coalescent() for every element r in the t-th internal list of the input list.

'''

from cl_pgs import Phylogenesis

import sys
sys.path.insert(0, 'Pedigrad_py/AsciiTree/')
from pet import print_evolutionary_tree

import sys
sys.path.insert(0, 'Pedigrad_py/PartitionCategory/')
from iop import _image_of_partition
from cl_er import EquivalenceRelation
from cl_mop import MorphismOfPartitions
from efp import _epi_factorize_partition

class Phylogeny:
  #The objects of the class are:
  #.phylogeneses (lists of Phylogenesis items)
  def __init__(self,phylogeneses):
    #Allocates a space in the memory to store the list of phylogenesis items
    #passed to the procedure. The allocation happens after the format of the
    #has been checked to be valid.
    self.phylogeneses = list()
    #The following lines
    for i in range(len(phylogeneses)):
      #A phylogenesis item is created by using the list of lists 
      #(i.e. the history) contained in phylogeneses[i][1].
      phy = Phylogenesis(phylogeneses[i])
      #If the i-th phylogenesis contained phylogeneses is not that of taxon
      #i, then the phylogenesis is not valid and the procedure returns an
      #error message before exiting the program. If the taxon of the i-th
      #phylogensis is i, then the Phylogenesis item is added to the list
      #contained in the object .Phylogeneses.
      if i != phy.taxon:
        print("Error: in Phylogeny: phylogeneses is invalid (no taxon should be missing and the taxa should be given in increasing order)")
        exit()
      else:
        self.phylogeneses.append(phy)
    #The following loop checks whether all the taxa coalescing with
    #the taxon i are all included in the range of the set of taxa of the
    #Phylogeny. 
    for i in range(len(self.phylogeneses)):
      #Gets the maximal taxa for the i-th phylogenesis by looking at the 
      #first generation.
      max_taxon = max(self.phylogeneses[i].history[len(self.phylogeneses[i].history)-1])
      #If the label of the maximal taxa contained the i-th phylogenesis is
      #greater than or equal to the number of taxa, then either the indexing
      #is not correct, or the collection of Phylogenesis items is missing an
      #item (as all taxa should have their own phylogenesis). In this case,
      #the procedure returns an error message and exits the program.
      if max_taxon >= len(self.phylogeneses):
        print("Error: in Phylogeny: the taxa are not compatible across the phylogeny")
        exit()
   
  def coalescent(self):
    #Allocates a space in the memory to store the output of the function,
    #namely the coalescent: the first generations of each of the Phylogenesis
    #items contained in self.phylogeneses.
    coalescent = list()
    for i in range(len(self.phylogeneses)):
      #The following line appends the first generation of the i-th
      #phylogenesis of self.phylogeneses to the list 'coalescent'.
      coalescent.append(self.phylogeneses[i].history[len(self.phylogeneses[i].history)-1])
    #The list of the first generations is returned.
    return coalescent
  
  #The variable 'extension' is supposed to contain pairs (t,l) where t
  #is a taxon of the phylogeny and l is the extension of the phylogenesis of t.
  #The role of the method .extend is to append the list l to the Phylogenesis
  #item associated with t.
  def extend(self,extension):
    #The variable indicates whether if the extension of the phylogeny
    #is 'complete', in the sense that all the lists l in 'extension' have
    #already been added in previous generations, which, in fact,
    #should also be the first ones.
    flag = False
    #The following loop checks all the lists l of 'extension' are already
    #appreaing in the first generations.
    for t in range(len(self.phylogeneses)):
      for i in range(len(extension)):
        #Checks if the list 'extension' requires to add a new generation
        #to the taxa t. Then the next 'if' tests whether the generation
        #is actually a new generation, adding new taxa to the phylogeny.
        if extension[i][0] == t:
          #The extension will provide a valid phylogeny if all the lists l 
          #contains the first generation associated with the history of the
          #taxon t with which they are coupled. The following lines check
          #that this is the case.
          for j in self.phylogeneses[t].history[len(self.phylogeneses[t].history)-1]:
            if not(j in extension[i][1]):
              print("Error: in Phylogeny.extend: the extension is not compatible with the phylogenesis of taxon "+ str(t))
              exit()
          #The following lines check whether the extension is actually adding
          #a new individual to the history of the taxon t. If this is not
          #the case for all the taxa of the extension, then the phylogeny
          #is considered to be already complete, so that the variable flag 
          #is never changed to the value True.
          for j in extension[i][1]:
            #The following lines check if new individuals appear in 
            #extension[i][1] in addition of those already in 
            #self.phylogeneses[t].history.
            if not(j in self.phylogeneses[t].history[len(self.phylogeneses[t].history)-1]):
              #A new generation has been detected, the phylogeny is therefore
              #not complete and 'flag' is set to True.
              flag = True
    #The following condition holds whenever there is at least one phylogenesis
    #that is not complete.
    if flag == True:
      #The following lines add the new generation l of a pair 
      #(t,l) in 'extension' to the taxa t. Otherwise, the first
      #generation of a taxa that do not appear in 'extension' 
      #is repeated in its phylogenesis.
      for t in range(len(self.phylogeneses)):
        #The variable found_flag indicates whether the taxa t appears in 
        #the first components of the pairs of the list 'extension' or not.
        found_flag = False 
        for i in range(len(extension)):
          if extension[i][0] == t:
            #The procedure _image_of_partition is used to eliminate the
            #repetitions of integers that can occur in extension[i][1].
            self.phylogeneses[t].history.append(\
            _image_of_partition(extension[i][1]))
            found_flag = True
            break
        #The taxa was not associated with any list l in 'extension'.
        if found_flag == False:
          #The first generation is repeated (there is no repetition of
          #integer in this list).
          self.phylogeneses[t].history.append(self.phylogeneses[t].history[len(self.phylogeneses[t].history)-1])
      #The following output indicates that the phylogeny was not complete,
      #and another run is necessary to determine if the phylogeny is now
      #completed.
      return True
    else:
      ##The following output indicates that the phylogeny is now complete.
      return False

  def make_friends(self,taxon):
    #The friendships are essentially formed at the level of the oldest
    #generation. Friendships will consist of unions of pairs of lists contained
    #in the output of self.coalescent().
    coalescent = self.coalescent()
    #Allocates two spaces in the memory to store the output of the function:
    #- 'friends' will contain indices (i.e. the taxa that can be 
    #  related to the input taxon).
    #- 'coalescence_hypothesis' that  contains the unions of the oldest
    #  generation of 'taxon' with the oldest generation associated with an
    #  individual in 'firends'.
    friends = list()
    coalescence_hypothesis = list()
    #The following loop fills in the lists 'friends' 
    #and 'coalescence_hypothesis'. The list 'friends' contains all those 
    #of the phylogeny that are not in coalescent[taxon]. The list
    #'coalescence_hypothesis' contains the union of coalescent[taxon] and 
    #coalescent[r] for every index r in the list 'friends'.
    for r in range(len(coalescent)):
      if not(r in coalescent[taxon]):
        friends.append(r)
        #The union of coalescent[taxon] and coalescent[r] is computed through
        #_image_of_partition and then sorted in order to give a unique
        #representative to the union (e.g. [0,1]U[2,5] should be the same
        #as [2,5]U[0,1].
        common_ancestor = _image_of_partition(coalescent[taxon]+coalescent[r])
        common_ancestor.sort()
        coalescence_hypothesis.append(common_ancestor)
    #the procedure returns the list of friends for the input taxon and the
    #associated common ancestors stored in the list 'coalescence_hypothesis'.
    return (friends,coalescence_hypothesis)

  def set_up_friendships(self):
    #Allocates two spaces in the memory to store the two types of output
    #given by the procedure self.make_friends for every taxon 
    #of self.phylogeneses. Specifically,
    #- 'friendships' is a list of lists whose t-th list contains the first
    #  output of the procedure self.make_friends for taxon t;
    #- 'coalescence_hypotheses'  is a list of lists whose t-th list contains
    #  the second output of the procedure self.make_friends for taxon t.
    friendships = list()
    coalescence_hypotheses = list()
    #For every taxon t, the two outputs of the procedure self.make_friends(t)
    #are appended to the lists 'friendships' and 'coalescence_hypotheses'.
    for t in range(len(self.phylogeneses)):
      network = self.make_friends(t)
      friendships.append(network[0])
      coalescence_hypotheses.append(network[1])
    #The two lists are returned.
    return (friendships,coalescence_hypotheses)

  def score(self,partitions,friendship_network):
    #The following function will allow us to check if there exists a morphism
    #of partitions between two given lists (seen as partitions).
    def homset(partition1,partition2):
        try:
          MorphismOfPartitions(partition1,partition2,False)
          return True
        except:
          return False
    #The following function returns a Boolean value indicating whether two
    #lists are equal or disjoint. If this is not the case, False is returned.
    def exact_condition(list1,list2):
      intersection = list()
      for k in list1: 
        if k in list2:
          intersection.append(k)
      #Either the two lists are disjoint.
      if intersection == []:
        return True
      #Or they are equal, which means that they are both equal to 
      #their intersection.
      else:
        #The following lines check that list1 is included in the intersection.
        for k in list1:
          if not(k in intersection):
            return False
        #The following lines check that list2 is included in the intersection.
        for k in list2:
          if not(k in intersection):
            return False
        return True
    #STEP 1:
    #The variable 'score_matrix' will encode a tensor of dimension 3,
    #which means a list of lists of lists. Its coefficients, of the from
    #score_matrix[i][t][r] are defined for
    #- an index i indexing a partition in the list 'partitions'
    #- an index t indexing a list in friendship_network
    #- an index r indexing a taxon in friendship_network[0][t]
    #and they each contain a pair (flag,label) where 
    # - 'label' is an integer representing the list stored in 
    #friendship_network[1][t][r] (i.e. a hypothetical ancestor) labeled with
    #respect to all the other lists of friendship_network[1][t] up to
    #list equality, which means that if the list friendship_network[1][t][r]
    #is equal to the list friendship_network[1][s][r], then 
    #score_matrix[i][t][r] and score_matrix[i][t][s] receive the same label.
    #- 'flag' is a Boolean value indicating whether the partitions indexed 
    #by i in 'partitions' satisfies the exactness condition for the
    #hypothetical ancestor friendship_network[1][s][r].
    score_matrix = list()
    #For convenience, the list of lists of lists friendship_network[1] is
    #renamed as 'hypotheses'.
    hypotheses = friendship_network[1]
    #The following loop gives labels to the different lists (i.e. the
    #hypothetical ancestors) in hypotheses in order to recognize them up 
    #to list equality.
    labeling = list()
    for t in range(len(hypotheses)):
      labeling.append(_epi_factorize_partition(hypotheses[t]))
    #The following loop fills the coefficients of 'score_matrix' in.
    for i in range(len(partitions)):
      #The variable score_row will contain the rows of the matrix.
      score_row = list()
      #The following loop runs over the set of indices representing
      #each taxon 't' of the phylogeny.
      for t in range(len(hypotheses)):
        #The variable 'score_coalescence' will be used to compute 
        #the component 'flag' of score_matrix[i][t][r]' while
        #the variable 'score_labeling' will be used to compute 
        #the component 'label' of score_matrix[i][t][r]'
        score_coalescence = list()
        score_labeling = list()
        #The following loop runs over the set of indices representing the
        #taxa 'r' of the phylogeny that may possibly coalesce with 't'.
        for r in range(len(hypotheses[t])):
          #The variable 'x' contains the obvious partition of the set of taxa 
          #whose only non-trivial part is the list of indices 
          #representing the hypothetical ancestor 'hypotheses[t][r]'.
          x = EquivalenceRelation([hypotheses[t][r]],len(self.phylogeneses)-1)
          #The following lines check whether there is a morphism of partitions
          #form 'x' to the partition partitions[i]. This condition will
          #later be referred to as the 'large score condition'.
          #i.e. x --> P(partitions[i])
          if homset(x.quotient(),partitions[i]):
            #If the condition is satisfied, then the hypothetical ancestor
            #hypotheses[t][r] is stored in 'score_coalescence[r]' and
            #its label is stored in 'score_labeling[r]'.
            score_coalescence.append(hypotheses[t][r])
            score_labeling.append(labeling[t][r])
        #The following lines now construct the coefficients of the list
        #score_matrix[i][t]
        score_coeff = list()
        #By construction, the following loop runs over the set of indices
        #representing the taxa 'r' of the phylogeny that satisfy the
        #'large score condition' (see above). The goal is now to determine
        #which of these taxa also satisfy the 'exact score condition'.
        for r in range(len(score_coalescence)):
          #The variable 'flag' is the Boolean condition meant to be
          #stored in the pair score_matrix[i][t][r] and is meant to 
          #indicate whether the 'exact score condition' is satisfied.
          flag = True
          #The following lines check whether 'r' satisfies the 'exact
          #score condition', which must be checked with respect to all 
          #the other taxa 's' satisfying the 'large score condition'.
          for s in range(len(score_coalescence)):
            if s != r:
              flag = flag and exact_condition(\
              score_coalescence[r],\
              score_coalescence[s])
          #As described above, the coefficient score_matrix[i][t][r]
          #is constructed as a pair (flag,label).
          score_coeff.append((flag,score_labeling[r]))
        #The list score_coeff corresponds to what is called the 'support
        #functor' in the mathematical version of the present work. 
        #Also, since the images of the support functor are sets, we need to
        #consider the output of the procedure _image_of_partition(score_coeff)
        #instead of the list score_coeff itself since it may contain several
        #times the same list. 
        #Use if needed:
        #print("[DEBUG] Support functor("+str((t,i))+"): " \
        #+ str(_image_of_partition(score_coeff)))
        score_row.append(_image_of_partition(score_coeff))
      score_matrix.append(score_row)  
    #STEP 2:
    #The following lines integrate the tensor score_matrix[i][t][r] over
    #the indices i, namely the indices indexing the partitions
    #of 'partitions'. More specifically, the following lines count the number
    #of segments making the large and exact scores for a given ancestor
    #represented by a certain label 'l'. 
    #Below, the variable 'score_cardinality' is meant to contain a matrix 
    #that contains the large and exact score.
    score_cardinality = list()
    #The following loops initialize the matrix 'score_cardinality' 
    #with null scores.
    for t in range(len(labeling)):
      row = list()
      #Note that the following loop runs over the image of labeling[t],
      #which means that only the representative of the hypothetical
      #ancestors is important and not the taxa 'r' they may be associated with.
      for l in range(len(_image_of_partition(labeling[t]))):
        #The first and second integer are the initial values for the large
        #and exact scores, respectively.
        row.append([0,0])
      score_cardinality.append(row)
    #The matrix 'score_cardinality' is now updated by counting the flags that
    #were set to False and True in the 3-dimensional tensor 'score_matrix'.
    for i in range(len(score_matrix)):
      for t in range(len(score_matrix[i])):
        for (f,l) in score_matrix[i][t]:
            if f == True:
              score_cardinality[t][l][1] = score_cardinality[t][l][1]+1
              score_cardinality[t][l][0] = score_cardinality[t][l][0]+1
            else:
              score_cardinality[t][l][0] = score_cardinality[t][l][0]+1
    #STEP 3:
    #The following lines are a copy of STEP 2 but where one produces a matrix
    #indexed by the 'friends' of the given taxon t instead of producing a
    #matrix indexed by the labels of the representative of the common
    #ancestors. Note that STEP 2 was essential for the count of the large and
    #exact scores, which are meant to be computed  with respect to the
    #hypothetical ancestors and not the 'friends' of taxon t.
    friendships = friendship_network[0]
    score_cardinality_adjusted = list()
    for t in range(len(labeling)):
      row = list()
      #This time, the following line is not computed with respect to the
      #image of labeling[t].
      for r in range(len(labeling[t])):
        row.append(())   
      score_cardinality_adjusted.append(row)
    for t in range(len(labeling)):
      for r in range(len(labeling[t])):
        score_cardinality_adjusted[t][r] = (friendships[t][r],score_cardinality[t][labeling[t][r]][0],score_cardinality[t][labeling[t][r]][1])
    #The procedure returns a triple (r,large,exact) where r runs over the
    #elements of friendships[t] where 'large' is the large score of the
    #possible ancestor hypotheses[t][r] and where 'exact' is the exact score
    #of the possible ancestor hypotheses[t][r].
    return score_cardinality_adjusted

  def choose(self,scores):
    #The following local function defines the non-strict lexicographical 
    #order on pairs of integers.
    def lex_order(pair1,pair2):
      return (pair1[0] < pair2[0]) \
      or ((pair1[0] == pair2[0]) and (pair1[1] <= pair2[1]))
    #The following local function defines the non-strict lexicographical 
    #order on pairs of integers.
    def lex_strict_order(pair1,pair2):
      return (pair1[0] < pair2[0]) \
      or ((pair1[0] == pair2[0]) and (pair1[1] < pair2[1])) 
    #A space is allocated to store the output of the procedure.
    result = list()
    #In the following loop, each internal list of the input list 'score' is
    #sorted with respect to the (opposite) lexicographical order of the last
    #and second last components of its elements. 
    #More specifically, every internal list score[t] contains pairs (r,l,e)
    #and these pairs are sorted with respect to the reverse lexicographical
    #order with respect to the part (e,l). Once the list is sorted, the
    #greatest local maximum of the function (e,l) -> (l,e) is found and all
    #the elements r associated with this local maximum (l,e) are stored
    #in a list called 'choose', which is appended to the list 'result'.
    for t in range(len(scores)):
      #Sorting 'score[t]' as follows ensures that the first local maximum 
      #of the function (e,l) -> (l,e) is actually the greatest one.
      scores[t].sort(key = lambda indiv_scores: \
      (-indiv_scores[2],-indiv_scores[1]))
      #Since the pair (e,l) are supposed to contain non-negative integers,
      #we look for the greatest local maximum by starting with the value (0,0).
      loc_max = (0,0)
      #The following loop compute the greatest local maximum of the function
      #(e,l) -> (l,e) for all the pairs (r,e,l) in score[t].
      for r in range(len(scores[t])):
        if lex_order(loc_max,scores[t][r][1:3]):
          loc_max = scores[t][r][1:3]
        else:
          break
      #A space is allocated to store the elements 'r' of the pairs (r,l,e) for 
      #which the pair (l,e) is the greatest local maximum of the map
      #(e,l) -> (l,e) relative to the pairs (l,e) coming from score[t].
      choose = list()
      #The following loop look for the values 'r' associated with the greatest 
      #local maximum (l,e).
      for r in range(len(scores[t])):
        if lex_strict_order(scores[t][r][1:3],loc_max):
          continue
        elif loc_max == scores[t][r][1:3]:
          choose.append(scores[t][r][0])
        else:
          break
      #The list of elements 'r' that are associated with the greatest local
      #maximum (l,e) is appended to the list 'result'
      result.append(choose)
    #The list of lists of elements 'r' reaching the greatest local maxima is
    #returned.
    return result

  def set_up_competition(self,best_fit):
    #The competition takes place in the oldest generation. 
    #competitors will consist of unions of pairs of lists contained
    #in the output of self.coalescent().
    coalescent = self.coalescent()
    #A space is allocated in the memory to store the different competitors.
    coalescence_hypothesis = list()
    #The following loop makes the union of the first generation associated 
    #with taxon t with the first generations associated with the taxa r in
    #best_fit[t].
    for t in range(len(coalescent)):
        #The following ensures that if best_fit[t] is empty, then the first
        #generation of the phylogenesis of t is given.
        common_ancestor = _image_of_partition(coalescent[t])
        #The following loop add the first generations of the friend of the 
        #taxon t to the 'common ancestors.
        for r in best_fit[t]:
          common_ancestor = _image_of_partition(common_ancestor+coalescent[r])
        #The list 'common_ancestor' to only give one representative to the 
        #union it represents.
        common_ancestor.sort()
        coalescence_hypothesis.append(common_ancestor)
    #The list of competitors is returned, where each competitor is indexed
    #by the integer of the taxon it is supposed to represent.
    return coalescence_hypothesis
