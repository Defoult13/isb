#include <iostream>
#include <cstdlib>
#include <ctime>
#include <sstream>

using namespace std;

// Генерация случайной последовательности бинарных чисел заданного размера
string generateRandomBinarySequence(int size) {
    string binarySequence = "";
    for (int i = 0; i < size; ++i) {
        int randomBit = rand() % 2; // Генерируем случайный бит (0 или 1)
        stringstream ss;
        ss << randomBit; // Преобразуем бит в строку и добавляем к последовательности
        binarySequence += ss.str();
    }
    return binarySequence;
}

int main() {
    srand(time(0)); // Инициализация генератора случайных чисел текущим временем

    int size;
    cout << "Введите размер последовательности бинарных чисел: ";
    cin >> size;

    string binarySequence = generateRandomBinarySequence(size);

    cout << "Случайная последовательность бинарных чисел размером " << size << ":\n";
    cout << binarySequence << endl;

    return 0;
}