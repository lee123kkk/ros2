#include <iostream>
using namespace std;

int main() {
	
	//Given P(POS), P(DOOR|POS) and P(DOOR|¬POS)
	double a = 0.0002 ; //P(POS) = 0.002
	double b = 0.6    ; //P(DOOR|POS) = 0.6
	double c = 0.05   ; //P(DOOR|¬POS) = 0.05
	
	//TODO: Compute P(¬POS) and P(POS|DOOR)
    // 1. 해당 위치에 있지 않을 확률 (전체 확률 1에서 뺌)
    double d = 1.0 - a; //P(¬POS)
    
    // 2. 베이즈 정리 공식 적용: (문에서 위치를 볼 확률 * 위치에 있을 확률) / 전체 문을 볼 확률
    // 전체 문을 볼 확률 = (b * a) + (c * d)
    double e = (b * a) / ((b * a) + (c * d)); //P(POS|DOOR)
	
	//Print Result
	cout << "P(POS|DOOR)= " <<    e    << endl;
	
	return 0;
}