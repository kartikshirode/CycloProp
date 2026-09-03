#!/bin/bash
#SBATCH -J cyclo-probe
#SBATCH -p gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=00:20:00
#SBATCH -o /home/kartikshirode/cycloprop/probe/out/probe-%j.log
#SBATCH -e /home/kartikshirode/cycloprop/probe/out/probe-%j.log

sec () { printf '\n===== %s =====\n' "$1"; }

sec "where am I"
hostname; date -u +%Y-%m-%dT%H:%M:%SZ
echo "JobID $SLURM_JOB_ID  node $SLURMD_NODENAME"
echo "SLURM_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK  SLURM_MEM_PER_NODE=$SLURM_MEM_PER_NODE"
echo "nproc sees: $(nproc)"
echo "nproc --all: $(nproc --all)"

sec "cpu model"
lscpu | grep -E "Model name|^CPU\(s\)|Thread|Core|Socket|MHz|NUMA node\(s\)|L3"

sec "cgroup limits actually applied"
cat /sys/fs/cgroup/cpu.max 2>/dev/null
cat /sys/fs/cgroup/memory.max 2>/dev/null
free -g | head -2

sec "gpu visible without --gres"
nvidia-smi --query-gpu=index,name,memory.total --format=csv 2>&1 | head -5

sec "node local scratch"
SCRATCH=/tmp/cyclo-$SLURM_JOB_ID
mkdir -p $SCRATCH && cd $SCRATCH && echo ok > t.txt && cat t.txt
df -h /tmp | tail -1
dd if=/dev/zero of=$SCRATCH/bench.bin bs=1M count=1024 2>&1 | tail -1
rm -rf $SCRATCH

sec "OUTBOUND INTERNET from compute node"
echo "-- DNS --"
timeout 8 getent hosts pypi.org 2>&1 | head -2
timeout 8 getent hosts github.com 2>&1 | head -2
echo "-- HTTPS pypi --"
timeout 12 curl -sS -o /dev/null -w "pypi HTTP %{http_code} in %{time_total}s\n" https://pypi.org/simple/ 2>&1
echo "-- HTTPS conda-forge --"
timeout 12 curl -sS -o /dev/null -w "condaforge HTTP %{http_code} in %{time_total}s\n" https://conda.anaconda.org/conda-forge/noarch/repodata.json 2>&1
echo "-- HTTPS github --"
timeout 12 curl -sS -o /dev/null -w "github HTTP %{http_code} in %{time_total}s\n" https://github.com 2>&1
echo "-- proxy env --"
env | grep -i proxy || echo "no proxy vars set"

sec "python and numpy speed"
source /home/apps/codes/miniconda3/etc/profile.d/conda.sh 2>/dev/null
python -c "import sys; print(sys.version)" 2>&1
python -c "import numpy; print('numpy', numpy.__version__)" 2>&1
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
python - <<'PY' 2>&1
try:
    import numpy as np, time
    n = 4000
    a = np.random.rand(n, n); b = np.random.rand(n, n)
    t = time.time(); a @ b; dt = time.time() - t
    print(f"dgemm {n}^3 in {dt:.2f}s = {2*n**3/dt/1e9:.1f} GFLOP/s")
    np.show_config()
except Exception as e:
    print("numpy bench unavailable:", e)
PY

sec "can podman run on a compute node"
which podman && timeout 30 podman info --format "{{.Host.OS}} {{.Host.Arch}} rootless={{.Host.Security.Rootless}}" 2>&1 | head -5

sec "done"
date -u +%Y-%m-%dT%H:%M:%SZ
