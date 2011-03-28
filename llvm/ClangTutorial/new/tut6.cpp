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
#include <clang/Parse/DeclSpec.h>
#include <clang/AST/ASTConsumer.h>
#include <clang/AST/Decl.h>
#include <clang/AST/DeclGroup.h>
#include <clang/Sema/ParseAST.h>
#include <clang/AST/ASTContext.h>

using namespace clang;

class MyASTConsumer : public ASTConsumer {
public:
	virtual void HandleTopLevelDecl(DeclGroupRef D) {
		static int count = 0;
		DeclGroupRef::iterator it;
		for(it = D.begin();
		    it != D.end();
		    it++) {
			//std::cout << *it << std::endl;
			count++;
			//std::cout << "count: " << count << std::endl;
			VarDecl *VD = dyn_cast<VarDecl>(*it);
			if(!VD) continue;
			std::cout << VD << std::endl;
			if(VD->isFileVarDecl() &&
			   VD->getStorageClass() != VarDecl::Extern) {
				std::cerr << "Read top-level variable decl: '" << VD->getDeclName().getAsString() << "'\n";
			}
		}
	}
};

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

	IdentifierTable tab(lang);
	SelectorTable sel;
	Builtin::Context builtins(*ti);
	MyASTConsumer c;
	ASTContext ctx(lang, sm, *ti, tab, sel, builtins);
	ParseAST(pp, &c, ctx, false, true);

	return 0;
}
