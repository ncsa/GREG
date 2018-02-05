#
#  Description: This module contains a class, Plots.
#
#  Filename:   Plots.py
#
#         written by JaeHyuk Kwack (jkwack2@illinois.edu)
#                    Blue Waters Scientific and Engineering Applications Support (SEAS) Group
#                    National Center for Supercomputing Applications - NCSA
#                    University of Illinois at Urbana-Champaign
# ------------------------------------------------------------------------------------------------------------------

## Importing Libraries
from __future__ import division
import math
import numpy as np
import matplotlib.pyplot as plt

class Plots:
   def __init__(self,fname,Regions):
      self.fname = fname
      self.Regions = Regions
      self.onPercentage = True

   def set_system(self,system,Max_y):
      if system=='BlueWaters':
         self.BW_DRAM = 70.0
         self.BW_L1 = 833.1
         self.BW_L2 = 383.0
         self.Max_DP = 223.7
         self.Max_SP = 447.0
         self.Max_y = max(self.Max_SP,Max_y)
      # Set the default environment variables
      self.set_environments()

   def set_environments(self):
      # Figure part
      self.font = {'family':'sans-serif','color':'black','weight':'normal','size':10}
      self.size_ratio = 5
      self.max_marker = 7
      self.min_marker = 2
      self.mean_marker = 5
      self.marker_type = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']
      self.n_alpha = 0.75
      self.max_legend = 20
      self.nDPI = 600
      self.slabel = 10
      self.x_range = np.array([0.01,100])
      self.y_range = np.array([1.0, 10**math.ceil(math.log10(self.Max_y))])
      # self.y_range = np.array([0.1, 10**math.ceil(math.log10(self.Max_y))])   # for SETSM
      self.Line_DRAM_x = [self.x_range[0],self.Max_SP/self.BW_DRAM]
      self.Line_DRAM_y = [self.x_range[0]*self.BW_DRAM,self.Max_SP]
      self.Line_L1_x = [self.x_range[0],self.Max_SP/self.BW_L1]
      self.Line_L1_y = [self.x_range[0]*self.BW_L1,self.Max_SP]
      self.Line_L2_x = [self.x_range[0],self.Max_SP/self.BW_L2]
      self.Line_L2_y = [self.x_range[0]*self.BW_L2,self.Max_SP]
      self.Line_DP_FLOP_x = [self.Max_DP/self.BW_L1,self.x_range[1]]
      self.Line_DP_FLOP_y = [self.Max_DP,self.Max_DP]
      self.Line_SP_FLOP_x = [self.Max_SP/self.BW_L1,self.x_range[1]]
      self.Line_SP_FLOP_y = [self.Max_SP,self.Max_SP]
      self.loc_DP_FLOP = [3.5,self.Max_DP*1.1]
      self.loc_SP_FLOP = [3.5,self.Max_SP*1.1]
      self.loc_L1 = [0.02,self.BW_L1*0.02*1.2]
      self.loc_L2 = [0.02,self.BW_L2*0.02*1.2]
      self.loc_DRAM = [0.02,self.BW_DRAM*0.02*1.2]
      self.annot_font_size = 8
      self.F = plt.gcf()
      self.fsize = self.F.get_size_inches()
      self.dy_box = self.fsize[1]/(np.log10(self.y_range)[1]-np.log10(self.y_range)[0])
      self.dx_box = self.fsize[0]/(np.log10(self.x_range)[1]-np.log10(self.x_range)[0])
      self.mem_angle = np.arctan(self.dy_box/self.dx_box)/math.pi*180.
      plt.rc('grid',linestyle=':',color='k',linewidth=0.1)
      plt.rc('lines',linewidth=1)
      plt.rc('legend',fontsize=9,loc='best')
      # plt.rc('legend',fontsize=8,loc='best')    # for SETSM
      plt.grid(True, which='both')
      self.colors = ('C0','C1','C2','C3','C4','C5','C6','C7','C8','C9')

   def draw_rooflines(self):
      # Drawing rooflines
      plt.loglog(self.Line_DRAM_x,self.Line_DRAM_y,'r--')
      plt.loglog(self.Line_L1_x,self.Line_L1_y,'r--')
      plt.loglog(self.Line_L2_x,self.Line_L2_y,'r--')
      plt.loglog(self.Line_DP_FLOP_x,self.Line_DP_FLOP_y,'b--')
      plt.loglog(self.Line_SP_FLOP_x,self.Line_SP_FLOP_y,'b--')
      plt.text(self.loc_DP_FLOP[0],self.loc_DP_FLOP[1],'DP peak: %d GFLOP/s/node'%int(round(self.Max_DP)),fontsize=self.annot_font_size,color='b')
      plt.text(self.loc_SP_FLOP[0],self.loc_SP_FLOP[1],'SP peak: %d GFLOP/s/node'%int(round(self.Max_SP)),fontsize=self.annot_font_size,color='b')
      plt.text(self.loc_L1[0],self.loc_L1[1],'L1: %d GB/s/node'%int(round(self.BW_L1)),ha='left',va='bottom',rotation=self.mem_angle,fontsize=self.annot_font_size,color='r')
      plt.text(self.loc_L2[0],self.loc_L2[1],'L2: %d GB/s/node'%int(round(self.BW_L2)),ha='left',va='bottom',rotation=self.mem_angle,fontsize=self.annot_font_size,color='r')
      plt.text(self.loc_DRAM[0],self.loc_DRAM[1],'DRAM: %d GB/s/node'%int(round(self.BW_DRAM)),ha='left',va='bottom',rotation=self.mem_angle,fontsize=self.annot_font_size,color='r')

   def draw_rooflines_w_color(self,unicolor):
      # Drawing rooflines
      plt.loglog(self.Line_DRAM_x,self.Line_DRAM_y,color=unicolor,linestyle='--')
      plt.loglog(self.Line_L1_x,self.Line_L1_y,color=unicolor,linestyle='--')
      plt.loglog(self.Line_L2_x,self.Line_L2_y,color=unicolor,linestyle='--')
      plt.loglog(self.Line_DP_FLOP_x,self.Line_DP_FLOP_y,color=unicolor,linestyle='--')
      plt.loglog(self.Line_SP_FLOP_x,self.Line_SP_FLOP_y,color=unicolor,linestyle='--')
      plt.text(self.loc_DP_FLOP[0],self.loc_DP_FLOP[1],'DP peak: %d GFLOP/s/node'%int(round(self.Max_DP)),fontsize=self.annot_font_size,color=unicolor)
      plt.text(self.loc_SP_FLOP[0],self.loc_SP_FLOP[1],'SP peak: %d GFLOP/s/node'%int(round(self.Max_SP)),fontsize=self.annot_font_size,color=unicolor)
      plt.text(self.loc_L1[0],self.loc_L1[1],'L1: %d GB/s/node'%int(round(self.BW_L1)),ha='left',va='bottom',rotation=self.mem_angle,fontsize=self.annot_font_size,color=unicolor)
      plt.text(self.loc_L2[0],self.loc_L2[1],'L2: %d GB/s/node'%int(round(self.BW_L2)),ha='left',va='bottom',rotation=self.mem_angle,fontsize=self.annot_font_size,color=unicolor)
      plt.text(self.loc_DRAM[0],self.loc_DRAM[1],'DRAM: %d GB/s/node'%int(round(self.BW_DRAM)),ha='left',va='bottom',rotation=self.mem_angle,fontsize=self.annot_font_size,color=unicolor)

   def write_axis_labels(self):
      # Axis labels
      plt.xlabel('Computational Intensity (FLOP/Byte)', fontdict=self.font)
      plt.ylabel('FLOP-rate/node (GFLOP/s/node)', fontdict=self.font)
      plt.tick_params(axis='both',labelsize =self.slabel )
      plt.xlim(self.x_range);                                       plt.ylim(self.y_range)

   def offPercentage(self):
      self.onPercentage = False

   def onPercentage(self):
      self.onPercentage = True

   def draw(self):
      self.draw_L1_DCA()
      self.draw_DCR_good()

   def draw_L1_DCA(self):
      # Drawing rooflines
      self.set_system('BlueWaters',0.0)
      self.draw_rooflines()
      self.write_axis_labels()
      # Drawing a plot for L1_DCA based CI and GFLOP/s/node
      print ('   Drawing a plot for L1_DCA based CI and GFLOP/s/node')
      # Drawing Pat_Regions
      for i,R in enumerate(self.Regions):
         if self.onPercentage:
            tmp_label = R.title+'('+'%s'%R.Time_percentage+'%)'
            tmp_markersize = max(np.log10(R.Time_percentage)*self.max_marker/2,self.min_marker)
            tmp_markertype = 'o'
         else:
            tmp_label = R.title
            tmp_markersize = self.mean_marker
            tmp_markertype = self.marker_type[i]
         plt.loglog(R.CI_L1_DCA,R.GFLOPS_per_Node,tmp_markertype,markersize=tmp_markersize,alpha=self.n_alpha,label=tmp_label)
      if len(self.Regions) <= self.max_legend:
         plt.legend()
      str_savefig = self.fname+'_Roofline_L1_DCA.png'
      plt.savefig(str_savefig,dpi=self.nDPI);                       plt.clf()

   def draw_DCR_good(self):
      # Drawing rooflines
      self.set_system('BlueWaters',0.0)
      self.draw_rooflines()
      self.write_axis_labels()
      # Drawing a plot for DCR_Good based CI and GFLOP/s/node
      print ('   Drawing a plot for DCR_Good based CI and GFLOP/s/node')
      # Drawing Pat_Regions
      for i,R in enumerate(self.Regions):
         if self.onPercentage:
            tmp_label = R.title+'('+'%s'%R.Time_percentage+'%)'
            tmp_markersize = max(np.log10(R.Time_percentage)*self.max_marker/2,self.min_marker)
            tmp_markertype = 'o'
         else:
            tmp_label = R.title
            tmp_markersize = self.mean_marker
            tmp_markertype = self.marker_type[i]
         plt.loglog(R.CI_DCR_Good,R.GFLOPS_per_Node,tmp_markertype,markersize=tmp_markersize,alpha=self.n_alpha,label=tmp_label)
      if len(self.Regions) <= self.max_legend:
         plt.legend()
      str_savefig = self.fname+'_Roofline_DCR_Good.png'
      plt.savefig(str_savefig,dpi=self.nDPI);                       plt.clf()








