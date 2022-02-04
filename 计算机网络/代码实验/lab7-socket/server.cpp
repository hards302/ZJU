#include <stdio.h>
#include <winsock2.h>
#include <time.h>

//�ͻ�������������͵Ľṹ��
struct text
{
	int type = 0; // 0 is sent message, 1 is get time, 2 is get name, 3 is get list.
	int target = 0; // ֻ����ѡ��6��������Ϣʱ�Ż���
	char data[256];
};

struct ClientInfo {
	char *IP;
	int port;
	int active;
	SOCKET tcp;
} ClientList[10];

u_short SERVER_PORT = 6666; //�����˿�
char serverName[64] = "********Server name: lab7server";
WORD wVersionRequested;
WSADATA wsaData;
int ret, nLeft, length;
SOCKET sListen, sClient, sServer; //�����׽���
struct sockaddr_in saServer, saClient;//��ַ��Ϣ
struct text message;
char *ptr = (char *)&message;
char addr[20];
BOOL fSuccess = TRUE;

void transMSG(SOCKET tcp, struct text *rec)
{
	char *s;
	memcpy(s+8, rec->data, sizeof(rec->data));
	send(ClientList[rec->target].tcp, s, 256, 0);
	printf("Message sent!\n");
}

void getTime(SOCKET tcp)
{
	time_t t;
	time(&t);
	struct tm* tt;
	tt = localtime(&t);
	char s[256];
	sprintf(s, "********The time is: %d.%d.%d %d:%d:%d", (1900 + tt->tm_year), (1 + tt->tm_mon),
		tt->tm_mday, tt->tm_hour, tt->tm_min, tt->tm_sec);
	send(tcp, s, 256, 0);
	printf("Time sent.\n");
}

void getName(SOCKET tcp)
{
	char s[256];
	memcpy(s, serverName, sizeof(serverName));
	send(tcp, s, 256, 0);
	printf("Name sent.\n");
}

void getList(SOCKET tcp)
{
	char s[256];
	strcpy(s, "********Active List:\n");
	for (int i = 0; i < 10; i++) {
		if (ClientList[i].active) {
			char *tmp;
			itoa(i, tmp, 10);
			strcat(s, tmp);
			strcat(s, "\n");
		}
	}
	send(tcp, s, 256, 0);
	printf("List sent.\n");
}

DWORD WINAPI handleClient(LPVOID param)
{
	SOCKET tcp = *((int *)param);
	SOCKADDR_IN ClientInfo = {0};
	int addrsize = sizeof(ClientInfo);
	getpeername(tcp, (struct sockaddr*)&ClientInfo, &addrsize);
	char *IP = inet_ntoa(ClientInfo.sin_addr);
	int port = ClientInfo.sin_port;
	for (int i = 1; i < 10; i++) {
		if (!ClientList[i].active) {
			ClientList[i].active = 1;
			ClientList[i].tcp = tcp;
			ClientList[i].IP = IP;
			ClientList[i].port = port;
			break;
		}
	}
	while (1) {
		char recvPackage[256];
		int recvState = recv(tcp, recvPackage, 256, 0);
		struct text* rec = (struct text*)recvPackage;
		if (recvState > 0) {
			printf("Package received!\n");
			switch (rec->type)
			{
				case 0:
					transMSG(tcp, rec);
					break;
				case 1:
					getTime(tcp);
					break;
				case 2:
					getName(tcp);
					break;
				case 3:
					getList(tcp);
					break;
				default:
					break;
			}
		}
		else {
			printf("Connection closed!\n");
			break;
		}
	}
	int closeflag = 1;
	for (int i = 1; i < 10; i++) {
		if (ClientList[i].tcp == tcp) {
			ClientList[i].active = 0;
			break;
		}
		if(ClientList[i].active == 1) closeflag = 0;
	}
	if(closeflag) {
		closesocket(tcp);
		free(param);
		return 0;
	}
}

int main()
{
	//WinSock��ʼ����
	wVersionRequested = MAKEWORD(2, 2);//ϣ��ʹ�õ�WinSock DLL�İ汾
	ret = WSAStartup( wVersionRequested, &wsaData );
	if (ret != 0)
	{
		printf("WSAStartup() failed!\n");
		return 0;
	}
	//ȷ��WinSock DLL֧�ְ汾2.2��
	if (LOBYTE(wsaData.wVersion) != 2 || HIBYTE( wsaData.wVersion ) != 2 )
	{
		WSACleanup();
		printf("Invalid Winsock version!\n");
		return 0;
	}

	//����socket��ʹ��TCPЭ�飺
	sListen = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if(sListen == INVALID_SOCKET)
	{
		WSACleanup();
		printf("socket() failed!\n");
		return 0;
	}
	
	//�������ص�ַ��Ϣ��
	saServer.sin_family = AF_INET;//��ַ����
	saServer.sin_port = htons(SERVER_PORT);//ע��ת��Ϊ�����ֽ���
	saServer.sin_addr.S_un.S_addr = htonl(INADDR_ANY);//ʹ��INADDR_ANYָʾ�����ַ

	//�󶨣�
	ret = bind(sListen, (struct sockaddr *)&saServer, sizeof(saServer));
	if (ret == SOCKET_ERROR)
	{
		printf("bind() failed! code:%d\n", WSAGetLastError());
		closesocket(sListen);//�ر��׽���
		WSACleanup();
		return 0;
	}

	//������������
	ret = listen(sListen, 5);
	if (ret == SOCKET_ERROR)
	{
		printf("listen() failed! code:%d\n", WSAGetLastError());
		closesocket(sListen);//�ر��׽���
		WSACleanup();
		return 0;
	}

	printf("Waiting for client connecting!\n");
	printf("tips : Ctrl+c to quit!\n");
	//�����ȴ����ܿͻ������ӣ�
	while (1) {
		length = sizeof(saClient);
		sServer = accept(sListen, (struct sockaddr *)&saClient, &length);
		if(sServer == INVALID_SOCKET)
		{
			printf("accept() failed! code:%d\n", WSAGetLastError());
			closesocket(sListen);//�ر��׽���
			WSACleanup();
			return 0;
		}
		HANDLE subThread;
		subThread = CreateThread(NULL, 0, handleClient, &sServer, 0, 0);
	}
	// 	printf("Accepted client: %s:%d\n", 
	// 	inet_ntoa(saClient.sin_addr), ntohs(saClient.sin_port));
	closesocket(sListen);//�ر��׽���
	closesocket(sServer);
	WSACleanup();
}