#!/usr/bin/env bash
# Login node survey. Read only. Answers the six open questions in _compute.md
# plus the Stage 2 tool question P-4 in 07-team-and-execution.md.
sec () { printf '\n===== %s =====\n' "$1"; }

sec "identity"
hostname; whoami; date -u +%Y-%m-%dT%H:%M:%SZ
cat /etc/os-release 2>/dev/null | grep -E '^(NAME|VERSION)=' 
uname -r

sec "partitions"
sinfo -o "%20P %5a %10l %6D %6t %N" 2>&1 | head -40

sec "node detail"
sinfo -N -o "%20N %10P %5c %10m %25G %10T" 2>&1 | head -40

sec "scontrol nodes"
scontrol show nodes 2>&1 | grep -E "NodeName|CPUAlloc|CPUTot|RealMemory|Gres=|State=" | head -60

sec "queue right now"
squeue -o "%.10i %.12P %.10u %.8T %.10M %.6D %R" 2>&1 | head -30

sec "my limits"
sacctmgr show assoc where user=$USER format=Account,User,Partition,GrpTRES,MaxJobs,MaxSubmit,QOS -P 2>&1 | head -20
scontrol show config 2>&1 | grep -iE "MaxArraySize|MaxJobCount|DefMemPerCPU|MaxMemPerCPU|SchedulerType" 

sec "storage quota"
df -h $HOME 2>&1 | tail -2
quota -s 2>&1 | head -10
lfs quota -h $HOME 2>&1 | head -10
du -sh $HOME 2>/dev/null

sec "home contents"
ls -la $HOME 2>&1 | head -30

sec "modules"
which module lmod modulecmd 2>&1
module avail 2>&1 | head -80

sec "containers"
which apptainer singularity docker podman 2>&1
apptainer --version 2>&1
singularity --version 2>&1

sec "MPI"
which mpirun mpiexec mpicc ompi_info 2>&1
mpirun --version 2>&1 | head -3
ompi_info 2>&1 | grep -iE "Open MPI:|MPI extensions" | head -5

sec "compilers"
which gcc g++ gfortran icc ifort nvcc cmake make 2>&1
gcc --version 2>&1 | head -1
cmake --version 2>&1 | head -1
nvcc --version 2>&1 | tail -2

sec "CFD and FEA solvers"
for t in openfoam simpleFoam blockMesh su2_CFD SU2_CFD ansys fluent cfx abaqus calculix ccx elmerfem ElmerSolver code_aster gmsh salome paraview pvpython foamRun; do
  p=$(command -v $t 2>/dev/null); [ -n "$p" ] && echo "FOUND $t -> $p"
done
ls /opt /home/apps /home/apps/codes /usr/local 2>/dev/null | head -60

sec "python and conda"
which python python3 conda mamba uv 2>&1
python3 --version 2>&1
ls /home/apps/codes/miniconda3/envs 2>/dev/null
conda env list 2>&1 | head -20

sec "GPU on login node"
nvidia-smi 2>&1 | head -15

sec "outbound internet from LOGIN node"
timeout 8 curl -sSI https://pypi.org/simple/ 2>&1 | head -3
timeout 8 getent hosts pypi.org 2>&1 | head -2

sec "done"
