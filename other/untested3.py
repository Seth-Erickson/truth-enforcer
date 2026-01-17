import json
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from ripser import ripser
from sklearn.decomposition import PCA
import os

# Configure Layout
plt.rcParams.update({'font.size': 8, 'figure.dpi': 150})

def analyze_and_report(json_file="topology_calibration.json"):
    print("🔭 Initializing Topological Analysis & Reporting...")
    
    try:
        with open(json_file, 'r') as f:
            cases = json.load(f)
    except FileNotFoundError:
        print("❌ Error: Calibration file not found.")
        return

    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Storage for the text report
    fingerprint_lines = []
    fingerprint_lines.append("=== TOPOLOGICAL FINGERPRINT REPORT v0.4 ===")
    fingerprint_lines.append(f"Source: {json_file}\n")

    # Setup Figure
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    for i, case in enumerate(cases):
        ax = axes[i]
        title = case['type']
        
        # 1. Embed & Reduce
        sentences = case['text'].replace('?', '.').split('.')
        sentences = [s.strip() for s in sentences if len(s.split()) > 3]
        
        embeddings = model.encode(sentences)
        n_components = min(len(sentences), 15)
        pca = PCA(n_components=n_components)
        reduced = pca.fit_transform(embeddings)

        # 2. Compute Persistence
        result = ripser(reduced, maxdim=1)
        diagrams = result['dgms']
        
        # 3. Extract H0 (Mass/Clusters) Stats
        h0 = diagrams[0]
        h0 = h0[~np.isinf(h0[:,1])]
        h0_lifetimes = h0[:, 1] - h0[:, 0]
        
        h0_max = np.max(h0_lifetimes) if len(h0_lifetimes) > 0 else 0
        h0_mean = np.mean(h0_lifetimes) if len(h0_lifetimes) > 0 else 0
        h0_std = np.std(h0_lifetimes) if len(h0_lifetimes) > 0 else 0
        h0_entropy = np.sum(h0_lifetimes) / len(sentences)

        # 4. Extract H1 (Loops/Holes) Stats
        h1 = diagrams[1]
        h1_loops = []
        if len(h1) > 0:
            h1 = h1[~np.isinf(h1[:,1])]
            h1_loops = h1[:, 1] - h1[:, 0] # Lifetimes of all loops
        
        h1_max = np.max(h1_loops) if len(h1_loops) > 0 else 0
        h1_sum = np.sum(h1_loops) if len(h1_loops) > 0 else 0
        h1_count = np.sum(h1_loops > 0.05) # Count significant loops
        
        # Signal-to-Noise Ratio (Loop Prominence)
        # How much bigger is the biggest loop compared to the average cluster noise?
        snr = h1_max / h0_mean if h0_mean > 0 else 0

        # --- BUILD TEXT REPORT ---
        fingerprint_lines.append(f"--- TEST CASE: {title} ---")
        fingerprint_lines.append(f"Sentences: {len(sentences)}")
        fingerprint_lines.append(f"H0 Mass (Entropy): {h0_entropy:.4f}")
        fingerprint_lines.append(f"H0 Structure: Mean={h0_mean:.4f} | StdDev={h0_std:.4f}")
        fingerprint_lines.append(f"H1 Loop Signal: MaxLife={h1_max:.4f} | TotalSum={h1_sum:.4f}")
        fingerprint_lines.append(f"Significant Loops (>0.05): {h1_count}")
        fingerprint_lines.append(f"Signal-to-Noise Ratio (H1/H0): {snr:.4f}")
        fingerprint_lines.append(f"Status Verdict: {'LOOP DETECTED' if snr > 0.5 or h1_sum > 0.2 else 'PASS'}")
        fingerprint_lines.append("")

        # --- PLOT GRAPHIC ---
        ax.scatter(h0[:,0], h0[:,1], c='blue', s=15, alpha=0.5, label='H0')
        if len(h1) > 0:
            ax.scatter(h1[:,0], h1[:,1], c='red', marker='^', s=80, edgecolors='black', label='H1')
            if h1_max > 0:
                ax.text(0.05, 0.9, f"Max H1: {h1_max:.3f}\nSNR: {snr:.2f}", transform=ax.transAxes, color='red', fontweight='bold')

        ax.plot([0, 2.5], [0, 2.5], 'k--', alpha=0.3)
        ax.set_title(title, fontweight='bold')
        ax.legend(loc='lower right')
        ax.grid(alpha=0.3)

    # Save outputs
    plt.tight_layout()
    plt.savefig("topology_report.png")
    
    with open("topology_fingerprint.txt", "w") as f:
        f.write("\n".join(fingerprint_lines))

    print("📸 Visuals saved to 'topology_report.png'")
    print("📄 Data saved to 'topology_fingerprint.txt'")

if __name__ == "__main__":
    analyze_and_report()
