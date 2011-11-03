%{
    int count = 0;
%}

%%

[0-9]+ count++;
[a-z]+ printf("%s\n", yytext);

%% 

int yywrap(void) {
    return 1;
}

int main(void) { 
    yylex();
    printf("count: %d\n", count);
    return 0;
}
