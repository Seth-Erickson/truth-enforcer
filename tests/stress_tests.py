from truth_enforcer import TruthEnforcer

def test_physics():
    print("🧪 Initializing Semantic Physics Lab...")
    lab = TruthEnforcer()
    
    # Sample A: High Semantic Mass (Factual, grounded)
    truth = "Gravity is a fundamental interaction. It causes mutual attraction between all things with mass. Gravity determines the motion of planets."
    
    # Sample B: Low Semantic Mass (Abstract, high entropy)
    fluff = "Synergy is the interaction of leveraging holistic paradigms. We must circle back to the low hanging fruit to shift the needle."
    
    print(f"\n🔬 Scanning Sample A (Truth)...")
    result_truth = lab.scan(truth)
    print(f"   -> Mass Score: {result_truth['mass_score']} ({result_truth['status']})")
    
    print(f"\n🌫️ Scanning Sample B (Fluff)...")
    result_fluff = lab.scan(fluff)
    print(f"   -> Mass Score: {result_fluff['mass_score']} ({result_fluff['status']})")
    
    # The Pivot: Did the physics hold?
    if result_truth['mass_score'] < result_fluff['mass_score']:
        print("\n✅ SUCCESS: Physics validated. Truth is heavier than Fluff.")
    else:
        print("\n❌ FAILURE: Physics inverted. Check calibration.")

if __name__ == "__main__":
    test_physics()
