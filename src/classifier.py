#coding: utf-8
import sys
import math
import random
import collections

class Classifier:
  def __init__(self, k, n_v_list):
    self.k = k

    #self.n_v_listなどは重復なし
    self.n_v_list = list(set(n_v_list))
    self.noun_set = (list(set(map(lambda (n,v): n, n_v_list))))
    self.verb_set = (list(set(map(lambda (n,v): v, n_v_list))))

    #個数はv_v_counterで記録
    self.n_v_counter = collections.Counter(n_v_list)

    # print "noun_list: " + str(len(self.noun_set)) #debug
    # print "verb_list: " + str(len(self.verb_set)) #debug
    
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
    for noun in self.noun_set:
      self.log_p_x_z[noun] = []
      for i in xrange(0, self.k):
        self.log_p_x_z[noun].append(math.log10(random.random()))

  #p(z | y)を乱数で初期化
  def init_log_p_y_z(self):
    self.log_p_y_z = {}
    for verb in self.verb_set:
      self.log_p_y_z[verb] = []
      for i in xrange(0, self.k):
        self.log_p_y_z[verb].append(math.log10(random.random()))

  #p(z | x, y)を乱数で初期化
  #p[x][y][z]の順なので注意すること
  def init_log_p_z_xy(self):
    self.log_p_z_xy = {}
    for noun in self.noun_set:
      self.log_p_z_xy[noun] = {}
      for verb in self.verb_set:
        self.log_p_z_xy[noun][verb] = []
        for i in xrange(0, self.k):
          self.log_p_z_xy[noun][verb].append(math.log10(random.random()))

  def get_perplexity(self, tuplelist):
    s = 0.0
    for (n, v) in tuplelist:
      p = 10.0 ** self.get_log_p_x_y(n, v)
      base = 2.0
      s += math.log(p, base)

    s /= (- len (tuplelist))
    return 2.0 ** s

  def learn_Estep(self):
    for (noun, verb) in self.n_v_list:
      #deno: 分母
      #   Sum_{z'} P(z')*P(x|z')*P(y|z')
      # = Sum_{z'} 10^log10(P(z')) * 10^log10(P(x|z')) * 10^log10(P(y|z'))
      # = Sum_{z'} 10^(log10(P(z') + log10(P(x|z')) + log10(P(y|z')))

      deno = (sum (map (lambda i: 10**(self.log_p_z[i] + self.log_p_x_z[noun][i] + self.log_p_y_z[verb][i]), xrange(0, self.k))))

      #nume:分子
      #   P(z)*P(x|z)*P(y|z)
      # = 10^log10(P(z)) * 10^log10(P(x|z)) * 10^log10(P(y|z))
      # = 10^(log10(P(z) + log10(P(x|z)) + log10(P(y|z)))

      for i in xrange(0, self.k):
        #nume = 10**(self.log_p_z[i] + self.log_p_x_z[noun][i] + self.log_p_y_z[verb][i])
        log10_nume = (self.log_p_z[i] + self.log_p_x_z[noun][i] + self.log_p_y_z[verb][i])

        self.log_p_z_xy[noun][verb][i] = log10_nume - math.log10(deno)

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

      for noun in self.noun_set:
        # print ("  " + noun) #debug
        nume = 0
        for verb in self.verb_set:
          # print ("    " + verb) #debug
          nume += self.n_v_counter[(noun, verb)] * (10 ** self.log_p_z_xy[noun][verb][i])
        if nume > 0:
          log_nume = math.log10(nume)
        else:
          print "line121: nume= " + str(nume)

          for _noun in self.noun_set:
            for _verb in self.verb_set:
              for _i in xrange(0, self.k):
                print str(_noun) + "\t" + str(_verb) + "\t" + str(_i) + "\t" + str(10 ** self.log_p_z_xy[_noun][_verb][_i])
          sys.exit(1)
          
        self.log_p_x_z[noun][i] = log_nume - log_deno

    #P(y | z)を更新
    # print "M-step: P(y | z)" #debug
    for i in xrange(0, self.k):
      # print ("z_" + str(i)) #debug
      deno = 0
      for (x, y) in self.n_v_list:
        deno += self.n_v_counter[(x, y)] * (10 ** self.log_p_z_xy[x][y][i])
      log_deno = math.log10(deno)

      for verb in self.verb_set:
        nume = 0
        for noun in self.noun_set:
          nume += self.n_v_counter[(noun, verb)] * (10 ** self.log_p_z_xy[noun][verb][i])
        if nume > 0:
          log_nume = math.log10(nume)
        else:
          print "line142: nume= " + str(nume)
          for _noun in self.noun_set:
            for _verb in self.verb_set:
              for _i in xrange(0, self.k):
                print str(_noun) + "\t" + str(_verb) + "\t" + str(_i) + "\t" + str(10 ** self.log_p_z_xy[_noun][_verb][_i])
          sys.exit(1)

        self.log_p_y_z[verb][i] = log_nume - log_deno

    return

  def learnEM(self):
    prev_log_likelihood = 0
    log_likelihood = 1000000
    eps = 10
    
    while (abs(log_likelihood - prev_log_likelihood) > eps):
      prev_log_likelihood = log_likelihood
      self.learn_Estep()
      self.learn_Mstep()

      log_likelihood = 0
      for (noun, verb) in self.n_v_list:
        log_likelihood += self.n_v_counter[(noun, verb)] * self.get_log_p_x_y(noun, verb)
      print str(log_likelihood) + " (" + str(log_likelihood - prev_log_likelihood) + ")" #debug

    return

  def get_log_p_x_y(self, noun, verb):
    ans = 0.0
    for i in xrange(0, self.k):
      ans += 10.0 ** (self.log_p_z[i] + self.log_p_x_z[noun][i] + self.log_p_y_z[verb][i])
    return math.log10(ans)


  def sum_of_p_z_is_1(self):
    eps = 0.0001
    sum = 0.0
    for i in xrange(0, self.k):
      sum += 10 ** self.log_p_z[i]

    return (abs(1.0 - sum) < eps)

  def sum_of_p_x_z_is_1(self):
    eps = 0.0001
    sum = 0.0
    for x in self.noun_set:
      for i in xrange(0, self.k):
        sum += 10 ** (self.log_p_x_z[x][i] + self.log_p_z[i])

    return (abs(1.0 - sum) < eps)

  def sum_of_p_y_z_is_1(self):
    eps = 0.0001
    sum = 0.0
    for y in self.verb_set:
      for i in xrange(0, self.k):
        sum += 10 ** (self.log_p_y_z[y][i] + self.log_p_z[i])

    return (abs(1.0 - sum) < eps)

  def sum_of_p_x_y_is_1(self):
    sum = 0.0
    eps = 0.0001

    for noun in self.noun_set:
      for verb in self.verb_set:
        sum += 10 ** self.get_log_p_x_y(noun, verb)

    return (abs(1.0 - sum) < eps)
        
