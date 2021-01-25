#!/bin/bash
#singularity exec -B `pwd`:/TMPDIR --pwd /TMPDIR /Apsim7.10-latest.ubuntu.sapp Apsim.exe "$@"
singularity exec -B `pwd`:/TMPDIR --pwd /TMPDIR /Apsim7.9-r4132.ubuntu.sapp Apsim.exe "$@"


#singularity exec -B `pwd`:/TMPDIR --pwd /TMPDIR /Apsim7.10-latest.ubuntu.sapp ApsimModel.exe "$@"
#singularity exec -B /$1:/TMPDIR --pwd TMPDIR /Apsim7.10-latest.ubuntu.sapp Apsim.exe $2

