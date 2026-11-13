---------------------------- MODULE MrDraft ----------------------------
EXTENDS Naturals, FiniteSets
CONSTANT MislabelEvidence
VARIABLES phase, baseKnown, hasChanges, evidence, dirty, result, topics
vars == <<phase, baseKnown, hasChanges, evidence, dirty, result, topics>>
Evidence == {"current-pass", "stale-pass", "failed", "absent"}
Topics == {"problem", "fix", "blast-radius", "verified-tested"}
Init == /\ phase = "scope"
        /\ baseKnown \in BOOLEAN
        /\ hasChanges \in BOOLEAN
        /\ evidence \in Evidence
        /\ dirty \in BOOLEAN
        /\ result = "none"
        /\ topics = {}
Resolve == /\ phase = "scope"
           /\ phase' = IF ~baseKnown THEN "blocked"
                        ELSE IF ~hasChanges THEN "empty" ELSE "inspect"
           /\ UNCHANGED <<baseKnown, hasChanges, evidence, dirty, result, topics>>
Draft == /\ phase = "inspect"
         /\ phase' = "draft"
         /\ result' = IF MislabelEvidence \/ evidence = "current-pass" THEN "passed"
                       ELSE IF evidence = "failed" THEN "failed" ELSE "unverified"
         /\ topics' = Topics
         /\ UNCHANGED <<baseKnown, hasChanges, evidence, dirty>>
NewRequest == /\ phase \in {"blocked", "empty", "draft"}
              /\ Init'
Hold == /\ phase \in {"blocked", "empty", "draft"}
        /\ UNCHANGED vars
Next == Resolve \/ Draft \/ NewRequest \/ Hold
Spec == Init /\ [][Next]_vars
TypeOK == /\ phase \in {"scope", "blocked", "empty", "inspect", "draft"}
          /\ baseKnown \in BOOLEAN /\ hasChanges \in BOOLEAN /\ dirty \in BOOLEAN
          /\ evidence \in Evidence /\ result \in {"none", "passed", "failed", "unverified"}
          /\ topics \subseteq Topics
ScopeSound == /\ (phase \in {"inspect", "draft"} => baseKnown /\ hasChanges)
              /\ (phase = "blocked" => ~baseKnown)
              /\ (phase = "empty" => baseKnown /\ ~hasChanges)
EvidenceSound == phase = "draft" => ((result = "passed") <=> (evidence = "current-pass"))
UnknownExplicit == phase = "draft" =>
    /\ (evidence = "failed" => result = "failed")
    /\ (evidence \in {"stale-pass", "absent"} => result = "unverified")
FourTopics == phase = "draft" => topics = Topics
NoDraft == phase # "draft"
=============================================================================
