# Required TLA+ verification

Every plan requires a meaningful TLA+ specification and actual TLC model checking
by the parent and both required reviewers before readiness. Keep the model as
small as the requested behavior permits; keep its abstraction explicit.

## Model the requested behavior

Write a concrete `.tla` module and one or more `.cfg` files under the mapped
project's plan `verifications/tla/`. Model actual domain state, inputs, transitions,
guards, effects and relevant failure/recovery behavior. For a stateless change,
model the input/validation/output relation instead of inventing a persistent
service. Do not substitute a generic agent-workflow model for a product feature.
If meaningful scope cannot yet be identified, clarify intent rather than claiming
formal verification of an unrelated or empty specification.

Map acceptance criteria and Mermaid transition IDs to TLA+ variables/actions and
named invariants or temporal properties. Separate requirements represented in the
model from those covered by concrete implementation/visual/operational checks.
Explain material omissions and the additional evidence required. A passing model
does not discharge an omitted requirement.

Define initial state(s), next-state relation, types, meaningful safety properties,
finite constants/domains and assumptions. Check temporal properties when the
request depends on eventual progress, stating the fairness/environment assumptions
needed. If liveness is not being checked, state that explicitly. Do not add
fairness, state constraints, or assumptions that silently eliminate failures the
request requires handling. A property that restates an assumption is not evidence
of the intended behavior.

Keep diagram and specification aligned. Inspect reachability/coverage or a focused
witness so a passing safety check is not caused by unreachable success/error
paths. Use a small negative/regression probe when useful to demonstrate that a
relevant violation is detected; do not build a broad mutation framework. For a
fix, reproduce the bad behavior/violated property when feasible and then check the
corrected model. Preserve traces and distinguish intended probe violations from
production-model failures. Never fix a counterexample merely by deleting its
property, excluding the bad state, or weakening the requirement.

## Run TLC and preserve evidence

Locate an installed Java executable and `tla2tools.jar`, or use an authorized
isolated tool setup. Record the actual tool/Java versions and tool identity; do
not silently alter global configuration. If execution is unavailable or needs
permission, resolve it through available authorized tooling or mark it BLOCKED.
Do not replace actual model checking with a parse, a simulated run, or a claim
that the reviewers have checked it by inspection.

Run explicit model-checking configurations with all required properties enabled.
For example, after setting task-specific paths to inspected values:

```sh
"$DAWG_JAVA" -cp "$DAWG_TLA_JAR" tlc2.TLC -workers 1 \
  -metadir "$DAWG_TLC_STATE_DIR" -config "$DAWG_TLA_CONFIG" "$DAWG_TLA_MODULE" \
  > "$DAWG_TLC_LOG" 2>&1
```

Use fresh private metadata/output locations per attempt and per agent. Keep
temporary state databases outside tracked source; save durable logs and receipts
under `verifications/tla/runs/`. Avoid pipelines that hide TLC's exit status.
Inspect the config's enabled properties and the entire output, not only exit 0.
Require completed finite exploration, nonempty meaningful reachable states and
no unexplored queue/timeout/counterexample/error for required checks. Syntax-only
success, simulation, interrupted runs and resource failures do not pass this gate.

Keep deadlock checking enabled unless a documented modeling decision justifies
its treatment. TLC's `-deadlock` flag disables the check; do not add it to enable
checking or suppress an unexplained failure. Represent valid terminal behavior
explicitly when appropriate. Avoid symmetry for liveness checking unless supported
and justified for the selected checker; disclose reductions and finite bounds.

For every required configuration and attempt, save:

- Exact module/configuration/imported-project-module hashes and tool identity.
- Java/TLC version, command, working directory and configuration constants,
  bounds, properties, assumptions, fairness, constraints and deadlock settings.
- Exit status, raw stdout/stderr, generated/distinct states and remaining queue,
  completion/error status, warnings and relevant coverage/traces.
- Expected outcome and actual result. An intentional negative probe needs the
  specific expected violation and trace; parser/runtime failure is not that result.
- Model revision, owning agent and requirement/implementation traceability.

Do not overwrite failed attempts. Model input identity includes all imported
project modules and effective configurations; a `.tla` filename or an old success
log alone does not identify the checked model.

## Both reviewers execute independently

Give `gpt-6-astra`/high and `gpt-6.1-sol`/high the same final module/configurations,
dependency identities, acceptance mapping and parent evidence. Each must:

1. Read the actual spec/config and inspect assumptions, properties, abstraction,
   fairness/deadlock handling, finite scope, relevant reachability and omissions.
2. Independently execute every required configuration in a fresh own run. A shared
   audited runner is allowed, but each must inspect its commands/configs and raw
   outputs instead of trusting the other agent's receipt or a summary boolean.
3. Save its own identities, logs, outcomes and semantic findings. Verify its
   checked input hashes match the final parent inputs. Independently assess whether
   those inputs represent the requested behavior and intended implementation.

Readiness requires the parent's and both reviewers' completed passing required
checks on identical current inputs, both semantic approvals and resolved material
findings. Missing/blocked/unrun reviewer execution is a blocker, not an approval.
Keep expected negative/witness probes separate from successful required models.

Material behavior, model/dependency, configuration/property, constant/bound,
assumption or fairness changes invalidate all three receipts. Rerun the parent
and both reviewers and reassess the changed contract. Unchanged exact inputs may
retain their executed receipts while reviewers inspect later implementation
conformance; do not reuse stale results across a changed model or requirements.

## State the limits and retain implementation checks

Report that the named properties hold for the checked abstraction and finite
configurations. Do not describe that as a mathematical proof for all sizes,
arbitrary source code, real scheduling, external services, or the truthfulness of
future agents. Keep relevant implementation tests, source-to-model correspondence
review and practical evidence in the plan. Formal checks complement that evidence.

Official references: [TLA+ tools and CLI](https://github.com/tlaplus/tlaplus),
[current TLC tools manual](https://github.com/tlaplus/tlaplus/blob/master/general/docs/current-tools.md).
