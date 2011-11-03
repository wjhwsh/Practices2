%{
    int yylineno;
%} 


%%

[0-9]+   {
    //FILE *fp = fopen("qq.txt", "a");
    //fprintf(fp, "%s\n", yytext);
    //fclose(fp);
}

addIndexType(.*); {
    FILE *fp = fopen("qq.txt", "a");
    fprintf(fp, "%s\n", yytext);
    fclose(fp);
}

%%


int yywrap(void) {
        return 1;
}

int main(int argc, char **argv) {
    yyin = fopen(argv[1], "r"); 
    yylex(); 
    fclose(yyin);
    return 0;
}
