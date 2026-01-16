import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from truth_enforcer import TruthEnforcer

def run_ekg():
    print("🏥 Initializing Semantic EKG (Cumulative Entropy Trace)...")
    lab = TruthEnforcer()
    
    sentences = [
        "Coffee cultivation requires specific climatic conditions.",
        "The beans thrive in high altitudes with distinct wet and dry seasons.",
        "Roasting transforms the chemical structure of the green bean.",
        "Napoleon Bonaparte commanded the artillery during the siege of Toulon.", # THE SPIKE
        "The brewing process extracts these oils into hot water.",
        "Espresso is made by forcing pressurized hot water through the grounds."
    ]
    
    print(f"\n📝 Analyzing {len(sentences)} sentences step-by-step...\n")
    print(f"{'STEP':<5} | {'ENTROPY':<10} | {'DELTA':<10} | {'SENTENCE'}")
    print("-" * 80)

    previous_score = 0
    buffer = ""

    for i, sent in enumerate(sentences):
        buffer += sent + " "
        
        # Need context to start
        if i < 2:
            print(f"{i+1:<5} | {'---':<10} | {'---':<10} | {sent[:40]}...")
            continue
            
        result = lab.scan(buffer)
        current_score = result.get('mass_score', 0)
            
        # Calculate Delta
        delta = current_score - previous_score if i > 2 else 0.0
            
        # Visual Indicator
        tag = ""
        if delta > 0.05: tag = "🔺 SPIKE"
        if delta < -0.05: tag = "⬇️ DROP"
        
        print(f"{i+1:<5} | {current_score:<10.4f} | {delta:<10.4f} | {sent[:30]}... {tag}")
        previous_score = current_score

if __name__ == "__main__":
    run_ekg()
