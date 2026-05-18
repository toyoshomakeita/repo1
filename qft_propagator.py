import numpy as np
import matplotlib.pyplot as plt

def klein_gordon_propagator_1d(x, m):
    """
    1次元のクライン-ゴルドン場のファインマン伝播関数の静的な振る舞いを近似的に計算します。
    (空間的な減衰の様子を可視化します)
    """
    # 伝播関数 D(x) は質量 m があると exp(-m|x|) のように指数関数的に減衰します
    return np.exp(-m * np.abs(x))

# 空間座標の設定 (-5 から 5 まで)
x = np.linspace(-5, 5, 500)

# 異なる質量パラメーター m
masses = [0.5, 1.0, 2.0]

plt.figure(figsize=(10, 6))

for m in masses:
    y = klein_gordon_propagator_1d(x, m)
    plt.plot(x, y, label=f'Mass m = {m}')

plt.title('Spatial correlation of Klein-Gordon Field (Static limit)')
plt.xlabel('Distance x')
plt.ylabel('Amplitude D(x)')
plt.legend()
plt.grid(True)

# グラフを保存
plt.savefig('qft_propagator.png')
print("QFT伝播関数の可視化が完了しました。qft_propagator.png に保存しました。")
