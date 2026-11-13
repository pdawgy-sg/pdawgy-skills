# Separate intentionally blocked scenario

Current phase: isolated verification. B1 BLOCKED, unchecked. Open issues: 1.
This expected blocker belongs to this scenario and is not an unresolved failure
of the separate recovered-addition case or the authored skill product.

## B-F1 — Required fixture tool cannot start

- Status: BLOCKED; not resolved.
- Affects: B1 unavailable-tool check.
- Expected: launch the required tool successfully.
- Actual: FileNotFoundError, errno 2; process never started, so no
  process exit code or successful verification is invented.
- Reproduction command: `/tmp/dawg-green-sol-eval/blocked/uniquely-absent-review-tool-sol-20261112` from blocked/.
- Cause: the requested executable path does not exist.
- First observation/evidence: blocked-attempt1.log; blocked-status.json.
- Needed action: Provide the correct installed tool path or authorize an isolated tool installation/setup; no installation or skip approval is supplied.
- Exit criteria: obtain applicable authorization/dependency, then actually run the
  intended check successfully and record its current input identity/results.
- Next action: request that dependency; continue independent safe source inspection.
- Resolution: NONE. Do not skip B1 or declare this case complete.
