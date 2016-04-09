import cv2
import numpy as np
from matplotlib import pylab as plt

def get_visualrhythm (source, type_visualrhythm = 'horizontal', params = None, frame_range = None, show=True, color=False):
  print source
  obj = cv2.VideoCapture (source);
  print obj.isOpened ()
  W, H = int (obj.get (3)), int (obj.get (4))
  if frame_range is None:
    frame_range = [1, int (obj.get (7))]
  vr = []
  clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(4,4))
  if type_visualrhythm == 'horizontal':
    obj.set (1, frame_range[0])
    for idx in xrange(frame_range[1]-frame_range[0]):
      _, img = obj.read()
      #img = cv2.equalizeHist(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY))
      #img = clahe.apply(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY))
      #img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
      vrr = [img[gap, :, :] for gap in xrange(0, H, params[0])]
      vrr2 = np.empty([0, vrr[0].shape[1]], np.uint8)
      for vrrr in vrr:
        vrr2 = np.vstack ((vrr2, vrrr))
      vrr2 = np.array(vrr2)
      #vr.append (img[params[0]][:][:]);
      vr.append (vrr2)
  elif type_visualrhythm == 'vertical':
    obj.set (1, frame_range[0])
    for idx in xrange(frame_range[1]-frame_range[0]):
      _, img = obj.read()
      vr.append (img[:, params[0], :]);
  elif type_visualrhythm == 'zigzag':
    obj.set (1, frame_range[0])
    for idx in xrange(frame_range[1]-frame_range[0]):
      _, img = obj.read()
      vr.append (np.array (get_zigzag (img, color, params[0], params[1], img.shape[1], img.shape[0])));

  if len (vr[0].shape) > 1:
    ans = np.array (vr)
  else:
    ans = np.array (vr).reshape (len(vr), vr[0, 1])

  if show:
    if len (ans.shape) > 2:
      plt.imshow (ans)
    else:
      plt.imshow (ans, cmap='gray')
    plt.show()
  return ans

def get_zigzag (img, color, row_gap, col_gap, W, H):
  #print W, H, row_gap, col_gap
  zigzag = [];
  m_row, m_col = row_gap * 1. / col_gap, col_gap * 1. / row_gap
  mv_r, mv_c = [1, - m_row, 0, m_row], [0, m_col, 1, -m_col]
  i_mv = 0
  r, c = 0., 0.
  state = 1
  step = 0
  while (r != H - 1 and c != W - 1):
    if state == 1:
      step += 1
      if r + 1 < H: r += 1
      else: c += 1
      if (c >= W): break;
      #print r, c
      #zigzag.append (img[int(r), int(c)])
      state = 1 if step < row_gap else 2
    elif state == 2:
      while True:
        if (int(r - m_row) >= 0 and int(c + m_col) < W):
          r -= m_row
          c += m_col
          zigzag.append (img[int (r), int(c), :] if color else img[int (r), int(c)])
        else:
          state = 3
          step = 0
          break
        #print r, c
    elif state == 3:
      step += 1
      if c + 1 < W: c += 1
      else: r += 1
      if (r >= H): break
      #print r, c
      #zigzag.append (img[int(r), int(c), :])
      state = 3 if step < col_gap else 4
    elif state == 4:
      while True:
        if (int (r + m_row) < H and int (c - m_col) >= 0):
          r += m_row
          c -= m_col
          zigzag.append (img[int (r), int(c), :] if color else img[int (r), int(c)])
        else:
          state = 1
          step = 0
          break
        #print r, c

  return zigzag

def get_random_walk (img, pattern_x, pattern_y):
  return img[pattern_x, pattern_y]


def extract_horizontal_from_frame(img, (H, W), gap):
  return np.array([img[row, :] for row in xrange(0, H, gap)], np.uint8).flatten()
def extract_vertical_from_frame(img, (H, W), gap):
  return np.array([img[:, col] for col in xrange(0, W, gap)], np.uint8).flatten()
def extract_zigzag_from_frame(img, (H, W), row_gap, col_gap):
  return np.array(visual_rhythm.get_zigzag(frame, False, row_gap, col_gap, W, H)).flatten()

def extract_from_frame(frame, type_visualrhythm, size, params):
  if type_visualrhythm[0] == 'h': #horizontal
    return (extract_horizontal_from_frame(frame, size, params[0]))
  elif type_visualrhythm[0] == 'v': #vertical
    return (extract_vertical_from_frame(frame, size, params[0]))
  elif type_visualrhythm[0] == 'z': #zigzag
    return (extract_zigzag_from_frame(frame, size, params[0], params[1]))
  return None

