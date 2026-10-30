# practo-healthcare-support-agent
Final Capstone — Practo Domain Support Agent (CrewAI)
## Task 4: Grounded Generation and Calibration

Embedding model: sentence-transformers/all-MiniLM-L6-v2

Distance metric: Cosine distance

Similarity conversion:
similarity = 1 - cosine_distance

Calibration queries:
- Five in-scope policy queries
- Three deliberately out-of-scope queries

### Fixed-size chunking

- Maximum out-of-scope similarity: [0.06138235330581665]
- Minimum in-scope similarity: [ 0.6114689111709595]
- Selected threshold: [0.33642563223838806]
- Calibration passed: [true]

### Sentence-based chunking

- Maximum out-of-scope similarity: [0.06463193893432617]
- Minimum in-scope similarity: [0.6204134821891785]
- Selected threshold: [0.3425227105617523]
- Calibration passed: [true]

Thresholds are derived from measured score ranges,
not selected from an arbitrary preset.

## Task 5: Chunking Evaluation

Both strategies were evaluated using the same five
in-scope queries, the same embedding model, and top-k = 5.

| Strategy | Mean Precision | Mean Recall |
|---|---:|---:|
| Fixed-size with overlap | 0.25666666666666665 | 1.0 |
| Sentence-based | 0.24666666666666667 |  1.0 |

Per-query results and retrieved document IDs are
available in evaluation/reports/.

### Recommendation

[I would deploy the fixed-size with overlap chunking strategy because it achieved a mean precision of 0.257 and a mean recall of 1.00, compared with 0.247 precision and 1.00 recall for sentence-based chunking. Both strategies retrieved all expected relevant policy documents, but fixed-size chunking achieved slightly higher precision, meaning it returned fewer irrelevant results while maintaining perfect recall in this evaluation. I would validate these results using additional unseen queries before deploying the selected strategy in production.]

## Task 6:

Testing started.
Records evaluated: 50
Escalation threshold: 0.7
Records flagged: 9
Flagged percentage: 18.00%
Days-since-created 80th percentile: 24
None


{'response': 'Your appointment is scheduled.', 'intent': 'appointment_lookup', 'status': 'Scheduled', 'consultation_fee_inr': 1200, 'escalation_score': 0.2, 'escalation_recommended': False, 'grounded': True, 'refused': False, 'evidence': []}
{'response': 'Your appointment is scheduled.', 'intent': 'appointment_lookup', 'status': 'Scheduled', 'consultation_fee_inr': 1200, 'escalation_score': 0.2, 'escalation_recommended': False, 'grounded': True, 'refused': False, 'evidence': []}


 LangChainDeprecationWarning: The class `InMemoryChatMessageHistory` was deprecated in LangChain 1.6.4 and will be removed in 2.0.0 See the short-term memory documentation for recommended alternatives: https://docs.langchain.com/oss/python/langchain/short-term-memory
  InMemoryChatMessageHistory()
You said: I am asking about Cardiology.
Your earlier message was: I am asking about Cardiology.

=== Fresh Session B ===
You said: What specialty did I mention?





Testing started.
Records evaluated: 50
Escalation threshold: 0.7
Records flagged: 9
Flagged percentage: 18.00%
Days-since-created 80th percentile: 24
None

=== POLICY QUESTION ===
╭───────────────────────────────────── 🚀 Crew Execution Started ─────────────────────────────────────╮
│                                                                                                     │
│  Crew Execution Started                                                                             │
│  Name: crew                                                                                         │
│  ID: 9b47b5c0-846f-488b-a41f-ccdc66674d13                                                           │
│                                                                                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────────────────── 📋 Task Started ──────────────────────────────────────────╮
│                                                                                                     │
│  Task Started                                                                                       │
│  Name: Retrieve policy evidence relevant to this request: What is the consultation fee for          │
│  Cardiology?. Return the retrieved text and source IDs. If the question asks about an individual    │
│  appointment, do not infer its status from policy documents.                                        │
│  ID: cd356a38-17fe-4804-8732-e634881f1a18                                                           │
│                                                                                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭───────────────────────────────────────── 🤖 Agent Started ──────────────────────────────────────────╮
│                                                                                                     │
│  Agent: Healthcare Policy Retrieval Specialist                                                      │
│                                                                                                     │
│  Task: Retrieve policy evidence relevant to this request: What is the consultation fee for          │
│  Cardiology?. Return the retrieved text and source IDs. If the question asks about an individual    │
│  appointment, do not infer its status from policy documents.                                        │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

Using an approximate input token count for model 'practo-deterministic-mock': assuming one token per four characters because a native token count is unavailable.
[Finalize] todos_count=0, todos_with_results=0
╭─────────────────────────────────────── ✅ Agent Final Answer ───────────────────────────────────────╮
│                                                                                                     │
│  Agent: Healthcare Policy Retrieval Specialist                                                      │
│                                                                                                     │
│  Final Answer:                                                                                      │
│  Deterministic mock response. No external language model was called.                                │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────────────── 📋 Task Completion ─────────────────────────────────────────╮
│                                                                                                     │
│  Task Completed                                                                                     │
│  Name: Retrieve policy evidence relevant to this request: What is the consultation fee for          │
│  Cardiology?. Return the retrieved text and source IDs. If the question asks about an individual    │
│  appointment, do not infer its status from policy documents.                                        │
│  Agent: Healthcare Policy Retrieval Specialist                                                      │
│                                                                                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────────────────── 📋 Task Started ──────────────────────────────────────────╮
│                                                                                                     │
│  Task Started                                                                                       │
│  Name: Inspect the request: What is the consultation fee for Cardiology?. If it contains a          │
│  specific appointment record ID, call the appointment status tool and return its actual result. If  │
│  no record ID is present, state that no lookup was made.                                            │
│  ID: dc54c6d4-b80c-42e6-b70f-c72b96258669                                                           │
│                                                                                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭───────────────────────────────────────── 🤖 Agent Started ──────────────────────────────────────────╮
│                                                                                                     │
│  Agent: Appointment Lookup Specialist                                                               │
│                                                                                                     │
│  Task: Inspect the request: What is the consultation fee for Cardiology?. If it contains a          │
│  specific appointment record ID, call the appointment status tool and return its actual result. If  │
│  no record ID is present, state that no lookup was made.                                            │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

Using an approximate input token count for model 'practo-deterministic-mock': assuming one token per four characters because a native token count is unavailable.
[Finalize] todos_count=0, todos_with_results=0
╭─────────────────────────────────────── ✅ Agent Final Answer ───────────────────────────────────────╮
│                                                                                                     │
│  Agent: Appointment Lookup Specialist                                                               │
│                                                                                                     │
│  Final Answer:                                                                                      │
│  Deterministic mock response. No external language model was called.                                │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────────────── 📋 Task Completion ─────────────────────────────────────────╮
│                                                                                                     │
│  Task Completed                                                                                     │
│  Name: Inspect the request: What is the consultation fee for Cardiology?. If it contains a          │
│  specific appointment record ID, call the appointment status tool and return its actual result. If  │
│  no record ID is present, state that no lookup was made.                                            │
│  Agent: Appointment Lookup Specialist                                                               │
│                                                                                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────────────────── 📋 Task Started ──────────────────────────────────────────╮
│                                                                                                     │
│  Task Started                                                                                       │
│  Name: Compose a patient-facing draft for: What is the consultation fee for Cardiology?. Use the    │
│  outputs from the policy and appointment tasks. Do not invent records, fees, statuses, or           │
│  policies. If the evidence is insufficient, state that clearly.                                     │
│  ID: 52c46053-5ae8-48e8-bdc0-20242160f479                                                           │
│                                                                                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭───────────────────────────────────────── 🤖 Agent Started ──────────────────────────────────────────╮
│                                                                                                     │
│  Agent: Patient Response Composer                                                                   │
│                                                                                                     │
│  Task: Compose a patient-facing draft for: What is the consultation fee for Cardiology?. Use the    │
│  outputs from the policy and appointment tasks. Do not invent records, fees, statuses, or           │
│  policies. If the evidence is insufficient, state that clearly.                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

Using an approximate input token count for model 'practo-deterministic-mock': assuming one token per four characters because a native token count is unavailable.
[Finalize] todos_count=0, todos_with_results=0
╭─────────────────────────────────────── ✅ Agent Final Answer ───────────────────────────────────────╮
│                                                                                                     │
│  Agent: Patient Response Composer                                                                   │
│                                                                                                     │
│  Final Answer:                                                                                      │
│  Deterministic mock response. No external language model was called.                                │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────────────── 📋 Task Completion ─────────────────────────────────────────╮
│                                                                                                     │
│  Task Completed                                                                                     │
│  Name: Compose a patient-facing draft for: What is the consultation fee for Cardiology?. Use the    │
│  outputs from the policy and appointment tasks. Do not invent records, fees, statuses, or           │
│  policies. If the evidence is insufficient, state that clearly.                                     │
│  Agent: Patient Response Composer                                                                   │
│                                                                                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────────────────── Crew Completion ──────────────────────────────────────────╮
│                                                                                                     │
│  Crew Execution Completed                                                                           │
│  Name: crew                                                                                         │
│  ID: 9b47b5c0-846f-488b-a41f-ccdc66674d13                                                           │
│  Final Output: Deterministic mock response. No external language model was called.                  │
│                                                                                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯



╭───────────────────────────────────────── Execution Traces ──────────────────────────────────────────╮
│                                                                                                     │
│  🔍 Detailed execution traces are available!                                                        │
│                                                                                                     │
│  View insights including:                                                                           │
│    • Agent decision-making process                                                                  │
│    • Task execution flow and timing                                                                 │
│    • Tool usage details                                                                             │
│                                                                                                     │
│  These traces are stored locally and may contain prompts, inputs, and outputs. Sharing uploads      │
│  them to CrewAI.                                                                                    │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
Share this execution trace with CrewAI? [y/N] (20s timeout): Deterministic mock response. No external language model was called.

=== APPOINTMENT QUESTION ===
╭───────────────────────────────────── 🚀 Crew Execution Started ─────────────────────────────────────╮
│                                                                                                     │
│  Crew Execution Started                                                                             │
│  Name: crew                                                                                         │
│  ID: 9b47b5c0-846f-488b-a41f-ccdc66674d13                                                           │
│                                                                                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────────────────── 📋 Task Started ──────────────────────────────────────────╮
│                                                                                                     │
│  Task Started                                                                                       │
│  Name: Retrieve policy evidence relevant to this request: Check appointment APT0001 and report its  │
│  status.. Return the retrieved text and source IDs. If the question asks about an individual        │
│  appointment, do not infer its status from policy documents.                                        │
│  ID: cd356a38-17fe-4804-8732-e634881f1a18                                                           │
│                                                                                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭───────────────────────────────────────── 🤖 Agent Started ──────────────────────────────────────────╮
│                                                                                                     │
│  Agent: Healthcare Policy Retrieval Specialist                                                      │
│                                                                                                     │
│  Task: Retrieve policy evidence relevant to this request: Check appointment APT0001 and report its  │
│  status.. Return the retrieved text and source IDs. If the question asks about an individual        │
│  appointment, do not infer its status from policy documents.                                        │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

Using an approximate input token count for model 'practo-deterministic-mock': assuming one token per four characters because a native token count is unavailable.
[Finalize] todos_count=0, todos_with_results=0
╭─────────────────────────────────────── ✅ Agent Final Answer ───────────────────────────────────────╮
│                                                                                                     │
│  Agent: Healthcare Policy Retrieval Specialist                                                      │
│                                                                                                     │
│  Final Answer:                                                                                      │
│  Deterministic mock response. No external language model was called.                                │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────────────── 📋 Task Completion ─────────────────────────────────────────╮
│                                                                                                     │
│  Task Completed                                                                                     │
│  Name: Retrieve policy evidence relevant to this request: Check appointment APT0001 and report its  │
│  status.. Return the retrieved text and source IDs. If the question asks about an individual        │
│  appointment, do not infer its status from policy documents.                                        │
│  Agent: Healthcare Policy Retrieval Specialist                                                      │
│                                                                                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────────────────── 📋 Task Started ──────────────────────────────────────────╮
│                                                                                                     │
│  Task Started                                                                                       │
│  Name: Inspect the request: Check appointment APT0001 and report its status.. If it contains a      │
│  specific appointment record ID, call the appointment status tool and return its actual result. If  │
│  no record ID is present, state that no lookup was made.                                            │
│  ID: dc54c6d4-b80c-42e6-b70f-c72b96258669                                                           │
│                                                                                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭───────────────────────────────────────── 🤖 Agent Started ──────────────────────────────────────────╮
│                                                                                                     │
│  Agent: Appointment Lookup Specialist                                                               │
│                                                                                                     │
│  Task: Inspect the request: Check appointment APT0001 and report its status.. If it contains a      │
│  specific appointment record ID, call the appointment status tool and return its actual result. If  │
│  no record ID is present, state that no lookup was made.                                            │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

Using an approximate input token count for model 'practo-deterministic-mock': assuming one token per four characters because a native token count is unavailable.
[Finalize] todos_count=0, todos_with_results=0
╭─────────────────────────────────────── ✅ Agent Final Answer ───────────────────────────────────────╮
│                                                                                                     │
│  Agent: Appointment Lookup Specialist                                                               │
│                                                                                                     │
│  Final Answer:                                                                                      │
│  Deterministic mock response. No external language model was called.                                │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────────────── 📋 Task Completion ─────────────────────────────────────────╮
│                                                                                                     │
│  Task Completed                                                                                     │
│  Name: Inspect the request: Check appointment APT0001 and report its status.. If it contains a      │
│  specific appointment record ID, call the appointment status tool and return its actual result. If  │
│  no record ID is present, state that no lookup was made.                                            │
│  Agent: Appointment Lookup Specialist                                                               │
│                                                                                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────────────────── 📋 Task Started ──────────────────────────────────────────╮
│                                                                                                     │
│  Task Started                                                                                       │
│  Name: Compose a patient-facing draft for: Check appointment APT0001 and report its status.. Use    │
│  the outputs from the policy and appointment tasks. Do not invent records, fees, statuses, or       │
│  policies. If the evidence is insufficient, state that clearly.                                     │
│  ID: 52c46053-5ae8-48e8-bdc0-20242160f479                                                           │
│                                                                                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭───────────────────────────────────────── 🤖 Agent Started ──────────────────────────────────────────╮
│                                                                                                     │
│  Agent: Patient Response Composer                                                                   │
│                                                                                                     │
│  Task: Compose a patient-facing draft for: Check appointment APT0001 and report its status.. Use    │
│  the outputs from the policy and appointment tasks. Do not invent records, fees, statuses, or       │
│  policies. If the evidence is insufficient, state that clearly.                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

Using an approximate input token count for model 'practo-deterministic-mock': assuming one token per four characters because a native token count is unavailable.
[Finalize] todos_count=0, todos_with_results=0
╭─────────────────────────────────────── ✅ Agent Final Answer ───────────────────────────────────────╮
│                                                                                                     │
│  Agent: Patient Response Composer                                                                   │
│                                                                                                     │
│  Final Answer:                                                                                      │
│  Deterministic mock response. No external language model was called.                                │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────────────── 📋 Task Completion ─────────────────────────────────────────╮
│                                                                                                     │
│  Task Completed                                                                                     │
│  Name: Compose a patient-facing draft for: Check appointment APT0001 and report its status.. Use    │
│  the outputs from the policy and appointment tasks. Do not invent records, fees, statuses, or       │
│  policies. If the evidence is insufficient, state that clearly.                                     │
│  Agent: Patient Response Composer                                                                   │
│                                                                                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────────────────── Crew Completion ──────────────────────────────────────────╮
│                                                                                                     │
│  Crew Execution Completed                                                                           │
│  Name: crew                                                                                         │
│  ID: 9b47b5c0-846f-488b-a41f-ccdc66674d13                                                           │
│  Final Output: Deterministic mock response. No external language model was called.                  │
│                                                                                                     │
│                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯

Deterministic mock response. No external language model was called.

=== VERIFIED LOOKUP RESULT ===
{
  "found": true,
  "record_id": "APT0001",
  "category": "Pediatrics",
  "status": "Scheduled",
  "consultation_fee_inr": 1063,
  "days_since_created": 7,
  "follow_up_required": false,
  "escalation_score": 0.0933,
  "escalation_recommended": false
}



(.venv) PS C:\practo-healthcare-support-agent> & c:\practo-healthcare-support-agent\.venv\Scripts\python.exe c:/practo-healthcare-support-agent/tests/validate_policy_response.py
{'response': 'Your appointment is scheduled.', 'intent': 'appointment_lookup', 'status': 'Scheduled', 'consultation_fee_inr': 1200, 'escalation_score': 0.2, 'escalation_recommended': False, 'grounded': True, 'refused': False, 'evidence': []}