
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
    A Topological Semantic Consistency Engine (v0.3.0 - H1 Enabled).

    H0 (Mass): Measures Semantic Consistency (Clumping).
H1 (Loop): Measures Circular Logic (Holes).
    """

    def __init__(self, model_name='all-MiniLM-L6-v2', adaptive_thresholds=False,
                 top_k_h0_ratio=3, h0_std_threshold=0.06, mass_rich_threshold=0.8,
                 h1_threshold=0.05): # Adjusted thresholds
        if "--json" not in sys.argv:
            print("🔌 Powering up TruthEnforcer (v0.3.0 H1-Ready)...", file=sys.stderr)

        self.model = SentenceTransformer(model_name)

        # Thresholds
        self.SOLID_THRESHOLD = 0.88
        self.FLUID_THRESHOLD = 0.95

        # New Adaptive Threshold Parameters
        self.adaptive_thresholds = adaptive_thresholds
        self.top_k_h0_ratio = top_k_h0_ratio
        self.h0_std_threshold = h0_std_threshold
        self.mass_rich_threshold = mass_rich_threshold
        self.h1_threshold = h1_threshold

    def _is_code(self, text_chunk: str) -> bool:
        code_indicators = ['def ', 'class ', 'import ', '{', '}', 'return ']
        matches = sum(1 for ind in code_indicators if ind in text_chunk)
        return matches >= 2

    def scan(self, text_chunk: str) -> dict:
        if self._is_code(text_chunk):
            return {"status": "SKIP", "reason": "Code block detected"}

        raw_splits = re.split(r'[.!?\n]+', text_chunk)
        sentences = [s.strip() for s in raw_splits if len(s.split()) > 4]

        if len(sentences) < 3:
            return {"status": "FRAGMENTED", "reason": "Insufficient meaningful sentences for topological analysis"}

        try:
            embeddings = self.model.encode(sentences)

            # Dynamic PCA
            n_components = min(len(sentences), 10)
            if n_components > 2:
                pca = PCA(n_components=n_components)
                reduced = pca.fit_transform(embeddings)
            else:
                reduced = embeddings

            # CALCULATE TOPOLOGY (H0 and H1)
            # maxdim=1 means we calculate H0 (clusters) AND H1 (loops)
            diagrams = ripser(reduced, maxdim=1)['dgms']

            # --- H0 ANALYSIS (Consistency) ---
            h0 = diagrams[0]
            h0_lifetimes = h0[:, 1] - h0[:, 0]
            h0_lifetimes = h0_lifetimes[~np.isinf(h0_lifetimes)]
            h0_entropy = np.sum(h0_lifetimes) / len(sentences)

            # New H0 metrics
            h0_std = 0.0
            h0_top_k_ratio = 0.0
            if len(h0_lifetimes) > 0:
                h0_std = np.std(h0_lifetimes)
                sorted_h0_lifetimes = np.sort(h0_lifetimes)[::-1] # Sort descending
                if len(sorted_h0_lifetimes) >= self.top_k_h0_ratio:
                    h0_top_k_ratio = np.sum(sorted_h0_lifetimes[:self.top_k_h0_ratio]) / np.sum(sorted_h0_lifetimes)
                elif len(sorted_h0_lifetimes) > 0: # If fewer lifetimes than k, sum all available
                    h0_top_k_ratio = np.sum(sorted_h0_lifetimes) / np.sum(sorted_h0_lifetimes) if np.sum(sorted_h0_lifetimes) > 0 else 0.0

            # --- H1 ANALYSIS (Circularity) ---
            h1 = diagrams[1] # The loops
            h1_lifetimes = np.array([])
            h1_score = 0.0
            h1_count = 0
            h1_avg_lifetime = 0.0

            if len(h1) > 0:
                h1_lifetimes = h1[:, 1] - h1[:, 0]
                h1_lifetimes = h1_lifetimes[~np.isinf(h1_lifetimes)]
                h1_score = np.sum(h1_lifetimes) # Total "Loopiness"
                h1_count = len(h1_lifetimes) # New: H1 count
                if h1_count > 0:
                    h1_avg_lifetime = np.mean(h1_lifetimes) # New: H1 average lifetime

            # --- VERDICT ---
            mass_score = round(h0_entropy, 4)
            loop_score = round(h1_score, 4)

            verdict = "UNKNOWN"

            if self.adaptive_thresholds:
                if mass_score == 0.0: verdict = "COLLAPSE"
                elif loop_score > self.h1_threshold: verdict = "LOOP DETECTED" # Use new h1_threshold
                elif mass_score < self.SOLID_THRESHOLD: verdict = "PASS"
                elif mass_score > self.FLUID_THRESHOLD and h0_std < self.h0_std_threshold and h0_top_k_ratio > self.mass_rich_threshold:
                    verdict = "RICH" # High mass but structured (low std, high top-k ratio)
                elif mass_score > self.FLUID_THRESHOLD: verdict = "REJECT"
                elif mass_score >= self.SOLID_THRESHOLD and mass_score <= self.FLUID_THRESHOLD:
                    if h0_std > self.h0_std_threshold or h0_top_k_ratio < self.mass_rich_threshold: # Example: more fluid if high std or low top-k
                        verdict = "AMBIGUOUS" # Borderline mass, mixed H0 structure signals
                    else:
                        verdict = "WARN" # Default warning for borderline mass
                else: verdict = "WARN"
            else: # Original verdict logic
                if mass_score == 0.0: verdict = "COLLAPSE"
                elif mass_score < self.SOLID_THRESHOLD: verdict = "PASS"
                elif mass_score > self.FLUID_THRESHOLD: verdict = "REJECT"
                else: verdict = "WARN"

                # If we detect a significant loop, flag it
                if loop_score > self.h1_threshold: # Use new h1_threshold
                    verdict = "LOOP DETECTED"


            return {
                "status": verdict,
                "mass_score": mass_score,    # Consistency
                "loop_score": loop_score,    # Circularity
                "h0_std": round(h0_std, 4),    # Std Dev of H0 lifetimes
                "h0_top_k_ratio": round(h0_top_k_ratio, 4), # Ratio of top K H0 lifetimes
                "h1_count": h1_count, # New: H1 cycles count
                "h1_avg_lifetime": round(h1_avg_lifetime, 4), # New: H1 average lifetime
                "threshold": self.SOLID_THRESHOLD
            }

        except Exception as e:
            return {"status": "ERROR", "reason": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TruthEnforcer CLI")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("text", nargs="?", help="Text string to analyze")
    group.add_argument("-f", "--file", help="Path to text file")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--adaptive_thresholds", action="store_true", help="Enable adaptive thresholds and refined H0 analysis")
    parser.add_argument("--top_k_h0_ratio", type=int, default=3, help="Number of top H0 lifetimes for ratio calculation (adaptive mode)")
    parser.add_argument("--h0_std_threshold", type=float, default=0.06, help="Threshold for H0 standard deviation (adaptive mode)")
    parser.add_argument("--mass_rich_threshold", type=float, default=0.8, help="Threshold for mass richness (adaptive mode)")
    parser.add_argument("--h1_threshold", type=float, default=0.05, help="Threshold for H1 loop detection") # New: h1_threshold arg

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
        engine = TruthEnforcer(adaptive_thresholds=args.adaptive_thresholds,
                               top_k_h0_ratio=args.top_k_h0_ratio,
                               h0_std_threshold=args.h0_std_threshold,
                               mass_rich_threshold=args.mass_rich_threshold,
                               h1_threshold=args.h1_threshold) # New: pass h1_threshold
        result = engine.scan(target_text)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\n" + "="*40)
            print(f"🧬 SEMANTIC PHYSICS REPORT (v0.3 - Adaptive: {args.adaptive_thresholds})")
            print("="*40)
            print(f"• Status:        {result.get('status', 'UNKNOWN')}")
            print(f"• Mass (H0):     {result.get('mass_score', 0.0)}")
            print(f"• Loop (H1):     {result.get('loop_score', 0.0)}")
            if args.adaptive_thresholds:
                print(f"• H0 Std Dev:    {result.get('h0_std', 0.0)}")
                print(f"• H0 Top K Ratio: {result.get('h0_top_k_ratio', 0.0)}")
                print(f"• H1 Count:      {result.get('h1_count', 0)}") # New: display H1 count
                print(f"• H1 Avg Life:   {result.get('h1_avg_lifetime', 0.0)}") # New: display H1 avg lifetime
            print("-" * 40)
            print("="*40 + "\n")

    except KeyboardInterrupt:
        sys.exit(0)
