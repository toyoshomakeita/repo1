import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [i**2 for i in x]

plt.plot(x, y)
plt.title("x^2 graph")
plt.savefig("graph.png")

print("graph saved")