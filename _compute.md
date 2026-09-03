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
- **No MPI.** `/usr/bin/mpiexec` exists and belongs to `slurm-torque`, a PBS compatibility shim
  rather than an MPI. No OpenMPI, MPICH, PMIx, UCX or libfabric is installed
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

## Traps still paid for

These cost time once in earlier projects, and two of them were confirmed again on 3 September.

- **`srun` is broken.** It fails with "Job credential expired". Everything goes through
  `sbatch`. Not retested this time, and nothing suggests it changed
- **`--cpus-per-task` defaults to 1.** Confirmed working when set: a job with
  `--cpus-per-task=16` saw `nproc` 16 against `nproc --all` 256, so affinity is applied. Memory
  is not capped the same way, since `free` inside that job still reported all 1007 GB
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

- 384 physical cores sitting idle with no walltime cap is a strong CFD machine, and a 2D
  transient cyclorotor case is small next to it
- 3 TB of memory and 126 TB of disk remove every capacity question
- The H200 cards are close to useless for OpenFOAM, which is a CPU code. They matter for the
  learning work this cluster was bought for, not for this project
- No system MPI means a parallel `decomposePar` run needs an MPI brought in beside the solver
- No Apptainer closes the clean container route, leaving podman as the fallback

The compute barely helps the thing due in 23 days. It helps a great deal with the thing due in
December, and it is a better machine for that than this file used to claim.

## Open questions, and where they landed

Every unknown the 26 August version listed is now closed.

| Question | Answer |
| --- | --- |
| Full partition list | One partition, `gpu`. There is no CPU partition to prefer |
| Node count, cores, what the MIG slices sit on | 3 nodes, 128 physical cores each, slices on H200 NVL |
| Outbound internet on compute nodes | Yes, unrestricted, no proxy |
| Storage quota per user | None enforced. 126 TB free |
| Apptainer or Singularity | Neither. podman only |
| MPI configured | No. It has to arrive with the solver |
