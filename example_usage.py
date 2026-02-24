from system_state_tracker import AutonomousSystem
import json

# Example usage
if __name__ == "__main__":
    # Create the autonomous system instance
    system = AutonomousSystem()
    
    print("Initial state:")
    print(system)
    
    # Step 1: Analyze request
    print("\nStep 1: Analyzing user request...")
    system = system.set_current_goal("Analyze user's instructions").plan_next_actions(
        "Parse request structure",
        "Identify key objectives",
        "Determine required actions"
    ).update_state(action_taken="Analyze user request")
    
    print("State after analysis:")
    print(system)
    
    # Step 2: Plan response
    print("\nStep 2: Planning response...")
    system = system.set_current_goal("Develop response strategy").plan_next_actions(
        "Generate response structure",
        "Create detailed plan",
        "Verify alignment with goals"
    ).update_state(action_taken="Plan response")
    
    print("State after planning:")
    print(system)
