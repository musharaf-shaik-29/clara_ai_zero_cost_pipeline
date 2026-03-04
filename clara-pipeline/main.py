import os
import shutil
from scripts.extract_demo_data import run_extraction  # pyre-ignore
from scripts.generate_agent_prompt import generate_agent  # pyre-ignore
from scripts.update_agent_config import run_update  # pyre-ignore
from scripts.tracker import create_task  # pyre-ignore

def main():
    print("Starting Clara AI Zero-Cost Pipeline...")

    demo_dir = "data/demo_calls"
    onboarding_dir = "data/onboarding_calls"
    outputs_dir = "outputs/accounts"
    
    # Ensure outputs directory exists, clean it for a fresh run
    if os.path.exists(outputs_dir):
        shutil.rmtree(outputs_dir)
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Process each of the 5 accounts
    for i in range(1, 6):
        account_id = f"account_{i}"
        print(f"\n--- Processing {account_id} ---")
        
        demo_file = os.path.join(demo_dir, f"demo_{i}.txt")
        onboarding_file = os.path.join(onboarding_dir, f"onboarding_{i}.txt")
        
        # Output directories
        account_dir = os.path.join(outputs_dir, account_id)
        v1_dir = os.path.join(account_dir, "v1")
        v2_dir = os.path.join(account_dir, "v2")
        
        # --- Pipeline A (Demo -> Preliminary Agent) ---
        print("[Pipeline A: Demo Call -> Preliminary Agent]")
        if os.path.exists(demo_file):
            v1_memo = run_extraction(demo_file, account_id, v1_dir)
            v1_agent = generate_agent(v1_memo, v1_dir, "v1")
            create_task(account_id, v1_memo, v1_agent, "v1")
        else:
            print(f"❌ Missing demo file: {demo_file}")
            continue

        # --- Pipeline B (Onboarding -> Updated Agent) ---
        print("\n[Pipeline B: Onboarding -> Agent Modification]")
        if os.path.exists(onboarding_file):
            v2_memo = run_update(v1_memo, onboarding_file, v2_dir, account_dir, account_id)
            v2_agent = generate_agent(v2_memo, v2_dir, "v2")
            print(f"Generated Agent Config (v2) -> {v2_agent}")
        else:
            print(f"⚠️ Missing onboarding file for {account_id}, skipping Pipeline B.")

    print("\nPipeline Execution Complete. Artifacts generated in outputs/accounts/")

if __name__ == "__main__":
    main()
