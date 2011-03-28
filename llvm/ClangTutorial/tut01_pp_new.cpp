#include <iostream>

#include <llvm/Support/raw_ostream.h>

#include <clang/Basic/Diagnostic.h>
#include <clang/Basic/TargetInfo.h>
#include <clang/Basic/FileManager.h>
#include <clang/Lex/Preprocessor.h>
#include <clang/Lex/HeaderSearch.h>
#include <clang/Frontend/TextDiagnosticPrinter.h>

using namespace clang;

int main()
{
    llvm::raw_stdout_ostream ost;
    TextDiagnosticPrinter tdp(ost);//, dops);
    Diagnostic diag(&tdp);
    LangOptions lang;
    SourceManager sm;
    FileManager fm;
    HeaderSearch headers(fm);
    TargetInfo *ti = TargetInfo::CreateTargetInfo(LLVM_HOSTTRIPLE);
    Preprocessor pp(diag, lang, *ti, sm, headers);

    return 0;
}
