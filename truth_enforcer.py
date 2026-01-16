import numpy as np
import re
import logging
import argparse
import sys
import json
import warnings
from sentence_transformers import SentenceTransformer
from ripser import ripser
from sklearn.decomposition import PCA

# Suppress infrastructure noise
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)

class TruthEnforcer:
    """
    A Topological Semantic Consistency Engine.
    
    Uses Persistent Homology (H0) to calculate the 'Semantic Mass' of a text block.
    High Entropy = Semantic Drift / Hallucination.
    Low Entropy = High Focus / Logical Consistency.
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # Only print loading message if NOT piping to JSON
        if "--json" not in sys.argv:
            print("🔌 Powering up TruthEnforcer (Calibrated)...", file=sys.stderr)
            
        self.model = SentenceTransformer(model_name)
        
        # CALIBRATED THRESHOLDS (Jan 2026 Stress Tests)
        self.SOLID_THRESHOLD = 0.88  # The "Coffee" Baseline
        self.FLUID_THRESHOLD = 0.95  # The "Napoleon" Danger Zone

    def _is_code(self, text_chunk: str) -> bool:
        """Filters out code blocks."""
        code_indicators = ['def ', 'class ', 'import ', '{', '}', 'return ']
        matches = sum(1 for ind in code_indicators if ind in text_chunk)
        return matches >= 2

    def scan(self, text_chunk: str) -> dict:
        """Scans text for Semantic Mass."""
        # 1. Filter Code
        if self._is_code(text_chunk):
            return {"status": "SKIP", "reason": "Code block detected"}

        # 2. Pre-process
        raw_splits = re.split(r'[.!?\n]+', text_chunk)
        sentences = [s.strip() for s in raw_splits if len(s.split()) > 4]

        if len(sentences) < 3:
            return {"status": "SKIP", "reason": "Insufficient data"}

        # 3. Physics Calculation (TDA)
        try:
            embeddings = self.model.encode(sentences)
            
            n_components = min(len(sentences), 10)
            if n_components > 2:
                pca = PCA(n_components=n_components)
                reduced = pca.fit_transform(embeddings)
            else:
                reduced = embeddings

            diagrams = ripser(reduced, maxdim=1)['dgms']
            h0 = diagrams[0]
            
            lifetimes = h0[:, 1] - h0[:, 0]
            lifetimes = lifetimes[~np.isinf(lifetimes)]
            entropy = np.sum(lifetimes) / len(sentences)

            # 4. The Verdict Logic
            mass_score = round(entropy, 4)
            
            # CHECK 1: The "Broken Record" Filter
            if mass_score == 0.0:
                verdict = "COLLAPSE"
            # CHECK 2: Standard Physics
            elif mass_score < self.SOLID_THRESHOLD:
                verdict = "PASS"
            elif mass_score > self.FLUID_THRESHOLD:
                verdict = "REJECT"
            else:
                verdict = "WARN"

            return {
                "status": verdict,
                "mass_score": mass_score,
                "threshold": self.SOLID_THRESHOLD
            }

        except Exception as e:
            return {"status": "ERROR", "reason": str(e)}

# --- CLI IMPLEMENTATION ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TruthEnforcer CLI")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("text", nargs="?", help="Text string to analyze")
    group.add_argument("-f", "--file", help="Path to text file")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()

    # Ingest
    target_text = ""
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                target_text = f.read()
        except FileNotFoundError:
            print(f"❌ Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    else:
        target_text = args.text

    # Execute
    try:
        engine = TruthEnforcer()
        result = engine.scan(target_text)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\n" + "="*40)
            print(f"🧬 SEMANTIC PHYSICS REPORT")
            print("="*40)
            print(f"• Status:      {result.get('status', 'UNKNOWN')}")
            print(f"• Mass Score:  {result.get('mass_score', 0.0)}")
            print("-" * 40)
            
            status = result.get('status')
            if status == 'PASS':
                print("✅ VERDICT: SOLID (High Semantic Density)")
            elif status == 'COLLAPSE':
                print("🛑 VERDICT: MODEL COLLAPSE (Repetition Loop)")
            elif status == 'REJECT':
                print("🌫️ VERDICT: GASEOUS (Hallucination/Drift Detected)")
            else:
                print("⚠️ VERDICT: UNSTABLE (Borderline Topology)")
            print("="*40 + "\n")

    except KeyboardInterrupt:
        sys.exit(0)
