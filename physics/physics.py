
from vpython import *

"""
 1. 參數設定, 設定變數及初始值
"""
size = 1    # 小球半徑
m = 1       # 小球質量
L = 100     # 地板長度
g = 9.8     # 重力加速度 9.8 m/s^2
t = 0       # 時間
dt = 0.001  # 時間間隔

"""
 2. 畫面設定
"""
scene = canvas(title="Projection with for loop", width=800, height=400, x=0, y=0,
               center=vec(0, 5, 0), background=vec(0, 0.6, 0.6))
floor = box(pos=vec(0, -size, 0), size=vec(L, 0.01, 10), texture=textures.metal)

# 開啟檔案 data.csv, 屬性為寫入, 先寫入欄位的標題
with open("data.csv", "w", encoding="UTF-8") as file:
    file.write("theta(degree), b, t(s), R(m)\n")

"""
 3. 物體運動部分
"""
def main(i=0, n=16, v0=30, degree=30):
    t = 0
    theta = radians(degree)
    ball = sphere(pos=vec(-L/2, 0, 0), radius=size, color=vec((n-i)/n, 0, i/n),
                  make_trail=True, v=vec(v0*cos(theta), v0*sin(theta), 0))
    while ball.pos.y - floor.pos.y >= size:
        rate(1000)
        ball.a = vec(0, -g, 0)
        ball.v += ball.a*dt
        ball.pos += ball.v*dt
        t += dt
    return degree, t, ball.pos.x + L/2

mx = 0
for i in range(0, 16): # 改變 theta 時設為16, 改變 b 時設為10
    degree = 15 + 5*i  # 改變 theta
    degree, t, r = main(i=i, degree=degree)
    print(degree, t, r)
    mx = max(mx, r)
    with open("data.csv", "a", encoding="UTF-8") as file:
        file.write(str(degree) + "," + str(t) + "," + str(r) + "\n")
print("the farthest distance is ", mx, "m.")
