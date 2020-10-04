#include <iostream>
#include <vector>

using namespace std;

int main()
{
	int n = 1;
	char c = '??';

	cout << "Hello World!\n";
	cout << "이남주 서울사이버대학교 2강 학습" << '\n';
	cout << c << "C" << "123" << false << n << "n" << true;

	vector<int> gf;
	// Ctrl + k + d 누르면 자동으로 라인 정리 됨.
	// gf에 데이터 저장
	for (int i = 0; i < 10; i++) {
		gf.push_back(i);
	}
	// gf 저장된 값 출력
	for (int i = 0; i < 10; i++) {
		cout << gf.at(i) << '\n';
	}


	return 0;
}
