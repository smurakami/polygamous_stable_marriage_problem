# coding: utf-8

"""安定結婚問題"""

import random as R
capacity = 3

DEBUG = False

class Man:
    """安定結婚アルゴリズムに置ける人のデータ構造"""
    def __init__(self, prop=None, priority_list = []):
        """
        prop: なにか荷物を持たせたかったらここに入れてあげると良い。
        priority_list: ここには好きな順に人が入っている。最初は空でも良い
        """
        self.prop = prop
        self.priority_list = priority_list
        self.id = None

    def setPriorityList(self, priority_list):
        """
        選好度リストをセットする。
        priority_list: ここに好きな順に人が入っている。
        """
        self.priority_list = priority_list

    def priorityRank(self, man):
        """相手を何番目に好むかの順位を返す"""
        return self.priority_list.index(man)

    def printPriorityList(self):
        """選好度リストの表示"""
        print self.id, ":",
        for elem in self.priority_list:
            print elem.id,
        print ""

class Male(Man):
    """安定結婚アルゴリズムにおける男性のデータ構造"""
    id_counter = 0 # idに使う

    def __init__(self, prop=None, priority_list=[]):
        Man.__init__(self, prop, priority_list) # 男性は人である
        self.id = Male.id_counter # id
        Male.id_counter += 1

    def setPartner(self, female):
        """彼女を決定する"""
        self.partner = female

    def removePartner(self):
        """彼女と別れる"""
        self.partner = None


class Female(Man):
    """安定結婚アルゴリズムにおける女性のデータ構造"""
    id_counter = 0

    def __init__(self, prop=None, priority_list=[]):
        Man.__init__(self, prop, priority_list) # 女性は人である
        self.id = Female.id_counter
        Female.id_counter += 1
        self.queue = [] # 現在つきあっている相手のリスト
        self.capacity = capacity # 何股までかけれるか

    def pop(self):
        """もっとも好みでない男性と別れる"""
        m = self.queue.pop()
        m.removePartner()
        return m

    def check(self):
        """浮気が起きないかチェック"""
        success = True
        stranger = [m for m in self.priority_list if m not in self.queue]
        for m in self.queue:
            for s in stranger:
                if self.priorityRank(s) < self.priorityRank(m):
                    if s.priorityRank(self) < s.priorityRank(s.partner):
                        print "blocking pair for", m.id, "and", self.id, ",",
                        print s.id, "and", s.partner.id
                        print s.id, "and", self.id
                        success = False
        return success

    def append(self, male):
        """新しい相手と付き合う"""
        for i, m in enumerate(self.queue):
            if self.priorityRank(male) < self.priorityRank(m):
                self.queue.insert(i, male)
                return
        self.queue.append(male)


def match(male, female):
    """男女をマッチングする"""
    female.append(male)
    male.setPartner(female)

def psmp(males, females):
    """安定結婚アルゴリズムの執行"""
    if DEBUG: print "psmp"
    p = {} # 各男性が何番目の女性を選ぶか
    for m in males:
        p[m] = 0
        while 0 <= p[m] < len(females):
            f = m.priority_list[p[m]]
            match(m, f)
            if len(f.queue) <= f.capacity:
                break
            else:
                m = f.pop()
                p[m] += 1


def printResult(females):
    """デバッグ用関数"""
    for f in females:
        print f.id, ":",
        for m in f.queue:
            print m.id,
        print ""

def check(males, females):
    """デバッグ用関数"""
    success = True
    for f in females:
        if not f.check():
            success = False
    return success

def shuffled(origin_list):
    """デバッグ用関数"""
    clone = list(origin_list)
    shuffled_list = []
    while len(clone) > 0:
        shuffled_list.append(clone.pop(R.randint(0, len(clone) - 1)))
    return shuffled_list


if __name__ == "__main__":
    SIZE = 10
    males = [Male() for i in range(SIZE)]
    females = [Female() for i in range(SIZE)]

    for m in males:
        m.setPriorityList(shuffled(females))

    for f in females:
        f.setPriorityList(shuffled(males))

    print "males: "
    for m in males:
        m.printPriorityList()

    print ""
    print "females: "
    for f in females:
        f.printPriorityList()


    # for f in females:
    #     for m in males:
    #         print m in f.priority_list

    psmp(males, females)

    print ""
    print "result: "
    printResult(females)

    if check(males, females):
        print "成功"
    else:
        print "失敗"
