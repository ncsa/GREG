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
$ python3 GREG_CrayPat_AMD_Interlagos.py ARG1 ARG2    # See the bottom for more details for ARG1 and ARG2
```

##### Inputs for a single CrayPat report
   * Details about ARGs (Arguments)
     * ARG1: a CrayPat report file, *required*
     * ARG2: number of threads per MPI rank, *optional* (default = 1)

##### Inputs for multiple CrayPat reports
   * Details about ARGs
     * ARG1: a text file listing the CrayPat reports, *required*
     * ARG2: If not empty, the script generates separate roofline plots for every CrayPat report listed in ARG1. Otherwise, a single roofline plot is generated for specified data of CrayPat reports, *optional*

   * Format for the list in ARG1
     * Each line includes one Pat_Region of a CrayPat report.
     * Delimiter for items in a line is a space.
     * The first item in a line is a filename of a CrayPat report. (*required*)
     * The second item in a line is a legend name to be showed in the roofline plot. No space is allowed for the legend name. (*required*)
     * The third item in a line is a Pat_Region name. If it is not specified, it is set to *Total* region as a default. (*optional*)
     * The forth itme in a line is number of threads for an OpenMP treaded run. If it is not specified, it is set to 1 as a default. (*optional*)
     * An example is as follows:
      > ./SPP/SPP_CrayPat_report_AWP_large &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; AWP  
      > ./SPP/SPP_CrayPat_report_Cactus_4096Nodes &emsp;&emsp;&emsp;&emsp;&thinsp;&thinsp;&thinsp; Cactus &emsp; Total &emsp; 8  
      > ./SPP/SPP_CrayPat_report_MILC_large &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&thinsp;&thinsp; MILC  
      > ./SPP/SPP_CrayPat_report_NAMD_400XEs_1600MPIs &emsp; NAMD &emsp; Perfsuite_all &emsp;  1  
      > ./SPP/SPP_CrayPat_report_NWChem &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&thinsp; NWChem  
      > ./SPP/SPP_CrayPat_report_PPM2F &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&thinsp; PPM &emsp; USER/wworkerbee_.REGION@li.8755  
      > ./SPP/SPP_CrayPat_report_PSDNS8192nodes &emsp;&emsp;&emsp;&emsp;&emsp; PSDNS &emsp; USER/dns_  
      > ./SPP/SPP_CrayPat_report_QMCPACK_160000tasks &emsp;&emsp; QMCPACK  
      > ./SPP/SPP_CrayPat_report_RMG_3456XEoptimized &emsp;&emsp;&thinsp;&thinsp; RMG &emsp; Total &emsp; 32  
      > ./SPP/SPP_CrayPat_report_VPIC_147456tasks &emsp;&emsp;&emsp;&emsp;&thinsp;&thinsp;&thinsp; VPIC  

##### Outputs (i.e., two roofline plots)
  * Roofline plot based on DATA_CACHE_REFILLS_FROM_L2_OR_NORTHBRIDGE:GOOD (DCR_GOOD) counter data, *recommended*
  * Roofline plot based on PAPI_L1_DCA counter data, *CrayPat default*



## Bug report and requests
Send bug reports and requests for improvement to JaeHyuk Kwack (jkwack2@illinois.edu).

