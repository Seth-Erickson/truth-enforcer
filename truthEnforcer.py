import numpy as np
import re
import logging
from sentence_transformers import SentenceTransformer
from ripser import ripser
from sklearn.decomposition import PCA
import warnings

# Suppress noise
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)

class TruthEnforcer:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        print("🔌 Powering up TruthEnforcer (Calibrated)...")
        self.model = SentenceTransformer(model_name)
        # CALIBRATED THRESHOLDS based on 2026-01-15 Stress Test
        self.SOLID_THRESHOLD = 0.88  # Anything below this is High Mass (Truth)
        self.FLUID_THRESHOLD = 0.95  # Anything above this is Gaseous (Fluff)

    def _is_code(self, text_chunk: str) -> bool:
        """Heuristic to detect if chunk is code (low semantic density)."""
        code_indicators = ['def ', 'class ', 'import ', '{', '}', 'return ']
        matches = sum(1 for ind in code_indicators if ind in text_chunk)
        return matches >= 2

    def scan(self, text_chunk: str) -> dict:
        """
        Scans text for Semantic Mass.
        Returns permission to proceed (GO/NO-GO).
        """
        # 1. Filter Code
        if self._is_code(text_chunk):
            return {"status": "SKIP", "reason": "Code block detected"}

        # 2. Pre-process (Split by sentence delimiters)
        # Filters out short navigational noise
        raw_splits = re.split(r'[.!?\n]+', text_chunk)
        sentences = [s.strip() for s in raw_splits if len(s.split()) > 4]

        if len(sentences) < 3:
            return {"status": "SKIP", "reason": "Insufficient data"}

        # 3. Physics Calculation (TDA)
        try:
            embeddings = self.model.encode(sentences)
            
            # Dynamic PCA (Prevent Dimensionality Curse)
            n_components = min(len(sentences), 10)
            if n_components > 2:
                pca = PCA(n_components=n_components)
                reduced = pca.fit_transform(embeddings)
            else:
                reduced = embeddings

            diagrams = ripser(reduced, maxdim=1)['dgms']
            
            # H0 Entropy Calculation
            h0 = diagrams[0]
            lifetimes = h0[:, 1] - h0[:, 0]
            lifetimes = lifetimes[~np.isinf(lifetimes)]
            
            # Normalized Entropy
            entropy = np.sum(lifetimes) / len(sentences)

            # 4. The Verdict
            if entropy < self.SOLID_THRESHOLD:
                verdict = "PASS" # High Mass
            elif entropy > self.FLUID_THRESHOLD:
                verdict = "REJECT" # Low Mass (Hallucination risk)
            else:
                verdict = "WARN" # Borderline

            return {
                "status": verdict,
                "mass_score": round(entropy, 4),
                "threshold": self.SOLID_THRESHOLD
            }

        except Exception as e:
            return {"status": "ERROR", "reason": str(e)}
