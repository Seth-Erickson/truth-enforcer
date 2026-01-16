import sys
import os

# Add parent directory to path so we can import the engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from truth_enforcer import TruthEnforcer

def test_trojan_horse():
    """
    Validates the 'Ethos Circuit Breaker' logic.
    Injects a semantic outlier (Napoleon) into a consistent cluster (Coffee).
    """
    print("🧪 Initializing Physics Engine...")
    lab = TruthEnforcer()
    
    # Sample A: Consistent Logic
    clean_text = (
        "Coffee cultivation requires specific climatic conditions. "
        "The beans thrive in high altitudes with distinct wet and dry seasons. "
        "Roasting transforms the chemical structure of the green bean. "
        "The brewing process extracts these oils into hot water."
    )
    
    # Sample B: The Trojan Horse
    dirty_text = (
        "Coffee cultivation requires specific climatic conditions. "
        "The beans thrive in high altitudes with distinct wet and dry seasons. "
        "Napoleon Bonaparte commanded the artillery during the siege of Toulon. " # <--- THE LIE
        "Roasting transforms the chemical structure of the green bean. "
        "The brewing process extracts these oils into hot water."
    )
    
    print(f"\n☕ Scanning Clean Sample...")
    score_clean = lab.scan(clean_text)['mass_score']
    print(f"   -> Entropy: {score_clean}")
    
    print(f"\n🐴 Scanning Trojan Horse Sample...")
    score_dirty = lab.scan(dirty_text)['mass_score']
    print(f"   -> Entropy: {score_dirty}")
    
    # Validation Logic
    if score_dirty > score_clean:
        print("✅ SUCCESS: Trojan Horse detected (Entropy Spike confirmed).")
    else:
        print("❌ FAILURE: Physics inverted.")

if __name__ == "__main__":
    test_trojan_horse()
