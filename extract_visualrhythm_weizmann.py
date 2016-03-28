## Require opencv

import os
import cv2
import visual_rhythm
import time

init_time = time.time ()

source = '/home/berthin/Dropbox/UNICAMP/Abnormal_Event_Detection/DataSets/weizmann/'
source = '/Users/berthin/Documents/unicamp/Datasets/KTH/'
##single action
if not False:
  action = 'running'
  dest   = '/Users/berthin/Documents/unicamp/optical-flow/VideoDescriptor/VisualRhythm/vi_rth_kth2/'

  videos_list = os.listdir (source + action + '/' + action + '_mp4')
  gap = 10

  vr = [visual_rhythm.get_visualrhythm (source + action + '/' + action + '_mp4/' + video_name, type_visualrhythm = 'horizontal', params = [gap], frame_range = None, show = False) for video_name in videos_list if video_name[-3:] == 'mp4']

  idx = 0
  for img in vr:
    idx += 1
    gray = cv2.cvtColor (img, cv2.COLOR_RGB2GRAY)
    cv2.imwrite ('%s/%s_horizontal_gap=%d_img=%d.bmp' % (dest, action, gap, idx), gray)

## multiple actions
if not True:
  #actions = ['bend', 'jack', 'jump', 'pjump', 'run', 'side', 'skip', 'walk', 'wave1', 'wave2']
  actions = ['bend', 'jack', 'side', 'pjump', 'wave2', 'wave1']
  dest   = '/home/berthin/Documents/optical-flow/VideoDescriptor/VisualRhythm/kth_VR_all/'

  gap = 10
  for action in actions:
    videos_list = os.listdir (source + action)

    vr = [visual_rhythm.get_visualrhythm (source + action + '/' + video_name, type_visualrhythm = 'horizontal', params = [gap], frame_range = None, show = False) for video_name in videos_list]

    idx = 0
    for img in vr:
      idx += 1
      gray = cv2.cvtColor (img, cv2.COLOR_RGB2GRAY)
      cv2.imwrite ('%s/%s_horizontal_gap=%d_img=%d.bmp' % (dest, action, gap, idx), gray)

finish_time = time.time ()

print (finish_time - init_time)
