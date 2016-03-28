from skimage import io
import numpy as np
import os
import time

init_time = time.time ()

source = '/home/berthin/Documents/optical-flow/VideoDescriptor/VisualRhythm/vi_rth_weizmann/horizontal_gap=10/'
#dest   = '/home/berthin/Documents/optical-flow/VideoDescriptor/VisualRhythm/vi_rth_weizmann/patterns_horizontal_gap=10/'
dest   = '/home/berthin/Documents/optical-flow/VideoDescriptor/VisualRhythm/vi_rth_weizmann/patterns_horizontal_gap=10_v2/'

files = os.listdir (source)

thr_std = 10
#thr_cvr = 0.4

for im_name in files:
  im_0 = io.imread (source + im_name, as_grey = True)
  patt_idx = 0
  for im_1 in np.hsplit (im_0, im_0.shape[1] // 180):
    #patt_idx += 1
    last_col = -1
    pattern = np.empty ([im_1.shape[0], 0], np.uint8)
    for col in xrange (im_1.shape[1]):
      if np.std (im_1[:, col]) < thr_std:
      #if np.std (im_1[:, col]) < thr_cvr * np.std (im_1[:, col]):
        if (last_col != -1) and col - last_col > 10:
          pattern = np.hstack ((pattern, im_1[:, last_col:col]))
          #io.imsave ('%s%s_img=%d_p%d.bmp' % (dest, im_name[:-4], im_idx, patt_idx), im_1[:, last_col:col])
          #patt_idx += 1
        last_col = -1
      else:
        last_col = col if last_col == -1 else last_col
    if last_col != -1 and col - last_col > 10:
      pattern = np.hstack ((pattern, im_1[:, last_col:col]))
      #io.imsave ('%s%s_img=%d_p%d.bmp' % (dest, im_name[:-4], im_idx, patt_idx), im_1[:, last_col:col])
    if pattern.shape[1] > 10:
      io.imsave ('%s%s_p%d.bmp' % (dest, im_name[:-4], patt_idx), pattern)
      patt_idx += 1

finish_time = time.time ()
print (finish_time - init_time)
