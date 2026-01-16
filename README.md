# TruthEnforcer: Topological Semantic Consistency Engine

**Version:** 0.2.0 (The "Trojan Horse" Release)
**Author:** Seth Erickson
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
pip install .    print(f"   -> Entropy: {score_dirty}")
    
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
