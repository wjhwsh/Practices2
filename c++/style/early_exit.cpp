// version 1
Something(Instruction *I) {
  if (!isa<TerminatorInst>(I) &&
      I->hasOneUse() && SomeOtherThing(I)) {
    ... some long code ....
  }
  
  return 0;
}

// version 2
Value *DoSomething(Instruction *I) {
  if (isa<TerminatorInst>(I))
    return 0;

  if (!I->hasOneUse())
    return 0;

  if (!SomeOtherThing(I))
    return 0;
    
  ... some long code ....
}

// version 1
for (BasicBlock::iterator II = BB->begin(), E = BB->end(); II != E; ++II) {
    if (BinaryOperator *BO = dyn_cast<BinaryOperator>(II)) {
      Value *LHS = BO->getOperand(0);
      Value *RHS = BO->getOperand(1);
      if (LHS != RHS) {
        ...
      }
    }
  }
// version 2
for (BasicBlock::iterator II = BB->begin(), E = BB->end(); II != E; ++II) {
  BinaryOperator *BO = dyn_cast<BinaryOperator>(II);
  if (!BO) continue;
  
  Value *LHS = BO->getOperand(0);
  Value *RHS = BO->getOperand(1);
  if (LHS == RHS) continue;
  ...
}


