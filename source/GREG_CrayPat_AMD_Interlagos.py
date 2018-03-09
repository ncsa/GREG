#
#  Description: Draw roofline plots after reading CrayPat reports
#
#  Filename:   GREG_CrayPat_AMD_Interlagos.py
#  Update description :
#         1) Read a filename of a CrayPat report or a list of pat_reports via command line arguments
#              - the list file should use the following format
#                    line 1: filename1, legend_name1, Pat_Region_name1,       nThread[optional]
#                       .....
#                    line n: filename(n), legend_name(n), Pat_Region_name(n), nThread[optional]
#              - If the 2nd CLA (Command Line Argument) exists, the script generates roofline plots for every CrayPat report in the list.
#                Otherwise, it generates combined roofline plots for CrayPat reports in the list.
#              - Using the nThread, Flop-rates are multiplied by nThread. This is to overcome the issus that CrayPat gets OPS from only master thread. 
#                    This assumes that each thread do the similar number of OPS. 
#                    The default value is 1. 
#              - For a single CrayPat report:
#                    the second CLA: nThreads  (default:1)
#         2) Read number of nodes from the pat_report
#         3) Read PAPI_FP_OPS,PAPI_L1_DCA, DATA_CACHE_REFILLS_FROM_L2_OR_NORTHBRIDGE_GOOD (DCR_Good) and MFLOPS of each pat_region
#         4) Compute Computational Intensities (DCR_Good based CI and L1_DCA based CI) of pat_regions
#         5) Write a table for pat_region name, GFLOPs/node and CIs 
#         6) Draw plots for roofline and points for pat_regions
#
#         written by JaeHyuk Kwack (jkwack2@illinois.edu)
#                    Blue Waters Scientific and Engineering Applications Support (SEAS) Group
#                    National Center for Supercomputing Applications - NCSA
#                    University of Illinois at Urbana-Champaign
# ------------------------------------------------------------------------------------------------------------------

## Importing Libraries
from __future__ import division
import sys
from CrayPat.PatReport import PatReport
from Plots.Plots import Plots

#
# Getting command line arguements
try:
   fname = sys.argv[1]
except IndexError:
   sys.exit("******** ERROR: Enter a filename for a CrayPat report or a list of CrayPat reports (i.e., the first command line argument)")

# Check if the file is a CrayPat report or a list file
fpat = open(fname,'r')
A = fpat.readlines()
fpat.close()
if A[0].split()[0] == 'CrayPat/X:':
   # When fname is a CrayPat report file name
   islist = False
   # Getting nThread from command line arguments
   try:
      nThread = int(sys.argv[2])
   except IndexError:
      print ("   [Warning] You can specify the number of threads using the second command line argument. Now it is set to '1'. ")
      nThread = 1

   A = []
   Rep = PatReport(fname,nThread)
   Rep.write_csv()
   P = Plots(Rep.fname,Rep.Regions)
   P.draw()   

else:
   # When fname has a list of CrayPat reports
   islist = True
   # Read the 2nd CLA
   is2ndCLA = False
   try:
      tmp = sys.argv[2]
      is2ndCLA = True
   except IndexError:
      pass

   # Read Pat_reports in the list file
   legend_names = []
   reports = []
   for line in A:
      # Reading nThread
      try:
         nThread=int(line.split()[3])
      except IndexError:   
         print ("   [Warning] You can specify the number of threads using the fourth optional input. Now it is set to '1'. ")
         nThread = 1

      Rep = PatReport((line.split()[0]),nThread)
      if is2ndCLA:
         Rep.write_csv()
         P = Plots(Rep.fname,Rep.Regions)
         P.draw()

      Region_name=line.split()[2]
      reports.append([ Rep,line.split()[1],line.split()[2] ] )    # Report, legend_name, Region_name
   # Create a Region for plot from multiple Pat_reports
   if not is2ndCLA:
      Regions = []
      for Row in reports:
         Rep = Row[0]
         for Reg in Rep.Regions:
            if Reg.title == Row[2]:
               Regions.append(Reg)
               Regions[len(Regions)-1].title = Row[1]
      # Plot filename
      plot_fname = fname
      P = Plots(plot_fname, Regions)
      P.offPercentage()
      P.draw()





