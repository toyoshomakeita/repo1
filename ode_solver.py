import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# 微分方程式: dy/dt = -k * y
# これは放射性崩壊や冷却の法則などで見られる基本的な指数減少のモデルです。

def model(y, t, k):
    dydt = -k * y
    return dydt

# 初期条件
y0 = 5

# 時間点
t = np.linspace(0, 20, 100)

# パラメータ k (減少率)
k = 0.3

# 微分方程式を解く
y = odeint(model, y0, t, args=(k,))

# 結果のプロット
plt.plot(t, y)
plt.xlabel('Time (t)')
plt.ylabel('y(t)')
plt.title(f'Solution of dy/dt = -{k}y')
plt.grid(True)

# グラフを保存
plt.savefig('ode_solution.png')
print("計算が完了し、ode_solution.png にグラフを保存しました。")
