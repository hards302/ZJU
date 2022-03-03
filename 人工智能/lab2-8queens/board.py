import numpy as np
import copy

class Chessboard:
    def __init__(self, show = True):
        """
        ��ʼ������״̬
        """
        
        self.boardInit(show)
    
    def boardInit(self, show = True):
        ''' 
        �������� 
        '''
        
        self.chessboardMatrix = np.zeros((8,8),dtype=np.int8)    #���̳�ʼ��
        self.unableMatrix = np.zeros((8,8),dtype=np.int8)        #��ֹ����λ��
        self.queenMatrix = np.zeros((8,8),dtype=np.int8)         #����λ��
        
        printMatrix = np.zeros((9,9),dtype=np.int8)              #���̻��ƾ���
        for i in range(8):
            printMatrix[0][i+1] = i
            printMatrix[i+1][0] = i
        self.printMatrix = printMatrix
        if show:
            self.printChessboard()
    
    def trans(self, x):
        ''' 
        ���̻����ַ�ת�� 
        '''
        
        return{0:'-',-1:'x',1:'o'}.get(x)
    
    def isOnChessboard(self, x,y):
        ''' 
        �ж������Ƿ���������
        '''
        
        return (x*(7-x) >=0 and y*(7-y) >=0)
        
    def setLegal(self, x, y):
        ''' 
        ��ֹ����λ��ָ��
        '''
        
        return (self.unableMatrix +1)[x][y]

    def setQueen(self, x, y, show = True):
        '''
        ����֮���������
        '''
        
        if self.setLegal(x, y):
            self.queenMatrix[x][y] =1                                       #����λ��
            for i in range(8):
                self.unableMatrix[x][i] =-1                                 #�����޷�����
                self.unableMatrix[i][y] =-1                                 #�����޷�����
            for i in range(-7,8):
                if self.isOnChessboard(x+i,y+i):
                    self.unableMatrix[x+i][y+i] =-1                         #���Խ����޷�����
                if self.isOnChessboard(x+i,y-i):
                    self.unableMatrix[x+i][y-i] =-1                         #���Խ����޷�����
            self.chessboardMatrix = self.unableMatrix +2*self.queenMatrix   #��������
            self.printMatrix[1:9,1:9] = self.chessboardMatrix
            if show:
                self.printChessboard()
            return True
        else:
            print('����ʧ��')
            return False
        
    def play(self):
        '''
        ��һ���
        '''
        
        while True:
            action = input("���������һ���Ϸ�������(e.g. '2-3'���������¿�ʼ������'init'�������˳�������'Q'��): ")

            if action == 'init':
                self.boardInit()
                continue
            if action == 'Q' or action == 'q' or action == 'quit' or action == 'QUIT':
                break

            if '-' in action:
                x,y =action.split('-')
            elif ',' in action:
                x,y =action.split(',')
            else:
                x = action[0]
                y = action[-1]
            
            if x.isdigit() and y.isdigit():
                self.setQueen(int(x),int(y))
                if self.isWin():
                    print('Win!')
                    self.printMatrix[1:9,1:9] = self.queenMatrix
                    self.printChessboard()
                    action = input("���������'Y'������һ��,������������ֵ�˳�: ")
                    if action == 'y' or action == 'Y':
                        self.boardInit()
                        self.Play()
                    else:
                        break
                    
                elif self.isLose():
                    print('Lose!')
                    self.printMatrix[1:9,1:9] = self.queenMatrix
                    self.printChessboard()
                    action = input("���������'Y'������һ��,������������ֵ�˳�: ")
                    if action == 'y' or action == 'Y':
                        self.boardInit()
                        self.play()
                    else:
                        break
                    
            else:
                print('������Ϸ������ָ������.')
        

    def isWin(self):
        '''
        ʤ�������ж�
        '''
        
        if sum(sum(self.queenMatrix)) ==8:
            return True
        else:
            return False

    def isLose(self):
        '''
        ʧ�������ж�
        '''
        
        if not self.isWin() and sum(sum(self.unableMatrix)) ==-64:
            return True
        else:
            return False

    def printChessboard(self, showALL = True):
        '''
        ��������
        '''
        
        if showALL:
            Board = self.printMatrix
        else:
            Board = self.printMatrix
            Board[1:9,1:9] = self.queenMatrix
            
        for i in range(9):
            for j in range(9):
                if i+j==0:
                    print('  ', end='')
                elif (i==0 and j!=8) or j==0 :
                    print(str(Board[i][j])+' ', end='')
                elif i==0 and j==8:
                    print(str(Board[i][j])+' ')
                elif j!=8:
                    print(self.trans(Board[i][j])+' ', end='')
                else:
                    print(self.trans(Board[i][j])+' ')