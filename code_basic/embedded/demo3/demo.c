#include <stdio.h>

typedef struct {
    char title[50];
    char author[50];
    int id;
}Book;


int main() {
    Book book = {"The Great Gatsby", "F. Scott Fitzgerald", 1};
    // book.id = 1;
    // book.author = "F. Scott Fitzgerald";
    printf("Enter book title: %s \n", book.title);
    printf("Enter book author: %s \n", book.author);
    printf("Enter book id: %d \n", book.id);

    return 0;
}