import math
import copy
import random
class AIPlayer:
    """
    AI ���
    """

    def __init__(self, color):
        """
        ��ҳ�ʼ��
        :param color: ���巽��'X' - ���壬'O' - ����
        """

        self.color = color
        
    def ucb1(self, node, t, c):
        '''
        ����ucb1ֵ
        :param node: ���ؿ������Ľڵ�
        :param t: �������Ĵ���
        :param c: ucb1���������еĳ���c
        :return: ucb1��ֵ
        '''
        pos, T, reward, childern = node # pos����node������λ�ã�T��ʾt��ҡ���о���node�Ĵ�����reward����node�Ľ���
        if T == 0:
            T = 0.000000001
        if t == 0:
            t = 1
        a = reward / T
        b = math.log(t)
        d = c * math.sqrt(2 * b / T)
        return a + d
    
    def select_path(self, root, t):
        '''
        ���ؿ�����������һ����ѡ��
        :param root: ���ؿ��������ڵ�
        :param t: ҡ������
        :return: �Ӹ��ڵ��ߵ�Ŀǰѡ��Ҷ�ӽڵ��node����tuple
        '''
        current_path = []
        childern = root
        temp_t = t
        AI_turn = True
        
        while True:
            if len(childern) == 0:
                break
            maxchild = []           # ��¼ucb1ֵ���ĺ��ӡ����ܴ�����ͬ�������������list����
            childid = 0             # ���ӵ��±�
            
            if AI_turn:
                maxval = -1         # ��¼ucb1ֵ�����/��Сֵ
            else:
                maxval = 2
            
            for child in childern:
                pos, times, reward, t_childern = child
                if AI_turn:
                    cval = AIPlayer.ucb1(self, child, temp_t, 1)
                    if cval >= maxval:
                        if cval == maxval:
                            maxchild.append(childid)
                        else:
                            maxchild = [childid]
                            maxval = cval
                else:
                    cval = AIPlayer.ucb1(self, child, temp_t, -1)
                    if cval <= maxval:
                        if cval == maxval:
                            maxchild.append(childid)
                        else:
                            maxchild = [childid]
                            maxval = cval
                            
                childid = childid + 1
                
            maxid = maxchild[random.randrange(0, len(maxchild))]  # ���������Ӽ�ѡһ��
            pos, times, reward, t_childern = childern[maxid]
            current_path.append(pos)
            temp_t = times
            childern = t_childern
            AI_turn = not(AI_turn)
            
        return current_path
    
    def expand(self, board, color):
        '''
        ���ؿ����������ڶ�������չ
        :param board: ����
        :param color: ��Ҫ��չ�����ӵ���ɫ��X-���壬O-����
        :return: ���ɺϷ�����������
        '''
        pos = list(board.get_legal_actions(color))
        childern = []
        for p in pos:
            childern.append((p, 0, 0, []))
        return childern
        
        
    def simulation(self, board, color):
        '''
        ���ؿ�����������������ģ��
        :param board: ����
        :param color: ��Ҫ���ӵ���ɫ
        :param steps: ģ��Ĳ���
        :return: �Ƿ����Ӯ
        '''
        
        # ����������������ӣ�һ��һ��
        action_list = list(board.get_legal_actions(color))
        
        if len(action_list) == 0:
            if color == 'X':
                neg_color = 'O'
            else:
                neg_color = 'X'
            neg_action_list = list(board.get_legal_actions(neg_color)) # �����ǰ�ж���û�����ӵĵط����������������
            if len(neg_action_list) == 0:
                return board.get_winner()
            action_list = neg_action_list
            color = neg_color
            
        action = random.choice(action_list)
        board._move(action, color)
        
        color = 'X' if color == 'O' else 'O'
        return AIPlayer.simulation(self, board, color) # �ݹ�����������ֱ������
        
    def back_propagation(self, board, root, iswon, path, color):
        '''
        ���ؿ������������Ĳ�������
        :param board: ����
        :param root: ���ؿ������ĸ��ڵ�
        :param iswon: ���������Ƿ�Ӯ��
        :param path: ���ݵ�node·��
        :param color: ��ǰ�������ɫ
        '''
        childern = root
        for maxele in path:
            cid = 0           # ���ӵ��±�
            for child in childern:
                pos, times, reward, t_childern = child
                if maxele == pos:
                    break
                cid = cid + 1
                
            if maxele == pos:
                times += 1
                if iswon:
                    reward += 1
                if len(t_childern) == 0: # �������Ҷ�ӽڵ㣬��������չһ�㺢��
                    t_childern = AIPlayer.expand(self, board, color)
                childern[cid] = (pos, times, reward, t_childern)
            childern = t_childern
        
        return root

    def get_move(self, board):
        """
        ���ݵ�ǰ����״̬��ȡ�������λ��
        :param board: ����
        :return: action �������λ��, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '����'
        else:
            player_name = '����'
        print("���һ�ᣬ�Է� {}-{} ����˼����...".format(player_name, self.color))

        # -----------------��ʵ������㷨����--------------------------------------
        action = None
        temp_board1 = copy.deepcopy(board) # �������ֹ�޸�����
        temp_board2 = copy.deepcopy(board)
        root = AIPlayer.expand(self, temp_board1, self.color)
#         print(f'root = {root}')
        for ep in range(1, 5000):
            path = AIPlayer.select_path(self, root, ep) 
            # print(f'path = {path}')
            
            temp_color = self.color
            for pos in path:
                temp_board1._move(pos, temp_color)
                temp_color = 'X' if temp_color == 'O' else 'O'
            
            isWon = AIPlayer.simulation(self, temp_board2, self.color)
            root = AIPlayer.back_propagation(self, temp_board1, root, isWon, path, self.color)
        
        max_reward = -1
#         print(f'root = {root}')
        for child in root:
            pos, times, reward, t_childern = child
            if times > 0 and reward / times > max_reward:
                action = pos
                max_reward = reward / times
#         print(f'action = {action}')
        # ------------------------------------------------------------------------

        return action
