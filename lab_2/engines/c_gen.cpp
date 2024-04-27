#include <iostream>
#include <cstdlib>
#include <ctime>
#include <sstream>

using namespace std;

// Генерация случайной последовательности бинарных чисел заданного размера
string generateRandomBinarySequence(int size) {
    string binarySequence = "";
    for (int i = 0; i < size; ++i) {
        int randomBit = rand() % 2;
        stringstream ss;
        ss << randomBit;
        binarySequence += ss.str();
    }
    return binarySequence;
}

int main() {
    srand(time(0));

    int size;
    cout << "Введите размер последовательности бинарных чисел: ";
    cin >> size;

    string binarySequence = generateRandomBinarySequence(size);

    cout << "Случайная последовательность бинарных чисел размером " << size << ":\n";
    cout << binarySequence << endl;

    return 0;
}