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

## Ramsey 2022, located and still unreachable

Ramsay Allen Ramsey, December 2022. *Development and Flight Testing of a 25-Kilogram
Quad-Cyclocopter.* MS thesis, Texas A&M University. Handle 1969.1/198531, item UUID
`692efcdd-c56a-4c7a-b507-f3e673986b51`.

No extract here, because the file cannot be fetched from a script. What is here instead is the
exact address, so nobody spends a fourth session looking for it.

```
https://oaktrust.library.tamu.edu/bitstreams/748b37d5-3cd9-449e-af50-4689341f9849/download
```

`RAMSEY-THESIS-2022.pdf`, 84,853,674 bytes. Two things block it and they are separate problems.

The URL answers 403 with a `cf-mitigated: challenge` header, which is the same Cloudflare
JavaScript wall that kept Kellen out for two weeks. Every route was tried: the item page, the
handle, the DSpace 7 REST API under `/server/api/`, a fetch tool and a third party text
extraction proxy. All five get the interstitial. A real browser passes.

The Wayback route that rescued Kellen and Benedict does not exist here. The CDX index has zero
captures of the handle, the item page, the legacy bitstream path or the DSpace 7 bitstream
above. Ramsey was deposited in December 2022 and released in September 2023, which is after the
legacy `/bitstream/handle/` paths stopped being the ones crawlers followed, so there is nothing
archived to fall back to. Older TAMU items are captured on the legacy path and still fetch fine,
which is what makes the gap specific rather than a broken query.

So it needs a browser and 85 MB of connection. Both are human actions.

## The OAI-PMH endpoint is not behind Cloudflare

This is the useful part and it is worth knowing before fighting the front end again.

```
https://oaktrust.library.tamu.edu/server/oai/request?verb=GetRecord&metadataPrefix=ore&identifier=oai:oaktrust.library.tamu.edu:1969.1/198531
```

That answers 200 to plain curl. Harvesters use OAI and it is not proxied through the challenge.
Swap `metadataPrefix=oai_dc` for title, author, dates and the full abstract; `ore` lists every
bitstream in the item with its filename, mimetype and byte length, which is where the URL and
the 84,853,674 above came from; `didl` names the primary bitstream alone, which is the quickest
way to tell the thesis from its licence file and thumbnails.

Any OAKTrust item works, with its handle substituted. It gives metadata and addresses, never
file bytes.

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
from, captured 26 August 2026.

`techfest-api-cycloprop-4sep.json` is the same record pulled again on 4 September and kept
beside it rather than over it, which is what makes a diff possible at all. Everything that
governs the submission is identical across the two, and the PDF at the live URL still hashes to
the bytes committed here. Registrations moved from 11 to 57 and the sponsor image and link were
cleared. To repeat the check on the send date:

```
curl -s https://techfest.org/api/compis/ | python -c "import json,sys;print([c for c in json.load(sys.stdin) if c['compi_id']=='cycloprop'][0])"
``` `context.md` at the repository root is built from these and outranks every other document
here on what the competition actually requires. The PDF is small enough to commit, so it is
committed.
