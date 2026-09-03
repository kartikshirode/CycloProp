#!/bin/bash
#SBATCH -J cyclo-probe2
#SBATCH -p gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=00:15:00
#SBATCH -o /home/kartikshirode/cycloprop/probe/out/probe2-%j.log
#SBATCH -e /home/kartikshirode/cycloprop/probe/out/probe2-%j.log

sec () { printf '\n===== %s =====\n' "$1"; }

sec "asked for 8 cpus. what does each route report"
echo "SLURM_CPUS_PER_TASK = $SLURM_CPUS_PER_TASK"
echo "nproc (affinity aware) = $(nproc)"
echo "nproc --all            = $(nproc --all)"
echo "/proc/cpuinfo count    = $(grep -c ^processor /proc/cpuinfo)"
echo "lscpu CPU(s)           = $(lscpu | awk '/^CPU\(s\):/{print $2}')"
echo "getconf _NPROCESSORS_ONLN = $(getconf _NPROCESSORS_ONLN)"
echo "affinity mask          = $(taskset -cp $$ 2>/dev/null)"

sec "cgroup: is there a cpu or memory cap at all"
echo "cgroup path: $(cat /proc/self/cgroup)"
for f in /sys/fs/cgroup/cpu.max /sys/fs/cgroup/memory.max /sys/fs/cgroup/cpuset.cpus /sys/fs/cgroup/cpuset.cpus.effective; do
  printf '%-45s ' "$f"
  if [ -r "$f" ]; then cat "$f"; else echo "ABSENT"; fi
done
CG=$(awk -F: '{print $3}' /proc/self/cgroup | head -1)
for f in cpu.max memory.max cpuset.cpus.effective; do
  p="/sys/fs/cgroup$CG/$f"
  printf '%-70s ' "$p"
  if [ -r "$p" ]; then cat "$p"; else echo "ABSENT"; fi
done

sec "what an autoscaling library would grab"
source /home/apps/codes/miniconda3/etc/profile.d/conda.sh 2>/dev/null
python -c "import os;print('os.cpu_count()      =',os.cpu_count());print('len(sched_getaffinity)=',len(os.sched_getaffinity(0)))" 2>&1

sec "memory: can a job exceed its --mem=32G request"
python -c "
import numpy as np
try:
    a = np.zeros(int(48e9//8), dtype='float64')   # 48 GB, over the 32G request
    a[::10000000] = 1.0
    print('allocated and touched 48 GB against a 32G request: NOT capped')
    del a
except MemoryError as e:
    print('MemoryError, so the request IS enforced:', e)
except Exception as e:
    print('other:', type(e).__name__, e)
" 2>&1

sec "rootless podman on a compute node"
cd /home/kartikshirode
which podman
podman info --format "os={{.Host.OS}} arch={{.Host.Arch}} rootless={{.Host.Security.Rootless}}" 2>&1 | head -3
echo "-- can it pull and run --"
timeout 300 podman run --rm docker.io/library/alpine:3.20 sh -c "echo podman-ran-ok; cat /etc/alpine-release" 2>&1 | tail -5

sec "done"
