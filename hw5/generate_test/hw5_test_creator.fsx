// Requires existance of completed HW 5

let rec printExpr expr =
    match expr with
    | X -> sprintf "X"
    | Y -> sprintf "Y"
    | Const c -> sprintf "(Const %f)" c
    | Neg e -> sprintf "(Neg (%s))" (printExpr e)
    | Add (e1, e2) -> sprintf "(Add (%s, %s))" (printExpr e1) (printExpr e2)
    | Sub (e1, e2) -> sprintf "(Sub (%s, %s))" (printExpr e1) (printExpr e2)
    | Mul (e1, e2) -> sprintf "(Mul (%s, %s))" (printExpr e1) (printExpr e2)



let genTestAssertions (exprStr: string) (expr: Expression) (desc: string) =
    printfn "test %s %s \"%s\"" exprStr (printExpr (simplify expr)) desc

// Paste in tests gen assertations here
[ genTestAssertions
      "((Mul((Mul((Add((Sub(Y, (Sub(X, Y)))), Y)), X)), (Mul((Mul((Add(Y, X)), (Neg(X)))), (Mul(X, (Add(Y, Y)))))))))"
      ((Mul((Mul((Add((Sub(Y, (Sub(X, Y)))), Y)), X)), (Mul((Mul((Add(Y, X)), (Neg(X)))), (Mul(X, (Add(Y, Y)))))))))
      "Gary's Generated test 0_1645860446" ]
