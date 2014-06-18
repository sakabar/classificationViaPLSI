#coding: utf-8
import random
import math

class Classifier:
  def __init__(self, k, n_v_list):
    self.k = k
    self.n_v_list = n_v_list

    self.noun_list = list(set(map(lambda (n,v): n, n_v_list)))
    self.verb_list = list(set(map(lambda (n,v): v, n_v_list)))

    #初期化
    self.init_log_p_z()
    self.init_log_p_x_z()
    self.init_log_p_y_z()
    self.init_log_p_z_xy()

  #p(z)を乱数で初期化
  def init_log_p_z(self):
    self.log_p_z = []
    for i in xrange(0, self.k):
      self.log_p_z.append(math.log10(random.random()))

  #p(z | x)を乱数で初期化
  def init_log_p_x_z(self):
    self.log_p_x_z = {}
    for noun in self.noun_list:
      self.log_p_x_z[noun] = []
      for i in xrange(0, self.k):
        self.log_p_x_z[noun].append(math.log10(random.random()))

  #p(z | y)を乱数で初期化
  def init_log_p_y_z(self):
    self.log_p_y_z = {}
    for verb in self.verb_list:
      self.log_p_y_z[verb] = []
      for i in xrange(0, self.k):
        self.log_p_y_z[verb].append(math.log10(random.random()))

  #p(z | x, y)を乱数で初期化
  #p[x][y][z]の順なので注意すること
  def init_log_p_z_xy(self):
    self.log_p_z_xy = {}
    for noun in self.noun_list:
      self.log_p_z_xy[noun] = {}
      for verb in self.verb_list:
        self.log_p_z_xy[noun][verb] = []
        for i in xrange(0, self.k):
          self.log_p_z_xy[noun][verb].append(math.log10(random.random()))

  def get_perplexity(self, tuplelist):
    s = 0.0
    for (n, v) in tuplelist:
      p = 10 ** self.get_log_p_x_y(n, v)
      base = 2
      s += math.log(p, base)

    s /= (- len (tuplelist))
    return 2**s

  def learn_Estep(self):
    for (noun, verb) in self.n_v_list:
      log_deno = math.log10(sum (map (lambda i: 10**(self.log_p_z[i] + self.log_p_x_z[noun][i] + self.log_p_y_z[verb][i]), xrange(0, self.k))))
      for i in xrange(0, self.k):
        log_nume = self.log_p_z[i] + self.log_p_x_z[noun][i] + self.log_p_y_z[verb][i]

        self.log_p_z_xy[noun][verb][i] = log_nume - log_deno
    
  def learnEM(self):
    self.learn_Estep()
    return

        
  #getter
  def get_k(self):
    return self.k

  def get_n_v_list(self):
    return self.n_v_list

  def get_log_p_x_z(self):
    return self.log_p_x_z

  def get_log_p_y_z(self):
    return self.log_p_y_z
    
  def get_log_p_z_xy(self):
    return self.log_p_z_xy

  def get_log_p_x_y(self, n, v):
    ans = 0.0
    for i in xrange(0, self.k):
      ans += 10**(self.log_p_z[i] + self.log_p_x_z[n][i] + self.log_p_y_z[v][i])
    return math.log10(ans)
    
