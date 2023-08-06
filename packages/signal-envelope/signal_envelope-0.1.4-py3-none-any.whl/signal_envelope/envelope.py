### signal-envelope ###
import numpy as np
import wave
import numpy as np
import ctypes

def read_wav(path):
  """returns signal & fps"""
  wav = wave.open(path , 'r')
  signal = np.frombuffer(wav.readframes(-1) , np.int16).astype(np.double)
  fps = wav.getframerate()
  return signal, fps

def save_wav(signal, name = 'test.wav', fps = 44100): 
  '''save .wav file to program folder'''
  o = wave.open(name, 'wb')
  o.setframerate(fps)
  o.setnchannels(1)
  o.setsampwidth(2)
  o.writeframes(np.int16(signal)) # Int16
  o.close()


###############################
###  Python implementation  ###
###############################

def _get_circle(x0, y0, x1, y1, r):
  '''returns center of circle that passes through two points'''  
  q = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
  c = np.sqrt(r * r - (q / 2)**2)
  x3 = (x0 + x1) / 2
  y3 = (y0 + y1) / 2 
  if y0 + y1 >= 0:
    xc = x3 + c * (y0 - y1) / q
    yc = y3 + c * (x1 - x0) / q
  else:
    xc = x3 - c * (y0 - y1) / q
    yc = y3 - c * (x1 - x0) / q

  return xc, yc

def _get_pulses(W):
  '''Sorts a signal into pulses, returning positive and negative X, Y coordinates, and filtering out noise'''
  n = W.size
  sign = np.sign(W[0])
  x = 1
  while np.sign(W[x]) == sign:
    x += 1
  x0 = x + 1
  sign = np.sign(W[x0])
  posX = []
  # posY = []
  negX = []
  # negY = []
  for x in range(x0, n):
    if np.sign(W[x]) != sign: # Prospective pulse
      if x - x0 > 2:          # Not noise
        xp = x0 + np.argmax(np.abs(W[x0 : x]))
        yp = W[xp]
        if np.sign(yp) >= 0:
          posX.append(xp)
          # posY.append(yp)
        else:
          negX.append(xp)
          # negY.append(yp)
      x0 = x
      sign = np.sign(W[x])
  # return np.array(posX), np.array(posY), np.array(negX), np.array(negY)
  return np.array(posX), np.array(negX)

def _get_radius_average(X, Y):
  # m0 = (Y[-1] - Y[0]) / (X[-1] - X[0])
  k_sum = 0
  # mm = np.sqrt(m0**2 + 1)                            
  for i in range(len(X) - 1):
    x = (X[i + 1] - X[i])                            
    y = (Y[i + 1] - Y[i])                            
    k = y / (x * np.sqrt(x*x + y*y))
    k_sum += k
  r = np.abs(1 / (k_sum / (len(X) - 1)))
  # print("m0: ", m0, "k: ", k_sum)
  return r

def _get_frontier(X, Y):
  '''extracts the frontier via snowball method'''
  scaling = (np.sum(X[1:] - X[:-1]) / 2) / np.sum(Y)
  Y = Y * scaling
  
  r = _get_radius_average(X, Y)
  idx1 = 0
  idx2 = 1
  frontierX = [X[0]]
  # frontierY = [Y[0]]
  n = len(X)
  # print("n: ",n, " r: ", r_of_x(0)," Y0: ", Y[0])
  while idx2 < n:
    xc, yc = _get_circle(X[idx1], Y[idx1], X[idx2], Y[idx2], r)
    empty = True
    for i in range(idx2 + 1, n):
      if np.sqrt((xc - X[i])**2 + (yc - Y[i])**2) < r:
        empty = False
        idx2 += 1
        break
    if empty:
      frontierX.append(X[idx2])
      # frontierY.append(Y[idx2])
      idx1 = idx2
      idx2 += 1
  frontierX = np.array(frontierX)
  # frontierY = np.array(frontierY) / scaling
  # print(frontierX.size)
  return frontierX

def get_frontiers_py(W, mode=0):
  "If mode == 0: Returns positive and negative indices frontiers of a signal"
  "If mode == 1: Returns indices of the envelope of a signal"
  PosX, NegX = _get_pulses(W)
  if PosX.size == 0 or NegX.size == 0:
    print("Error: nonperiodic signal, no pulses found")
    return
  if mode == 0:    
    PosFrontierX = _get_frontier(PosX, W[PosX])
    NegFrontierX = _get_frontier(NegX, W[NegX])
    return PosFrontierX, NegFrontierX
  else:
    X = np.unique(np.hstack([PosX, NegX]))
    FrontierX = _get_frontier(X, np.abs(W[X]))
    return FrontierX

###############################
###  C++ implementation  ######
###############################

def get_frontiers_cpp(W, mode=0):
  if mode == 0: # Frontiers mode
    result = lib.compute_raw_envelope(W.ctypes.data_as(ctypes.POINTER(ctypes.c_float)), ctypes.c_size_t(W.size), ctypes.
    c_size_t(mode))
    if result == 1:
      print("Error: nonperiodic signal, no pulses found")
      return
    pos_n = lib.get_pos_size()
    neg_n = lib.get_neg_size()

    lib.get_pos_X.restype = np.ctypeslib.ndpointer(dtype=ctypes.c_size_t, shape=(pos_n,))
    lib.get_neg_X.restype = np.ctypeslib.ndpointer(dtype=ctypes.c_size_t, shape=(neg_n,))

    pos_X = lib.get_pos_X()
    neg_X = lib.get_neg_X()
    return np.copy(pos_X), np.copy(neg_X)

  else:        # Envelope mode
    result = lib.compute_raw_envelope(W.ctypes.data_as(ctypes.POINTER(ctypes.c_float)), ctypes.c_size_t(W.size), ctypes.c_size_t(mode))
    if result == 1:
      print("Error: nonperiodic signal, no pulses found")
      return
    pos_n = lib.get_pos_size()
    lib.get_pos_X.restype = np.ctypeslib.ndpointer(dtype=ctypes.c_size_t, shape=(pos_n,))
    pos_X = lib.get_pos_X()
    return np.copy(pos_X)



