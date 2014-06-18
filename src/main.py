#coding: utf-8
import sys
import classifier

if __name__ == '__main__':
  n_v_list = []
  for line in open('data/train_nvpair.txt', 'r'):
    n_v = line.rstrip().split(" ")
    n_v_list.append(tuple(n_v))

    
  k = 3
  clf = classifier.Classifier(k, n_v_list)

  #学習
  clf.learnEM()

  #テストデータの読み込み
  testData = []
  for line in sys.stdin:
    n_v = line.rstrip().split(" ")
    testData.append(tuple(n_v))

  #パープレキシティの計算
  perplexity = clf.get_perplexity(testData)
  print perplexity
