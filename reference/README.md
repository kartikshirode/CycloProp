# Reference sources

What sits in this folder, where each file came from, and how to get the originals back.

The two theses are the primary sources behind the thrust coefficient, the figure of merit and
the solidity band. Their PDFs are **not** committed. Together they run to 52 MB against a
repository of about 2.2 MB, so what lives here is the machine text extract of each one plus the
sha256 of the PDF it was taken from. Anybody who needs the figures, the plots or the
photographs re-fetches the PDF with the command below and checks the hash.

The extracts are the source authors' words, reproduced exactly as PyMuPDF returned them. No
editing, no reflowing, no dash substitution. They are evidence, and rewriting incoming evidence
to satisfy our own style rules would damage it. `tools/check.py` skips this whole directory for
that reason.

## Kellen 2019

Adam John Kellen, 2019. *Performance Measurements on a UAV-Scale Cycloidal Rotor in Hover.*
MS thesis, Texas A&M University. Handle 1969.1/184958. 86 pages, 35,336,607 bytes,
sha256 `b914b37c3f1858cb2684725e196c4825cae687de9b13c9fd44389a9e3cd21dbb`.

Extract: [kellen2019-extract.txt](kellen2019-extract.txt)

```
curl -L -o kellen2019.pdf "https://web.archive.org/web/20221012021039id_/https://oaktrust.library.tamu.edu/bitstream/handle/1969.1/184958/KELLEN-THESIS-2019.pdf"
```

## Benedict 2010

Moble Benedict, 2010. *Fundamental Understanding of the Cycloidal-Rotor Concept for Micro Air
Vehicle Applications.* PhD dissertation, University of Maryland. Handle 1903/11257. 312 pages,
17,607,165 bytes, sha256 `998819c2abc785c3caf6741847de13f94bb135d57f0b46528f619943273e3355`.

Extract: [benedict2010-extract.txt](benedict2010-extract.txt)

```
curl -L -o benedict2010.pdf "https://web.archive.org/web/20230314013537id_/https://drum.lib.umd.edu/bitstream/handle/1903/11257/Moble_umd_0117E_11828.pdf"
```

## Use the Wayback copies, not the live repositories

Both live routes fail from a script and they fail for different reasons.

OAKTrust, which holds Kellen, sits behind a Cloudflare JavaScript challenge. The item page, the
bitstream and the handle URL all answer 403 to anything without a browser engine, and it is not
a permissions gate: a real browser passes in about two seconds. That is what kept this thesis
out of the project for two weeks.

DRUM, which holds Benedict, was returning a maintenance page. Different failure, same result.

The `id_` segment in both URLs matters. It tells the Wayback Machine to serve the archived
bytes as captured, with no toolbar injection and no rewriting, so what you get is the original
PDF. Drop it and you get an HTML wrapper instead. Check the hash after fetching either file;
a mismatch usually means the URL lost its `id_`.

## The problem statement

`cycloprop-problem-statement.pdf` and `cycloprop-problem-statement.txt` are the official
Techfest problem statement, and `techfest-api-cycloprop.json` is the API payload it was pulled
from. `context.md` at the repository root is built from these and outranks every other document
here on what the competition actually requires. The PDF is small enough to commit, so it is
committed.
