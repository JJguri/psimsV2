Code developers
==============

- Jonathan Ojeda (QAAFI, The University of Queensland)
- Peter deVoil (QAAFI, The University of Queensland)

### Collaborators to update the code

-  Isaiah Huber (Iowa State University)
-  Chris James (School of Agriculture and Food Sciences, The University of Queensland)
-  Diego Perez (Data Analytics Specialist & Cyber Security Expert)

TERRA Project Team involved in the pSIMS application
==============

### The University of Queensland
- Prof Graeme Hammer (QAAFI)
- Prof Scott Chapman (SAFS)
- Dr Jonathan Ojeda (QAAFI)
- Peter deVoil (QAAFI)
- Chris James (SAFS)

### Purdue University
- Prof Mitchell Tuinstra
- Kai-Wei Yang (PhD student)

pSIMS
==============
pSIMS is a suite of tools, data, and models developed to facilitate access 
to high-resolution climate impact modeling. This system largely automates 
the labor-intensive processes of creating and running data ingest and transformation 
pipelines and allows researchers to use high-performance computing to run simulations 
that extend over large spatial extents, run for many growing seasons, or evaluate many 
alternative management practices or other input configurations. In so doing, pSIMS 
dramatically reduces the time and technical skills required to investigate global change 
vulnerability, impacts and potential adaptations. pSIMS is designed to support integration 
and high-resolution application of any site-based climate impact model that can be compiled 
in a Unix environment (with a focus on primary production: agriculture, livestock, and forestry).

**For more information about pSIMS, please see the following paper:**

Elliott, Joshua, et al. (2014) The parallel system for integrating impact models and sectors (pSIMS).
Environmental Modelling & Software 62: 509-516.
[link to the paper](http://dx.doi.org/10.1016/j.envsoft.2014.04.008)

pSIMSV2
==============

The original pSIMS was developed in 2014 (see paper above), 
We updated pSIMS to pSIMSV2 which is able to run the soft in an Unix Environments with all
dependencies installed by a singularity container without 
the need to install the soft dependencies manually (as in pSIMS).
Also, we updated some packages were obsolete.

The singularity image to run pSIMSV2 are hosted
[here](http://qaafi-hss8hy2.instrument.net.uq.edu.au/singularity-images/) 
for APSIM Classic 7.9. All examples below are an implementation of pSIMSV2 for APSIM 7.9.  

About the research project
==============

Regional scale estimations of sorghum biomass are crucial to identify optimum 
genotype × environment × management (G×E×M) combinations to ensure potential 
biomass production for bioenergy. This work was part of the [TERRA](https://www.purdue.edu/terra/) project.
Using pSIMSV2 we explored the following questions: which factors (G, E and M) 
are dominant in explaining sorghum biomass variability? and how do the drivers 
of sorghum biomass variability change with genotype and irrigation strategy at regional 
scale in the US?

Using the APSIM gridded platform (pAPSIM) within pSIMSV2, four genotypes [grain (GS), sudangrass 
(SS), photosensitive, (PS) and photo-insensitive (PI)] were simulated across the 
potential areas for energy sorghum in the US under rainfed and irrigated conditions 
over 30 years.

Software dependencies installed by the singularity image 
==============

This software list is installed automatically when the singularity image is used for runs including several
tiles. When the user is testing single tiles and not using singularity, it needs to be installed manually.

* python==2.7
* apsim 7.9
* mono
* swift 0.95
* nco 4.4.3
* netcdf4

_Note: this packages are in the requirements.txt file at psims/pysims/_

* numpy==1.15
* airspeed==0.5.4.dev20150515
* cachetools==0.8.0
* calmap==0.0.6
* cdo==1.3.0
* certifi==0.0.8
* chardet==1.0.1
* click==6.6
* click-plugins==1.0.3
* cligj==0.4.0
* colorama==0.3.6
* cycler==0.10.0
* Fiona==1.6.3.post1
* geojson==1.3.2
* matplotlib==1.5.1
* nco==0.0.2
* netCDF4==1.2.2
* pandas==0.17.1
* pyparsing==2.1.1
* python-dateutil==2.4.2
* pytz==2015.7
* PyYAML==3.11
* requests==2.9.1
* Rtree==0.8.2
* ruamel.base==1.0.0
* ruamel.ordereddict==0.4.9
* ruamel.yaml==0.11.1
* scipy==0.17.0
* Shapely==1.5.15
* six==1.10.0
* wget==3.2
* xarray==0.7.1
* XlsxWriter==0.8.4

Data inputs
==================

Data inputs are provided for download and other are hosted in this repo.

### Global climate and soil data (30 arc-minute resolution)

Two full global gridded dataset available for pSIMS users:

* _Climate:_ [AgMERRA Climate Forcing Dataset for Agricultural Modeling](https://data.giss.nasa.gov/impacts/agmipcf/#:~:text=The%20AgMERRA%20and%20AgCFSR%20climate,variables%20required%20for%20agricultural%20models.)
* _Soil:_ [Harmonized World Soil Database](http://www.fao.org/soils-portal/data-hub/soil-maps-and-databases/harmonized-world-soil-database-v12/en/)

Due to the size of these datasets, they are available
only via Globus online. If you do not already have a
Globus account, you may create one at globus.org. The endpoint name
is davidk#psims. Harmonized World Soil Database files are available
in the .../soils/hwsd200.wrld.30min directory. AgMERRA climate data is available in the .../clim/ggcmi/agmerra directory.

You can also create your own datasets (or use others) and pass it to this tool.
1. Download and extract climate dataset from (if you want to use AgMERRA climate data)
   - http://users.rcc.uchicago.edu/~davidkelly999/psims/agmerra.tar.gz (19GB)
2. Download and extract soil dataset from (if you want to use the FAO Harmonized World Soil Database v 1.2)
   - http://users.rcc.uchicago.edu/~davidkelly999/psims/gsde.tar.gz (1.8GB)

### Climate data for the USA (1 km resolution)

A template to convert [Daymet climate data](https://daac.ornl.gov/cgi-bin/dsviewer.pl?ds_id=1840) to a pSIMS format was 
created by the authors of this repo using the [PyDaymet](https://pypi.org/project/pydaymet/) 
Python package (contact them for more information). For PyDaymet information please 
visit the [GitHub](https://github.com/cheginit/pydaymet) repo.

This template aggregates climate daymet data from 1 km resolution to 30 arc-minute resolution to be inputted in pSIMS
and following the format established in psims2met.py (see translators folder in this repo).

### Campaign file

3. Download and extract campaign dataset from
   - http://users.rcc.uchicago.edu/~davidkelly999/psims/campaign.tar.gz (474KB)

### APSIM template and XML files

4. Reference dataset is provided in the folder **refdata** in this repo

### Tile list

5. An example tilelists is provided in the **tilelist** folder in this repo.

### Mask

6. Download and extract masks from
   - http://users.rcc.uchicago.edu/~davidkelly999/psims/masks.tar.gz (12KB)

Parameter file
==================
The parameter file is a YAML-formatted file containing all the parameters of a pSIMSV2
run. It defines things like the number of simulation years, the path to climate input files,
and which model to use. Below is a list of parameters and a description of what it does.

Parameter      | Description
---------      |------------
aggregator     | Aggregator options, used to average a variable across a region
checker        | Checker translator and options, check if a tile should be simulated or not
delta          | Simulation delta, gridcell spacing in arcminutes
executable     | Name of executable and arguments to run for each grid
lat\_zero      | Top edge of the North most grid cell in the campaign
lon\_zero      | Left edge of the West most grid cell in the campaign
long\_names    | Long names for variables, in same order that variables are listed
model          | Defines the type of model to run. Valid options are dssat45, dssat46, apsim75
num\_lats      | Number of latitudes to be included in final nc4 file (starting with lat\_zero)
num\_lons      | Number of longitudes to be included in final nc4 file (starting with lon\_zero)
num\_years     | Number of years to simulate
out\_file      | Defines the prefix of the final nc4 filename
outtypes       | File extensions of files to include in output tar file
refdata        | Directory containing reference data. Will be copied to each simulation
ref\_year      | Reference year (the first year of the simulation)
scens          | Number of scenarios in the campaign
soils          | Directory containing soils
tappcmp        | Campaign translator and options
tappinp        | Input translator and options, goes from experiment.json and soil.json to model specific files
tapptilewth    | Weather tile translator and options
tapptilesoil   | Soil tile translator and options
tappnooutput   | The "no output" translator and options, typically used to create empty data
tappwth        | Weather translator and options, converts .psims.nc format into model specfic weather files
tdelta         | Tile delta gridcell spacing in arcminutes
postprocess    | Name of translator and options to run after running executable
var\_units     | Units to use for each variable, in the same order that variables are listed
variables      | Define the variables to extract to final outputs
weather        | Defines the directory where weather data is stored

Below we provide an example of a parameter file:

```

model:       apsim79
weather:     .../agmerra2degtile
soils:       .../gsde2degtile
refdata:     .../refdata
out_file:    output
executable:  ...
outtypes:    .met,.apsim,.out,.json,.txt

ref_year:    1980
num_years:   30
scen_years:  30
scens: 8

delta:       "30,30"
tdelta:      "120,120"

num_lats:    52
num_lons:    72
lat_zero:    49.75
lon_zero:    -107.75
irr_flag:    true
irr_1st:     false

# Variables to extract
variables:   planting_date,biomass,rad40DAS,rad80DAS,radHarv,temp40DAS,temp80DAS,tempHarv,rain40DAS,rain80DAS,rainHarv,RadiationIn,TempIn,aMinT,aMaxT,RainIn,sw_stress_expan,PAWC,DaysAfterSowing,FloweringDAS,IrrigationIn,sw_stress_photo,N_stress_expan,N_stress_photo,WU,potential_ET,actual_ET,LeafNo,MaxLAI,ESW1av,sw0_40,sw40_80,sw80_harv,tp0_40,tp40_80,tp80_harv,ri0_40,ri40_80,ri80_harv,DOY
var_units:   "date,kg/ha,MJ/m2,MJ/m2,MJ/m2,oC,oC,oC,mm,mm,mm,MJ/m2,oC,oC,oC,mm,(0-1),mm,days,days,mm,,,mm,mm,mm,,,,,,,,,,,,,,"
long_names:  "planting_date,biomass,rad40DAS,rad80DAS,radHarv,temp40DAS,temp80DAS,tempHarv,rain40DAS,rain80DAS,rainHarv,RadiationIn,TempIn,aMinT,aMaxT,RainIn,sw_stress_expan,PAWC,DaysAfterSowing,FloweringDAS,IrrigationIn,sw_stress_photo,N_stress_expan,N_stress_photo,WU,potential_ET,actual_ET,LeafNo,MaxLAI,ESW1av,sw0_40,sw40_80,sw80_harv,tp0_40,tp40_80,tp80_harv,ri0_40,ri40_80,ri80_harv,DOY"

# Only simulate points in the crop mask
#checker:
#  class: SimpleChecker
#  simgfile: .../masks/masks/cropmask.nc4

# Campaign translator
tappcmp:
   class:         camp2json
   campaignfile:  Campaign.nc4
   expfile:       exp_template.json
   outputfile:    experiment.json

# Input translator
tappinp:
    class:         apsim75.jsons2apsim
    soilfile:      soil.json
    soiltile:      1.soil.nc4
    expfile:       experiment.json
    templatefile:  template.apsim
    outputfile:    Generic.apsim

# Weather translator
tappwth:
   class:      apsim79.psims2met
   inputfile:  1.clim.nc4
   variables:  tasmin,tasmax,rsds,pr,wind
   outputfile: Generic.met

# Post processing translation
postprocess:
    class:     apsim79.out2psims
    inputfile: Generic.out

tapptilewth:
    class:     tile_translator

tapptilesoil:
    class:     tile_translator_soil

tappnooutput:
    class: nooutput2psims
```

Experiment and Campaign Files
==============
When pysims is run, the user must specify a campaign directory with the --campaign parameter.
Typically this campaign directory contains two relevant files named **Campaign.nc4** and **exp_template.json**.
These files are used by the jsons2dssat and jsons2apsim translators to create experiment files for the crop model.

The exp_template.json file contains key-value pairs for data that will be written to the experiment file.
These values represent things like fertiliser rate applications, irrigation rates and timing and planting dates.
Static settings for the experiment are stored in **exp_template.json**.
Values that vary by lat, lon, scenario, or time get stored in **Campaign.nc4**.

Below is an example of a **exp_template.json** for a sorghum experiment:

```
{
    "crop_name": "Sorghum",
    "start_date": "01/01/1980",
    "end_date": "31/12/1985",
    "log": "",  
    "reporting_frequency": "harvesting",
    "output_variables": [
        {"name": "dd/mm/yyyy as Date"},
        {"name": "planting_date"},
        {"name": "biomass"},
        {"name": "ExtinctionCoef"},		
        {"name": "radInt"},
        {"name": "PAWC"},
        {"name": "WU"},
        {"name": "potential_ET"},
        {"name": "DaysAfterSowing"},
        {"name": "IrrigationIn"},
        {"name": "FloweringDAS"},
        {"name": "LeafNo"},
        {"name": "MaxLAI"},
        {"name": "RainIn"},
        {"name": "TempIn"},
        {"name": "aMinT"},
        {"name": "aMaxT"},
        {"name": "RadiationIn"},
        {"name": "FertiliserIn"},
        {"name": "actual_ET"}
        ],
"initial_condition": {
        "icrn": ".5",
        "icrip": "100",
        "icnd": "0",
        "icrp": "0",
        "icrt": "300",
        "icrz#": "1",
        "icrze": "1",
        "icrag": "500",
        "icrdp": "30",
        "icdat": "19800101",
        "standing_fraction": "0",
        "water_fraction_full": "1",
        "soilLayer": [
          {"icno3": ".1"  ,"icbl": "5"  ,"icnh4": ".1"},
          {"icno3": ".1"  ,"icbl": "15" ,"icnh4": ".1"},
          {"icno3": ".1"  ,"icbl": "30" ,"icnh4": ".1"},
          {"icno3": ".1"  ,"icbl": "100","icnh4": ".1"},
          {"icno3": ".1" ,"icbl": "200","icnh4": ".1"}
         ]
      },
      "weather": {
        "file": "Generic"
      },
      "planting": {
        "pdate": "15-may",
        "edate": "15-dec",
        "cultivar": "medium",
        "row_spacing": "0.7",
        "depth": "30",
        "sowing_density": "8",
        "skiprow": "solid",
        "ftn": "2"
      },
      "fertilizer": {
        "automatic_fertilizer": "off",
        "fert_criteria": "100",
        "fert_critical": "90",
        "type_auto": "NO3_N",
        "initial_amount": "200",
        "type": "NH4NO3",
        "days_after_sowing": "45",
        "subsequent_amount": "200",
        "depth": "40"
      },
      "irrigation": {
        "automatic_irrigation": "off",
        "asw_depth": "2000",
        "crit_fr_asw": "1",
        "efficiency": "1",
        "allocation_limits": "off",
        "allocation": "10",
        "default_no3_conc": "0.0",
        "default_nh4_conc": "0.0",
        "default_cl_conc": "0.0"
      },
      "reset": {
        "date": "14-may",
        "water": "yes",
        "nitrogen": "yes",
        "surfaceOM": "yes"
      }
}
```

But users may not want to these settings everywhere.
If they have planting dates (pdate) that change by location, users may create a variable 
in **Campaign.nc4** called pdate. The most basic version of this would be a NetCDF variable in the format of 
float pdate(lat, lon). When pysims runs for a given point, the appropriate value would transfer from
**Campaign.nc4** into the experiment file. If pdate is not defined in Campaign.nc4, the static value from 
**exp_template.json** is used instead (in this example on 15 May).
This process works the same for all variables, not just limited to pdate.

Below is an example of a **Campaign.nc4** for a sorghum experiment. In this experiment we use variable planting dates (pdate),
irrigation (automatic_irrigation) and genotype (cultivar). We combined 2 irrigation strategies, 4 genotypes and variable 
planting date by tile.

```
{
  dimensions:
    lat = 360;
    scen = 8;
    lon = 720;
  variables:
    double lat(lat=360);
      :units = "degrees_north";
      :_Storage = "contiguous";

    float cultivar(scen=8, lat=360, lon=720);
      :long_name = "GS,GS,SS,SS,FSPS,FSPS,FS,FS";
      :_DeflateLevel = 5; // int
      :units = "Mapping";

    float scen(scen=8);

    double lon(lon=720);
      :units = "degrees_east";
      :_Storage = "contiguous";

    float pdate(scen=8, lat=360, lon=720);
      :long_name = "Planting date";
      :_DeflateLevel = 5; // int
      :units = "Julian day";

    int automatic_irrigation(scen=8);
      :units = "Mapping";
      :long_name = "off,on,off,on,off,on,off,on";

  // global attributes:
  :person_notes = "Jonathan Ojeda";
  :history = "pSIMS setup for sorghum modelling in USA";
}
```

Below we provide a visual example of the variable planting date across a region in the US included in the campaign file:

![image](/img/pdate.jpg)

Template file
===========

In the **refdata** folder there is an apsim file (**.apsim**) called **template.apsim**. This file is the template apsim file pSIMSV2
will use for every single simulation to create apsim outputs. Here is the place were specific output variables need to be created, 
for example the following code calculates the accumulated irrigation applied from sowing to harvest:

```
<variable>sum of irrigation on end_of_day from sowing to harvesting as IrrigationIn</variable> 
```

Then this variable need to be specified in the **parameter** file as an output as 'IrrigationIn' to be reported in the APSIM report.

The **refdata** folder also contains template apsim XML files for all crops. Any change to the APSIM code (for example the
implementation of new cultivar parameters) need to coded here.

Mask file
===========

In the parameter file there is an option to enable a mask nc file to be implemented. If the users enable this option,
they will need to indicate the location of this file.

```
# Only simulate points in the crop mask
checker:
  class: SimpleChecker
  simgfile: .../masks/masks/cropmask.nc4
```

Data aggregation
===========
The aggregation script is responsible for taking the final output of a psims
simulation and computing the average value for a variable across some geographic region.
To enable aggregation, add a section named 'aggregator' to your parameters file with the following parameters:

Parameter | Description
-----     | -----------
aggfile   | Location of an aggfile. The aggfile contains information about geographic boundries at given lats/lons. Common uses here are gadm regions and food producing units.
weightfile| Location of the weightfile, used to give certain geographic areas more weight than others
levels    | Comma separated list of levels from the aggfile (example: gadm0, gadm1, gadm2)

The aggfile and weightfile must match the resolution used in your simulation. To generate a new aggfile you can use the gdal_rasterize utility to convert from a gadm shapefile to a netcdf file, then use bin/create_agg_limits.py to add the required variables and dimensions.

Example parameters:
```
aggregator:
    aggfile: /path/to/agg.nc
    weightfile: /path/to/weight.nc
    levels: gadm0
```

Tilelists
=========

A tilelist file contains a list of latitudes and longitudes indexes to be processed,
in the format of "latidx/lonidx". Here is an example:

```
0024/0044
0024/0045
```
Tile number can be calculated as follows:

for 0024_0044 (**latidx**=24; **lonidx**=44):

* Latitude (°) -->  90 - (2 * **latidx**) = 42 °N
* Longitude (°) --> -180 (2 * **lonidx**) = -92 °E


Steps to run pSIMS in a Unix environment
==============

_Before to run pSIMSV2 you should check:_

* If you are running pSIMSV2 remotely, check all files were updated in the remote PC.
* In params file check the number of scenarios and the exported variables.
* Check location of psims folder.
* Check location of sh files that runs apsim.
* Check refdata (template.apsim and Sorghum.xml) if some scripts were changed.
* Check campaign (exp_template.json) data aligns with scenario number in params file.
* Be carefull with the commas when the variables are specified in the params file. Do not need 
a comma after the last variable (e.g. rain, yield, biomass: mm, kg/ha, kg/ha) 

## Run in a local computer

_Note: Be sure you type sudo -s and put the password before to start._

#### _Run a single lat/lon combination_
```
/psims/pysims/pysims.py --param .../params.apsim.sample --campaign .../campaign/created_campaign/test3/ --tlatidx 0024 --tlonidx 0044 --latidx 0096 --lonidx 0173
```

#### _Run a single tile_
```
/psims/pysims/pysims.py --param .../params.apsim.sample --campaign .../campaign/created_campaign/test3/ --tlatidx 0024 --tlonidx 0044 
```
#### _Run several tiles together_

In this case the command is looking for the **psims** folder because for more than a tile swift is implemented to
apply parallel computing. Therefore, remember to install swift in your computer before to run several tiles together.

```
./psims -s local -p /psims/pysims/params.apsim.sample -c .../campaign/sorghum/ -t .../TileLists/test -r jon
```

## Run in a computer via remote control through Ubuntu

#### _Run a single lat/lon combination_
```
.../psims/pysims/pysims.py --param .../params.apsim.sample --campaign .../campaign/created_campaign/test2/ --tlatidx 0024 --tlonidx 0044 --latidx 0096 --lonidx 0173
```

#### _Run a single tile_
```
.../psims/pysims/pysims.py --param .../params.apsim.sample --campaign .../campaign/created_campaign/test2/ --tlatidx 0024 --tlonidx 0044
```

#### _Run several tiles together_

In this command, pSIMSV2 is using swift to do runs in parallel, so it was already installed by the singularity image.

```
singularity exec -B /data:/data -B /run/shm:/run/shm .../PSIMs.Apsim79.sapp .../psims/psims -s local -p .../paramsFiles/PetePC/params.apsim.sample -c .../campaign/created_campaign/test3/ -t .../TileLists/sorghumEnergy
```

## Run on a cluster (HPC)

#### _Run a single lat/lon combination_
```
export PYTHONNOUSERSITE=1
.../shfiles/pysims.sh --param .../params.apsim.sample --campaign .../campaign/created_campaign/test2/ --tlatidx 0024 --tlonidx 0044 --latidx 0096 --lonidx 0173 
```
#### _Run a single tile_

```
export PYTHONNOUSERSITE=1
.../shfiles/pysims.sh --param .../params.apsim.sample --campaign .../campaign/created_campaign/test2/ --tlatidx 0024 --tlonidx 0044
```
Arguments description
==================

_Note: this description was done for the code implemented to run pSIMSV2 in a computer through remote control._

**-s:** indicates if the run is implemented in a computer (local) or in a cluster (cluster).

**-p:** indicates the parameter file location (e.g. .../paramsFiles/PetePC/params.apsim.sample)

**-c:** indicates the campaign file location (e.g. .../campaign/created_campaign/test3/)

**-t:** indicates the tile file location (e.g. .../TileLists/sorghumEnergy)

Output Files
============

The output/ directory contains a directory for each latitude being processed.
Within each latitude directory, a tar.gz file exists for each longitude. For example, if your gridList
contained a grid 100/546, you would see an output file called runNNN/output/100/546output.tar.gz. This
file is generated from within the Swift work directory. Which files get included in the file is determined
by how you set "outtypes" in your parameter file.

The **parts/** directory contains the output NetCDF files for each grid being processed. When grid 0024/0044
is done processing, you will see a file called runNNN/parts/0024/546.psims.nc.

The combined nc file is saved in the runNNN directory. Its name depends on the value of
"out_file" in your params file. If you set out_file to "out.psims.apsim75.cfsr.whea", the final
combined nc file would be called "out.psims.apsim75.cfsr.whea.nc4".

Below we provide an output example for the sorghum experiment. The figure shows the biomass yield of sorghum across
a region in the US at 30 arc-minute resolution. This map is for a given year and genotype under rainfed conditions.

![image](/img/biomass.jpg)

Data visualisation
============

Fast visualisation of the PSIMSV2
outputs (and campaign files) can be done using [Panoply](https://www.giss.nasa.gov/tools/panoply/).
Panoply plots geo-referenced and other arrays from netCDF, HDF, GRIB, and other datasets.
Panoply is a cross-platform application that runs on Macintosh, Windows, Linux and other desktop computers. 