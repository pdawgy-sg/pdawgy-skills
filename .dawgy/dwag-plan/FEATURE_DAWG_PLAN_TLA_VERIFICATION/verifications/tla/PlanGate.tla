------------------------------ MODULE PlanGate ------------------------------
EXTENDS Integers, TLC

CONSTANTS MaxRevision, ImplementAuthorized, EnforceReviewChecks
Reviewers == {"astra", "sol"}
Results == {"pending", "pass", "fail", "blocked"}
Phases == {"draft", "ready", "implementing", "verified", "committed", "delivered"}

VARIABLES phase, revision, parentResult, parentRevision,
          reviewResults, reviewRevisions, approvals, implementationPassed

vars == <<phase, revision, parentResult, parentRevision,
          reviewResults, reviewRevisions, approvals, implementationPassed>>

Init ==
    /\ phase = "draft"
    /\ revision = 0
    /\ parentResult = "pending"
    /\ parentRevision = -1
    /\ reviewResults = [r \in Reviewers |-> "pending"]
    /\ reviewRevisions = [r \in Reviewers |-> -1]
    /\ approvals = {}
    /\ implementationPassed = FALSE

CheckParent(result) ==
    /\ phase = "draft"
    /\ parentResult' = result
    /\ parentRevision' = revision
    /\ UNCHANGED <<phase, revision, reviewResults, reviewRevisions,
                    approvals, implementationPassed>>

CheckReviewer(reviewer, result) ==
    /\ phase = "draft"
    /\ reviewResults' = [reviewResults EXCEPT ![reviewer] = result]
    /\ reviewRevisions' = [reviewRevisions EXCEPT ![reviewer] = revision]
    /\ approvals' = approvals \ {reviewer}
    /\ UNCHANGED <<phase, revision, parentResult, parentRevision,
                    implementationPassed>>

Approve(reviewer) ==
    /\ phase = "draft"
    /\ reviewResults[reviewer] = "pass"
    /\ reviewRevisions[reviewer] = revision
    /\ approvals' = approvals \cup {reviewer}
    /\ UNCHANGED <<phase, revision, parentResult, parentRevision,
                    reviewResults, reviewRevisions, implementationPassed>>

CurrentChecks ==
    /\ parentResult = "pass"
    /\ parentRevision = revision
    /\ \A r \in Reviewers :
        /\ reviewResults[r] = "pass"
        /\ reviewRevisions[r] = revision
        /\ r \in approvals

MarkReady ==
    /\ phase = "draft"
    /\ parentResult = "pass"
    /\ parentRevision = revision
    /\ IF EnforceReviewChecks THEN CurrentChecks ELSE TRUE
    /\ phase' = "ready"
    /\ UNCHANGED <<revision, parentResult, parentRevision,
                    reviewResults, reviewRevisions, approvals, implementationPassed>>

Revise ==
    /\ revision < MaxRevision
    /\ phase # "delivered"
    /\ revision' = revision + 1
    /\ phase' = "draft"
    /\ parentResult' = "pending"
    /\ parentRevision' = -1
    /\ reviewResults' = [r \in Reviewers |-> "pending"]
    /\ reviewRevisions' = [r \in Reviewers |-> -1]
    /\ approvals' = {}
    /\ implementationPassed' = FALSE

Implement ==
    /\ phase = "ready"
    /\ ImplementAuthorized
    /\ phase' = "implementing"
    /\ UNCHANGED <<revision, parentResult, parentRevision,
                    reviewResults, reviewRevisions, approvals, implementationPassed>>

Verify(result) ==
    /\ phase = "implementing"
    /\ implementationPassed' = result
    /\ phase' = IF result THEN "verified" ELSE "implementing"
    /\ UNCHANGED <<revision, parentResult, parentRevision,
                    reviewResults, reviewRevisions, approvals>>

Commit ==
    /\ phase = "verified"
    /\ implementationPassed
    /\ phase' = "committed"
    /\ UNCHANGED <<revision, parentResult, parentRevision,
                    reviewResults, reviewRevisions, approvals, implementationPassed>>

Push(result) ==
    /\ phase = "committed"
    /\ phase' = IF result THEN "delivered" ELSE "committed"
    /\ UNCHANGED <<revision, parentResult, parentRevision,
                    reviewResults, reviewRevisions, approvals, implementationPassed>>

Hold ==
    /\ phase \in {"ready", "delivered"}
    /\ UNCHANGED vars

Next ==
    \/ \E result \in Results \ {"pending"} : CheckParent(result)
    \/ \E reviewer \in Reviewers, result \in Results \ {"pending"} :
           CheckReviewer(reviewer, result)
    \/ \E reviewer \in Reviewers : Approve(reviewer)
    \/ MarkReady
    \/ Revise
    \/ Implement
    \/ \E result \in BOOLEAN : Verify(result)
    \/ Commit
    \/ \E result \in BOOLEAN : Push(result)
    \/ Hold

Spec == Init /\ [][Next]_vars
TypeOK ==
    /\ phase \in Phases
    /\ revision \in 0..MaxRevision
    /\ parentResult \in Results
    /\ parentRevision \in -1..MaxRevision
    /\ reviewResults \in [Reviewers -> Results]
    /\ reviewRevisions \in [Reviewers -> -1..MaxRevision]
    /\ approvals \subseteq Reviewers
    /\ implementationPassed \in BOOLEAN
ReadinessSound == phase # "draft" => CurrentChecks
DeliverySound == phase \in {"committed", "delivered"} =>
    (ImplementAuthorized /\ implementationPassed /\ CurrentChecks)
PlanningOnlySafe == ~ImplementAuthorized => phase \in {"draft", "ready"}
NoReadyReached == phase = "draft"
=============================================================================
