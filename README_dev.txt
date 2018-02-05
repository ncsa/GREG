NCSA-RT (NCSA-Roofline Toolkit): scripts for generating roofline analysis plots

Author: JaeHyuk Kwack (jkwack2@illinois.edu),
        Blue Waters Scientific and Engineering Applications Support (SEAS) Group,
        National Center for Supercomputing Applications - NCSA,
        University of Illinois at Urbana-Champaign

Send bug reports and requests for improvement to jkwack2@illinois.edu.

Examples:
   - Roofline plots for a single CrayPat report
      Execution line:      % python3 NCSA-RT_CrayPat.py {a filename of a CrayPat report} {number of threads per MPI rank, optional, default:1}
      Output files:        two roofline plots; roofline_DCR_Good and roofline_L1_DCA

   - Roofline plots for multiple CrayPat report
      Execution line:      % python3 NCSA-RT_CrayPat.py {a filename of a list of CrayPat reports} {the 2nd CLA}
      Output files:        two roofline plots; roofline_DCR_Good and roofline_L1_DCA
      The list format:     line 1: filename1, legend_name1, Pat_Region_name1[optional], nThread[optional]
                           ...
                           line n: filename(n), legend_name(n), Pat_Region_name(n)[optional],  nThread[optional]
      Rule of the 2nd CLA: If the 2nd CLA(Command Line Argument) exists, the script generates roofline plots for every CrayPat report in the list. Otherwise, it generates combined roofline plots for all CrayPat reports in the list


