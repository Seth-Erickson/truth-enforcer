# TruthEnforcer: Topological Semantic Consistency Engine

**Version:** 0.2.0 (The "Trojan Horse" Release)
**Author:** Seth Erickson / Axion Research
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
🚀 Usage (CLI)
1. Quick Scan (String)

```Bash

python truth_enforcer.py "Gravity is consistent. It binds matter together."
```
2. Deep Scan (File)

```Bash

python truth_enforcer.py -f my_manifesto.txt
```
3. Pipeline Mode (JSON Output)

```Bash

python truth_enforcer.py -f suspicious_bot_output.txt --json
```
🧠 Theory of Operation
Vectorization: We convert sentences into high-dimensional vectors (384-dim) using all-MiniLM-L6-v2.

Dimensional Reduction: We apply Dynamic PCA to reduce noise while preserving local structure.

Topological Homology: We use ripser to calculate the H0 (Connected Components) persistence diagram.

Entropy Calculation: We measure the "lifetimes" of the topological features.

⚠️ Limitations
The "Corporate BS" Paradox: Well-structured corporate jargon often scores as "Solid" because the words are highly correlated in the embedding space.

The "Poet" Problem: Creative writing or high-concept metaphors (Dream Logic) may be flagged as "Unstable" due to rapid context switching.

🛡️ License
This project is released under the Apache 2.0 License. Copyright 2026 Seth Erickson / Axion Research
