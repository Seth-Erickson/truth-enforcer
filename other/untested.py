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

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)

class TruthEnforcer:
    """
    A Topological Semantic Consistency Engine (v1.0 - Calibrated).
    
    Physics Constants (Derived from Empirical Calibration):
    - SINGULARITY_LIMIT < 0.15:  Indicates excessive repetition (Tautology/Mantra).
    - CHAOS_LIMIT > 0.60:        Indicates high entropy (Hallucination/Gibberish).
    - LOOP_SNR_THRESHOLD > 0.50: Defines a 'True Loop' vs background noise.
    """

    def __init__(self, model_name='all-MiniLM-L6-v2'):
        if "--json" not in sys.argv:
            print("🔌 Powering up TruthEnforcer (v1.0 Calibrated)...", file=sys.stderr)

        self.model = SentenceTransformer(model_name)
        
        # The empirically derived constants
        self.SINGULARITY_LIMIT = 0.15
        self.CHAOS_LIMIT = 0.60
        self.LOOP_SNR_THRESHOLD = 0.50

    def _is_code(self, text_chunk: str) -> bool:
        code_indicators = ['def ', 'class ', 'import ', '{', '}', 'return ']
        matches = sum(1 for ind in code_indicators if ind in text_chunk)
        return matches >= 2

    def scan(self, text_chunk: str) -> dict:
        if self._is_code(text_chunk):
            return {"status": "SKIP", "reason": "Code block detected"}

        raw_splits = re.split(r'[.!?\n]+', text_chunk)
        sentences = [s.strip() for s in raw_splits if len(s.split()) > 3]

        if len(sentences) < 4:
            return {"status": "SKIP", "reason": "Insufficient data"}

        try:
            embeddings = self.model.encode(sentences)

            # PCA: Project to 10D
            n_components = min(len(sentences), 10)
            pca = PCA(n_components=n_components)
            reduced = pca.fit_transform(embeddings)

            # TOPOLOGY
            diagrams = ripser(reduced, maxdim=1)['dgms']

            # --- H0 (Mass/Entropy) ---
            h0 = diagrams[0]
            h0_lifetimes = h0[:, 1] - h0[:, 0]
            h0_lifetimes = h0_lifetimes[~np.isinf(h0_lifetimes)]
            
            # 1. Calculate H0 Mean (The Noise Floor)
            h0_mean = np.mean(h0_lifetimes) if len(h0_lifetimes) > 0 else 0.001
            
            # 2. Calculate Entropy (State of Matter)
            h0_entropy = np.sum(h0_lifetimes) / len(sentences)

            # --- H1 (Loop) ---
            h1 = diagrams[1]
            h1_max_life = 0.0
            if len(h1) > 0:
                h1_lifetimes = h1[:, 1] - h1[:, 0]
                h1_lifetimes = h1_lifetimes[~np.isinf(h1_lifetimes)]
                if len(h1_lifetimes) > 0:
                    h1_max_life = np.max(h1_lifetimes)

            # 3. Calculate Signal-to-Noise Ratio (SNR)
            # How much does the biggest loop stand out above the background clutter?
            snr = h1_max_life / h0_mean if h0_mean > 0 else 0

            # --- VERDICT LOGIC v1.0 ---
            mass_score = round(h0_entropy, 4)
            snr_score = round(snr, 4)
            verdict = "UNKNOWN"

            # Step 1: Check State of Matter
            if mass_score > self.CHAOS_LIMIT:
                verdict = "CHAOS" # Hallucination / Scatter
            elif mass_score < self.SINGULARITY_LIMIT:
                verdict = "SINGULARITY" # Suspiciously dense / Repetitive
                # Singularities are often tautologies, so we check for loops
                if snr > self.LOOP_SNR_THRESHOLD:
                    verdict = "CIRCULAR LOGIC"
            else:
                # Step 2: Solid State (Normal Argument)
                # Check for Logical Fallacies (Loops)
                if snr > self.LOOP_SNR_THRESHOLD:
                    verdict = "LOOP DETECTED"
                else:
                    verdict = "PASS" # Solid, linear, consistent

            return {
                "status": verdict,
                "mass_entropy": mass_score,
                "loop_snr": snr_score,
                "h1_max_life": round(h1_max_life, 4)
            }

        except Exception as e:
            return {"status": "ERROR", "reason": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("text", nargs="?", help="Text string to analyze")
    group.add_argument("-f", "--file", help="Path to text file")
    group.add_argument("-b", "--benchmark", help="Path to JSON benchmark file")
    parser.add_argument("--json", action="store_true", help="Output JSON")

    args = parser.parse_args()
    engine = TruthEnforcer()

    if args.benchmark:
        try:
            with open(args.benchmark, 'r') as f:
                cases = json.load(f)
            print(f"\n🧬 SEMANTIC PHYSICS REPORT (v1.0)")
            print("="*75)
            print(f"{'TYPE':<15} | {'STATUS':<15} | {'ENTROPY':<10} | {'SNR':<10} | {'MAX_H1':<10}")
            print("-" * 75)
            for case in cases:
                res = engine.scan(case['text'])
                print(f"{case['type']:<15} | {res['status']:<15} | {res['mass_entropy']:<10} | {res['loop_snr']:<10} | {res['h1_max_life']:<10}")
            print("="*75 + "\n")
        except FileNotFoundError:
            sys.exit(1)
    else:
        target_text = ""
        if args.file:
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    target_text = f.read()
            except FileNotFoundError:
                sys.exit(1)
        else:
            target_text = args.text
        
        result = engine.scan(target_text)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\n" + "="*40)
            print(f"🧬 SEMANTIC PHYSICS REPORT")
            print("="*40)
            print(f"• Status:        {result.get('status')}")
            print(f"• Entropy:       {result.get('mass_entropy')}")
            print(f"• Loop SNR:      {result.get('loop_snr')}")
            print("="*40 + "\n")
