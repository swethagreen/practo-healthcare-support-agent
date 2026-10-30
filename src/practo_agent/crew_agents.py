# src/practo_agent/crew_agents.py

from crewai import Agent, Crew, Process, Task

from practo_agent.tools import (
    check_appointment_status,
    rag_lookup,
)


import practo_agent.mock_llm


def build_practo_crew():
    llm = practo_agent.mock_llm.MockLLM()

    retrieval_agent = Agent(
        role="Healthcare Policy Retrieval Specialist",
        goal=(
            "Retrieve relevant policy evidence from the "
            "approved healthcare knowledge base."
        ),
        backstory=(
            "You retrieve policy evidence and do not invent "
            "missing policy information."
        ),
        tools=[rag_lookup],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    lookup_agent = Agent(
        role="Appointment Lookup Specialist",
        goal=(
            "Retrieve the requested appointment record and "
            "report its actual status, fee, and escalation score."
        ),
        backstory=(
            "You rely exclusively on the appointment dataset "
            "and never invent appointment details."
        ),
        tools=[check_appointment_status],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    composer_agent = Agent(
        role="Patient Response Composer",
        goal=(
            "Compose a clear, concise response using the "
            "retrieved policy evidence and appointment results."
        ),
        backstory=(
            "You distinguish verified records from policy "
            "evidence and acknowledge missing information."
        ),
        tools=[],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    policy_task = Task(
        description=(
            "Retrieve policy evidence relevant to this request: "
            "{query}. Return the retrieved text and source IDs. "
            "If the question asks about an individual appointment, "
            "do not infer its status from policy documents."
        ),
        expected_output=(
            "Retrieved policy evidence with source document IDs."
        ),
        agent=retrieval_agent,
    )

    lookup_task = Task(
        description=(
            "Inspect the request: {query}. If it contains a "
            "specific appointment record ID, call the appointment "
            "status tool and return its actual result. If no "
            "record ID is present, state that no lookup was made."
        ),
        expected_output=(
            "The actual appointment lookup result, or an explicit "
            "statement that no lookup was required."
        ),
        agent=lookup_agent,
    )

    composition_task = Task(
        description=(
            "Compose a patient-facing draft for: {query}. "
            "Use the outputs from the policy and appointment tasks. "
            "Do not invent records, fees, statuses, or policies. "
            "If the evidence is insufficient, state that clearly."
        ),
        expected_output=(
            "A concise draft grounded in the available evidence."
        ),
        agent=composer_agent,
        context=[policy_task, lookup_task],
    )

    return Crew(
        agents=[
            retrieval_agent,
            lookup_agent,
            composer_agent,
        ],
        tasks=[
            policy_task,
            lookup_task,
            composition_task,
        ],
        process=Process.sequential,
        verbose=True,
        memory=False,
    )