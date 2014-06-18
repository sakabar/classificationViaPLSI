#coding: utf-8
import random
import math
import collections

class Classifier:
  def __init__(self, k, n_v_list):
    self.k = k

    #self.n_v_listなどは重復なし
    self.n_v_list = list(set(n_v_list))
    self.noun_list = (list(set(map(lambda (n,v): n, n_v_list))))
    self.verb_list = (list(set(map(lambda (n,v): v, n_v_list))))

    #個数はv_v_counterで記録
    self.n_v_counter = collections.Counter(n_v_list)

    # print "noun_list: " + str(len(self.noun_list)) #debug
    # print "verb_list: " + str(len(self.verb_list)) #debug
    
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


  def learn_Mstep(self):
    #P(z)を更新
    # print "M-step: P(z)" #debug
    deno = 0
    for j in xrange(0, self.k):
      for (noun, verb) in self.n_v_list:
        deno += self.n_v_counter[(noun, verb)] * (10 ** self.log_p_z_xy[noun][verb][j])
    log_deno = math.log10(deno)

    for i in xrange(0, self.k):
      # print ("z_" + str(i)) #debug
      nume = 0
      for (noun, verb) in self.n_v_list:
        nume += self.n_v_counter[(noun, verb)] * (10 ** self.log_p_z_xy[noun][verb][i])
      log_nume = math.log10(nume)

      self.log_p_z[i] = log_nume - log_deno


    #P(x | z)を更新
    # print "M-step: P(x | z)" #debug
    for i in xrange(0, self.k):
      # print ("z_" + str(i)) #debug
      deno = 0
      for (x, y) in self.n_v_list:
        deno += self.n_v_counter[(x, y)] * (10 ** self.log_p_z_xy[x][y][i])
      log_deno = math.log10(deno)

      for noun in self.noun_list:
        # print ("  " + noun) #debug
        nume = 0
        for verb in self.verb_list:
          # print ("    " + verb) #debug

          # これがボトルネックだった
          # if (noun, verb) in self.n_v_list:
          nume += self.n_v_counter[(noun, verb)] * (10 ** self.log_p_z_xy[noun][verb][i])
        log_nume = math.log10(nume)
          
        self.log_p_x_z[noun][i] = log_nume - log_deno

    #P(y | z)を更新
    # print "M-step: P(y | z)" #debug
    for i in xrange(0, self.k):
      # print ("z_" + str(i)) #debug
      deno = 0
      for (x, y) in self.n_v_list:
        deno += self.n_v_counter[(x, y)] * (10 ** self.log_p_z_xy[x][y][i])
      log_deno = math.log10(deno)

      for verb in self.verb_list:
        nume = 0
        for noun in self.noun_list:
          nume += self.n_v_counter[(noun, verb)] * (10 ** self.log_p_z_xy[noun][verb][i])
        log_nume = math.log10(nume)
          
        self.log_p_y_z[verb][i] = log_nume - log_deno

    return

  def learnEM(self):
    prev_log_likelihood = 0
    log_likelihood = 1000000
    eps = 100
    
    while (abs(log_likelihood - prev_log_likelihood) > eps):
      prev_likelihood = log_likelihood
      self.learn_Estep()
      self.learn_Mstep()

      log_likelihood = 0
      for (noun, verb) in self.n_v_list:
        log_likelihood += self.n_v_counter[(noun, verb)] * self.get_log_p_x_y(noun, verb)
      print log_likelihood

    return


  #getter
  def get_k(self):
    return self.k

  def get_n_v_list(self):
    return self.n_v_list

  # def get_log_p_x_z(self):
  #   return self.log_p_x_z

  def get_log_p_y_z(self):
    return self.log_p_y_z

  def get_log_p_z_xy(self):
    return self.log_p_z_xy

  def get_log_p_x_y(self, noun, verb):
    ans = 0.0
    for i in xrange(0, self.k):
      ans += 10.0 ** (self.log_p_z[i] + self.log_p_x_z[noun][i] + self.log_p_y_z[verb][i])
    return math.log10(ans)

