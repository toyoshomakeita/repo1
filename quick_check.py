import numpy as np

class IsingSimulation:
    def __init__(self, L, T):
        self.L, self.T = L, T
        self.spins = np.random.choice([1, -1], size=(L, L))
    def step(self, n):
        for _ in range(n * self.L**2):
            i, j = np.random.randint(0, self.L, 2)
            dE = 2 * self.spins[i, j] * (self.spins[(i+1)%self.L, j] + self.spins[(i-1)%self.L, j] + self.spins[i, (j+1)%self.L] + self.spins[i, (j-1)%self.L])
            if dE <= 0 or np.random.rand() < np.exp(-dE / self.T):
                self.spins[i, j] *= -1

def get_binder(L, T):
    sim = IsingSimulation(L, T)
    for _ in range(500): sim.step(1)
    ms = []
    for _ in range(2000):
        sim.step(1)
        ms.append(np.mean(sim.spins))
    ms = np.array(ms)
    return 1 - np.mean(ms**4) / (3 * np.mean(ms**2)**2)

Tc_theory = 2.269185
print(f"Theory Tc: {Tc_theory:.4f}")
for L in [8, 16]:
    u = get_binder(L, Tc_theory)
    print(f"L={L}, T={Tc_theory:.4f}, Binder U_L={u:.4f}")
