# GREG: General Roofline Evaluation Gadget

Roofline analysis model is a visually intuitive performance model used to provide performance estimates of science and engineering applications. It shows inherent hardware limitations as well as the potential benefit of optimizations. Even though Intel started supporting a roofline analysis feature with Intel Advisor version 2017 Update 2 (“officially”), roofline analysis on other vendors’ processors such AMD, ARM, IBM, and NVIDIA is not practically available. *GREG* performs roofline analysis on non-Intel processors using corresponding hardware counters and performance profilers. Based on the analyses, users will be able to categorize science and engineering applications in terms of operational intensity, and try to improve the performance at scale. 

## GREG_CrayPat_AMD_Interlagos

* Target Processor: [AMD Bulldozer Family 15h processors](https://developer.amd.com/resources/developer-guides-manuals/) (e.g., AMD 6276 Interlargos processor)
* Tested System: [NCSA Blue Waters](https://bluewaters.ncsa.illinois.edu/blue-waters-overview)
* Employed Profiling Tool: [Cray Performance Measurement and Analysis Tools - CrayPat](https://bluewaters.ncsa.illinois.edu/cpmat)

#### Instructions to get a CrayPat report on Blue Waters
  1. Updating modules for CrayPat  
    `$ module unload darshan`  
    `$ module load perftools-base perftools` 
  2. Building your application again after cleaning up existing object files
  3. Instrument the executable binary with "-w"  
    `$ pat_build -w a.out`  
    It will generate `a.out+pat`. 
  4. Run the instrumented executable binary ending with "+pat" with the following environmental variables in your job  
    `$ export PAT_RT_SUMMARY=0`  
    `$ export PAT_RT_PERFCTR=DATA_CACHE_REFILLS_FROM_L2_OR_NORTHBRIDGE:GOOD,PAPI_L1_DCA,PAPI_FP_OPS`  
    After completing the execution, CrayPat generates *an xf file* or *a folder* starting with "a.out+pat+" (e.g., a.out+pat+17402-6240t).   
  5. Producing a CrayPat report using the `pat_report` command.   
    `$ pat_report -o {a CrayPat report name you want} {the name of the xf file or the folder} `

#### Roofline Analysis on Blue Waters
```
$ modlue load bwpy                                    # on Blue Waters
$ cd ~/GREG/source                                    # if GREG is located on $(HOME)
$ python3 GREG_CrayPat_AMD_Interlagos.py CLA1 CLA2    # See the bottom for more details for CLA1 and CLA2
```

##### Inputs for a single CrayPat report
   * Details about CLAs (Command Line Arguments)
     * CLA1: a CrayPat report file, *required*
     * CLA2: number of threads per MPI rank, *optional* (default = 1)

##### Inputs for multiple CrayPat reports
   * Details about CLAs (Command Line Arguments)
     * CLA1: a text file listing the CrayPat reports, *required*
     * CLA2: If not empty, the script generates separate roofline plots for every CrayPat report listed in CLA1. Otherwise, a single roofline plot is generated for specified data of CrayPat reports, *optional*

   * Format for the list in CLA1
      > line 1: filename1, legend_name1, Pat_Region_name1 (*optional*), number of threads (*optional*)  
      > ...  
      > line n: filename(n), legend_name(n), Pat_Region_name(n) (*optional*), number of threads (*optional*)

##### Outputs (i.e., two roofline plots)
  * Roofline plot based on DATA_CACHE_REFILLS_FROM_L2_OR_NORTHBRIDGE:GOOD (DCR_GOOD) counter data, *recommended*
  * Roofline plot based on PAPI_L1_DCA counter data, *CrayPat default*



## Bug report and requests
Send bug reports and requests for improvement to JaeHyuk Kwack (jkwack2@illinois.edu).

