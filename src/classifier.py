#coding: utf-8
import random

class Classifier:
  def __init__(self, k, n_v_list):
    self.k = k
    self.n_v_list = n_v_list

    self.noun_list = list(set(map(lambda (n,v): n, n_v_list)))
    self.verb_list = list(set(map(lambda (n,v): v, n_v_list)))
    self.init_p_z()
    self.init_p_z_x()
    self.init_p_z_y()


  #p(z)を乱数で初期化
  def init_p_z(self):
    self.p_z = []
    for i in xrange(0, self.k):
      self.p_z.append(random.random())

  #p(z | x)を乱数で初期化
  def init_p_z_x(self):
    self.p_z_x = {}
    for noun in self.noun_list:
      self.p_z_x[noun] = []
      for i in xrange(0, self.k):
        self.p_z_x[noun].append(random.random())

  #p(z | y)を乱数で初期化
  def init_p_z_y(self):
    self.p_z_y = {}
    for verb in self.verb_list:
      self.p_z_y[verb] = []
      for i in xrange(0, self.k):
        self.p_z_y[verb].append(random.random())

        
  def get_k(self):
    return self.k

  def get_n_v_list(self):
    return self.n_v_list

  def get_p_z_x(self):
    return self.p_z_x

  def get_p_z_y(self):
    return self.p_z_y
    
  def get_p_z_xy(self):
    return self.p_z_xy

  def learnEM(self):
    #仮実装
    return

  def get_perplexity(self, tuplelist):
    #仮実装
    return 1.0
