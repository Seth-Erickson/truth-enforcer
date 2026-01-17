import json
import random

def generate_calibration_suite(filename="topology_calibration.json"):
    data = []

    # --- 1. THE DENSE CRYSTAL (High Mass / H0) ---
    # Strategy: 40 sentences, dense synonymy. "Solid Rock".
    crystal_terms = ["Thermodynamics", "Heat", "Energy", "Entropy", "Physics", "Kinetic", "Thermal", "Work", "System", "Equilibrium"]
    crystal_templates = [
        "{0} is a fundamental concept in the study of {1}.",
        "The laws of {4} dictate the behavior of {2} and {3}.",
        "In a closed {8}, {3} tends to increase over time.",
        "{6} energy is often defined as the transfer of {2}."
    ]
    crystal_sentences = []
    for _ in range(40): 
        t = random.choice(crystal_templates)
        s = t.format(*[random.choice(crystal_terms) for _ in range(10)]) 
        crystal_sentences.append(s)
    
    data.append({
        "id": "test_case_crystal",
        "type": "HIGH_MASS",
        "text": " ".join(crystal_sentences)
    })

    # --- 2. THE RAZOR LOOP (High Loop / H1) ---
    # Strategy: PURE REPETITION. 4 distinct points.
    # We repeat the EXACT same 4 sentences 10 times. 
    # This creates 4 infinitely dense points arranged in a perfect square.
    loop_cycle = [
        "The market is stable because the demand is high.",  # A -> B
        "The demand is high because the supply is limited.", # B -> C
        "The supply is limited because the prices are fixed.", # C -> D
        "The prices are fixed because the market is stable."   # D -> A
    ]
    loop_text = " ".join(loop_cycle * 10) # 40 sentences total
    
    data.append({
        "id": "test_case_loop",
        "type": "HIGH_LOOP",
        "text": loop_text
    })

    # --- 3. THE HIGH-PRESSURE GAS (Chaos / Low H0) ---
    # Strategy: Maximum Entropy. "The Cloud".
    gas_sentences = []
    chaos_templates = ["The {0} {1} the {2}.", "Why does {0} {1} {2}?"]
    nouns = ["banana", "neutrino", "democracy", "sushi", "algorithm", "cat", "taxes", "Jupiter", "jazz", "cement"]
    verbs = ["eats", "simulates", "votes for", "orbits", "taxes", "compiles", "bakes", "discovers"]
    
    for _ in range(50):
        s = random.choice(chaos_templates).format(
            random.choice(nouns), random.choice(verbs), random.choice(nouns)
        )
        gas_sentences.append(s)

    data.append({
        "id": "test_case_gas",
        "type": "LOW_MASS",
        "text": " ".join(gas_sentences)
    })

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Generated {filename} with Razor-Loop Topology.")

if __name__ == "__main__":
    generate_calibration_suite()
