# 2次元イジング模型：数式対応型・全コード詳細解説

このノートブックでは、統計力学の「数式」と「プログラム」の対応関係、およびコードの「一行ずつの意味」を統合して解説します。

---

## 1. 理論と実装の対応（クイックリファレンス）

まずは、物理法則がどのようにコードに翻訳されているかを確認します。

### A. エネルギー変化 $\Delta E = 2 J s_i \sum s_j$
```python
dE = 2 * self.spins[i, j] * ( # 2 * s_i
    self.spins[(i+1)%L, j] + self.spins[(i-1)%L, j] + # 周囲4サイトの和
    self.spins[i, (j+1)%L] + self.spins[i, (j-1)%L]
)
```

### B. 遷移確率 $W = \min(1, e^{-\Delta E / T})$
```python
if dE <= 0 or np.random.rand() < np.exp(-dE / self.T):
    self.spins[i, j] *= -1 # 確率に基づいて反転
```

### C. ビンダー累積量 $U_L = 1 - \frac{\langle m^4 \rangle}{3 \langle m^2 \rangle^2}$
```python
m2 = np.mean(ms**2)
m4 = np.mean(ms**4)
u_l = 1 - m4 / (3 * m2**2)
```

---

## 2. 実装コードの一行ずつ詳細解説

次に、プログラム全体の流れと、各行の役割を詳しく見ていきます。

### 2.1 `IsingSimulation` クラス
物理的なルールを司る「シミュレーターの本体」です。


```python
class IsingSimulation:
    def __init__(self, L, T):
        # 格子サイズLと温度Tをインスタンス変数として保存
        self.L, self.T = L, T
        # スピンの初期状態を作成。+1(上)か-1(下)をランダムにL×Lの行列に配置する
        self.spins = np.random.choice([1, -1], size=(L, L))
    
    def step(self):
        L = self.L
        # 1 MCS (Monte Carlo Step) 分の試行を行う（合計 L^2 回）
        for _ in range(L*L):
            # 0 から L-1 の範囲でランダムに縦・横のインデックスを選ぶ
            i, j = np.random.randint(0, L, 2)
            
            # 注目スピンとその隣接4スピンの積の和。%L は端を反対側に繋げる周期境界条件。
            dE = 2 * self.spins[i, j] * (
                self.spins[(i+1)%L, j] + self.spins[(i-1)%L, j] +
                self.spins[i, (j+1)%L] + self.spins[i, (j-1)%L]
            )
            
            # メトロポリス法のアルゴリズム：エネルギーが下がるなら即反転、
            # 上がるなら熱ゆらぎの確率(0~1)が判定値(exp)を超えたときのみ反転する。
            if dE <= 0 or np.random.rand() < np.exp(-dE / self.T):
                self.spins[i, j] *= -1
    
    def get_mag(self):
        # 格子全体の平均磁化を計算。全ての要素の和を全サイト数で割る処理に相当。
        return np.mean(self.spins)
```

### 2.2 解析実行関数 `run_full_analysis`
データを集計し、統計的な物理量を導出するフェーズです。


```python
def run_full_analysis(Ls, temps, n_steps=2000, n_burnin=500):
    # サイズごとに結果を整理するための空の入れ物を作成
    data = {L: {'m': [], 'u': []} for L in Ls}
    
    for L in Ls:
        for T in temps:
            # 各温度ごとに新しいシミュレーションを開始
            sim = IsingSimulation(L, T)
            
            # 最初の数回(n_burnin)は、初期のランダム状態から平衡状態へ落ち着かせるために「捨て」のステップを実行
            for _ in range(n_burnin): sim.step()
            
            ms = []
            # 平衡状態に達した後、測定(n_steps)を開始して磁化の時系列データを取得
            for _ in range(n_steps):
                sim.step()
                ms.append(sim.get_mag())
            
            ms = np.array(ms)
            # 統計平均を計算。np.mean は時間軸方向のアンサンブル平均をとることに相当。
            m2 = np.mean(ms**2)
            m4 = np.mean(ms**4)
            
            # 磁化の絶対値平均（|m|）をリストに追加
            data[L]['m'].append(np.mean(np.abs(ms)))
            # ビンダー累積量を計算して追加
            data[L]['u'].append(1 - m4 / (3 * m2**2))
            
    return data
```

## 3. まとめ：物理とプログラムの融合

1.  **数式**は物理の本質（ルール）を示している。
2.  **コードの1行**はそのルールをコンピューターが理解できる計算手順に変換している。
3.  **コメント**は、なぜその計算が必要なのかという意図を説明している。

この3つの視点を同時に持つことで、物理シミュレーションを完全に理解することができます。
