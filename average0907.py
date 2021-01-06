# import garyCutSlice2 as gcs
import grayCutSlice1 as gcs
import brainrender
from ZXScene import ZXScene
# from brainrender.scene import Scene
# scene = Scene(base_dir=r'D:\BrainRender1126\result')
# print(scene.atlas._root_bounds)  # 读取横纵坐标


saveroute = r'D:\BrainRender1126\SelectivityFraction\figure1_z\gray'
direction = 'z'
ColorType = 'gray'   # gray
for deep in range(9450, 10800, 50):  #13100
    gcs.grayCutSlice1(ColorType=ColorType, deep=deep, saveroute=saveroute, direction=direction)

