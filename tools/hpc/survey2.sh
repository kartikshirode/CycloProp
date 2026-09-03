#!/usr/bin/env bash
sec () { printf '\n===== %s =====\n' "$1"; }

sec "app trees"
ls -la /home/apps/codes /home/apps/utils 2>/dev/null
ls /opt 2>/dev/null
ls /usr/local 2>/dev/null

sec "CFD FEA mesh viz search on disk"
for d in /home/apps /opt /usr/local /share; do
  [ -d "$d" ] && find "$d" -maxdepth 4 -iname "*foam*" -o -maxdepth 4 -iname "*su2*" -o -maxdepth 4 -iname "*ansys*" -o -maxdepth 4 -iname "*fluent*" -o -maxdepth 4 -iname "*gmsh*" -o -maxdepth 4 -iname "*paraview*" -o -maxdepth 4 -iname "*calculix*" -o -maxdepth 4 -iname "*elmer*" 2>/dev/null | head -20
done
echo "-- rpm --"
rpm -qa 2>/dev/null | grep -iE "openfoam|su2|gmsh|paraview|calculix|elmer|openmpi|mpich|petsc|hdf5|netcdf|vtk|fftw|lapack|blas|eigen" | head -40

sec "mpiexec provenance"
ls -l /usr/bin/mpiexec 2>&1
rpm -qf /usr/bin/mpiexec 2>&1
ls /usr/lib64/openmpi/bin 2>/dev/null | head -10
ls /usr/lib64/mpich/bin 2>/dev/null | head -10
rpm -qa 2>/dev/null | grep -iE "^(openmpi|mpich|pmix|libfabric|ucx)" | head -20

sec "dev headers and build tools"
for t in cmake3 ninja flex bison patch git svn wget curl tar unzip python3-config pkg-config; do
  p=$(command -v $t 2>/dev/null); [ -n "$p" ] && echo "FOUND $t -> $p"
done
rpm -qa 2>/dev/null | grep -iE "^(gcc-gfortran|gcc-c\+\+|cmake|zlib-devel|openmpi-devel|scotch|metis|boost)" | head -20

sec "conda envs"
ls -la /home/apps/codes/miniconda3/envs 2>/dev/null
ls -la $HOME/envs $HOME/.conda/envs 2>/dev/null

sec "python stack in base"
source /home/apps/codes/miniconda3/etc/profile.d/conda.sh 2>/dev/null && conda env list 2>&1 | head -20
/home/apps/codes/miniconda3/bin/python -c "import sys;print(sys.version)" 2>&1
/home/apps/codes/miniconda3/bin/python -c "import numpy,scipy;print('numpy',numpy.__version__,'scipy',scipy.__version__)" 2>&1

sec "slurm accounting and defaults"
scontrol show partition 2>&1 | head -30
sacctmgr show qos format=Name,MaxWall,MaxTRES,Priority -P 2>&1 | head -10

sec "my past jobs"
sacct -u $USER --starttime=2026-01-01 --format=JobID,JobName%20,Partition,AllocCPUS,ReqMem,Elapsed,State -P 2>&1 | head -25

sec "node local scratch"
ls -ld /tmp /scratch /local 2>/dev/null
df -h /tmp 2>&1 | tail -2

sec "done"
