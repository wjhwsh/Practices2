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

class MyAction : public MinimalAction {
	const Preprocessor& pp;
public:
	MyAction(Preprocessor& prep)
		: MinimalAction(prep), pp(prep) {}
	
	virtual Action::DeclPtrTy
	ActOnDeclarator(Scope *S, Declarator &D) {
		// Print names of global variables. Differentiating between
		// global variables and global functions is Hard in C, so this
		// is only an approximation.
		
		const DeclSpec& DS = D.getDeclSpec();
		SourceLocation loc = D.getIdentifierLoc();
		
		if (
			// Only global declarations...
			D.getContext() == Declarator::FileContext
			
			// ...that aren't typedefs or `extern` declarations...
			&& DS.getStorageClassSpec() != DeclSpec::SCS_extern
			&& DS.getStorageClassSpec() != DeclSpec::SCS_typedef
			
			// ...and no functions...
			&& !D.isFunctionDeclarator()
			
			// ...and in a user header
			&& !pp.getSourceManager().isInSystemHeader(loc)
			) {
			IdentifierInfo *II = D.getIdentifier();
			std::cerr << "Found global user declarator " << II->getName() << std::endl;
		}
		
		return MinimalAction::ActOnDeclarator(S, D);
	}
};

int main()
{
	llvm::raw_stdout_ostream ost;
	//DiagnosticOptions dops;
	TextDiagnosticPrinter tdp(ost);//, dops);
	Diagnostic diag(&tdp);
	LangOptions lang;
	//lang.GNUMode = 1;
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
	MyAction action(pp);
	Parser p(pp, action);
	p.ParseTranslationUnit();

	return 0;
}
