%{
    #include <stdio.h>

    FILE *yyin, *fout;

    int yylex(void);
    void yyerror(char *);

    enum BOARD_TYPE {
        ODM_BOARD_NORMAL = 1, 
        ODM_BOARD_HIGHPWR = 2, 
        ODM_BOARD_MINICARD = 4, 
        ODM_BOARD_SLIM = 8, 
        ODM_BOARD_COMBO = 10
    };
    enum BUS_TYPE {
        RT_PCI_INTERFACE = 1, 
        RT_USB_INTERFACE = 2, 
        RT_SDIO_INTERFACE = 4, 
    };
    enum SUPPORT_TYPE {
        ODM_AP = 1, 
        ODM_ADSL = 2, 
        ODM_CE = 4, 
        ODM_MP= 8, 
    };

    char *odm1;
    char *odm2;

    unsigned int board_num, support_num, bus_num;
    unsigned int hex[1000], body[1000], idx;
    unsigned int body_line_count, count;
    unsigned int start_hex, elseif_start;

    int xtod(char c); 
    int HextoDec(const char *hex);
    int xtoi(const char *hex);   // hex string to integer
    void CalculateTypeNumber(const char *key, const char *value);
    void StoreOffsetInfo(); 
%}

%union {
    const char *str;
    int num;
};

%token <str> ID HW_PARAM
%token <str> EQ_OP NE_OP AND_OP OR_OP ASSIGN
%token IF ELSE COMMENT_START COMMENT_END

%start program

%%

program:
        if_condition condition
        ;
condition:
        elseif_condition condition
        | else_condition
        |
        ;
elseif_condition:
        ELSE if_expression body {
            hex[idx] += board_num;
            hex[idx] += bus_num << 8;
            hex[idx] += support_num << 16;
            hex[idx] += 0xFF000000;
            printf("%X 0xCDEF\n", hex[idx]);
            fprintf(fout, "\n\n0x%08X, 0xCDEF,\n\n", hex[idx]);
            //fprintf(fout, "%X 0xCDEF\n", hex[idx]);

            int i;
            for ( i = 0; i < count; ++i) {
                printf("\t0x%03X 0x%08X\n", body[2*i], body[2*i + 1]);
                fprintf(fout, "0x%03X, 0x%08X, ", body[2*i], body[2*i + 1]);
            }

        }
        ;
else_condition:
        ELSE body {
            int i = 0, result = 0;
            //for (i = 0; i < idx; ++i)
            //    printf("[%d]: %x\n", i, hex[i]);
            for (i = 0; i < idx; ++i) 
                result |= hex[i];
            result = ~result;
            result &= 0x000F071F;
            result |= 0xFF000000;
            printf("%X 0xCDCD\n", result);
            fprintf(fout, "\n\n0x%08X, 0xCDCD, \n\n", result);

            for ( i = 0; i < count; ++i) {
                printf("\t0x%03X 0x%08X\n", body[2*i], body[2*i + 1]);
                fprintf(fout, "0x%03X, 0x%08X, ", body[2*i], body[2*i + 1]);
            }

            printf("%X 0xDEAD\n", start_hex);
            fprintf(fout, "\n\n0x%08X, 0xDEAD", start_hex);
            fprintf(fout, " };\n");
        }
        ;

if_condition:
        if_expression body {
            hex[idx] += board_num;
            hex[idx] += bus_num << 8;
            hex[idx] += support_num << 16;
            hex[idx] += 0xFF000000;
            if (start_hex == 0) {
                start_hex = hex[0];
                printf("%X 0xABCD\n", start_hex);
                fprintf(fout, "const unsigned int PHY_REG_1TArray[] = { ");
                fprintf(fout, "\n\n0x%08X, 0xABCD,\n\n", start_hex);
            }
            idx++;

            int i;
            for ( i = 0; i < count; ++i) {
                printf("\t0x%03X 0x%08X\n", body[2*i], body[2*i + 1]);
                fprintf(fout, "0x%03X, 0x%08X, ", body[2*i], body[2*i + 1]);
            }

            // reset
            board_num = support_num = bus_num = 0;
        }
        ;

if_expression:
        IF '(' primary_expr ')' 
        ;
primary_expr:
        or_expr AND_OP primary_expr
        | or_expr
        ;
or_expr:
        | '(' single_expr ')'  
        | single_expr  
        | '(' single_expr OR_OP or_expr ')' 
        | single_expr OR_OP or_expr  
        ;

single_expr:
        ID EQ_OP ID { 
                odm1 = strdup($1); 
                odm2 = strdup($3); 
                
                CalculateTypeNumber(odm1, odm2);

                //printf("\n[%s][%s]\n", $1, $3); 
          }
        | ID NE_OP ID { 
          }
        ;

body:
        hw_param_statement { 
            StoreOffsetInfo();
        }
        | '{' hw_param_statement '}' {
            StoreOffsetInfo();
        }
        | '{' hw_param_statement hw_param_statement '}' { 
            StoreOffsetInfo();
        }
        ;

hw_param_statement:
        hw_param_statement HW_PARAM HW_PARAM { 
            int i = body_line_count;
            body[2*i] = xtoi($2);
            body[2*i + 1] = xtoi($3);
            body_line_count++; 
        } 
        | HW_PARAM HW_PARAM { 
            int i = body_line_count;
            body[2*i] = xtoi($1);
            body[2*i + 1] = xtoi($2);
            body_line_count++; 
        } 
        | ';'
        |
        ;

%%

void StoreOffsetInfo() {
            count = body_line_count;
            if (elseif_start)
                ;//printf("%X 0xCDEF\n", hex[idx-1]);
            int i;
            for (i = 0; i < body_line_count; ++i) {
                //printf("\t%X, %X, ", body[i], body[i+1]);
                //printf("\n");
            }
            if (elseif_start == 0)
                elseif_start = 1;
            body_line_count = 0;
}

void CalculateTypeNumber(const char *key, const char *value) 
{
    if (strcmp(key, "ODM_BOARD_TYPE") == 0) {
        if (strcmp(value, "ODM_BOARD_NORMAL") == 0) {
            board_num += ODM_BOARD_NORMAL;
        } else if (strcmp(value, "ODM_BOARD_HIGHPWR") == 0) {
            board_num += ODM_BOARD_HIGHPWR;
        } else if (strcmp(value, "ODM_BOARD_MINICARD") == 0) {
            board_num += ODM_BOARD_MINICARD;
        } else if (strcmp(value, "ODM_BOARD_SLIM") == 0) {
            board_num += ODM_BOARD_SLIM;
        } else if (strcmp(value, "ODM_BOARD_COMBO") == 0) {
            board_num += ODM_BOARD_COMBO;
        } else {
            printf("ODM_BOARD_TYPE value error: (key, value) = ((%s), (%s))\n", key, value);
        }
        //printf("\nCalculateTypeNumber: %s: %u\n", key, board_num);
    } else if (strcmp(key, "DEV_BUS_TYPE") == 0) {
        if (strcmp(value, "RT_PCI_INTERFACE") == 0) {
            bus_num += RT_PCI_INTERFACE;
        } else if (strcmp(value, "RT_USB_INTERFACE") == 0) {
            bus_num += RT_USB_INTERFACE;
        } else if (strcmp(value, "RT_SDIO_INTERFACE") == 0) {
            bus_num += RT_SDIO_INTERFACE;
        } else {
            printf("DEV_BUS_TYPE value error\n");
        }
        //printf("\nCalculateTypeNumber: %s: %u\n", key, bus_num);
    } else if (strcmp(key, "ODM_SUPPORT_TYPE") == 0) {
        if (strcmp(value, "ODM_AP") == 0) {
            support_num += ODM_AP;
        } else if (strcmp(value, "ODM_ADSL") == 0) {
            support_num += ODM_ADSL;
        } else if (strcmp(value, "ODM_CE") == 0) {
            support_num += ODM_CE;
        } else if (strcmp(value, "ODM_MP") == 0) {
            support_num += ODM_MP;
        } else {
            printf("ODM_SUPPORT_TYPE value error\n");
        }
        //printf("\nCalculateTypeNumber: %s: %u\n", key, support_num);
    } else {
        printf("No such type!\n");
    }
}

int xtod(char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    return 0;        // not Hex digit
}
int HextoDec(const char *hex)
{
    if (*hex == 0) return 0;
        return  HextoDec(hex-1) * 16 +  xtod(*hex) ; 
}
 
int xtoi(const char *hex)      // hex string to integer
{
    return HextoDec( hex + strlen(hex) - 1 );
}

void yyerror(char *s) {
    fprintf(stderr, "Unknown token: %s\n", s);
}

void parseAndPrintTextFile(int argc,  char **argv) {
//int main(int argc, char **argv) {

    fout = fopen("rtl8192cu/BB/Hal8192CUHWImg_BB.c", "w+");
    if (argc > 1) {
        yyin = fopen("rtl8192cu/BB/PHY_REG_1T.txt", "r");
        yyparse(); /* Calls yylex() for tokens. */
    } else {
        printf("syntax: %s filename\n", argv[0]);
    }
    fclose(fout);

//    return 0;
}
