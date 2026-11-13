------------------------------ MODULE Recovery ------------------------------
EXTENDS Integers, TLC

CONSTANTS MaxRevision, EnforceRecord, EnforceGreenGate
Checks == {"tests", "verification"}
Results == {"notrun", "pass", "fail", "blocked"}
VARIABLES phase, revision, results, checkedRevision, open, history, logged, repairReady
vars == <<phase, revision, results, checkedRevision, open, history, logged, repairReady>>

Init ==
    /\ phase = "working"
    /\ revision = 0
    /\ results = [c \in Checks |-> "notrun"]
    /\ checkedRevision = [c \in Checks |-> -1]
    /\ open = {}
    /\ history = {}
    /\ logged = [c \in Checks |-> FALSE]
    /\ repairReady = [c \in Checks |-> FALSE]

Run(check, result) ==
    /\ phase \in {"working", "verified"}
    /\ check \notin open \/ repairReady[check]
    /\ phase' = "working"
    /\ results' = [results EXCEPT ![check] = result]
    /\ checkedRevision' = [checkedRevision EXCEPT ![check] = revision]
    /\ open' = IF result = "pass" THEN open \ {check} ELSE open \cup {check}
    /\ history' = IF result # "pass" /\ EnforceRecord
                  THEN history \cup {check} ELSE history
    /\ logged' = [logged EXCEPT ![check] = IF result = "pass" THEN TRUE ELSE EnforceRecord]
    /\ repairReady' = [repairReady EXCEPT ![check] = FALSE]
    /\ UNCHANGED revision

Repair(check) ==
    /\ phase = "working"
    /\ check \in open
    /\ repairReady' = [repairReady EXCEPT ![check] = TRUE]
    /\ UNCHANGED <<phase, revision, results, checkedRevision, open, history, logged>>

AllGreen == \A c \in Checks : results[c] = "pass" /\ checkedRevision[c] = revision

Complete ==
    /\ phase = "working"
    /\ IF EnforceGreenGate THEN AllGreen /\ open = {} ELSE history # {}
    /\ phase' = "verified"
    /\ UNCHANGED <<revision, results, checkedRevision, open, history, logged, repairReady>>

Invalidate ==
    /\ revision < MaxRevision
    /\ revision' = revision + 1
    /\ phase' = "working"
    /\ results' = [c \in Checks |-> "notrun"]
    /\ checkedRevision' = [c \in Checks |-> -1]
    /\ repairReady' = [c \in Checks |-> FALSE]
    /\ UNCHANGED <<open, history, logged>>

Hold == phase = "verified" /\ UNCHANGED vars
Next ==
    \/ \E check \in Checks, result \in Results \ {"notrun"} : Run(check, result)
    \/ \E check \in Checks : Repair(check)
    \/ Complete
    \/ Invalidate
    \/ Hold

Spec == Init /\ [][Next]_vars
TypeOK ==
    /\ phase \in {"working", "verified"}
    /\ revision \in 0..MaxRevision
    /\ results \in [Checks -> Results]
    /\ checkedRevision \in [Checks -> -1..MaxRevision]
    /\ open \subseteq Checks
    /\ history \subseteq Checks
    /\ logged \in [Checks -> BOOLEAN]
    /\ repairReady \in [Checks -> BOOLEAN]
IssueRecorded == \A c \in open : logged[c] /\ c \in history
CompletesOnlyGreen == phase = "verified" => AllGreen /\ open = {}
HistoryPreserved == [][history \subseteq history']_vars
NoRecoveredCompletion == ~(phase = "verified" /\ history # {})
=============================================================================
