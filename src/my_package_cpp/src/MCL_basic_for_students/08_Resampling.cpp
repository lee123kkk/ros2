#include <iostream>
using namespace std;

double w[] = { 0.6, 1.2, 2.4, 0.6, 1.2 };

//TODO: Define a ComputeProb function and compute the Probabilities
void ComputeProb(double w[], int n) {
    double sum = 0.0;
    
    // 1. 모든 가중치의 합 구하기
    for(int i = 0; i < n; i++) {
        sum += w[i];
    }
    
    // 2. 각 가중치를 총합으로 나누어 확률로 변환하고 출력하기
    for(int i = 0; i < n; i++) {
        w[i] = w[i] / sum;
        cout << "P" << i + 1 << "=" << w[i] << endl;
    }
}

int main()
{
    //TODO: Print Probabilites each on a single line
    int n = sizeof(w) / sizeof(w[0]);
    ComputeProb(w, n);
    
    return 0;
}
