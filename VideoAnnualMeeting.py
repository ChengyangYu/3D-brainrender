import brainrender
brainrender.SHADER_STYLE = 'cartoon'
brainrender.WHOLE_SCREEN = True
brainrender.DISPLAY_INSET = False
from brainrender.scene import Scene
from matplotlib import cm
import numpy as np
from brainrender.animation.video import BasicVideoMaker
import os
import h5py


path = r'D:\Render'
# 读取数据内容(transient.h5py文件)
with h5py.File(os.path.join(r"D:\BrainRender1126", "transient_6.hdf5"), "r") as ffr:
    sus_trans = np.array(ffr["sus_trans"], dtype="int8")
    reg = [x.decode() for x in ffr["reg"]]

reg_set = list(set(reg))
sums = []

for one_reg in reg_set:
    reg_sel = [x == one_reg for x in reg]
    count = np.sum(reg_sel)
    trans = np.sum(np.logical_and(reg_sel, sus_trans[1, :]))
    sums.append([one_reg, count, trans, trans / count])

dist = [x[3] for x in sums if x[1] >= 100]
dmin = np.floor(np.min(dist) * 100).astype(np.int)
dmax = np.floor(np.max(dist) * 100).astype(np.int)

screenshot_params = dict(
    folder=r'D:\SampleVedio',
    name='br0',  # 修改保存的图片的名字， 代码后边会给你加生成时间，精确到日期和秒
    scale=3,  # scale越大分辨率越高，通常大于1
    type='.png'   # svg图片保存不了？只能保存png和jpg格式,默认为png
)
scene = Scene(screenshot_kwargs=screenshot_params,
              base_dir=r'D:\PyCharmProject\brain3Dtest\result', camera='sagittal_video')  # 绘制3D旋转视频时camera="sagittal", SCREENSHOT_TRANSPARENT_BACKGROUND=False设置非透明背景，但是好像效果不明显
jmap = cm.get_cmap('jet', dmax - dmin + 1)
jetmap = jmap(range(dmax - dmin + 1))

# Add the whole thalamus in gray
for s in sums:
    if s[1] >= 100 and s[0] != 'Unlabeled' and s[0] != 'root':
        cmIdx = np.floor(s[3] * 100).astype(np.int) - dmin
        scene.add_brain_regions([s[0]], colors=jetmap[cmIdx][:3], use_original_color=False, alpha=0.25,
                                add_labels=False)  # alpha值设置透明度，越小越透明
# scene.add_actor_label(mos, 'MOs', size=400, color='blackboard', xoffset=250) 添加脑区标签，要想脑区名字不被截掉需要在后边跑循环
#scene.add_image(image_file_path=r'C:\Users\Fish\Desktop\BrainRender-master\colorbar.png')
#scene.render()
vmkr = BasicVideoMaker(scene, video_format='mp4')
vmkr.make_video(azimuth=1, niters=360, duration=20, save_name="figure1Vedio_test", elevation=0, roll=0)

