## The present directory contains:

1. a python file: Pedigrad.py (headers)
2. a pdf file: documentation.pdf (the documentation for the library)
3. a directory ```Pedigrad_py``` containing the modules: 
   * AsciiTree;
   * PartitionCategory;
   * PedigradCategory;
   * Phylogeny;
   * and SegmentCategory.
4. a directory ```User``` containing a tutorial
5. a directory ```Truncation_method``` containing the truncation method used in the paper version of this project.

## To use the functions and classes of the library, you can follow one of the following installation procedures:

**Installation 1 (quick)**

1. Put Pedigrad.py and Pedigad_py in location X
2. Create your main file in location X, where Pedigrad.py and Pedigad_py are;
3. Include the following line to your main file:
```
    from Pedigrad import *
```
4. Use the Pedigrad library (see documentation). 


**Installation 2 (to use from another directory)**

1. Put Pedigrad_py in location X;
2. Put Pedigrad.py and your main file in location Y;
3. Include the following line to your main file:

from Pedigrad import *

4. Update the paths in Pedigrad.py as follows:

* Change ```'Pedigrad_py/PartitionCategory/'``` to ```'path/to/X/Pedigrad_py/PartitionCategory/'```

* Change ```'Pedigrad_py/PedigradCategory/'``` to ```'path/to/X/Pedigrad_py/PedigradCategory/'```

* Change ```'Pedigrad_py/AsciiTree/'``` to ```'path/to/X/Pedigrad_py/AsciiTree/'```

5. Use the Pedigrad library (see documentation). 


**Installation 3 (if you know what you are doing)**

- Use any other adequate installation procedure.


## To import a non importable function from the library:

Copy the following text in the appropriate section of Pedigrad.py and replace ```NameOfModule```, ```_non_importable_function``` and ```now_portable_function``` with the desired names.

```
    from NameOfModule import _non_importable_function
    def now_portable_function(*args):
      return _non_importable_function(*args)
```



