ID [A-Z]+_[A-Z_]+
%{
    
    #include "y.tab.h"
    #include <stdlib.h>

#define YY_NO_UNISTD_H 1

    void comment();
    void yyerror(char *);
%}


%%

{ID}              {
                      yylval.str = strdup(yytext);
                      //printf("%s\n", yytext);
                      return ID;
                  }

"("               {   return('('); }
")"               {   return(')'); }

("{"|"<%")        {   return('{'); }
("}"|"%>")        {   return('}'); }

"=="              {   return(EQ_OP); }
"!="              {   return(NE_OP); }
"&&"              {   return(AND_OP); }
"||"              {   return(OR_OP); }
";"               {   return(';'); }
"<-"              {   return(ASSIGN); }

0x[0-9A-Fa-f]+    {   
                      yylval.str = strdup(yytext);
                      //printf("%s\n", yytext);
                      return HW_PARAM; 
                  }

"if"              {   return IF;}
"else"            {   return ELSE;}
"/*"              {   comment(); }

[ \t\v\n\f]       ;       /* skip whitespace */

\/\/[^\n]*\n      ;

.                 ;       //yyerror(yytext);

%%

void comment() {
    char c, c1, c2; 

loop:
    //while ((c = input()) != '*' && c != 0)
    //    ;//putchar(c);

    //if ((c1 = input()) != '/' && c != 0) {   
    //    unput(c1);
    //    goto loop;
    //}   
    //if (c != 0)
    //    ;//putchar(c1);

    while ( (c1 = input()) != 0 ) {
        c2 = input();
        if (c1 == '*' && c2 == '/') {
            break;
        }
        unput(c2);
    }
}

int yywrap() {
    return 1;
}
