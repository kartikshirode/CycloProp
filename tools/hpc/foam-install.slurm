#!/bin/bash
#SBATCH -J cyclo-foam-install
#SBATCH -p gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=96G
#SBATCH --time=03:00:00
#SBATCH -o /home/kartikshirode/cycloprop/probe/out/foam-install-%j.log
#SBATCH -e /home/kartikshirode/cycloprop/probe/out/foam-install-%j.log

set -o pipefail
sec () { printf '\n===== %s =====\n' "$1"; }
ENV=$HOME/envs/foam

sec "start"
hostname; date -u +%Y-%m-%dT%H:%M:%SZ
source /home/apps/codes/miniconda3/etc/profile.d/conda.sh

sec "create env"
if [ ! -d "$ENV" ]; then
  conda create -y -p "$ENV" python=3.11 --solver=libmamba 2>&1 | tail -15
else
  echo "env already exists at $ENV"
fi

sec "install openfoam from conda-forge"
conda install -y -p "$ENV" -c conda-forge --solver=libmamba openfoam 2>&1 | tail -40
echo "conda install exit: $?"

sec "what landed"
conda activate "$ENV"
echo "PREFIX=$CONDA_PREFIX"
ls $ENV/bin 2>/dev/null | grep -iE "foam|blockMesh|snappy|decomposePar|checkMesh|mpirun" | head -30
ls $ENV/opt 2>/dev/null | head -10

sec "openfoam env sourcing"
for cand in $ENV/opt/openfoam*/etc/bashrc $ENV/etc/openfoam/bashrc $ENV/share/openfoam/etc/bashrc; do
  [ -f "$cand" ] && echo "FOUND bashrc: $cand"
done

sec "solver version"
which simpleFoam blockMesh pimpleFoam checkMesh decomposePar 2>&1
simpleFoam -help 2>&1 | head -6
blockMesh -help 2>&1 | head -4

sec "mpi that came with it"
which mpirun mpiexec 2>&1
mpirun --version 2>&1 | head -2

sec "done"
date -u +%Y-%m-%dT%H:%M:%SZ
