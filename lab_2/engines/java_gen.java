import java.util.Random;

public class RandomBinaryGenerator {
    public static void main(String[] args) {
        int size = 10;
        String randomBinarySequence = generateRandomBinarySequence(size);
        System.out.println("Случайная последовательность бинарных чисел: " + randomBinarySequence);
    }

    public static String generateRandomBinarySequence(int size) {
        Random random = new Random();
        StringBuilder binarySequence = new StringBuilder();

        for (int i = 0; i < size; i++) {
            int randomBit = random.nextInt(2);
            binarySequence.append(randomBit);
        }

        return binarySequence.toString();
    }
}
