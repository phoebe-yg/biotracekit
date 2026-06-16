# Web Reviewer MVP Notes

The web reviewer branch tests whether a BioTraceKit dossier can become a clear review surface for scientists who do not want to read workflow source code.

## What It Proves

- A JSON dossier can drive a useful dashboard without a server.
- FAIR readiness checks can be made visible at a glance.
- Tool, container, parameter, input, and output inventories can be reviewed together.
- A methods summary can be copied into a handoff note or draft manuscript section.

## How To Try It

From this branch, run:

```bash
python3 -m http.server 4173 --directory web
```

Then open:

```text
http://localhost:4173
```

## Next Questions

- Should the app load `biotracekit.json` files from a GitHub release or artifact?
- Should the dashboard be generated as a static site by the CLI?
- Which review comments should become machine-readable policy checks?
