import json

import practo_agent.crew_agents
import practo_agent.tools


def main():
    crew = practo_agent.crew_agents.build_practo_crew()

    # Sample 1: Policy question
    policy_query = (
        "What is the consultation fee for Cardiology?"
    )

    print("\n=== POLICY QUESTION ===")
    policy_result = crew.kickoff(
        inputs={"query": policy_query}
    )
    print(policy_result)

    # Sample 2: Appointment lookup
    appointment = practo_agent.tools.lookup_appointment("APT0001")

    if not appointment["found"]:
        raise RuntimeError(
            "Expected sample appointment was not found."
        )

    appointment_query = (
        "Check appointment APT0001 and report its status."
    )

    print("\n=== APPOINTMENT QUESTION ===")
    appointment_result = crew.kickoff(
        inputs={"query": appointment_query}
    )
    print(appointment_result)

    print("\n=== VERIFIED LOOKUP RESULT ===")
    print(json.dumps(appointment, indent=2))


if __name__ == "__main__":
    main()