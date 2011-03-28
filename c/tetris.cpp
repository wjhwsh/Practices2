#include <windows.h>
#include <iostream>
#include <stdio.h>
#include <conio.h>
#include <time.h>
using namespace std ;
#define set_color(c) SetConsoleTextAttribute(hOut,c)

enum {H=23, W=14, nBlock=7};                //畫面長寬, 方塊數目
HANDLE hIn, hOut;                           //I/O 控制器
bool   bExit = false;                       //是否持續遊戲
int    level=0, score=0;                    //關卡, 積分
int    ox=4, oy=1;                          //畫面左上原點
int    B, N;                                //當前&下一個 方塊的編號
int    X, Y, dir=0;                         //方塊位置, 所處方位(0~3)
int    delay_time = 20;                     //延遲時間
int    flexible_time = 20;                  //加速按鍵控制的程度
char   room[W][H];                          //畫面
int    block[nBlock][4] =                   //方塊樣式
       {{0x6220,0x1700,0x2230,0x0740},      // L
        {0x6440,0x0e20,0x44c0,0x8e00},      // _|
        {0x04e0,0x0464,0x00e4,0x04c4},      // T
        {0x4620,0x6c00,0x4620,0x6c00},      // z
        {0x2640,0xc600,0x2640,0xc600},      // 反z
        {0x0f00,0x4444,0x0f00,0x4444},      // |
        {0x0660,0x0660,0x0660,0x0660}};     // 田

void gotoxy (int x, int y)
{
    static COORD c; c.X = x; c.Y = y;
    SetConsoleCursorPosition (hOut, c);
}
void draw (int x, int y, char* s) {gotoxy (x*2,y); cout<<s;}
void over (int x, int y, char* s) {draw(x,y,s);getch();exit(1);}

bool bMove_block (int bx, int by, int d)        //傳入新位置與旋轉方向
{                                               //檢驗方塊能否變動     
    for (int p = 0x8000, x, y=0; y<4; y++)
        for (x=0; x<4; x++, p>>=1) 
            if ((block[B][d]&p) && room[bx+x-ox][by+y-oy])
                return false;
    return true; 
} 

void show_next_block (char* s)
{
    set_color (N+7);                            //設定顯示色
    int x, y, p = 0x8000; 
    for (y=0; y<4; y++)
        for (x=0; x<4; x++, p>>=1) 
            if (block[N][0] & p) draw (ox+W+2+x, 2+y, s);
}
void show_block (char* s)
{
    set_color (B+7);                            //設定顯示色
    int x, y, p = 0x8000; 
    for (y=0; y<4; y++)
        for (x=0; x<4; x++, p>>=1) 
            if (block[B][dir] & p) draw (x+X, y+Y, s);
}
void show_room()
{
    for (int x,y=0; y<H; y++)
        for (x=0; x<W; x++)
            if (room[x][y]) {
                set_color (room[x][y]);
                draw (ox+x, oy+y, "█");
            }else draw (ox+x, oy+y, "  ");
}

void try_move_block (int x, int y, int d)       //嘗試移動
{
    if (!bMove_block (x,y,d)) return;
    show_block ("  "); X = x; Y = y; dir = d;
    show_block ("█");
}

int remove_lines()
{
    int x, y, i,j, line=0;
    for (y=1; y<H-1; y++) {
        for (x=1; x<W-1; x++) 
            if (!room[x][y]) break;
        if (x==W-1) {
            line++;
            for (i=1; i<W-1; i++) room[i][0] = 0;
            for (i=y; i>1; i--) 
                for (j=1; j<W-1; j++) 
                    room[j][i] = room[j][i-1];
            show_room ();
        }        
    }return line;
}

void move_block()
{
    if (bMove_block (X,Y+1,dir)) {try_move_block (X,Y+1,dir); return;}
    if (Y==0) over (ox+2, H/2, "G a m e    O v e r");
         
    for (int p = 0x8000, x, y=0; y<4; y++)
        for (x=0; x<4; x++, p>>=1) 
            if (block[B][dir] & p) 
                room[X+x-ox][Y+y-oy] = B+7; 

    int n = remove_lines();
    level = (score+=(1+n*n)*4)/200;
    delay_time = 10-level;
    if (level > 10) over (ox+4, H/2, "Y o u    W i n");
    
    show_next_block ("  ");
    B = N; X = ox+W/2-1; Y = 0; 
    N = rand() % nBlock;
    show_next_block ("█");       
}

void init()                                     //初始配置
{
    srand (time(0));
    hOut = GetStdHandle (STD_OUTPUT_HANDLE);
    hIn  = GetStdHandle (STD_INPUT_HANDLE);
    HANDLE err = INVALID_HANDLE_VALUE;
    if (hIn == err || hOut == err) {
        puts ("handle failed"); getch (); exit (1);
    }    
    for (int x=0; x<W; x++) room[x][H-1] = 4;  
    for (int y=0; y<H; y++) room[0][y] = room[W-1][y] = 4;
    
    B = rand() % nBlock;
    N = rand() % nBlock;
    X = ox+W/2-1; 
    Y = 0;
    show_room();   
    show_next_block ("█");
}

void key_control()                              //按鍵控制
{
    static DWORD count;
    static INPUT_RECORD ir;    
    ReadConsoleInput (hIn, &ir, 1, &count);
    if (!ir.Event.KeyEvent.bKeyDown) return;                       
    
    switch (ir.Event.KeyEvent.wVirtualKeyCode) {                    
        case VK_ESCAPE: bExit = true; break;
        case VK_DOWN : try_move_block (X,Y+1,dir); break;
        case VK_LEFT : try_move_block (X-1,Y,dir); break;
        case VK_RIGHT: try_move_block (X+1,Y,dir); break;
        case VK_UP   : try_move_block (X,Y,(dir+1)&3); break;
    }        
}

void main ()                                    //主程式
{
    int i; init();
    while (!bExit)
    {     
        for (i=0; i<flexible_time; i++) {       //加速按鍵處理       
            if (kbhit()) key_control();
            Sleep (delay_time);
        }          
        move_block ();          
        set_color (14);
        gotoxy (ox+W*2+8, 10); cout<< "Level: "<<level+1;
        gotoxy (ox+W*2+8, 12); cout<< "Score: "<<score;
    }
}
