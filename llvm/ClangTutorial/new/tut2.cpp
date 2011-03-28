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
	TextDiagnosticPrinter tdp(ost);
	Diagnostic diag(&tdp);
	LangOptions lang;
	SourceManager sm;
	FileManager fm;
	HeaderSearch headers(fm);
	TargetInfo *ti = TargetInfo::CreateTargetInfo(LLVM_HOSTTRIPLE);
	Preprocessor pp(diag, lang, *ti, sm, headers);

	const FileEntry *file = fm.getFile("foo.c");
	sm.createMainFileID(file, SourceLocation());
	pp.EnterMainSourceFile();

	Token Tok;

	do {
		pp.Lex(Tok);
		if(diag.hasErrorOccurred())
			break;
		pp.DumpToken(Tok);
		std::cerr << std::endl;
	} while(Tok.isNot(tok::eof));

	return 0;
}
