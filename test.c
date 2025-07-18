#include <stdio.h>

int main() {
    int number, square;

    // Ask the user for input
    printf("Enter a number: ");
    scanf("%d", &number);

    // Calculate the square
    square = number * number;

    // Print the resultgcc
    printf("Square of %d is %d\n", number, square);

    return 0;
}
