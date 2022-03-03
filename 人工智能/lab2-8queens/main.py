import numpy as np           # �ṩά���������������
import copy                  # ��copyģ�鵼����ȿ�������
from board import Chessboard
from itertools import permutations

# ���������࣬�����������
class Game:
    def __init__(self, show = True):
        """
        ��ʼ����Ϸ״̬.
        """
        
        self.chessBoard = Chessboard(show)
        self.solves = []
        self.gameInit()
        
    # ������Ϸ
    def gameInit(self, show = True):
        """
        ��������.
        """
        
        self.Queen_setRow = [-1] * 8
        self.chessBoard.boardInit(False)
        
    ##############################################################################
    ####                ������������������(����������Զ��庯��)                 #### 
    ####              �����self.solves = �˻ʺ��������н��list                ####
    ####             ��:[[0,6,4,7,1,3,5,2],]����˻ʺ��һ����Ϊ                ####
    ####           (0,0),(1,6),(2,4),(3,7),(4,1),(5,3),(6,5),(7,2)            ####
    ##############################################################################
    #                                                                            #
    
    def run(self, row=0):
        a = list(range(8))
        for l in list(permutations(a)):
            self.gameInit(False)
            flag = 1
            for i,item in enumerate(l):
                if self.chessBoard.setQueen(i,item,False) == False:
                    flag = 0
                    break
            if flag == 1 and self.chessBoard.isWin():
                self.solves.append(list(l))
#         self.solves.append([0,6,4,7,1,3,5,2])

    #                                                                            #
    ##############################################################################
    #################             ��ɺ���ǵ��ύ��ҵ             ################# 
    ##############################################################################
    
    def showResults(self, result):
        """
        ���չʾ.
        """
        
        self.chessBoard.boardInit(False)
        for i,item in enumerate(result):
            if item >= 0:
                self.chessBoard.setQueen(i,item,False)
        
        self.chessBoard.printChessboard(False)
    
    def get_results(self):
        """
        ������(�����޸Ĵ˺���).
        return: �˻ʺ�����н��list.
        """
        
        self.run()
        return self.solves
   