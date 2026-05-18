import math

def calculate_sqrt(x):
    # CIの失敗テスト用：わざとバグを入れます
    return x * 2

if __name__ == "__main__":
    x = 2
    y = calculate_sqrt(x)
    print("x =", x)
    print("sqrt(x) =", y)