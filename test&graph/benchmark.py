import matplotlib.pyplot as plt

# Data extracted from Table 5.4
platforms = [
    'RTX 4090\n(1.7B, bf16)', 
    'RTX 3060\n(1.7B, bf16)', 
    'Apple M2 Pro\n(1.7B, fp16)', 
    'RTX 3060\n(0.6B, bf16)', 
    'Intel i7-13700H\n(0.6B, fp32)'
]
rtf = [0.38, 0.65, 0.79, 0.26, 1.24]
memory = [4.8, 4.8, 5.2, 2.1, 3.4] # in GB

# -----------------------------------------------------------------------------
# Figure 5.4: Real-Time Factor by platform
# -----------------------------------------------------------------------------
plt.figure(figsize=(10, 5))
colors_rtf = ['#27ae60' if r < 1.0 else '#c0392b' for r in rtf]
bars_rtf = plt.bar(platforms, rtf, color=colors_rtf, width=0.5, edgecolor='black', alpha=0.85)
plt.axhline(y=1.0, color='grey', linestyle='--', linewidth=1.2, label='Real-time Threshold (RTF = 1.0)')
plt.ylabel('Real-Time Factor (RTF)')
plt.title('Figure 5.4: Real-Time Factor by Platform (Lower is Faster)', pad=15, weight='bold')
plt.ylim(0, 1.5)
plt.legend(frameon=True, loc='upper left')

for bar in bars_rtf:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.03, f'{yval:.2f}', ha='center', va='bottom', weight='bold')
plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# Figure 5.5: Peak memory use by platform
# -----------------------------------------------------------------------------
plt.figure(figsize=(10, 5))
bars_mem = plt.bar(platforms, memory, color='#d35400', width=0.5, edgecolor='black', alpha=0.85)
plt.ylabel('Peak Memory Consumption (GB)')
plt.title('Figure 5.5: Peak Memory Use by Platform', pad=15, weight='bold')
plt.ylim(0, 6.5)

for bar in bars_mem:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f'{yval:.1f} GB', ha='center', va='bottom', weight='bold')
plt.tight_layout()
plt.show()
