
       void main()
        {
            yyparse();
        }
        int yyerror(char* msg)
        {
        printf("Error: %s
        encountered \n", msg);

