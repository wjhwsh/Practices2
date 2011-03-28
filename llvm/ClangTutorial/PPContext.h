#ifndef PP_CONTEXT
#define PP_CONTEXT

#include <string>

#include "llvm/Config/config.h"

#include "clang/Basic/Diagnostic.h"
#include "clang/Basic/TargetInfo.h"
#include "clang/Basic/SourceManager.h"
#include "clang/Basic/FileManager.h"

#include "clang/Lex/HeaderSearch.h"
#include "clang/Lex/Preprocessor.h"


//------- added by Kordan
#include "clang/Basic/SourceLocation.h"
#include "clang/Frontend/TextDiagnosticPrinter.h"
#include "clang/Frontend/DiagnosticOptions.h"

struct PPContext {
  // Takes ownership of client.
    int temp = 0;
  PPContext(clang::DiagnosticClient* client = 0,
            const std::string& triple = LLVM_HOSTTRIPLE,
            llvm::raw_ostream &os = &temp,
            const clang::DiagnosticOptions &diags = &temp,
            bool OwnsOutputStream = false     
           )         
      
    : diagClient( (client == 0) ? (new clang::TextDiagnosticPrinter(os, diags, OwnsOutputStream)) : (client) ),
      diags(diagClient),
      target(clang::TargetInfo::CreateTargetInfo(triple)),
      headers(fm),
      pp(diags, opts, *target, sm, headers)
  {
    // Configure warnings to be similar to what command-line `clang` outputs
    // (see tut03).
    // XXX: move warning initialization to libDriver
    using namespace clang;
    diags.setDiagnosticMapping(diag::warn_pp_undef_identifier,diag::MAP_IGNORE);
  }

  ~PPContext()
  {
    delete diagClient;
    delete target;
  }

  clang::DiagnosticClient* diagClient;
  clang::Diagnostic diags;
  clang::LangOptions opts;
  clang::TargetInfo* target;
  clang::SourceManager sm;
  clang::FileManager fm;
  clang::HeaderSearch headers;
  clang::Preprocessor pp;
};

#endif
