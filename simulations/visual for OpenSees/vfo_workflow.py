"""
vfo Workflow for OpenSees TCL Output
======================================
Requirements: pip install vfo numpy matplotlib
Does NOT require OpenSeesPy.

Usage:
  1. Run build_odb() once to create the ODB directory from your TCL files.
  2. Run visualise() or animate() any time after that.
  3. For live vfo interactive window: run plot_with_vfo() (requires display).
"""

import os, re, sys, json
import numpy as np
import matplotlib
matplotlib.use('Agg')           # change to 'TkAgg' or 'Qt5Agg' for interactive
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

plt.style.use("MyLaTeXPlotStyle")

# ── Mock openseespy so vfo internal functions load without it ──────────────
import unittest.mock as mock
_mock = mock.MagicMock()
sys.modules.setdefault('openseespy', _mock)
sys.modules.setdefault('openseespy.opensees', _mock)

import vfo.internal_database_functions as idbf

# ── CONFIG — edit these paths ──────────────────────────────────────────────
TCL_NODES_FILE    = "../the conf paper/TCL-Files/model1/soil_nodesByDOF_4DOF.tcl"
TCL_ELEMENTS_FILE = "../the conf paper/TCL-Files/model1/elements_SSPbrickUP.tcl"
RESULTS_DIR       = "../the conf paper/results1"
MODEL_NAME        = "Model1"
LOAD_CASE         = "Geostatic"     # or "Dynamic"
DISP_FILE         = os.path.join(RESULTS_DIR, "gravP_disp.out")
N_REC_NODES       = 32             # nodeRange 1 32 in recorder

# ── 1. PARSE FUNCTIONS ─────────────────────────────────────────────────────

def parse_nodes(filepath):
    nodes = {}
    with open(filepath) as f:
        for line in f:
            m = re.match(r"^\s*node\s+(\d+)\s+([\d.e+-]+)\s+([\d.e+-]+)\s+([\d.e+-]+)", line)
            if m:
                nid = int(m.group(1))
                nodes[nid] = [float(m.group(2)), float(m.group(3)), float(m.group(4))]
    return nodes

def parse_elements(filepath):
    elements = []
    with open(filepath) as f:
        for line in f:
            m = re.match(r"^\s*element\s+SSPbrickUP\s+(\d+)\s+((?:\d+\s+){8})(\d+)", line)
            if m:
                eid  = int(m.group(1))
                nids = [int(x) for x in m.group(2).split()]
                mat  = int(m.group(3))
                elements.append((eid, nids, mat))
    return elements

# ── 2. BUILD ODB ───────────────────────────────────────────────────────────

def build_odb(nodes_tcl=TCL_NODES_FILE, elements_tcl=TCL_ELEMENTS_FILE,
              disp_file=DISP_FILE, n_rec=N_REC_NODES,
              model=MODEL_NAME, loadcase=LOAD_CASE):
    """
    Creates the ODB directory structure that vfo expects:
      ModelName_ODB/
        Nodes.out               — nodeID x y z
        Elements_8Node.out      — eleID n1..n8
        EleClassTags.out        — eleID classTag
        LoadCase/
          NodeDisp_All.out      — time + (nNodes×3) displacements
    """
    nodes    = parse_nodes(nodes_tcl)
    elements = parse_elements(elements_tcl)
    n_total  = len(nodes)

    ODB   = f"{model}_ODB"
    LC    = os.path.join(ODB, loadcase)
    os.makedirs(ODB, exist_ok=True)
    os.makedirs(LC,  exist_ok=True)

    # Nodes.out
    with open(os.path.join(ODB, 'Nodes.out'), 'w') as f:
        for nid in sorted(nodes.keys()):
            x, y, z = nodes[nid]
            f.write(f"{nid} {x} {y} {z}\n")

    # Elements_8Node.out
    with open(os.path.join(ODB, 'Elements_8Node.out'), 'w') as f:
        for eid, nids, _ in elements:
            f.write(f"{eid} " + " ".join(map(str, nids)) + "\n")

    # EleClassTags.out  (19 = BrickUP / 8-node brick in vfo)
    with open(os.path.join(ODB, 'EleClassTags.out'), 'w') as f:
        for eid, _, _ in elements:
            f.write(f"{eid} 19\n")

    # NodeDisp_All.out — pad unrecorded nodes with zeros
    raw = np.loadtxt(disp_file)
    time_arr = raw[:, 0]
    n_steps  = len(time_arr)
    disp_rec = raw[:, 1:].reshape(n_steps, n_rec, 3)

    disp_all = np.zeros((n_steps, n_total, 3))
    disp_all[:, :n_rec, :] = disp_rec
    disp_flat = disp_all.reshape(n_steps, n_total * 3)
    np.savetxt(os.path.join(LC, 'NodeDisp_All.out'),
               np.column_stack([time_arr, disp_flat]), fmt='%.6e')

    # Dummy files vfo may look for
    for fname in ['NodeReaction.out', 'EleForce.out']:
        np.savetxt(os.path.join(LC, fname),
                   np.column_stack([time_arr, np.zeros((n_steps, 1))]), fmt='%.6e')

    print(f"ODB built at {ODB}/")
    return nodes, elements

# ── 3. VISUALISE ───────────────────────────────────────────────────────────

MAT_COLORS = {1:'#a0c8ff',2:'#70aaff',3:'#4488ee',4:'#2266cc',
              5:'#ffdd55',6:'#ff8822',7:'#cc4400',10:'#44cc88'}
MAT_LABELS = {1:'Frozen 1',2:'Frozen 2',3:'Frozen 3',4:'Frozen 4',
              5:'Sand Dr=40%',6:'Sand Dr=60%',7:'Sand Dr=85%',10:'Unfrozen'}

def _hex_faces(nids, id2idx):
    n = [id2idx[nid] for nid in nids]
    return [[n[0],n[1],n[2],n[3]], [n[4],n[5],n[6],n[7]],
            [n[0],n[1],n[5],n[4]], [n[2],n[3],n[7],n[6]],
            [n[0],n[3],n[7],n[4]], [n[1],n[2],n[6],n[5]]]

def plot_deformed(nodes, elements, disp_arr, timeSteps,
                  t_idx=-1, scale=200.0, save_path=None):
    nodes_arr, _, _ = idbf._readNodesandElements(MODEL_NAME)
    id2idx = {int(r[0]): i for i, r in enumerate(nodes_arr)}
    coords = nodes_arr[:, 1:] + disp_arr[t_idx] * scale

    xs, ys, zs = coords[:,0], coords[:,1], coords[:,2]
    x_range = (xs.max()+2) - (xs.min()-1)
    y_range = (ys.max()+2) - (ys.min()-1)
    z_range = (zs.max()+2) - (zs.min()-2)

    # Auto-size the figure to match model proportions (Z is ~8x taller than XY)
    # Use the true aspect but cap height so it stays on screen
    fig_w = 10.0
    aspect_ratio = z_range / max(x_range, y_range)   # ~8 for this model
    fig_h = min(fig_w * aspect_ratio * 0.55, 22.0)   # 0.55 accounts for 3D perspective foreshortening
    fig = plt.figure(figsize=(fig_w, fig_h))
    fig.patch.set_facecolor('#0d0e12')

    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#13151c')

    # Expand axes to use most of the figure canvas
    ax.set_position([0.05, 0.02, 0.90, 0.96])

    drawn = set()
    for eid, nids, mat in elements:
        faces = [[coords[i] for i in f] for f in _hex_faces(nids, id2idx)]
        col = MAT_COLORS.get(mat, '#888')
        pc = Poly3DCollection(faces, alpha=0.22, linewidth=0.35)
        pc.set_facecolor(col); pc.set_edgecolor('#3a4055')
        ax.add_collection3d(pc)
        if mat not in drawn:
            ax.plot([], [], [], 's', color=col, ms=8,
                    label=MAT_LABELS.get(mat, f'mat {mat}'))
            drawn.add(mat)

    ax.set_xlim(xs.min()-1, xs.max()+2)
    ax.set_ylim(ys.min()-1, ys.max()+2)
    ax.set_zlim(zs.min()-2, zs.max()+2)
    ax.set_box_aspect([x_range, y_range, z_range])   # true proportions — unchanged

    for attr, lbl in [('set_xlabel','X (m)'),('set_ylabel','Y (m)'),('set_zlabel','Z (m)')]:
        getattr(ax, attr)(lbl, color='#aaa', fontsize=8)
    ax.tick_params(colors='#777', labelsize=6)
    ax.legend(fontsize=7, labelcolor='#ccc', facecolor='#1a1d26',
              edgecolor='#333', loc='lower left')
    ax.set_title(f't = {timeSteps[t_idx]:.1f} s   (disp x{scale:.0f})',
                 color='white', fontsize=9)
    ax.view_init(elev=18, azim=-50)

    if save_path:
        plt.savefig(save_path, dpi=250, bbox_inches='tight', facecolor='#0d0e12')
        print(f"Figure saved: {save_path}")
    return fig, ax

def animate_deformed(nodes, elements, disp_arr, timeSteps,
                     scale=200.0, n_frames=30, save_path='animation.gif'):
    nodes_arr, _, _ = idbf._readNodesandElements(MODEL_NAME)
    id2idx  = {int(r[0]): i for i, r in enumerate(nodes_arr)}
    base_c  = nodes_arr[:, 1:]
    fidx    = np.linspace(0, len(timeSteps)-1, n_frames, dtype=int)

    xs0 = base_c[:,0]; ys0 = base_c[:,1]; zs0 = base_c[:,2]
    x_range = (xs0.max()+2) - (xs0.min()-1)
    y_range = (ys0.max()+2) - (ys0.min()-1)
    z_range = (zs0.max()+2) - (zs0.min()-2)

    fig_w = 10.0
    aspect_ratio = z_range / max(x_range, y_range)
    fig_h = min(fig_w * aspect_ratio * 0.55, 22.0)
    fig = plt.figure(figsize=(fig_w, fig_h))
    fig.patch.set_facecolor('#0d0e12')

    ax = fig.add_subplot(111, projection='3d')

    def update(fi):
        ax.clear(); ax.set_facecolor('#13151c')
        ax.set_position([0.05, 0.02, 0.90, 0.96])
        coords = base_c + disp_arr[fidx[fi]] * scale
        drawn = set()
        for eid, nids, mat in elements:
            faces = [[coords[i] for i in f] for f in _hex_faces(nids, id2idx)]
            col = MAT_COLORS.get(mat, '#888')
            pc = Poly3DCollection(faces, alpha=0.22, linewidth=0.35)
            pc.set_facecolor(col); pc.set_edgecolor('#3a4055')
            ax.add_collection3d(pc)
            if mat not in drawn:
                ax.plot([], [], [], 's', color=col, ms=7,
                        label=MAT_LABELS.get(mat, f'mat {mat}'))
                drawn.add(mat)
        xs = coords[:,0]; ys = coords[:,1]; zs = coords[:,2]
        ax.set_xlim(xs.min()-1, xs.max()+2)
        ax.set_ylim(ys.min()-1, ys.max()+2)
        ax.set_zlim(zs.min()-2, zs.max()+2)
        ax.set_box_aspect([x_range, y_range, z_range])
        ax.set_xlabel('X (m)', color='#aaa', fontsize=7)
        ax.set_ylabel('Y (m)', color='#aaa', fontsize=7)
        ax.set_zlabel('Z (m)', color='#aaa', fontsize=7)
        ax.tick_params(colors='#777', labelsize=6)
        ax.set_title(f't = {timeSteps[fidx[fi]]:.1f} s  (x{scale:.0f})',
                     color='white', fontsize=9)
        ax.legend(fontsize=6, labelcolor='#ccc', facecolor='#1a1d26',
                  edgecolor='#333', loc='lower left')
        ax.view_init(elev=18, azim=-50)

    ani = animation.FuncAnimation(fig, update, frames=n_frames, interval=150)
    ani.save(save_path, writer='pillow', fps=6, dpi=150)
    plt.close()
    print(f"Animation saved: {save_path}")
    return ani

# ── MAIN ───────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # Step 1: Build ODB (do this once)
    nodes, elements = build_odb()

    # Step 2: Read ODB with vfo
    _, disp_arr, _ = idbf._readNodeDispData(MODEL_NAME, LOAD_CASE)
    nodes_arr, _, _ = idbf._readNodesandElements(MODEL_NAME)
    raw = np.loadtxt(DISP_FILE)
    timeSteps = raw[:, 0]

    # Step 3: Visualise
    plot_deformed(nodes, elements, disp_arr, timeSteps,
                  t_idx=-1, scale=200, save_path='deformed_final.png')
    animate_deformed(nodes, elements, disp_arr, timeSteps,
                     scale=200, n_frames=10, save_path='geostatic_animation.gif')
    print("Done.")