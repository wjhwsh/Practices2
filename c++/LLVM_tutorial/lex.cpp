#include <iostream>

using namespace std;

enum Token {
    tok_eof = -1,
    tok_def = -2,
    tok_extern = -3,
    tok_identifier = -4,
    tok_number = -5,
};

static string IdentifierStr;
static double NumVal;

//the Lexer function
static int gettok() {
    static int LastChar = ' ';

    // no whitespace
    while(isspace(LastChar))
        LastChar = getchar();

    // identifiers and specific keywords
    if( isalpha(LastChar) ) {
        IdentifierStr = LastChar;
        while(isalnum(LastChar = getchar()) ) 
            IdentifierStr += LastChar;

        if(IdentifierStr == "def")
            return tok_def;
        if(IdentifierStr == "extern")
            return tok_extern;
        return tok_identifier;
    }

    // numbers, including floating numbers
    if(isdigit(LastChar) || LastChar == '.') {
        string NumStr;
        do {
            NumStr += LastChar;
            LastChar = getchar();
        } while(isdigit(LastChar) || LastChar == '.');
        NumVal = strtod(NumStr.c_str(), 0);
        return tok_number;
    }

    // comments
    if(LastChar == '#') {
        // ignore one line 
        do 
            LastChar = getchar();
        while(LastChar != EOF && LastChar != '\n' && LastChar != '\r');

        // we have nothing to return from one commented line, so if not the EOF, lex it again to get token.
        if(LastChar != EOF)
            return gettok();
    }

    // EOF
    if(LastChar == EOF)
        return tok_eof;
    
    // Otherwise, just return the character as its ascii value
    int ThisChar = LastChar; 
    LastChar = getchar();
    return ThisChar;
}



int main( int argc, char **argv) {
    int i ;
    for(i = 0; i < 10; i++) {
        int a = gettok();
        cout << a << endl;
    }
    //static int LastChar = 'j';
    //while(! isspace(LastChar)) {
    //    LastChar = getchar();
    //    cout << LastChar << endl;
    //    if (isspace(LastChar))
    //        cout << "YES" << endl;
    //}
    return 0;
}
