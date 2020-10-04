// C_Programing_ThirdClass.cpp : 이 파일에는 'main' 함수가 포함됩니다. 거기서 프로그램 실행이 시작되고 종료됩니다.
//

#include <iostream>

using namespace std;
int main()
{
	/* 예제1 (각 가로 세로의 길이의 연산을 받아 넓이 구하는 방식)
	cout << "가로 길이 입력>>";
	int width;
	cin >> width;

	cout << "세로 길이 입력>>";
	int height;
	cin >> height;

	int area = width * height;
	cout << "전체 넓이는: " << area << "\n";
	*/

	/*예제2 (연속 연산 사용 하여 넒이 구함)*/
	cout << "가로와세로 길이 입력>>";
	int width;
	int height;
	cin >> width >> height;

	int area = width * height;
	cout << "전체 넓이는: " << area << "\n";
	

}

