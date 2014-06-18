#coding: utf-8
import random
import math

class Classifier:
  def __init__(self, k, n_v_list):
    self.k = k
    self.n_v_list = n_v_list

    self.noun_list = list(set(map(lambda (n,v): n, n_v_list)))
    self.verb_list = list(set(map(lambda (n,v): v, n_v_list)))
    self.init_p_z()
    self.init_p_x_z()
    self.init_p_y_z()


  #p(z)を乱数で初期化
  def init_p_z(self):
    self.p_z = []
    for i in xrange(0, self.k):
      self.p_z.append(random.random())

  #p(z | x)を乱数で初期化
  def init_p_x_z(self):
    self.p_x_z = {}
    for noun in self.noun_list:
      self.p_x_z[noun] = []
      for i in xrange(0, self.k):
        self.p_x_z[noun].append(random.random())

  #p(z | y)を乱数で初期化
  def init_p_y_z(self):
    self.p_y_z = {}
    for verb in self.verb_list:
      self.p_y_z[verb] = []
      for i in xrange(0, self.k):
        self.p_y_z[verb].append(random.random())

        
  def get_k(self):
    return self.k

  def get_n_v_list(self):
    return self.n_v_list

  def get_p_x_z(self):
    return self.p_x_z

  def get_p_y_z(self):
    return self.p_y_z
    
  def get_p_z_xy(self):
    return self.p_z_xy

  def learnEM(self):
    #仮実装
    return

  def get_p_x_y(self, n, v):
    ans = 0.0
    for i in xrange(0, self.k):
      ans += self.p_z[i] * self.p_x_z[n][i] * self.p_y_z[v][i]
    return ans
    
  def get_perplexity(self, tuplelist):
    s = 0.0
    for (n, v) in tuplelist:
      s += math.log(self.get_p_x_y(n, v), 2)

    s /= (- len (tuplelist))
    return 2**s
