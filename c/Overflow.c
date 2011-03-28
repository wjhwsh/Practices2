#include <stdio.h>
#include <stdint.h>

int main() {
    long long a = -2147483648;
    printf("%lld\n", a+a/2);
    return 0;
}
