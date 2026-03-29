import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os

# ── Model catalogue ────────────────────────────────────────────────────────────
# dz format: loose / medDense / dense  (all in metres)
MODELS = {
    1:  dict(dz_loose=0.50, dz_med=0.50, dz_dense=0.50, nodes=804,  label='M1  0.5/0.5/0.5'),
    # 2:  dict(dz_loose=0.50, dz_med=1.00, dz_dense=1.50, nodes=492,  label='M2  0.5/1.0/1.5'),
    # 3:  dict(dz_loose=1.00, dz_med=2.00, dz_dense=2.40, nodes=260,  label='M3  1.0/2.0/2.4'),
    # 4:  dict(dz_loose=1.00, dz_med=2.50, dz_dense=4.00, nodes=224,  label='M4  1.0/2.5/4.0'),
    # 5:  dict(dz_loose=1.00, dz_med=3.00, dz_dense=4.00, nodes=216,  label='M5  1.0/3.0/4.0'),
    # 6:  dict(dz_loose=2.00, dz_med=3.00, dz_dense=4.00, nodes=156,  label='M6  2.0/3.0/4.0'),
    # 7:  dict(dz_loose=2.50, dz_med=3.33, dz_dense=4.00, nodes=140,  label='M7  2.5/3.3/4.0'),
    # 8:  dict(dz_loose=5.00, dz_med=6.00, dz_dense=6.00, nodes=88,   label='M8  5.0/6.0/6.0'),
    # 9:  dict(dz_loose=0.50, dz_med=0.50, dz_dense=1.00, nodes=644,  label='M9  0.5/0.5/1.0'),
    10: dict(dz_loose=1.0, dz_med=1.0, dz_dense=6.0, nodes=284,  label='M10 1.0/1.0/6.0'),
} 

# node id → (column index for X-accel, depth, description)
NODE_COL = {
    6:  (1,   0.0,  'Surface'),
    19: (4,  -4.0,  'Active/Loose interface (-4 m)'),
    23: (7,  -34.0, 'Structure toe (-34 m)  ★'),
}

# ── Colours ────────────────────────────────────────────────────────────────────
_tab = cm.get_cmap('tab10')
COLORS = {mid: _tab(i) for i, mid in enumerate(sorted(MODELS))}
COLORS[1] = 'black'    # finest reference — always black

# ── Load available results ─────────────────────────────────────────────────────
datasets = {}
for mid in MODELS:
    path = f"results/results{mid}/accelRigidBaseSPConf.out"
    if os.path.exists(path):
        try:
            datasets[mid] = np.loadtxt(path)
            print(f"  loaded model {mid:2d}  ({datasets[mid].shape[0]} steps)")
        except Exception as e:
            print(f"  [WARN] model {mid}: {e}")
    else:
        print(f"  [skip] model {mid} — file not found")

if not datasets:
    raise RuntimeError("No result files found.")

dt = np.diff(next(iter(datasets.values()))[:, 0]).mean()
print(f"\nRecording dt = {dt:.4f} s\n")

# ── Response spectrum (Newmark average-acceleration, 5 % damping) ──────────────
def response_spectrum(accel, dt, periods, zeta=0.05):
    """Return pseudo-spectral acceleration Sa [m/s²] for each period."""
    gam, bet = 0.5, 0.25
    Sa = np.empty(len(periods))
    for i, T in enumerate(periods):
        if T < 2 * dt:
            Sa[i] = np.max(np.abs(accel))
            continue
        w = 2 * np.pi / T
        c, k = 2 * zeta * w, w ** 2
        keff = k + gam / (bet * dt) * c + 1.0 / (bet * dt ** 2)
        u = v = 0.0
        a = -accel[0]
        max_u = 0.0
        for ag in accel[1:]:
            peff = (-ag
                    + u / (bet * dt ** 2) + v / (bet * dt) + (0.5 / bet - 1.0) * a
                    + c * (gam / (bet * dt) * u + (gam / bet - 1.0) * v
                           + dt * (gam / (2 * bet) - 1.0) * a))
            u_n = peff / keff
            a_n = (u_n - u) / (bet * dt ** 2) - v / (bet * dt) - (0.5 / bet - 1.0) * a
            v   = v + dt * ((1 - gam) * a + gam * a_n)
            u, a = u_n, a_n
            if abs(u) > max_u:
                max_u = abs(u)
        Sa[i] = k * max_u
    return Sa

periods = np.logspace(-2, 0.7, 80)   # 0.01 s → 5 s

# ── Compute metrics for every loaded model ─────────────────────────────────────
print("Computing response spectra (this takes a moment)...")
results = {}
for mid, data in datasets.items():
    row = {}
    for nid, (col, depth, desc) in NODE_COL.items():
        sig = data[:, col]
        row[f'pga_{nid}'] = np.max(np.abs(sig))
        row[f'sa_{nid}']  = response_spectrum(sig, dt, periods)
    results[mid] = row
    print(f"  done model {mid}")

# ── Figures 1a/1b/1c — Response spectra per node ──────────────────────────────
# Convergence = all curves overlap. No reference model needed.
for nid, (col, depth, desc) in NODE_COL.items():
    fig, ax = plt.subplots(figsize=(10, 6))
    for mid, row in sorted(results.items()):
        ax.plot(periods, row[f'sa_{nid}'],
                color=COLORS[mid], lw=2.0 if mid == 1 else 1.2,
                label=MODELS[mid]['label'], alpha=0.85)
    ax.set_xscale('log')
    ax.set_xlabel('Period  T  (s)', fontsize=12)
    ax.set_ylabel('Sa  (m/s²)  —  5 % damping', fontsize=12)
    ax.set_title(f'Response spectra — node {nid}  ({desc})\n'
                 'Convergence = all curves overlap', fontsize=12, fontweight='bold')
    ax.legend(fontsize=8, loc='upper right')
    ax.grid(True, which='both', alpha=0.3)
    fig.tight_layout()

# ── Figure 2 — Engineering convergence: metrics vs number of nodes ─────────────
# How to read: moving left→right (coarse→fine), curve flattens = converged.
# The leftmost model where the curve is already flat = your optimal mesh.
mids_sorted  = sorted(results.keys())
node_counts  = np.array([MODELS[m]['nodes'] for m in mids_sorted])

idx02 = np.argmin(np.abs(periods - 0.2))
idx10 = np.argmin(np.abs(periods - 1.0))

# 3 rows (nodes 6, 19, 23)  ×  2 cols (PGA, Sa at representative period)
fig2, axes = plt.subplots(3, 2, figsize=(13, 12))
fig2.suptitle('Engineering convergence metrics vs number of nodes\n'
              'Curve flattens = converged  |  No reference model needed',
              fontsize=12, fontweight='bold')

def conv_plot(ax, values, ylabel, title):
    colors_s = [COLORS[m] for m in mids_sorted]
    ax.scatter(node_counts, values, c=colors_s, s=70, zorder=5)
    ax.plot(node_counts, values, 'k--', lw=0.8, alpha=0.4)
    for nc, v, mid in zip(node_counts, values, mids_sorted):
        ax.annotate(f'M{mid}', (nc, v), textcoords='offset points',
                    xytext=(5, 4), fontsize=8)
    ax.set_xlabel('Number of nodes', fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_title(title, fontsize=10)
    ax.grid(True, alpha=0.3)

for row_idx, (nid, (col, depth, desc)) in enumerate(NODE_COL.items()):
    conv_plot(axes[row_idx, 0],
              [results[m][f'pga_{nid}'] for m in mids_sorted],
              'PGA  (m/s²)',
              f'PGA — node {nid}  ({desc})')
    conv_plot(axes[row_idx, 1],
              [results[m][f'sa_{nid}'][idx02] for m in mids_sorted],
              'Sa  (m/s²)',
              f'Sa(T≈{periods[idx02]:.2f}s) — node {nid}  ({desc})')

fig2.tight_layout()
plt.show()
