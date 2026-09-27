# Compute: Baramati HPC

First assembled 26 August 2026 from the local ssh config and from job scripts in two earlier
projects that ran on these same servers. **Rewritten 3 September 2026, when the cluster was
reachable and every line below was measured rather than inferred.** The survey and probe
scripts are in `tools/hpc/`, and the raw logs stay on the cluster under `~/cycloprop/probe/out/`.

## Access

```
Host baramati
    HostName 172.16.100.105
    User kartikshirode
    Port 22
    ServerAliveInterval 30
    ServerAliveCountMax 4
```

Key is `~/.ssh/id_ed25519`, comment `kartik@baramati`. The login node answers as
`aicoeserver01`, Rocky Linux 9.8, kernel 5.14. `172.16.100.105` is RFC1918, so the cluster is
reachable only from its own network, and off that network there is no route at all. Vendor is
Benchmark Computer Solutions.

## What the cluster actually is

Measured 3 September 2026. The earlier version of this table guessed from four old job scripts
and it was wrong in the direction that matters: the machine is far larger than the jobs that
had been run on it.

| Property | Measured | How |
| --- | --- | --- |
| Scheduler | Slurm, `sched/backfill` | `scontrol show config` |
| Partitions | One, `gpu`. There is no CPU partition | `sinfo` |
| Nodes | `aicoeserver03`, `04`, `05`, all idle, queue empty | `sinfo`, `squeue` |
| CPU | 2 x AMD EPYC 9554, 64 cores per socket, 2 threads per core | `lscpu` inside a job |
| Cores per node | 128 physical, 256 logical. 768 logical across the partition | `scontrol show partition` |
| Memory per node | 1,000,000 MB, roughly 977 GB. 3 TB across the partition | `scontrol` |
| GPU, as Slurm sees it | 14 x `1g.18gb` MIG slices on 03 and 04, 8 x `1g.24gb` on 05 | `sinfo -N` |
| GPU, physically | 2 x NVIDIA H200 NVL per node, 143,771 MiB each | `nvidia-smi` inside a job |
| Walltime ceiling | `MaxTime=UNLIMITED`, `DefaultTime=NONE` | `scontrol show partition` |
| Array ceiling | `MaxArraySize=1001`, `MaxJobCount=10000` | `scontrol show config` |
| QOS limits | `normal`, with no MaxWall and no MaxTRES set | `sacctmgr show qos` |
| Home storage | 128 TB, 126 TB free, no quota enforced. 60 GB used today | `df -h`, `quota` |
| Node-local scratch | `/` has 728 GB with 675 GB free, 2.7 GB/s sequential write | `dd` inside a job |
| Modules | Three only: `anaconda3-22.5`, `cuda-12.8`, `miniconda3` | `module avail` |

Two rows there deserve a second read. The walltime is uncapped, so the earlier note that
`--time=12:00:00` "was accepted" was reading a self-imposed limit as a cluster limit. And a job
that asked for no `--gres` at all could still see both H200 cards, so GPU isolation is not
enforced by the scheduler. Do not assume a neighbouring job cannot reach your device.

## What is not installed, which is the finding that matters

Searched `/home/apps`, `/opt`, `/usr/local` and the rpm database.

- **No CAE software of any kind.** No OpenFOAM, SU2, ANSYS, Fluent, CalculiX, Elmer, Code_Aster,
  gmsh, Salome or ParaView. `/home/apps/codes` holds exactly two things, a CUDA installer and a
  miniconda3 tree
- **No system MPI.** `/usr/bin/mpiexec` exists and belongs to `slurm-torque`, a PBS
  compatibility shim rather than an MPI. No OpenMPI, MPICH, PMIx, UCX or libfabric is installed
  at system level. One arrives with the solver, which the next section covers
- **No Apptainer, no Singularity, no Docker.** `podman` is present, so rootless containers are
  the only container route
- **No gfortran, no cmake, no nvcc** outside the `cuda-12.8` module. gcc and g++ 11.5 and make
  are there, along with flex, bison, zlib-devel and boost

So this is a machine learning GPU cluster. It is a very good one, and nobody has ever run
engineering analysis on it. Anything CAE has to be brought in, and the next section decides how
easily that can happen.

## The assumption that was wrong: compute nodes have internet

The previous version of this file said "Assume no internet on compute nodes until proven
otherwise, and stage everything you need." That was carried across from the Vaani work, which
shipped a probe job specifically to test it and then set `HF_HUB_OFFLINE=1` regardless.

Job 985 on `aicoeserver03` resolved DNS and got HTTP 200 from pypi.org, conda-forge and
github.com, with no proxy variables set anywhere. The login node does the same. Staging a
dependency tree across from the laptop is no longer necessary, which matters here because the
laptop is the side of this link with the poor connection.

## A CFD stack now exists on the cluster, and what it took

Installed 3 September as job 987 and verified as job 1004. `conda create -p $HOME/envs/foam`
then `conda install -c conda-forge --solver=libmamba openfoam` gives **OpenFOAM v2412** in 18
minutes, and it brings its own MPICH 4.3.2, PETSc 3.23.5, scotch, BLIS and a zen4 build variant
that matches the EPYC 9554 on these nodes. No root, no container, no compiler needed.

What it does out of the box:

| Step | Result |
| --- | --- |
| `blockMesh` on pitzDaily | 12,225 cells |
| `checkMesh` | Mesh OK. Max non-orthogonality 5.95, max skewness 0.26 |
| `simpleFoam` serial | Converged in 281 iterations, 4.79 s solver time |
| `simpleFoam -parallel` on 4, 8, 16 ranks | Converged in 288, 293 and 293 iterations |
| Solver time across those | 4.79 s serial, 1.70 s on 4, 1.06 s on 8, 1.07 s on 16 |

The case saturates at 8 ranks because 12,225 cells is far too small to scale further, so read
that column as proof the parallel path runs rather than as a scaling result.

### The packaging bug that costs a day if you meet it cold

Parallel runs fail out of the box, and the way they fail hides the cause.

`simpleFoam` has `DT_RPATH` of `$ORIGIN/../lib:$ORIGIN/../lib/sys-mpich:$ORIGIN/../lib/dummy`,
and `FOAM_MPI` is set to `sys-mpich`. The package puts the parallel Pstream library in
`lib/mpich-3.3` instead, so no `lib/sys-mpich` exists, the loader falls through to `lib/dummy`,
and every rank dies with "The dummy Pstream library cannot be used in parallel mode".

The fix is one symlink:

```
ln -s mpich-3.3 $HOME/envs/foam/lib/sys-mpich
```

Two things that do not fix it, both tried. `LD_LIBRARY_PATH` loses because this is `DT_RPATH`
and not `DT_RUNPATH`, so the rpath wins. `LD_PRELOAD` of the right library loads it ahead of
`libOpenFOAM` and dies on `undefined symbol: _ZTIN4Foam9UOPstreamE`.

Worse, under `mpirun` this presents as a **hang rather than an error**. Each rank hits the
fatal, calls `exit()` without `MPI_Abort`, and Hydra waits for siblings that will never check
in. Job 993 sat there for 11 minutes looking like a fabric problem. It was not: MPI itself
passes `MPI_Barrier` and `MPI_Allreduce` at 4 and 8 ranks under every launcher and every
`FI_PROVIDER` setting tried.

### Smaller things that cost time in the same session

- The pitzDaily tutorial ships **no `decomposeParDict`**. Write one before `decomposePar`
- Its `functions` block includes `streamLines`, which does cross processor particle tracking.
  Strip `functions` from `system/controlDict` before timing anything
- `mpicc` needs `MPICH_CC=/usr/bin/gcc`. The conda wrapper looks for
  `x86_64-conda-linux-gnu-cc`, and the conda compiler toolchain is not in the env
- MPICH is built `ch4:ucx,ofi`. UCX reports `self`, `tcp` on `enp2s0f0` and `enp2s0f1`,
  `posix`, `sysv`, `cma` and the CUDA transports. **There is no InfiniBand.** Single node is
  shared memory and fine; anything spanning nodes runs over ethernet and will scale poorly

## Traps still paid for

These cost time once in earlier projects, and two of them were confirmed again on 3 September.

- **`srun` is broken.** It fails with "Job credential expired". Everything goes through
  `sbatch`. Not retested this time, and nothing suggests it changed
- **`--cpus-per-task` defaults to 1.** Set it. Affinity is applied when you do: job 992 asked
  for 8 and `taskset` came back `16-19,144-147`, which is 4 cores of 2 threads
- **Nothing is capped by a cgroup, and this is the sharpest trap on the machine.** Jobs run in
  `/system.slice/slurmd.service` with `cpu.max` at `max 100000`, `memory.max` at `max` and
  `cpuset.cpus.effective` at `0-255`. Two consequences. `nproc` and `sched_getaffinity` read
  the affinity mask and report 8, while `os.cpu_count()`, `/proc/cpuinfo`, `lscpu` and
  `getconf` all report 256, so any library that sizes its thread pool the usual way puts 256
  threads on 8 CPUs. And `--mem` is a scheduling hint rather than a limit: job 992 requested
  32G, then allocated and touched 48 GB without complaint. A runaway job takes the node down
  with whatever else is on it, so set `OMP_NUM_THREADS` from `SLURM_CPUS_PER_TASK` by hand and
  size arrays against what you asked for
- **Rootless podman needs `XDG_RUNTIME_DIR` set by hand under `sbatch`.** Called plainly it
  fails with `lstat /run/user/1052: no such file or directory`, because a batch job gets no
  user session. Point it at a job-local directory first
- **CRLF kills `sbatch`.** Force LF with `.gitattributes`, and run `sed -i "s/\r$//"` on job
  files after any sync anyway
- **Windows ssh strips quotes.** Confirmed again on 3 September: `squeue -o "%.20j"` sent
  through ssh came back as "Unrecognized option: %.20j". Write the file, `scp` it, run it
- **uv venvs on the cluster have no pip.** Call `.venv/bin/python` directly
- **Base conda is not writable.** `conda create -p $HOME/envs/<name>` is the route, which is
  what `~/mkenv.sh` already does
- **Only the `torch-gpu` conda env is built for sm_120**
- **Stage the repo, do not clone on the cluster.** Both prior projects tar and scp a subset, so
  what runs matches what is local

## Layout convention

```
~/envs/<name>              python env for the project
~/<project>/repo           the synced subset
~/<project>/out/<jobid>/   one output file per array task
~/cycloprop/probe/         the survey and probe scripts, with out/ for their logs
```

Per-task scratch goes to node-local `/tmp` and is deleted on exit, because array tasks that
mutate a shared tree stomp on each other.

## What this does for CycloProp

### Stage 1: still nothing, and that has not changed

Stage 1 is a design document. Literature, sizing arithmetic, a weight budget and writing. The
gate script runs in seconds on the laptop, and no sweep in this project wants 768 cores.
Nothing on the critical path to 26 September touches this cluster.

### Stage 2: the hardware is excellent and the software is absent

Stage 2 wants CAD, kinematic and aerodynamic analysis and a structural assessment, and item 3
in `stage-1/design/07-team-and-execution.md` commits to transient CFD with the blade area
coefficient "either confirmed or replaced". Against that:

- **The solver exists now.** OpenFOAM v2412 runs, serial and parallel, verified on a converged
  case. Item 3 has a tool, and it is GPL, so the licence question that `[P-4]` raises does not
  arise for the CFD half
- 384 physical cores sitting idle with no walltime cap is a strong CFD machine, and a 2D
  transient cyclorotor case is small next to it
- 3 TB of memory and 126 TB of disk remove every capacity question
- One node is the sweet spot. 128 physical cores inside shared memory covers a 2D transient
  case comfortably, and going wider means ethernet, which is the wrong trade
- The H200 cards are close to useless for OpenFOAM, which is a CPU code. They matter for the
  learning work this cluster was bought for, not for this project
- FEA and multibody are still open. Nothing was installed or tested for items 2 and 4, and
  CalculiX and Elmer are both on conda-forge if the same route is wanted

The compute barely helps the thing due in 23 days. It helps a great deal with the thing due in
December, and it is a better machine for that than this file used to claim.

### Sharing the cluster

UAV-X is on these same three nodes, building podman images under `stage-1/hpc/` in that repo.
Jobs 994 and 996 were its work while 993 through 1004 were this one's. Since `--mem` is not
enforced, a runaway job here takes down whatever of theirs is on the same node, so check
`squeue` before submitting anything large.

## Open questions, and where they landed

Every unknown the 26 August version listed is now closed.

| Question | Answer |
| --- | --- |
| Full partition list | One partition, `gpu`. There is no CPU partition to prefer |
| Node count, cores, what the MIG slices sit on | 3 nodes, 128 physical cores each, slices on H200 NVL |
| Outbound internet on compute nodes | Yes, unrestricted, no proxy |
| Storage quota per user | None enforced. 126 TB free |
| Apptainer or Singularity | Neither. podman only, and it needs `XDG_RUNTIME_DIR` under sbatch |
| MPI configured | None at system level. MPICH 4.3.2 arrives with conda-forge OpenFOAM and works, over shared memory on one node and TCP across nodes |
