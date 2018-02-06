#
#  Description: This module contains a class, PatReport.
#
#  Filename:   PatReport.py
#
#         written by JaeHyuk Kwack (jkwack2@illinois.edu)
#                    Blue Waters Scientific and Engineering Applications Support (SEAS) Group
#                    National Center for Supercomputing Applications - NCSA
#                    University of Illinois at Urbana-Champaign
# ------------------------------------------------------------------------------------------------------------------

## Importing Libraries
from __future__ import division
from CrayPat.PatRegion import PatRegion

class PatReport:
   def __init__(self,fname,nThread):
      self.fname=fname
      self.nThread=nThread
      self.HiMem = 0.0
      self.read_PatReport()

   def read_PatReport(self):
      # Reading the CrayPat report
      print ("   Reading %s"%self.fname)
      fpat = open(self.fname,'r')
      A = fpat.readlines()
      fpat.close()

      # Reading number of compute node
      for line in A:
         line_split = line.split()
         if len(line_split) != 0:
            if ''.join(line_split[0:5]) == 'NumberofPEs(MPIranks):':
               nMPI = int(line_split[5].replace(",",""))
            if ''.join(line_split[0:5]) == 'NumbersofPEsperNode:':
               nMPIperNode = int(line_split[5].replace(",",""))
               break
      nNode = nMPI/nMPIperNode
      print ('   Number of MPI ranks          = %d '%(nMPI) )
      print ('   Number of MPI ranks per Node = %d '%(nMPIperNode) )
      print ('   Number of Compute Node       = %d '%(nNode) )
      print ('   Number of Threads            = %d '%(self.nThread) )

      # Counting number of user pat_regions
      Regions= []
      for i,line in enumerate(A):
         line_split = line.split()
         if len(line_split) != 0:
            if line_split[0] == '==============================================================================':
               if A[i+2].split()[0] == '------------------------------------------------------------------------------':
                  word = ''.join(A[i+1].split())
                  Regions.append(PatRegion(word,nNode,self.nThread,i,A))

      # Discarding Regions with CI = 0
      Regions_core = []
      for i,R in enumerate(Regions):
         if R.CI_L1_DCA*R.CI_DCR_Good != 0:
            Regions_core.append(R)
      self.Regions = Regions_core
      for R in self.Regions:
         R.show()

      # Read HiMem
      self.read_HiMem(A)

   def read_HiMem(self,A):
   # Read Memory High Water Mark by Numa Node (e.g., read the following block)
   # Table 4:  Memory High Water Mark by Numa Node
   #
   #   Process |    HiMem |    HiMem |    HiMem |    HiMem | Numanode
   #     HiMem |     Numa |     Numa |     Numa |     Numa |  PE=HIDE
   #  (MBytes) |   Node 0 |   Node 1 |   Node 2 |   Node 3 |
   #           | (MBytes) | (MBytes) | (MBytes) | (MBytes) |
   #
   #     269.7 |     71.5 |     72.5 |     63.6 |     62.1 | Total
   # |-----------------------------------------------------------------
   # |     67.1 |     58.4 |      4.6 |      2.2 |      1.9 | numanode.0
   # |     67.8 |      4.4 |     59.2 |      2.2 |      1.9 | numanode.1
   # |     67.7 |      4.3 |      4.3 |     56.9 |      2.2 | numanode.2
   # |     67.1 |      4.4 |      4.3 |      2.2 |     56.2 | numanode.3
   # |=================================================================
      HiMem_candidate = []
      for i,line in enumerate(A):
         if line.startswith('Table 4:  Memory High Water Mark by Numa Node'):
            words = A[i+7].split()
            HiMem_candidate.append(float(words[2]))
            HiMem_candidate.append(float(words[4]))
            HiMem_candidate.append(float(words[6]))
            HiMem_candidate.append(float(words[8]))
            for j in range(4):
               words = A[i+9+j].split()
               HiMem_candidate.append(float(words[1]))
            self.HiMem = max(HiMem_candidate)
            break

   def write_csv(self):
      # Write Pat_Regions to a CSV file
      fname_out =self.fname+'_data.csv'
      print ('   Writing CrayPat data to %s file'%fname_out)
      fcsv = open(fname_out,'w')
      fcsv.write('PatRegions,time_percentage,time,OPS,L1_DCA,L1_DCA_based_CI,DCR_Good,DCR_Good_based_CI,GFLOP/s/node\n')
      for R in self.Regions:
         fcsv.write('%s,%f,%f,%d,%d,%f,%d,%f,%f\n'%(R.title,R.Time_percentage,R.Time,R.PAPI_FP_OPS,R.PAPI_L1_DCA,R.CI_L1_DCA,R.DCR_Good,R.CI_DCR_Good,R.GFLOPS_per_Node))
      fcsv.write('HiMem per MPI,%f,MBytes'%(self.HiMem))
      fcsv.close()
