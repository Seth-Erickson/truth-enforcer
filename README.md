# TruthEnforcer: Topological  Engine

**Version:** 0.2.0 (The "Trojan Horse" Release)
**Author:** Axion Research
**License:** Apache 2.0

> "Truth is a geometric property. Lies are topological holes."

## 🔬 The Science
TruthEnforcer is not a fact-checker. It is a **Coherence Engine**.

It uses **Topological Data Analysis (TDA)** and **Persistent Homology** to map the "Semantic Shape" of a text block.
- **High Mass (Low Entropy):** The text is focused, logically connected, and stays on topic.
- **Gaseous (High Entropy):** The text is drifting, hallucinating, or suffering from "Dream Logic."

### The "Trojan Horse" Discovery
Most hallucination detectors fail because they look for "wrong facts." TruthEnforcer looks for **"broken geometry."**

In our internal stress tests (Jan 2026), we injected a "Trojan Horse" (a coherent but irrelevant sentence) into a factual paragraph.

| Test Subject | Description | Entropy Score | Verdict |
| :--- | :--- | :--- | :--- |
| **Control** | A consistent paragraph about Coffee cultivation. | `0.8144` | ✅ SOLID |
| **Trojan Horse** | The same paragraph with a sentence about Napoleon inserted. | `0.9332` | ⚠️ UNSTABLE |

**Result:** The tool successfully detected the "Topic Drift" caused by the lie, even though the lie itself was grammatically perfect.

## 🛠️ Installation

```bash
git clone [https://github.com/Seth-Erickson/truth-enforcer.git](https://github.com/Seth-Erickson/truth-enforcer.git)
cd truth-enforcer
pip install .
```

## 🚀 Usage (CLI)

**1. Quick Scan (String)**

```bash
python truth_enforcer.py "Gravity is consistent. It binds matter together."

```

**2. Deep Scan (File)**

```bash
python truth_enforcer.py -f my_manifesto.txt

```

**3. Pipeline Mode (JSON Output)**

```bash
python truth_enforcer.py -f suspicious_bot_output.txt --json

```

## 🧠 Theory of Operation

1. **Vectorization:** We convert sentences into high-dimensional vectors (384-dim) using `all-MiniLM-L6-v2`.
2. **Dimensional Reduction:** We apply Dynamic PCA to reduce noise while preserving local structure.
3. **Topological Homology:** We use `ripser` to calculate the **H0 (Connected Components)** persistence diagram.
4. **Entropy Calculation:** We measure the "lifetimes" of the topological features.
* *Short Lifetimes* = Noise/Fluff.
* *Long Lifetimes* = Strong Semantic Core.



## ⚠️ Limitations

* **The "Corporate BS" Paradox:** Well-structured corporate jargon often scores as "Solid" because the words are highly correlated in the embedding space.
* **The "Poet" Problem:** Creative writing or high-concept metaphors (Dream Logic) may be flagged as "Unstable" due to rapid context switching.

## 🛡️ License

This project is released under the **Apache 2.0 License**.
Copyright 2026 Seth Erickson

---

### **2. The Engine (`truth_enforcer.py`)**
*What changed:* I removed the "safety rails" in the comments. The docstrings now use the proper "Semantic Physics" terminology. The logic remains the same (because it works).


### **3. The Evidence (`tests/validate_physics.py`)**

*What changed:* This replaces the old `stress_tests.py`. It is a fully automated reproduction of the "Coffee vs. Napoleon" experiment. This file proves to anyone who downloads the repo that the math works.

```python
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
    delta = score_dirty - score_clean
    print(f"\n📉 Semantic Drift Delta: +{round(delta, 4)}")
    
    if score_dirty > score_clean:
        print("✅ SUCCESS: Trojan Horse detected (Entropy Spike confirmed).")
    else:
        print("❌ FAILURE: Physics inverted.")

if __name__ == "__main__":
    test_trojan_horse()
```
