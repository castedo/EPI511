Extras for Harvard Class EPI511: Advanced Population & Medical Genetics
=======================================================================

The EPI511.py file provided in the EPI511 class is a few years old.
In contrast, the [minihapmap.py](minihapmap.py) file in this respository:

* reads the data files ~40 times faster
* makes it not painful to load all autosomal chromosome SNPs
* makes it easy to interactively load additional populations one at a
time (each taking only a few seconds to load)
* makes it easier to explore and use all the chromosome and population data
* will use ~1.3GB of RAM if all 11 populations and all autosomal chromosomes are loaded
* is ~15 lines of code shorter
* demonstrates some good Python programming practices such as:
  * use `class`
  * avoid needing to modify the reusable file in order to use it
  * use pathlib.Path  
  * avoid global variables

If you have any questions, feel free to email castedo@castedo.com.

