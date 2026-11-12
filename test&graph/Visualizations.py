import matplotlib.pyplot as plt
import numpy as np

# Set clean scientific plotting style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 13})

# Data extracted from Table 5.3
pipelines = [
    'Ground-truth\nAudio', 
    '1.7B Custom\nVoice (Vivian)', 
    '1.7B Voice\nDesign', 
    '1.7B Voice Clone\n(Full Prompt)', 
    '1.7B Voice Clone\n(X-vector Only)', 
    '0.6B Voice\nClone', 
    '1.7B Voice Clone\n(Mandarin)'
]
mos = [4.78, 4.52, 4.41, 4.38, 4.12, 3.96, 4.45]
sim_mos = [4.85, np.nan, np.nan, 4.28, 3.89, 3.75, 4.31]
wer = [1.8, 2.1, 2.6, 2.4, 3.2, 4.1, 2.2]

# -----------------------------------------------------------------------------
# Figure 5.1: Naturalness (MOS) by pipeline
# -----------------------------------------------------------------------------
plt.figure(figsize=(10, 5))
bars = plt.bar(pipelines, mos, color='#2b5c8f', width=0.55, edgecolor='black', alpha=0.9)
plt.ylabel('Mean Opinion Score (MOS)')
plt.title('Figure 5.1: Naturalness (MOS) by Pipeline', pad=15, weight='bold')
plt.ylim(0, 5.5)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f'{yval:.2f}', ha='center', va='bottom', weight='bold')
plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# Figure 5.2: Naturalness (MOS) and speaker similarity (SIM-MOS) for cloning pipelines
# -----------------------------------------------------------------------------
cloning_pipelines = [p for i, p in enumerate(pipelines) if not np.isnan(sim_mos[i])]
c_mos = [mos[i] for i, p in enumerate(pipelines) if not np.isnan(sim_mos[i])]
c_sim_mos = [sim_mos[i] for i, p in enumerate(pipelines) if not np.isnan(sim_mos[i])]

x = np.arange(len(cloning_pipelines))
width = 0.35

plt.figure(figsize=(10, 5))
rects1 = plt.bar(x - width/2, c_mos, width, label='Naturalness (MOS)', color='#348abd', edgecolor='black')
rects2 = plt.bar(x + width/2, c_sim_mos, width, label='Speaker Similarity (SIM-MOS)', color='#e24a33', edgecolor='black')

plt.ylabel('Score (1-5 Scale)')
plt.title('Figure 5.2: Naturalness (MOS) and Speaker Similarity (SIM-MOS) for Cloning Pipelines', pad=15, weight='bold')
plt.xticks(x, cloning_pipelines)
plt.ylim(0, 5.5)
plt.legend(frameon=True, facecolor='white', edgecolor='none')

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., height + 0.1, f'{height:.2f}', ha='center', va='bottom', fontsize=10)

autolabel(rects1)
autolabel(rects2)
plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# Figure 5.3: Word Error Rate by pipeline
# -----------------------------------------------------------------------------
plt.figure(figsize=(10, 5))
bars_wer = plt.bar(pipelines, wer, color='#8e44ad', width=0.55, edgecolor='black', alpha=0.9)
plt.ylabel('Word Error Rate (WER %)')
plt.title('Figure 5.3: Word Error Rate (WER) by Pipeline', pad=15, weight='bold')
plt.ylim(0, 5.0)
for bar in bars_wer:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f'{yval:.1f}%', ha='center', va='bottom', weight='bold')
plt.tight_layout()
plt.show()
