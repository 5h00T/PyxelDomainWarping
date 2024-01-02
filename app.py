import pyxel
import numpy as np

class App:
    def __init__(self):
        self.noise = np.vectorize(pyxel.noise)
        pyxel.init(100, 100)
        # カラーパレットを設定
        pyxel.colors.from_list([
            0x111111,
            0x111122,
            0x111133,
            0x111144,
            0x111155,
            0x111166,
            0x111177,
            0x111188,
            0x111199,
            0x1111aa,
            0x1111bb,
            0x1111cc,
            0x1111dd,
            0x1111ee,
            0x1111ff,
            0xffffff,
        ])
        #２次元配列を初期化
        self.width = pyxel.width
        self.height = pyxel.height
        self.values = [[0 for i in range(self.width)] for j in range(self.height)]
        
        pyxel.run(self.update, self.draw)
        

    def update(self):
        # すべてのピクセルに対してノイズを生成
        x = np.arange(self.width) / self.width
        y = np.arange(self.height) / self.height
        x1, y1 = np.meshgrid(x, y)
        x2 = self.fbm(x1, y1, 1)
        y2 = self.fbm(x1 + 1, y1 + 1, 1)
        x3 = self.fbm(x1 + 4.0 * x2 + 3.5 + 0.01 * pyxel.frame_count, y1 + 4.0 * y2 + 2.2 + 0.17 * pyxel.frame_count, 1)
        y3 = self.fbm(x1 + 4.0 * x2 + 6.2 + 0.02 * pyxel.frame_count, y1 + 4.0 * y2 + 1.7 + 0.13 * pyxel.frame_count, 1)
        value = self.fbm(x1 + 2.0 * x3, y1 + 2.0 * y3, 1)
        value = (value + 1) / 2
        value = np.clip(value, 0, 1)
        self.values = value
            
    def draw(self):
        pyxel.cls(0)
        for x in range(0, self.width):
            for y in range(0, self.height):
                value = self.values[x][y]
                pyxel.pset(x, y, int(value * 15))
        
    def fbm(self, x, y, octaves):
        value = 0
        for i in range(0, octaves):
            value += self.noise(x, y) * 0.5 ** i
        return value

App()