// version 1 
case 'J': {
    if (Signed) {
      Type = Context.getsigjmp_bufType();
      if (Type.isNull()) {
        Error = ASTContext::GE_Missing_sigjmp_buf;
        return QualType();
      } else {
        break;
      }
    } else {
      Type = Context.getjmp_bufType();
      if (Type.isNull()) {
        Error = ASTContext::GE_Missing_jmp_buf;
        return QualType();
      } else {
        break;
      }
    }
  }
  }

// version 2
  case 'J':
    if (Signed) {
      Type = Context.getsigjmp_bufType();
      if (Type.isNull()) {
        Error = ASTContext::GE_Missing_sigjmp_buf;
        return QualType();
      }
    } else {
      Type = Context.getjmp_bufType();
      if (Type.isNull()) {
        Error = ASTContext::GE_Missing_jmp_buf;
        return QualType();
      }
    }
    break;

// version 3
  case 'J':
    if (Signed)
      Type = Context.getsigjmp_bufType();
    else
      Type = Context.getjmp_bufType();
    
    if (Type.isNull()) {
      Error = Signed ? ASTContext::GE_Missing_sigjmp_buf :
                       ASTContext::GE_Missing_jmp_buf;
      return QualType();
    }
    break;

