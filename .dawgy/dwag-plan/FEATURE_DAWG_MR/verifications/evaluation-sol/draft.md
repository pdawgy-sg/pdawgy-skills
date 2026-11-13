Comparison: `main` merge-base `4fee0028ef162896cfc02a7af4ab00137a17c7d4` → committed head `7ff8c71ea4473d82d999dd2eca399bcfebfdda83`.

# Fix fractional shipping quotes

## Problem

Fractional shipments are rounded down even though billing is per started kilogram:
a 1.2 kg shipment is quoted at 5 instead of 10 currency units.

## Fix

Round positive weights up with `math.ceil` before applying the existing rate.
Whole-kilogram prices and rejection of nonpositive weights remain in place.

## Blast radius

Changes `shipping.quote` and its direct CLI consumer's quoted amounts for fractional
weights. The signature and rate stay unchanged; `math` is standard library. Adds
focused checks and execution records. CLI display formatting is still a known gap;
other consumers were not exhaustively audited.

## Verified / tested

Recorded fixture-author evidence, not rerun while drafting. These setup runs
preceded the commit; matching fingerprints identify the inspected code/checks,
while a clean-HEAD execution is not established:

- `python -B -m checks.check_quote`: exit 0 for fractional and whole-weight cases.
  `verification/current-pass.json` fingerprints match the committed source/check.
- `python -B -m checks.check_cli_output`: **exit 1**; CLI prints `10` instead of
  expected `Shipping: 10`. Current source/check fingerprints match
  `verification/current-failure.json`; this failure remains unresolved.
- `verification/stale.json` records an older integer-only pass against pre-fix
  source; it does not verify this committed change. Added test files alone do
  not establish a passing run.

No tests were launched during drafting. Staged notes, dirty source and untracked
files were excluded from this committed comparison.
