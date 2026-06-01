# 2次元イジング模型：最終報告書

このノートブックは、イジング模型のシミュレーションと理論の比較をまとめたものです。

## 1. モンテカルロ法の実装


```python
import numpy as np
import matplotlib.pyplot as plt

class IsingSimulation:
    def __init__(self, L, T):
        self.L, self.T = L, T
        self.spins = np.random.choice([1, -1], size=(L, L))
    
    def step(self):
        L = self.L
        for _ in range(L*L):
            i, j = np.random.randint(0, L, 2)
            dE = 2 * self.spins[i, j] * (
                self.spins[(i+1)%L, j] + self.spins[(i-1)%L, j] +
                self.spins[i, (j+1)%L] + self.spins[i, (j-1)%L]
            )
            if dE <= 0 or np.random.rand() < np.exp(-dE / self.T):
                self.spins[i, j] *= -1
    
    def get_mag(self):
        return np.mean(self.spins)
```

## 2. 解析の実行

ビンダー累積量 U = 1 - <m^4> / (3 * <m^2>^2) を計算します。


```python
def run_full_analysis(Ls, temps, n_steps=1000, n_burnin=300):
    data = {L: {'m': [], 'u': []} for L in Ls}
    for L in Ls:
        for T in temps:
            sim = IsingSimulation(L, T)
            for _ in range(n_burnin): sim.step()
            ms = []
            for _ in range(n_steps):
                sim.step()
                ms.append(sim.get_mag())
            ms = np.array(ms)
            m2 = np.mean(ms**2)
            m4 = np.mean(ms**4)
            data[L]['m'].append(np.mean(np.abs(ms)))
            data[L]['u'].append(1 - m4 / (3 * m2**2))
    return data

Ls = [8, 16]
temps = np.linspace(2.0, 2.6, 10)
results = run_full_analysis(Ls, temps)
```

## 3. 結果の可視化


```python
plt.figure(figsize=(10, 6))
for L in Ls:
    plt.plot(temps, results[L]['u'], 'o-', label=f'L={L}')
plt.axvline(2.269, color='k', ls='--', label='Exact Tc (2.269)')
plt.title('Binder Cumulant')
plt.legend(); plt.grid(True)
plt.show()
```
