%{
    #include <stdio.h>

    FILE *yyin;

    int yylex(void);
    void yyerror(char *);

    enum BOARD_TYPE {
        ODM_BOARD_NORMAL = 1, 
        ODM_BOARD_HIGHPWR = 2, 
        ODM_BOARD_MINICARD = 4, 
        ODM_BOARD_SLIM = 8, 
        ODM_BOARD_COMBO = 10
    };
    enum SUPPORT_TYPE {
        ODM_AP = 1, 
        ODM_ADSL = 2, 
        ODM_CE = 4, 
        ODM_MP= 8, 
    };
    enum BUS_TYPE {
        RT_PCI_INTERFACE = 1, 
        RT_USB_INTERFACE = 2, 
        RT_SDIO_INTERFACE = 4, 
    };
    //enum TEAM_TYPE {
    //    RT_PCI_INTERFACE = 1, 
    //    RT_USB_INTERFACE = 2, 
    //    RT_SDIO_INTERFACE = 4, 
    //};

    char *odm1;
    char *odm2;

    unsigned int board_num, support_num, bus_num, sw_num;

    void CalculateTypeNumber(const char *key, const char *value);
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
        if_condition body condition
        ;
condition:
        else_condition
        | elseif_condition
        |
        ;
else_condition:
        ELSE body
        ;
elseif_condition:
        ELSE if_condition body condition 
        ;

if_condition:
        IF '(' primary_expr ')' { 
            // reset
            printf("\n===================\n\
BOARD:   %u\n\
SUPPORT: %u\n\
BUS:     %u\n\
SW:      %u\n\
===================\n", board_num, support_num, bus_num, sw_num);
            board_num = support_num = bus_num = sw_num = 0;
        }
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

                printf("\n[%s][%s]\n", $1, $3); 
          }
        | ID NE_OP ID { 
          }
        ;

body:
        hw_param_statement 
        | '{' hw_param_statement hw_param_statement '}' 
        ;

hw_param_statement:
        HW_PARAM ASSIGN HW_PARAM ';' 
        | ';'
        |
        ;

%%

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
        printf("\nCalculateTypeNumber: %s: %u\n", key, board_num);
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
        printf("\nCalculateTypeNumber: %s: %u\n", key, bus_num);
    } else if (strcmp(key, "ODM_ODM_SUPPORT_TYPE") == 0) {
        if (strcmp(value, "ODM_AP") == 0) {
            support_num += ODM_AP;
        } else if (strcmp(value, "ODM_ADSL") == 0) {
            support_num += ODM_ADSL;
        } else if (strcmp(value, "ODM_CE") == 0) {
            support_num += ODM_CE;
        } else if (strcmp(value, "ODM_MP") == 0) {
            support_num += ODM_MP;
        } else {
            printf("ODM_ODM_SUPPORT_TYPE value error\n");
        }
        printf("\nCalculateTypeNumber: %s: %u\n", key, support_num);
    } else if (strcmp(key, "SW_TEAM_TYPE") == 0) {
        if (strcmp(value, "") == 0) {
        } else if (strcmp(value, "") == 0) {
        } else if (strcmp(value, "") == 0) {
        } else if (strcmp(value, "") == 0) {
        } else if (strcmp(value, "") == 0) {
        } else {
            printf("SW_TEAM_TYPE value error\n");
        }
        printf("\nCalculateTypeNumber: %s: %u\n", key, sw_num);
    } else {
        printf("No such type!\n");
    }
}

void yyerror(char *s) {
    fprintf(stderr, "%s\n", s);
}

int main(int argc, char **argv) {

    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        yyparse(); /* Calls yylex() for tokens. */
    } else {
        printf("syntax: %s filename\n", argv[0]);
    }

    printf("\n\n\tOh~~~~ %s\n", odm1);

    return 0;
}
