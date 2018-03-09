# GREG: General Roofline Evaluation Gadget

Roofline analysis model is a visually intuitive performance model used to provide performance estimates of science and engineering applications. It shows inherent hardware limitations as well as the potential benefit of optimizations. Even though Intel started supporting a roofline analysis feature with Intel Advisor version 2017 Update 2 (“officially”), roofline analysis on other vendors’ processors such AMD, ARM, IBM, and NVIDIA is not practically available. *GREG* performs roofline analysis on non-Intel processors using corresponding hardware counters and performance profilers. Based on the analyses, users will be able to categorize science and engineering applications in terms of operational intensity, and try to improve the performance at scale. 

## GREG_CrayPat_AMD_Interlagos

* Target Processor: [AMD Bulldozer Family 15h processors](https://developer.amd.com/resources/developer-guides-manuals/) (e.g., AMD 6276 Interlargos processor)
* Tested System: [NCSA Blue Waters](https://bluewaters.ncsa.illinois.edu/blue-waters-overview)
* Employed Profiling Tool: [Cray Performance Measurement and Analysis Tools - CrayPat](https://bluewaters.ncsa.illinois.edu/cpmat)

#### Roofline plots for a sinlge CrayPat report
   * Execution: `$ python3 GREG_CrayPat_AMD_Interlagos.py CLA1 CLA2`

   * Details about CLAs (Command Line Arguments)
     * CLA1: a filename of a CrayPat report, *required*
     * CLA2: number of threads per MPI rank, *optional* (default = 1)

   * Outputs: two roofline plots
     * Roofline plot based on DATA_CACHE_REFILLS_FROM_L2_OR_NORTHBRIDGE:GOOD (DCR_GOOD) counter data, *recommended*
     * Roofline plot based on PAPI_L1_DCA counter data, *CrayPat default*

#### Roofline plots for multiple CrayPat reports
   * Execution: `$ python3 GREG_CrayPat_AMD_Interlagos.py CLA1 CLA2`

   * Details about CLAs (Command Line Arguments)
     * CLA1: a text filename that includes a list of CrayPat reports, *required*
     * CLA2: If CLA2 exists, the script generates roofline plots for every CrayPat report in the list, *optional* 

   * Outputs: two roofline plots
     * Roofline plot based on DATA_CACHE_REFILLS_FROM_L2_OR_NORTHBRIDGE:GOOD (DCR_GOOD) counter data, *recommended*
     * Roofline plot based on PAPI_L1_DCA counter data, *CrayPat default*

   * Format for the list
      > line 1: filename1, legend_name1, Pat_Region_name1 (*optional*), number of threads (*optional*)  
      > ...  
      > line n: filename(n), legend_name(n), Pat_Region_name(n) (*optional*), number of threads (*optional*)


## Bug report and requests
Send bug reports and requests for improvement to JaeHyuk Kwack (jkwack2@illinois.edu).

