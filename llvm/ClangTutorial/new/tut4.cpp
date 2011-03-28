#include <iostream>

#include <llvm/Support/raw_ostream.h>

#include <clang/Basic/Diagnostic.h>
#include <clang/Basic/TargetInfo.h>
#include <clang/Basic/FileManager.h>
#include <clang/Lex/Preprocessor.h>
#include <clang/Lex/HeaderSearch.h>
#include <clang/Frontend/TextDiagnosticPrinter.h>
#include <clang/Frontend/InitHeaderSearch.h>
#include <clang/Frontend/InitPreprocessor.h>
#include <clang/Basic/IdentifierTable.h>
#include <clang/Parse/Action.h>
#include <clang/Parse/Parser.h>

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
	InitHeaderSearch init(headers);
	init.AddDefaultSystemIncludePaths(lang);
	init.Realize();
	TargetInfo *ti = TargetInfo::CreateTargetInfo(LLVM_HOSTTRIPLE);
	Preprocessor pp(diag, lang, *ti, sm, headers);

	PreprocessorInitOptions ppio;
	InitializePreprocessor(pp, ppio);

	const FileEntry *file = fm.getFile("foo.c");
	sm.createMainFileID(file, SourceLocation());
	pp.EnterMainSourceFile();

	IdentifierTable tab(lang);
	MinimalAction action(pp);
	Parser p(pp, action);
	p.ParseTranslationUnit();
	tab.PrintStats();

	return 0;
}
