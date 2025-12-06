import matplotlib.pyplot as plt
import numpy as np

# Create figure
fig, axes = plt.subplots(1, 2, figsize=(12, 5), facecolor="white")

# --- Panel 1: MSA snippet ---
msa_sequences = [
    "MKTAYIAKQRQISFVKSH",
    "MKTAYIAK-RQISFVKS-",
    "MKT-YIAKQRQISFVKSH",
    "MKTAYIAKQRQ--VKSHP",
    "MKTAYIAKQ-QISFVKSH"
]
conserved_positions = [0, 1, 2, 3, 4, 5, 8, 12]

for i, seq in enumerate(msa_sequences):
    for j, aa in enumerate(seq):
        if j in conserved_positions and aa != "-":
            axes[0].text(j, -i, aa, color="red", fontweight="bold", fontsize=11, ha="center", va="center")
        else:
            axes[0].text(j, -i, aa, color="black", fontsize=10, ha="center", va="center")

axes[0].set_xlim(-0.5, len(msa_sequences[0]))
axes[0].set_ylim(-len(msa_sequences), 1)
axes[0].set_title("Multiple Sequence Alignment (MSA)", fontsize=13, fontweight="bold")
axes[0].axis("off")

# --- Panel 2: Contact map ---
n_residues = 18
contact_map = np.random.rand(n_residues, n_residues)
contact_map = (contact_map + contact_map.T) / 2
im = axes[1].imshow(contact_map, cmap="viridis", origin="lower")
axes[1].set_title("Residue–Residue Contact Map", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Residue index")
axes[1].set_ylabel("Residue index")

# Add colorbar
cbar = plt.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)
cbar.set_label("Co-evolution score", fontsize=10)

plt.tight_layout()
plt.savefig("feature_generation.png", dpi=300)  # Saves the figure
plt.show()