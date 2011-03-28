#include <iostream>
#include <vector>
#include <string>


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

static map<char, int> BinopPrecedence;

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

static int CurTok;
static int getNextToken() {
    return CurTok = gettok();
}

//---------------------------------------------------------Parser-----------------------------------------------------------



// Expression
class ExprAST {
    public:
        virtual ~ExprAST() {}
};


// Number
class NumberExprAST: public ExprAST {
    double Val;
    public:
        NumberExprAST(double val): Val(val) {}
};

// Variable
class VariableExprAST: public ExprAST {
    string Name;
    public:
        VariableExprAST(const string &name): Name(name) {}
};

/// Binary Operator
class BinaryExprAST : public ExprAST {
  char Op;
  ExprAST *LHS, *RHS;
public:
  BinaryExprAST(char op, ExprAST *lhs, ExprAST *rhs) 
    : Op(op), LHS(lhs), RHS(rhs) {}
};

/// Function call
class CallExprAST : public ExprAST {
  string Callee;
  vector<ExprAST*> Args;
public:
  CallExprAST(const std::string &callee, std::vector<ExprAST*> &args)
    : Callee(callee), Args(args) {}
};

/// Function Prototype (e.g., name and arguments)
class PrototypeAST {
  string Name;
  vector<std::string> Args;
public:
  PrototypeAST(const std::string &name, const std::vector<std::string> &args)
    : Name(name), Args(args) {}
};


/// Function Definition
class FunctionAST {
  PrototypeAST *Proto;
  ExprAST *Body;
public:
  FunctionAST(PrototypeAST *proto, ExprAST *body)
    : Proto(proto), Body(body) {}
};

// Error-Handling Function
ExprAST *Error(const char *Str) { fprintf(stderr, "Error: %s\n", Str); return 0; }
PrototypeAST *ErrorP(const char *Str) { Error(Str); return 0; }
FunctionAST *ErrorF(const char *Str) { Error(Str); return 0; }

// Precedence
static int GetTokPrecedence() {
    if(!isascii(CurTok))
        return -1;
    int TokPrec = BinopPrecedence[CurTok];
    if(TokPrec <= 0)
        return -1;
    return TokPrec;
}

//------------------------Parser Function-------------------------------
static ExprAST *ParseBinOpRHS(int ExprPrec, ExprAST *LHS) {
    while(1) {
        int TokPrec = GetTokPrecedence();

        if(TokPrec < ExprPrec)
            return LHS;
        
        int BinOp = CurTok;
        getNextToken(); //eat BinOp

        ExprAST *RHS = ParsePrimary();
        if(!RHS) 
            return 0;
        int NextPrec = GetTokPrecedence();
        if(TokPrec < NextPrec) {
          //...
        }


    }
}

static ExprAST *ParseExpression() {
    ExprAST *LSH = ParsePrimary();
    if(!LSH) 
        return 0;
    return ParseBinOpRHS(0, LHS);
}

static ExprAST *ParseParenExpr() {
    getNextToken();
    ExprAST *V = ParseExpression();
    if(!V) 
        return 0;
    if(CurTok != ')')
        Error("Expected '\'");
    getNextToken();
    return V;
}

static ExprAST *ParseIdentifierExpr() {
    string IdName = IdentifierStr;
    
    getNextToken(); // eat identifier

    if(CurTok != '(')
        return new VariableExprAST(IdName);


    getNextToken();  // eat (
    vector<ExprAST*> Args;

    // this Identifier might be a function name for function call
    if(CurTok != ')') {
        while(1) {         // eat "foo" and "bar" of (foo, bar)
            ExprAST *Arg = ParseExpression();
            if(!Arg)
                return 0;
            Args.push_back(Arg);

            if(CurTok == ')')
                break;
            if(CurTok != ',')
                return Error("Expected ')' or ',' in argument list");
            getNextToken();
        }
    }
    
    getNextToken(); // eat )
    return new CallExprAST(Idname, Args);
}

static ExprAST *ParseNumberExpr() {
    ExprAST *Result = new NumberExprAST(NumVal);
    getNextToken();
    return Result;
}


//------------------------End of Parser Function-------------------------------




//---------------------------------------------------------End of Parser-----------------------------------------------------------


int main( int argc, char **argv) {

    BinopPrecedence['<'] = 10;
    BinopPrecedence['+'] = 20;
    BinopPrecedence['-'] = 30;
    BinopPrecedence['*'] = 40; // highest


    int a = gettok();
    std::cout << a << endl;
    //static int LastChar = 'j';
    //while(! isspace(LastChar)) {
    //    LastChar = getchar();
    //    cout << LastChar << endl;
    //    if (isspace(LastChar))
    //        cout << "YES" << endl;
    //}
    return 0;
}
