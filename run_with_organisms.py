import json
"""
AI-Librarian with Agent-Farm Organisms
"""

# Load organism configuration
config_path = Path(__file__).parent / "agent_farm_organisms.json"
with open(config_path) as f:
    organisms = json.load(f)

print("✓ Loaded evolved organisms from Agent-Farm")
print(f"  Version: {organisms['version']}")
print(f"  Deployed: {organisms['deployment_date']}")
print()
print("Active organisms:")
for role, data in organisms['agents'].items():
    if data:
        print(f"  - {role}: {data['organism_id']} (fitness={data['fitness']:.3f})")

# Run AI-Librarian with organism intelligence
print("\n🚀 Starting AI-Librarian with evolved organism intelligence...")
