#include <stdio.h> 
#include <stdlib.h> 
#define NUM 10    //  要拆解的數字 
#define DEBUG 0 

int main(void) { 
    printf("數字拆解\n"); 
    printf("3 = 2+1 = 1+1+1 所以3有三種拆法\n"); 
    printf("4 = 3 + 1 = 2 + 2 = 2 + 1 + 1 = 1 + 1 + 1 + 1");   
    printf("共五種\n"); 
    printf("5 = 4 + 1 = 3 + 2 = 3 + 1 + 1");
    printf(" = 2 + 2 + 1 = 2 + 1 + 1 + 1 = 1 + 1 +1 +1 +1");
    printf("共七種\n"); 
    printf("依此類推，求 %d 有幾種拆法？", NUM); 
    
    int table[NUM][NUM/2+1] = {0}; // 動態規畫表格 
    int count = 0; 
    int result = 0; 

    // 初始化 
    int i;
    for(i = 0; i < NUM; i++){ 
        table[i][0] = 1;  // 任何數以0以下的數拆解必只有1種 
        table[i][1] = 1;  // 任何數以1以下的數拆解必只有1種 
    }        
    // 動態規劃 
    for(i = 2; i <= NUM; i++){ 
       int j;
       for(j = 2; j <= i; j++){ 
            if(i + j > NUM) // 大於 NUM 
                continue; 
            
            count = 0;
            int k;
            for(k = 1 ; k <= j; k++){ 
                count += table[i-k][(i-k >= k) ? k : i-k];
            } 
            table[i][j] = count; 
        }            
    } 

    // 計算並顯示結果 
    int m;
    for(m = 1 ; m <= NUM; m++) 
        result += table[NUM-m][(NUM-m >= m) ? m : NUM-m];
    printf("\n\nresult: %d\n", result); 

    if(DEBUG) { 
        printf("\n除錯資訊\n"); 
        int i;
        for(i = 0; i < NUM; i++) { 
            int j;
            for(j = 0; j < NUM/2+1; j++) 
                 printf("%2d", table[i][j]); 
            printf("\n"); 
        } 
    } 

    return 0; 
}
