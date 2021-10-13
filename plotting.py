from simmu_final import*
import matplotlib.pyplot as plt

plt.scatter(cycle, mem, color = 'k')

plt.xlabel('Cycle')
plt.ylabel('Address')
plt.title("Memory address vs Cycle")
plt.legend()
plt.show()