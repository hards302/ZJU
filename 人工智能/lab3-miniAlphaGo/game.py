# !/usr/bin/Anaconda3/python
# -*- coding: utf-8 -*-

from func_timeout import func_timeout, FunctionTimedOut
import datetime
from board import Board
from copy import deepcopy


class Game(object):
    def __init__(self, black_player, white_player):
        self.board = Board()  # ����
        # ���������ϵ�ǰ�������֣���Ĭ���� None
        self.current_player = None
        self.black_player = black_player  # ����һ��
        self.white_player = white_player  # ����һ��
        self.black_player.color = "X"
        self.white_player.color = "O"

    def switch_player(self, black_player, white_player):
        """
        ��Ϸ�������л����
        :param black_player: ����
        :param white_player: ����
        :return: ��ǰ���
        """
        # �����ǰ����� None ���� ����һ�� white_player���򷵻� ����һ�� black_player;
        if self.current_player is None:
            return black_player
        else:
            # �����ǰ����Ǻ���һ�� black_player �򷵻� ����һ�� white_player
            if self.current_player == self.black_player:
                return white_player
            else:
                return black_player

    def print_winner(self, winner):
        """
        ��ӡӮ��
        :param winner: [0,1,2] �ֱ��������ʤ�������ʤ��ƽ��3�ֿ��ܡ�
        :return:
        """
        print(['�����ʤ!', '�����ʤ!', 'ƽ��'][winner])

    def force_loss(self, is_timeout=False, is_board=False, is_legal=False):
        """
         ����3�����Ϸ�����ͳ�ʱ�������Ϸ,�޸�����Ҳ����
        :param is_timeout: ʱ���Ƿ�ʱ��Ĭ�ϲ���ʱ
        :param is_board: �Ƿ��޸�����
        :param is_legal: �����Ƿ�Ϸ�
        :return: Ӯ�ң�0,1��,���Ӳ� 0
        """

        if self.current_player == self.black_player:
            win_color = '���� - O'
            loss_color = '���� - X'
            winner = 1
        else:
            win_color = '���� - X'
            loss_color = '���� - O'
            winner = 0

        if is_timeout:
            print('\n{} ˼������ 60s, {} ʤ'.format(loss_color, win_color))
        if is_legal:
            print('\n{} ���� 3 �β����Ϲ���,�� {} ʤ'.format(loss_color, win_color))
        if is_board:
            print('\n{} ���ԸĶ���������,�� {} ʤ'.format(loss_color, win_color))

        diff = 0

        return winner, diff

    def run(self):
        """
        ������Ϸ
        :return:
        """
        # ����ͳ��˫������ʱ��
        total_time = {"X": 0, "O": 0}
        # ����˫��ÿһ������ʱ��
        step_time = {"X": 0, "O": 0}
        # ��ʼ��ʤ����������Ӳ�
        winner = None
        diff = -1

        # ��Ϸ��ʼ
        print('\n=====��ʼ��Ϸ!=====\n')
        # ���̳�ʼ��
        self.board.display(step_time, total_time)
        while True:
            # �л���ǰ���,�����ǰ����� None ���߰��� white_player���򷵻غ��� black_player;
            #  ���򷵻� white_player��
            self.current_player = self.switch_player(self.black_player, self.white_player)
            start_time = datetime.datetime.now()
            # ��ǰ��Ҷ����̽���˼���󣬵õ�����λ��
            # �жϵ�ǰ���巽
            color = "X" if self.current_player == self.black_player else "O"
            # ��ȡ��ǰ���巽�Ϸ�����λ��
            legal_actions = list(self.board.get_legal_actions(color))
            # print("%s�Ϸ����������б�"%color,legal_actions)
            if len(legal_actions) == 0:
                # �ж���Ϸ�Ƿ����
                if self.game_over():
                    # ��Ϸ������˫����û�кϷ�λ��
                    winner, diff = self.board.get_winner()  # �õ�Ӯ�� 0,1,2
                    break
                else:
                    # ��һ���кϷ�λ��,�л����巽
                    continue

            board = deepcopy(self.board._board)

            # legal_actions ������ 0 ���ʾ��ǰ���巽�кϷ�����λ��
            try:
                for i in range(0, 3):
                    # ��ȡ����λ��
                    action = func_timeout(60, self.current_player.get_move,
                                          kwargs={'board': self.board})

                    # ��� action �� Q ��˵���������������
                    if action == "Q":
                        # ˵�������������Ϸ�����������Ӹ�������Ӯ��
                        break
                    if action not in legal_actions:
                        # �жϵ�ǰ���巽�����Ƿ���ϺϷ�����,������Ϸ�,����Ҫ�Է���������
                        print("�����Ӳ����Ϲ���,���������ӣ�")
                        continue
                    else:
                        # ���ӺϷ���ֱ�� break
                        break
                else:
                    # ����3�β��Ϸ���������Ϸ��
                    winner, diff = self.force_loss(is_legal=True)
                    break
            except FunctionTimedOut:
                # ���ӳ�ʱ��������Ϸ
                winner, diff = self.force_loss(is_timeout=True)
                break

            # ����ʱ��
            end_time = datetime.datetime.now()
            if board != self.board._board:
                # �޸����̣�������Ϸ��
                winner, diff = self.force_loss(is_board=True)
                break
            if action == "Q":
                # ˵�������������Ϸ�����������Ӹ�������Ӯ��
                winner, diff = self.board.get_winner()  # �õ�Ӯ�� 0,1,2
                break

            if action is None:
                continue
            else:
                # ͳ��һ�����õ�ʱ��
                es_time = (end_time - start_time).seconds
                if es_time > 60:
                    # �ò�����60�������������
                    print('\n{} ˼������ 60s'.format(self.current_player))
                    winner, diff = self.force_loss(is_timeout=True)
                    break

                # ��ǰ�����ɫ���������
                self.board._move(action, color)
                # ͳ��ÿ����������������ʱ��
                if self.current_player == self.black_player:
                    # ��ǰѡ���Ǻ���һ��
                    step_time["X"] = es_time
                    total_time["X"] += es_time
                else:
                    step_time["O"] = es_time
                    total_time["O"] += es_time
                # ��ʾ��ǰ����
                self.board.display(step_time, total_time)

                # �ж���Ϸ�Ƿ����
                if self.game_over():
                    # ��Ϸ����
                    winner, diff = self.board.get_winner()  # �õ�Ӯ�� 0,1,2
                    break

        print('\n=====��Ϸ����!=====\n')
        self.board.display(step_time, total_time)
        self.print_winner(winner)

        # ����'black_win','white_win','draw',��������
        if winner is not None and diff > -1:
            result = {0: 'black_win', 1: 'white_win', 2: 'draw'}[winner]

            # return result,diff

    def game_over(self):
        """
        �ж���Ϸ�Ƿ����
        :return: True/False ��Ϸ����/��Ϸû�н���
        """

        # ���ݵ�ǰ���̣��ж�����Ƿ���ֹ
        # �����ǰѡ��û�кϷ������λ�ӣ����л�ѡ�֣��������һ��ѡ��Ҳû�кϷ�������λ�ã������ֹͣ��
        b_list = list(self.board.get_legal_actions('X'))
        w_list = list(self.board.get_legal_actions('O'))

        is_over = len(b_list) == 0 and len(w_list) == 0  # ����ֵ True/False

        return is_over

#
#
# if __name__ == '__main__':
#     from Human_player import HumanPlayer
#     from Random_player import RandomPlayer
#     from AIPlayer import AIPlayer
#
#     # x = HumanPlayer("X")
#     x = RandomPlayer("X")
#     o = RandomPlayer("O")
# #     # x = AIPlayer("X")
# #     o = AIPlayer("O")
#     game = Game(x, o)
#     game.run()
