import brainrender
brainrender.SHADER_STYLE = 'ambient'  # plastic
# brainrender.DEFAULT_STRUCTURE_ALPHA = 0.5
brainrender.DISPLAY_ROOT=True
#brainrender.ROOT_COLOR = 'transparent'
brainrender.ROOT_ALPHA = 0.3
brainrender.DISPLAY_INSET = False    # 不要开右下角小窗
from ZXScene import ZXScene
import h5py
import numpy as np
import os
from matplotlib import cm


with h5py.File(os.path.join(r"D:\BrainRender1126", "transient_6.hdf5"), "r") as ffr:
    sus_trans = np.array(ffr["sus_trans"], dtype="int8")
    reg = [x.decode() for x in ffr["reg"]]

reg_set = list(set(reg))
sums = []
for one_reg in reg_set:
    reg_sel = [x == one_reg for x in reg]
    count = np.sum(reg_sel)
    if count >= 20:
        trans = np.sum([np.logical_and(reg_sel, sus_trans[0, :]), np.logical_and(reg_sel, sus_trans[1, :]), np.logical_and(reg_sel, sus_trans[3, :])])# np.sum(np.logical_and(reg_sel, sus_trans[(0, 1, 3), :]))   #0,1,3
        sums.append([one_reg, count, trans, trans / count])

dist = [x[3] for x in sums if x[1] >= 100]
dmin = np.floor(np.min(dist) * 100).astype(np.int)
dmax = np.floor(np.max(dist) * 100).astype(np.int)
scene = ZXScene(base_dir=r'D:\BrainRender1126\result')
jmap = cm.get_cmap('jet', dmax - dmin + 1)
jetmap = jmap(range(dmax - dmin + 1))

Actors = []
for s in sums:
    if s[1] >= 100 and s[0] != 'Unlabeled' and s[0] != 'root':
        cmIdx = np.floor(s[3] * 100).astype(np.int) - dmin
        # Actors[s[0]] = scene.add_brain_regions([s[0]], colors=jetmap[cmIdx][:3], use_original_color=False, alpha=0.8,
        #                                       add_labels=False)  # alpha值设置透明度，越小越透明
        Actors.append(scene.add_brain_regions([s[0]], colors=jetmap[cmIdx][:3], use_original_color=False, alpha=0.3,
                                              add_labels=False))  # alpha值设置透明度，越小越透明


scene.render(camera='three_quarters_camera_mirror', zoom=1, interactive=False)  # zoom的大小决定了后边截图的大小 coronal sagittal top three_quarters_camera_mirror
scene.take_screenshot()


# 判断数据中是否有嗅球
# a1=0
# a2=0
# a3=0
# a4=0
# a5=0
# a6=0

# for i in sums:
#     if i[0] == 'AOB':
#         a1 = a1+1
#     if i[0] == 'AOBgl':
#         a2 = a2+1
#     if i[0] == 'AOBgr':
#         a3 =a3+1
#     if i[0] == 'AOBmi':
#         a4 = a4+1
#     if i[0] == 'MOB':
#         a5 = a5+1
#     if i[0] == 'onl':
#         a6 = a6+1



