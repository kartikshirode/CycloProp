#!/bin/bash
#SBATCH -J cyclo-mpi-comm2
#SBATCH -p gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --time=00:30:00
#SBATCH -o /home/kartikshirode/cycloprop/probe/out/mpi-comm2-%j.log
#SBATCH -e /home/kartikshirode/cycloprop/probe/out/mpi-comm2-%j.log

sec () { printf '\n===== %s =====\n' "$1"; }
source /home/apps/codes/miniconda3/etc/profile.d/conda.sh
conda activate $HOME/envs/foam
export OMP_NUM_THREADS=1
W=/tmp/mpicomm2-$SLURM_JOB_ID; rm -rf $W; mkdir -p $W; cd $W

sec "build with the system gcc"
cat > hello.c <<'EOC'
#include <mpi.h>
#include <stdio.h>
int main(int argc, char **argv) {
    int rank, size, sum;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Allreduce(&rank, &sum, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD);
    if (rank == 0) printf("MPI OK size=%d allreduce=%d expect=%d\n", size, sum, size*(size-1)/2);
    MPI_Finalize();
    return 0;
}
EOC
export MPICH_CC=/usr/bin/gcc
mpicc -o hello hello.c
echo "compile exit: $?"
ls -l hello 2>&1
[ -x ./hello ] || { echo "NO BINARY, stopping"; exit 1; }

sec "ucx transports available"
which ucx_info && ucx_info -d 2>/dev/null | grep -E "^#.*Transport|Device:" | head -20
fi_info -l 2>&1 | head -20

sec "A. default (ch4:ucx), 4 ranks, 90 s"
timeout 90 mpirun -np 4 ./hello; echo "A exit: $?  124=hung"

sec "B. UCX_TLS=sm,self"
UCX_TLS=sm,self timeout 90 mpirun -np 4 ./hello; echo "B exit: $?"

sec "C. force ofi netmod"
MPIR_CVAR_CH4_NETMOD=ofi timeout 90 mpirun -np 4 ./hello; echo "C exit: $?"

sec "D. ofi netmod + FI_PROVIDER=shm"
MPIR_CVAR_CH4_NETMOD=ofi FI_PROVIDER=shm timeout 90 mpirun -np 4 ./hello; echo "D exit: $?"

sec "E. ofi netmod + FI_PROVIDER=tcp"
MPIR_CVAR_CH4_NETMOD=ofi FI_PROVIDER=tcp timeout 90 mpirun -np 4 ./hello; echo "E exit: $?"

sec "F. 8 ranks on whatever worked above, default"
timeout 90 mpirun -np 8 ./hello; echo "F exit: $?"

sec "cleanup"
cd /tmp && rm -rf $W
