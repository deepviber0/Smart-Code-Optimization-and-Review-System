#include <stdio.h>
#define CONST_MACRO 100

void doSomething() {
    for (int i = 0; i < 10; i++) {
        int x = 50 * CONST_MACRO;
        printf("%d", x);
    }
}
