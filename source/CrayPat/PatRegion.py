#  Copyright (C) 2018, University of Illinois Board of Trustees. All Rights Reserved.
#  Licensed under the NCSA open source license
#
#  Description: This module contains a class, PatRegion.
#
#  Filename:   PatRegion.py
#
#         written by JaeHyuk Kwack (jkwack2@illinois.edu)
#                    Blue Waters Scientific and Engineering Applications Support (SEAS) Group
#                    National Center for Supercomputing Applications - NCSA
#                    University of Illinois at Urbana-Champaign
# ------------------------------------------------------------------------------------------------------------------

## Importing Libraries
from __future__ import division

class PatRegion:
   def __init__(self,title,nNode,nThread,iline,A):
      self.title=title
      self.nNode=nNode
      self.nThread = nThread
      self.read(iline,A)
   
   def read(self,iline,A):
      self.Time_percentage = 0.0
      self.Time = 0.0
      self.PAPI_L1_DCA=0
      self.DCR_Good = 0.0
      self.PAPI_FP_OPS=0
      self.GFLOPS_per_Node = 0.0
      self.CI_L1_DCA = 0.0
      self.CI_DCR_Good = 0.0
      for line in A[iline+1:]:
         if line[0:3]=='===':
            break
         line_split = line.split()
         if line_split[0]=='Time%':
            self.Time_percentage = float(line_split[1].replace("%",""))
         if line_split[0]=='Time':
            self.Time = float(line_split[1].replace(",",""))
         if line_split[0]=='PAPI_L1_DCA':
            self.PAPI_L1_DCA=int(float(line_split[len(line_split)-2].replace(",","")))
         if line_split[0]=='GOOD':
            self.DCR_Good=int(float(line_split[len(line_split)-2].replace(",","")))
         if line_split[0]=='PAPI_FP_OPS':
               self.PAPI_FP_OPS=int(float(line_split[len(line_split)-2].replace(",","")))
         if line_split[0]=='MFLOPS':
            self.GFLOPS_per_Node=float(line_split[2].replace("M/sec","").replace(",",""))/1000/self.nNode*self.nThread
      if self.PAPI_L1_DCA != 0:
         self.CI_L1_DCA = self.PAPI_FP_OPS*1.0/self.PAPI_L1_DCA/16
      if self.DCR_Good != 0:
         self.CI_DCR_Good = self.PAPI_FP_OPS*1.0/self.DCR_Good/64

   def show(self):
      # Printing out the data
      print ('  Pat_Region: %s, time%s = %5.1f%s, time = %5.1fsec'%(self.title,'%',self.Time_percentage,'%',self.Time) )
      print ('     OPS         = %21d'%(self.PAPI_FP_OPS) )
      print ('     L1_DCA      = %21d, L1_DCA_based_CI   = %12.3g'%(self.PAPI_L1_DCA,self.CI_L1_DCA) )
      print ('     DCR_Good    = %21d, DCR_Good_based_CI = %12.3g'%(self.DCR_Good,self.CI_DCR_Good) )
      print ('     GFLOPs/node = %21.6g GFLOP/s/node'%(self.GFLOPS_per_Node) )

