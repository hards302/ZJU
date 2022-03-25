#!/usr/bin/Anaconda3/python
# -*- coding: utf-8 -*-

class Board(object):
    """
    Board �ڰ������̣������8*8�������� X ��ʾ�������� O ��ʾ��δ����ʱ�� . ��ʾ��
    """

    def __init__(self):
        """
        ��ʼ������״̬
        """
        self.empty = '.'  # δ����״̬
        self._board = [[self.empty for _ in range(8)] for _ in range(8)]  # ���8*8
        self._board[3][4] = 'X'  # ��������
        self._board[4][3] = 'X'  # ��������
        self._board[3][3], self._board[4][4] = 'O', 'O'  # ��������

    def __getitem__(self, index):
        """
        ���Board[][] �����﷨
        :param index: �±�����
        :return:
        """
        return self._board[index]

    def display(self, step_time=None, total_time=None):
        """
        ��ӡ����
        :param step_time: ÿһ���ĺ�ʱ, ����:{"X":1,"O":0},Ĭ��ֵ��None
        :param total_time: �ܺ�ʱ, ����:{"X":1,"O":0},Ĭ��ֵ��None
        :return:
        """
        board = self._board
        # print(step_time,total_time)
        # ��ӡ����
        print(' ', ' '.join(list('ABCDEFGH')))
        # ��ӡ����������
        for i in range(8):
            # print(board)
            print(str(i + 1), ' '.join(board[i]))
        if (not step_time) or (not total_time):
            # ���̳�ʼ��ʱչʾ��ʱ��
            step_time = {"X": 0, "O": 0}
            total_time = {"X": 0, "O": 0}
            print("ͳ�����: �������� / ÿһ����ʱ / ��ʱ�� ")
            print("��   ��: " + str(self.count('X')) + ' / ' + str(step_time['X']) + ' / ' + str(
                total_time['X']))
            print("��   ��: " + str(self.count('O')) + ' / ' + str(step_time['O']) + ' / ' + str(
                total_time['O']) + '\n')
        else:
            # ����ʱչʾʱ��
            print("ͳ�����: �������� / ÿһ����ʱ / ��ʱ�� ")
            print("��   ��: " + str(self.count('X')) + ' / ' + str(step_time['X']) + ' / ' + str(
                total_time['X']))
            print("��   ��: " + str(self.count('O')) + ' / ' + str(step_time['O']) + ' / ' + str(
                total_time['O']) + '\n')

    def count(self, color):
        """
        ͳ�� color һ�����ӵ�������(O:����, X:����, .:δ����״̬)
        :param color: [O,X,.] ��ʾ�����ϲ�ͬ������
        :return: ���� color �����������ϵ�����
        """
        count = 0
        for y in range(8):
            for x in range(8):
                if self._board[x][y] == color:
                    count += 1
        return count

    def get_winner(self):
        """
        �жϺ���Ͱ������Ӯ��ͨ�����ӵĸ��������ж�
        :return: 0-����Ӯ��1-����Ӯ��2-��ʾƽ�֣���������Ͱ���������
        """
        # ����ڰ����ӳ�ʼ�ĸ���
        black_count, white_count = 0, 0
        for i in range(8):
            for j in range(8):
                # ͳ�ƺ������ӵĸ���
                if self._board[i][j] == 'X':
                    black_count += 1
                # ͳ�ư������ӵĸ���
                if self._board[i][j] == 'O':
                    white_count += 1
        if black_count > white_count:
            # ����ʤ
            return 0, black_count - white_count
        elif black_count < white_count:
            # ����ʤ
            return 1, white_count - black_count
        elif black_count == white_count:
            # ��ʾƽ�֣���������Ͱ���������
            return 2, 0

    def _move(self, action, color):
        """
        ���Ӳ���ȡ��ת���ӵ�����
        :param action: ���ӵ����� ������ D3 Ҳ������(2,3)
        :param color: [O,X,.] ��ʾ�����ϲ�ͬ������
        :return: ���ط�ת���ӵ������б�����ʧ���򷵻�False
        """
        # �ж�action �ǲ����ַ������������ת��Ϊ��������
        if isinstance(action, str):
            action = self.board_num(action)

        fliped = self._can_fliped(action, color)

        if fliped:
            # �оͷ�ת�Է���������
            for flip in fliped:
                x, y = self.board_num(flip)
                self._board[x][y] = color

            # ��������
            x, y = action
            # ���������� action ���괦��״̬���޸�֮���λ������ color[X,O,.]����״̬
            self._board[x][y] = color
            return fliped
        else:
            # û�з�ת��������ʧ��
            return False

    def backpropagation(self, action, flipped_pos, color):
        """
        ����
        :param action: ���ӵ������
        :param flipped_pos: ��ת���������б�
        :param color: ���ӵ����ԣ�[X,0,.]�������
        :return:
        """
        # �ж�action �ǲ����ַ������������ת��Ϊ��������
        if isinstance(action, str):
            action = self.board_num(action)

        self._board[action[0]][action[1]] = self.empty
        # ��� color == 'X'���� op_color = 'O';���� op_color = 'X'
        op_color = "O" if color == "X" else "X"

        for p in flipped_pos:
            # �ж�action �ǲ����ַ������������ת��Ϊ��������
            if isinstance(p, str):
                p = self.board_num(p)
            self._board[p[0]][p[1]] = op_color

    def is_on_board(self, x, y):
        """
        �ж������Ƿ����
        :param x: row ������
        :param y: col ������
        :return: True or False
        """
        return x >= 0 and x <= 7 and y >= 0 and y <= 7

    def _can_fliped(self, action, color):
        """
        ��������Ƿ�Ϸ�,������Ϸ������� False�����򷵻ط�ת�ӵ������б�
        :param action: ����λ��
        :param color: [X,0,.] ����״̬
        :return: False or ��ת�Է����ӵ������б�
        """
        # �ж�action �ǲ����ַ������������ת��Ϊ��������
        if isinstance(action, str):
            action = self.board_num(action)
        xstart, ystart = action

        # �����λ���Ѿ������ӻ��߳��磬���� False
        if not self.is_on_board(xstart, ystart) or self._board[xstart][ystart] != self.empty:
            return False

        # ��ʱ��color�ŵ�ָ��λ��
        self._board[xstart][ystart] = color
        # ����
        op_color = "O" if color == "X" else "X"

        # Ҫ����ת������
        flipped_pos = []
        flipped_pos_board = []

        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0],
                                       [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection
            y += ydirection
            # ���(x,y)�������ϣ�����Ϊ�Է�����,������������ϼ���ǰ��������ѭ����һ���Ƕȡ�
            if self.is_on_board(x, y) and self._board[x][y] == op_color:
                x += xdirection
                y += ydirection
                # ��һ���жϵ�(x,y)�Ƿ��������ϣ�������������ϣ�����ѭ����һ���Ƕ�,����������ϣ������whileѭ����
                if not self.is_on_board(x, y):
                    continue
                # һֱ�ߵ�������ǶԷ����ӵ�λ��
                while self._board[x][y] == op_color:
                    # ���һֱ�ǶԷ������ӣ���㣨x,y��һֱѭ����ֱ���㣨x,y)������߲��ǶԷ������ӡ�
                    x += xdirection
                    y += ydirection
                    # ��(x,y)�����˺Ͳ��ǶԷ�����
                    if not self.is_on_board(x, y):
                        break
                # �����ˣ���û������Ҫ��תOXXXXX
                if not self.is_on_board(x, y):
                    continue

                # ���Լ�������OXXXXXXO
                if self._board[x][y] == color:
                    while True:
                        x -= xdirection
                        y -= ydirection
                        # �ص�����������
                        if x == xstart and y == ystart:
                            break
                        # ��Ҫ��ת������
                        flipped_pos.append([x, y])

        # ��ǰ����ʱ���ϵ�����ȥ��������ԭ����
        self._board[xstart][ystart] = self.empty  # restore the empty space

        # û��Ҫ����ת�����ӣ����߷��Ƿ������� False
        if len(flipped_pos) == 0:
            return False

        for fp in flipped_pos:
            flipped_pos_board.append(self.num_board(fp))
        # �߷����������ط�ת���ӵ���������
        return flipped_pos_board

    def get_legal_actions(self, color):
        """
        ���պڰ���Ĺ����ȡ���ӵĺϷ��߷�
        :param color: ��ͬ��ɫ�����ӣ�X-���壬O-����
        :return: ���ɺϷ����������꣬��list()�������Ի�ȡ���еĺϷ�����
        """
        # ��ʾ����������8����ͬ�������꣬���緽������[0][1]���ʾ���������Ϸ���
        direction = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

        op_color = "O" if color == "X" else "X"
        # ͳ�� op_color һ���ڽ���δ����״̬��λ��
        op_color_near_points = []

        board = self._board
        for i in range(8):
            # i ����������0��ʼ��j��������Ҳ�Ǵ�0��ʼ
            for j in range(8):
                # �ж�����[i][j]λ�����ӵ����ԣ������op_color�������������һ��������
                # �������ѭ����ȡ��һ���������ӵ�����
                if board[i][j] == op_color:
                    # dx��dy �ֱ��ʾ[i][j]�������С��з����ϵĲ�����direction ��ʾ��������
                    for dx, dy in direction:
                        x, y = i + dx, j + dy
                        # ��ʾx��y����ֵ�ں���Χ�����������board[x][y]Ϊδ����״̬��
                        # ���ң�x,y������op_color_near_points �У�ͳ�ƶԷ�δ����״̬λ�õ��б�ſ�����Ӹ������
                        if 0 <= x <= 7 and 0 <= y <= 7 and board[x][y] == self.empty and (
                                x, y) not in op_color_near_points:
                            op_color_near_points.append((x, y))
        l = [0, 1, 2, 3, 4, 5, 6, 7]
        for p in op_color_near_points:
            if self._can_fliped(p, color):
                # �ж�p�ǲ����������꣬������򷵻���������
                # p = self.board_num(p)
                if p[0] in l and p[1] in l:
                    p = self.num_board(p)
                yield p

    def board_num(self, action):
        """
        ��������ת��Ϊ��������
        :param action:�������꣬����A1
        :return:�������꣬���� A1 --->(0,0)
        """
        row, col = str(action[1]).upper(), str(action[0]).upper()
        if row in '12345678' and col in 'ABCDEFGH':
            # ������ȷ
            x, y = '12345678'.index(row), 'ABCDEFGH'.index(col)
            return x, y

    def num_board(self, action):
        """
        ��������ת��Ϊ��������
        :param action:�������� ,����(0,0)
        :return:�������꣬���� ��0,0��---> A1
        """
        row, col = action
        l = [0, 1, 2, 3, 4, 5, 6, 7]
        if col in l and row in l:
            return chr(ord('A') + col) + str(row + 1)

# # # ����
# if __name__ == '__main__':
#     board = Board()  # ���̳�ʼ��
#     board.display()
#     print("----------------------------------X",list(board.get_legal_actions('X')))
#     # print("��ӡD2����ΪX",board._move('D2','X'))
#     print("==========",'F1' in list(board.get_legal_actions('X')))
#     # print('E2' in list(board.get_legal_actions('X')))
