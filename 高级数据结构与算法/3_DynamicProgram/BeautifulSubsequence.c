#include <stdio.h>
#include <math.h>
#define MAX_N 100000	
#define MO 1000000007
#define max(x,y) ((x)>(y)?(x):(y))
#define min(x,y) ((x)<(y)?(x):(y))
inline long long Rightest1(long long index);
long long GetSum(long long left, long long right, long long* FwTree);		// get sum of [left, right] 
void UpdateTree(long long index, long long x, long long* FwTree);			// update the tree
long long SumFromBegin(long long index, long long* FwTree);					// get sum of [1, index] 

int main(void) 
{
	long long n, diff;
	scanf("%lld %lld", &n, &diff);
	long long element;		// the element in the original sequence
	long long cur_bsn = 0;	// current number of beautiful sequences  

	long long FwTree1[MAX_N + 5] = { 0 };
	long long FwTree2[MAX_N + 5] = { 0 };
	//������Fenwick tree  ��������������1��
	//FwTree[0][]�� ��һ��Ԫ�ر�����ʱ��bsn��				�����ڵ�1����� 
	//FwTree[1][]�� ��һ��Ԫ�ص�2^i����iָ��Ԫ�ص�i�����룩	�����ڵ�2�����

	// initialize the tree2
	scanf("%lld", &element);
	UpdateTree(element, pow(2, 0), FwTree2);

	for (long long i = 1; i < n; i++) {
		scanf("%lld", &element);
		// ��element+/-diff���Ѷ�������ֳ����� �������ִ��� (����������ʱ��bsn�� �� ��2^i) 
		// ԭ���Ǳ����Ѷ������ ����if��֧�������ִ��� ���ڰ��Ѷ�δ����������index�������鴦 
		// ��ʱ��δ���������Ϊ0 ��Ӱ��
		// 1. ������Щ��element������Ѷ����� �����Ǳ�����ʱ��bsn
		long long update1 = (
			GetSum( min(element+diff+1, MAX_N), MAX_N, FwTree1) % MO
			+ GetSum(1, max(element-diff-1, 1), FwTree1) % MO
			) % MO;
		// 2. ������Щ��element���С���Ѷ����� ��2^i (���ǵ�i�������)
		long long update2 = ( GetSum( max(element-diff, 1), min(element+diff, MAX_N), FwTree2)) % MO;
		// �ϲ��õ� Ϊ�˵õ���ǰbsn Ӧ�ӵ�ֵ
		long long update = (update1 + update2) % MO;
		cur_bsn = (cur_bsn + update) % MO;		//update current number of beautiful sequences

		UpdateTree(element, update, FwTree1);		//update tree1
		UpdateTree(element, pow(2, i), FwTree2);	//update tree2
	}
	printf("%lld", cur_bsn);
	return 0;
}

long long GetSum(long long left, long long right, long long* FwTree)	//get sum of [left, right] 
{
	return(SumFromBegin(right, FwTree) - SumFromBegin(left - 1, FwTree));
}
void UpdateTree(long long index, long long x, long long* FwTree)	//����(Ĭ��Ϊ+x)
{
	//���� �Ӹ���indexҶ�ڵ�����·�ϵ����е�
	while (index < MAX_N) {
		FwTree[index] = (FwTree[index] + x) % MO;
		index += Rightest1(index);	//index����Rightest1��ֵ�� ��Ϊ���ڵ�
	}
}
long long SumFromBegin(long long index, long long* FwTree)		//get sum of [1, index]
{
	long long sum = 0;
	while (index > 0) {
		sum = (sum + FwTree[index]) % MO;
		index -= Rightest1(index);	//index�Լ�Rightest1��ֵ�� ��ΪΪ���������� ��Ҫ�ӵ����ڵ�
	}
	return sum;
}
long long Rightest1(long long index)
{
	return(index&(-index));
} //ֻ�����ҵ�1���� ������0 ��ֵ
