import matplotlib.pyplot as plt
# Data extracted from Section 5.7
latency_modes = ['Cold Request (No Cache)', 'Warm Request (Prompt Cached)']
latency_values = [5.42, 3.74] # in seconds

# -----------------------------------------------------------------------------
# Figure 5.6: Cloning latency with and without a cached prompt
# -----------------------------------------------------------------------------
plt.figure(figsize=(7, 5))
bars_lat = plt.bar(latency_modes, latency_values, color=['#7f8c8d', '#2980b9'], width=0.4, edgecolor='black', alpha=0.9)
plt.ylabel('Generation Latency (seconds)')
plt.title('Figure 5.6: Cloning Latency Structural Impact of Prompt Caching', pad=15, weight='bold')
plt.ylim(0, 6.5)

# Illustrate the 1.68s delta reduction explicitly on the plot
plt.annotate('', xy=(1, 3.74), xytext=(1, 5.42),
             arrowprops=dict(arrowstyle="<->", color='#c0392b', lw=2))
plt.text(1.1, 4.58, '-1.68 s\n(31% Saved)', color='#c0392b', weight='bold', va='center')

for bar in bars_lat:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f'{yval:.2f} s', ha='center', va='bottom', weight='bold')

plt.tight_layout()
plt.show()
