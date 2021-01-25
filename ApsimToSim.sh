#!/bin/bash
#singularity exec -B `pwd`:/TMPDIR --pwd /TMPDIR /Apsim7.10-latest.ubuntu.sapp ApsimToSim.exe "$@"
singularity exec -B `pwd`:/TMPDIR --pwd /TMPDIR /Apsim7.9-r4132.ubuntu.sapp ApsimToSim.exe "$@"
