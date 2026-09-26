Kalash CR-1, Stage 1 calculations
Team Kalash, VPKBIET. Team ID TM-5A7C41AF909

What is here
  stage-1/design/numbers.json   every input and every result in the report
  tools/linkage.py              four-bar loop closure, pitch schedule, quasi steady
                                aerodynamic loads, pitch loads, thrust vector map
  tools/structure.py            blade section integration, structural margins,
                                bearing ratings, the 34 line mass budget, thrust to weight

How to run
  Python 3, tested on 3.12. No third party packages.

    python tools/linkage.py --write
    python tools/structure.py --write

  Run them in that order. linkage.py writes the kinematic and load blocks and
  structure.py then reads the pitch loads it wrote. Starting from the numbers.json in this
  folder, the two runs reproduce it byte for byte, which is how you can check that the
  stored results come from the stated inputs.

  Without --write, each script prints its results and leaves the file alone.

Not included
  The project also runs a checking script that recomputes every number quoted in the
  report text against numbers.json. It reads the whole project tree, so it won't run from
  this folder. We can share the full repository on request.
