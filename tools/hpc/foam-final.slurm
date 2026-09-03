#!/bin/bash
#SBATCH -J cyclo-foam-final
#SBATCH -p gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=64G
#SBATCH --time=00:40:00
#SBATCH -o /home/kartikshirode/cycloprop/probe/out/foam-final-%j.log
#SBATCH -e /home/kartikshirode/cycloprop/probe/out/foam-final-%j.log

sec () { printf '\n===== %s =====\n' "$1"; }
source /home/apps/codes/miniconda3/etc/profile.d/conda.sh
conda activate $HOME/envs/foam
export OMP_NUM_THREADS=1
ENV=$HOME/envs/foam

sec "the fix: point the RPATH name at the directory that exists"
echo "RPATH wants:  \$ORIGIN/../lib/sys-mpich"
echo "package has:  lib/mpich-3.3"
if [ ! -e $ENV/lib/sys-mpich ]; then
  ln -s mpich-3.3 $ENV/lib/sys-mpich && echo "symlink created"
else
  echo "symlink already present"
fi
ls -l $ENV/lib/sys-mpich
ldd $ENV/bin/simpleFoam 2>/dev/null | grep -i pstream

stage () {
  local C=$1 N=$2
  rm -rf $C; mkdir -p $C
  cp -r $ENV/tutorials/incompressible/simpleFoam/pitzDaily/. $C/
  cd $C
  sed -i '/^functions$/,$d' system/controlDict
  blockMesh > log.blockMesh 2>&1
  printf 'FoamFile\n{\n version 2.0;\n format ascii;\n class dictionary;\n location "system";\n object decomposeParDict;\n}\nnumberOfSubdomains %d;\nmethod scotch;\n' $N > system/decomposeParDict
  [ $N -gt 1 ] && decomposePar -force > log.decompose 2>&1
  grep -m1 "cells:" log.blockMesh
}

for N in 1 4 8 16; do
  sec "$N rank(s)"
  C=/tmp/foamfinal-$SLURM_JOB_ID-$N
  stage $C $N
  t0=$(date +%s.%N)
  if [ $N -eq 1 ]; then
    simpleFoam > log.solve 2>&1; rc=$?
  else
    timeout 400 mpirun -np $N simpleFoam -parallel > log.solve 2>&1; rc=$?
  fi
  t1=$(date +%s.%N)
  printf "ranks=%-3d exit=%s wall=%.2f s\n" $N $rc "$(echo "$t1-$t0" | bc)"
  grep -E "converged in|^ExecutionTime" log.solve | tail -2
  grep -iE "FATAL|error" log.solve | head -3
  cd /tmp; rm -rf $C
done

sec "done"
date -u +%Y-%m-%dT%H:%M:%SZ
