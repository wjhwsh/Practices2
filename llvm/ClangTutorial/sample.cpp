#include <iostream>
#include "llvm/Support/raw_ostream.h"
#include "llvm/Support/Host.h"
#include "clang/Frontend/DiagnosticOptions.h"
#include "clang/Frontend/TextDiagnosticPrinter.h"
#include "clang/Basic/LangOptions.h"
#include "clang/Basic/FileSystemOptions.h"
#include "clang/Basic/SourceManager.h"
#include "clang/Lex/HeaderSearch.h"
#include "clang/Basic/FileManager.h"
#include "clang/Frontend/HeaderSearchOptions.h"
#include "clang/Frontend/Utils.h"
#include "clang/Basic/TargetOptions.h"
#include "clang/Basic/TargetInfo.h"
#include "clang/Lex/Preprocessor.h"
#include "clang/Frontend/PreprocessorOptions.h"
#include "clang/Frontend/FrontendOptions.h"
#include "clang/Basic/IdentifierTable.h"
#include "clang/Basic/Builtins.h"
#include "clang/AST/ASTContext.h"
#include "clang/AST/ASTConsumer.h"
#include "clang/Sema/Sema.h"
#include "clang/AST/DeclBase.h"
#include "clang/AST/Type.h"
#include "clang/AST/Decl.h"
#include "clang/Sema/Lookup.h"
#include "clang/Sema/Ownership.h"
#include "clang/AST/DeclGroup.h"
#include "clang/Parse/Parser.h"
#include "clang/Parse/ParseAST.h"

#include "clang/Basic/Version.h"
#include "clang/Frontend/CompilerInvocation.h"
#include "clang/Frontend/FrontendAction.h"
int main()
{
    clang::DiagnosticOptions diagnosticOptions;
    llvm::IntrusiveRefCntPtr<clang::DiagnosticIDs> pDiagIDs;
    clang::TextDiagnosticPrinter *pTextDiagnosticPrinter =
        new clang::TextDiagnosticPrinter(llvm::outs(), diagnosticOptions);
    clang::Diagnostic diagnostic(pDiagIDs, pTextDiagnosticPrinter);
    
    clang::LangOptions languageOptions;
    //languageOptions.CPlusPlus= 1;
    clang::CompilerInvocation::setLangDefaults(languageOptions, clang::IK_CXX);


    clang::FileSystemOptions fileSystemOptions;
    clang::FileManager fileManager(fileSystemOptions);
    clang::SourceManager sourceManager(diagnostic, fileManager);


    clang::HeaderSearch headerSearch(fileManager);
    clang::HeaderSearchOptions headerSearchOptions;
    headerSearchOptions.AddPath("/usr/include/linux",
            clang::frontend::Angled,
            false,
            false,
            false);
    headerSearchOptions.AddPath("/usr/include/c++/4.4",
            clang::frontend::Angled,
            false,
            false,
            false);

    headerSearchOptions.AddPath("/usr/include/c++/4.4/tr1",
            clang::frontend::Angled,
            false,
            false,
            false);
    headerSearchOptions.ResourceDir = "/home/modcarl/llvm-2.8/lib/clang/2.9/";
    
    clang::TargetOptions targetOptions;
    targetOptions.Triple = llvm::sys::getHostTriple();

    clang::TargetInfo *pTargetInfo = 
        clang::TargetInfo::CreateTargetInfo(
            diagnostic,
            targetOptions);

    clang::ApplyHeaderSearchOptions(
        headerSearch,
        headerSearchOptions,
        languageOptions,
        pTargetInfo->getTriple());

    clang::Preprocessor preprocessor(
        diagnostic,
        languageOptions,
        *pTargetInfo,
        sourceManager,
        headerSearch);

    clang::PreprocessorOptions preprocessorOptions;
    clang::FrontendOptions frontendOptions;
    clang::InitializePreprocessor(
        preprocessor,
        preprocessorOptions,
        headerSearchOptions,
        frontendOptions);
    const clang::FileEntry *pFile = fileManager.getFile("test.cpp");
    sourceManager.createMainFileID(pFile);

    const clang::TargetInfo &targetInfo = *pTargetInfo;

    clang::IdentifierTable identifierTable(languageOptions);
    clang::SelectorTable selectorTable;

    clang::Builtin::Context builtinContext(targetInfo);
    clang::ASTContext astContext(
        languageOptions,
        sourceManager,
        targetInfo,
        identifierTable,
        selectorTable,
        builtinContext,
        0);
    clang::ASTConsumer astConsumer;
    pTextDiagnosticPrinter->BeginSourceFile(languageOptions, &preprocessor);
    clang::ParseAST(preprocessor, &astConsumer, astContext); 

    pTextDiagnosticPrinter->EndSourceFile();

    return 0;
}
