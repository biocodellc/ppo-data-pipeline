# Processing image_scoring

The input file is a spreadsheet emailed to JBD by RG on 8/27/2019.
The phenophase_descriptions.csv file translates the values of the incoming file
to traits and upper and lower counts for part and whole plants.  There is some 
interesting thinking behind scoring images for use in a reasoner.  Primarily,
one should construct their scoring with a mind for traits that can be inferred.
For example, if flowers are absent, it is not really necessary to say that 
open flowers are also absent as a trait since the reasoner should pick this up.
Thus, in the phenophase_descriptions file we only score 'flower presence' with an
upper count of 0 for this case.  
