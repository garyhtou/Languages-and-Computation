(*
Gary Tou
CPSC 3400, HW 5 - F# Algebraric Simplifier
2/27/2022
https://seattleu.instructure.com/courses/1602042/assignments/6989795

Code based on preparatory material provided by Professor Kevin Lundeen
*)

// Algebraic expression
type Expression =
    | X
    | Y
    | Const of float
    | Neg of Expression
    | Add of Expression * Expression
    | Sub of Expression * Expression
    | Mul of Expression * Expression

// Pretty-printer for an algebraic expression
let exprToString expr =

    let rec toStr subexpr enclosingPrecedence =
        let parenthesize s myPrecedence =
            if myPrecedence <= enclosingPrecedence then
                s
            else
                (sprintf "(%s)" s)

        match subexpr with
        // precedence 0 are x and y literals
        | X -> "x"
        | Y -> "y"

        // precedence 1 is unary negation
        | Neg (Neg v) -> sprintf "-(-%s)" (toStr v 1) // avoid --ex in favor of -(-ex)
        | Neg u -> parenthesize (sprintf "-%s" (toStr u 1)) 1

        // precedence 2 is a constant (this is bumped up to get -(3) instead of -3 for Neg (Const 3.0))
        | Const c -> parenthesize (sprintf "%g" c) 2

        // precedence 3 for multiplicative ops
        | Mul (u, v) -> parenthesize (sprintf "%s * %s" (toStr u 3) (toStr v 3)) 3

        // precedence 4 for additive ops
        | Add (u, v) -> parenthesize (sprintf "%s + %s" (toStr u 4) (toStr v 4)) 4
        | Sub (u, v) -> parenthesize (sprintf "%s - %s" (toStr u 4) (toStr v 4)) 4

    toStr expr 5



let isVar expr =
    match expr with
    | X -> true
    | Y -> true
    | _ -> false

let isConst expr =
    match expr with
    | Const _ -> true
    | _ -> false

exception NotBaseCondition

let rec simplify (expr: Expression) =
    let simplifyBase (expr: Expression) (raiseError: bool) =
        match expr with
        // TRIVIAL
        | X -> X
        | Y -> Y
        | Const c -> Const c

        // OPERATIONS WITH CONSTANTS
        | Add (Const f1, Const f2) -> Const(f1 + f2)
        | Sub (Const f1, Const f2) -> Const(f1 - f2)
        | Mul (Const f1, Const f2) -> Const(f1 * f2)

        // IDENTITY
        | Add (Const 0.0, e)
        | Add (e, Const 0.0)
        | Sub (e, Const 0.0)
        //Sub (0, ?) is handled below in Negation
        | Mul (Const 1.0, e)
        | Mul (e, Const 1.0) -> simplify e

        // NEGATION
        | Neg (Const 0.0) -> Const 0.0 // No much thing as negative zero
        | Neg (Const f) -> Const(f * float (-1))
        | Sub (Const 0.0, e) -> simplify (Neg e)
        | Neg (Neg e) -> simplify e // Double negation

        // COMPLEMENT (cancel out)
        | Sub (e1, e2) when e1 = e2 -> Const 0.0

        // NULL
        | Mul (Const 0.0, _)
        | Mul (_, Const 0.0) -> Const 0.0

        // FULLY SIMPLIFIED (can't be further simplified)
        | Add (e1, e2)
        | Sub (e1, e2)
        | Mul (e1, e2) as e when
            ((isVar e1 && isVar e2)
             || (isVar e1 && isConst e2)
             || (isConst e1 && isVar e2))
            ->
            e
        | Neg (e) as negE when isVar e || isConst e -> negE
        | _ when raiseError -> raise NotBaseCondition
        | e -> e

    // RECURSIVE BRANCH SIMPLIFICATION
    try
        simplifyBase expr true
    with
    | NotBaseCondition ->
        match expr with
        | Add (e1, e2) -> simplifyBase (Add(simplify e1, simplify e2)) false
        | Sub (e1, e2) -> simplifyBase (Sub(simplify e1, simplify e2)) false
        | Mul (e1, e2) -> simplifyBase (Mul(simplify e1, simplify e2)) false
        | Neg (e) -> simplifyBase (Neg(simplify e)) false
        | e -> e


let testResults =
    let test expr expected description =
        let actual = simplify expr
        printfn "\n%s" description
        printfn "simplify (%s)" (exprToString expr)
        printfn "got: %s" (exprToString actual)

        if actual <> expected then
            printfn "but expected: %s\nFAILED" (exprToString expected)
            false
        else
            printfn "passed"
            true

    [ test (Add(Const 5.0, Const 3.0)) (Const 8.0) "t1 - addition involving two numbers"
      test (Sub(Const 5.0, Const 3.0)) (Const 2.0) "t2 - subtraction involving two numbers"
      test (Mul(Const 5.0, Const 3.0)) (Const 15.0) "t3 - multiplication involving two numbers"
      test (Neg(Const 4.0)) (Const -4.0) "t4 - negation involving a number"
      test (Neg(Const -9.0)) (Const 9.0) "t5 - negation involving a number"
      test (Add(X, Const 0.0)) X "t6 - addition with zero"
      test (Add(Const 0.0, Y)) Y "t7 - addition with zero"
      test (Sub(X, Const 0.0)) X "t8 - subtraction with zero"
      test (Sub(Const 0.0, Y)) (Neg Y) "t9 - subtraction with zero"
      test (Sub(Y, Y)) (Const 0.0) "t10 - subtraction of identical terms"
      test (Mul(X, Const 0.0)) (Const 0.0) "t11 - multiplication with zero"
      test (Mul(Const 0.0, Y)) (Const 0.0) "t12 - multiplication with zero"
      test (Mul(X, Const 1.0)) X "t13 - multiplication with one"
      test (Mul(Const 1.0, Y)) Y "t14 - multiplication with one"
      test (Neg(Neg X)) X "t15 - double negation"
      test (Sub(Mul(Const 1.0, X), Add(X, Const 0.0))) (Const 0.0) "t16 - recursive simplification"
      test (Add(Mul(Const 4.0, Const 3.0), Sub(Const 11.0, Const 5.0))) (Const 18.0) "t17"
      test (Sub(Sub(Add(X, Const 1.0), Add(X, Const 1.0)), Add(Y, X))) (Neg(Add(Y, X))) "t18"
      test (Sub(Const 0.0, Neg(Mul(Const 1.0, X)))) X "t19"
      test (Mul(Add(X, Const 1.0), Neg(Sub(Mul(Const 2.0, Y), X)))) (Mul(Add(X, Const 1.0), Neg(Sub(Mul(Const 2.0, Y), X)))) "t20"
      test ((Mul((Mul((Add((Sub(Y, (Sub(X, Y)))), Y)), X)), (Mul((Mul((Add(Y, X)), (Neg(X)))), (Mul(X, (Add(Y, Y))))))))) (Mul ((Mul ((Add ((Sub (Y, (Sub (X, Y)))), Y)), X)), (Mul ((Mul ((Add (Y, X)), (Neg (X)))), (Mul (X, (Add (Y, Y)))))))) "Gary's Generated test 0_1645860446"
      test ((Mul((Mul((Sub((Const 18.0), (Sub(X, (Const 14.0))))), (Add((Const -18.0), Y)))), (Neg(Y))))) (Mul ((Mul ((Sub ((Const 18.000000), (Sub (X, (Const 14.000000))))), (Add ((Const -18.000000), Y)))), (Neg (Y)))) "Gary's Generated test 1_1645860446"
      test ((Mul((Sub((Sub(X, Y)), (Neg((Sub(X, Y)))))), (Neg((Neg((Sub(X, X))))))))) (Const 0.000000) "Gary's Generated test 2_1645860446"
      test ((Sub((Neg((Mul(X, (Const 49.0))))), (Sub((Sub((Const -20.0), X)), Y))))) (Sub ((Neg ((Mul (X, (Const 49.000000))))), (Sub ((Sub ((Const -20.000000), X)), Y)))) "Gary's Generated test 3_1645860446"
      test ((Sub((Const -33.0), (Mul(X, (Sub(Y, X))))))) (Sub ((Const -33.000000), (Mul (X, (Sub (Y, X)))))) "Gary's Generated test 4_1645860446"
      test ((Sub((Sub((Const -45.0), Y)), (Mul((Const -22.0), (Mul(Y, (Sub((Neg((Const -13.0))), Y))))))))) (Sub ((Sub ((Const -45.000000), Y)), (Mul ((Const -22.000000), (Mul (Y, (Sub ((Const 13.000000), Y)))))))) "Gary's Generated test 5_1645860446"
      test ((Add((Mul(Y, (Neg((Mul(X, (Const -12.0))))))), (Mul((Neg(Y)), (Const -8.0)))))) (Add ((Mul (Y, (Neg ((Mul (X, (Const -12.000000))))))), (Mul ((Neg (Y)), (Const -8.000000))))) "Gary's Generated test 6_1645860446"
      test ((Neg((Add(Y, Y))))) (Neg ((Add (Y, Y)))) "Gary's Generated test 7_1645860446"
      test ((Sub((Mul((Mul((Neg(Y)), (Neg((Mul((Const 3.0), (Const -28.0))))))), (Sub(Y, (Sub((Const 8.0), (Sub((Add(Y, Y)), Y)))))))), (Add((Mul((Sub(Y, (Neg(Y)))), (Const -41.0))), (Add(Y, (Mul(Y, (Mul(X, (Const 39.0)))))))))))) (Sub ((Mul ((Mul ((Neg (Y)), (Const 84.000000))), (Sub (Y, (Sub ((Const 8.000000), (Sub ((Add (Y, Y)), Y)))))))), (Add ((Mul ((Sub (Y, (Neg (Y)))), (Const -41.000000))), (Add (Y, (Mul (Y, (Mul (X, (Const 39.000000))))))))))) "Gary's Generated test 8_1645860446"
      test ((Neg((Sub(Y, (Add(Y, (Add(X, (Const -22.0)))))))))) (Neg ((Sub (Y, (Add (Y, (Add (X, (Const -22.000000))))))))) "Gary's Generated test 9_1645860446"
      test ((Add((Const -29.0), (Const -18.0)))) (Const -47.000000) "Gary's Generated test 10_1645860446"
      test ((Neg((Sub(X, (Neg((Mul(X, (Add(X, (Const -46.0)))))))))))) (Neg ((Sub (X, (Neg ((Mul (X, (Add (X, (Const -46.000000))))))))))) "Gary's Generated test 11_1645860446"
      test ((Mul((Sub((Mul(Y, (Const -46.0))), (Sub((Mul(X, Y)), (Const -49.0))))), (Mul((Mul((Mul((Const 40.0), Y)), (Neg(X)))), (Add((Neg((Const 7.0))), (Add(Y, (Const 32.0)))))))))) (Mul ((Sub ((Mul (Y, (Const -46.000000))), (Sub ((Mul (X, Y)), (Const -49.000000))))), (Mul ((Mul ((Mul ((Const 40.000000), Y)), (Neg (X)))), (Add ((Const -7.000000), (Add (Y, (Const 32.000000))))))))) "Gary's Generated test 12_1645860446"
      test ((Sub((Sub((Const -43.0), (Sub(Y, (Const 41.0))))), (Neg(X))))) (Sub ((Sub ((Const -43.000000), (Sub (Y, (Const 41.000000))))), (Neg (X)))) "Gary's Generated test 13_1645860446"
      test ((Neg((Add((Const 6.0), X))))) (Neg ((Add ((Const 6.000000), X)))) "Gary's Generated test 14_1645860446"
      test ((Add((Add(X, (Neg((Const -31.0))))), (Neg((Const 36.0)))))) (Add ((Add (X, (Const 31.000000))), (Const -36.000000))) "Gary's Generated test 15_1645860446"
      test ((Mul((Neg((Sub((Const -28.0), (Mul((Const 7.0), (Const 9.0))))))), (Mul((Neg(X)), (Mul((Add((Const 28.0), X)), (Const 4.0)))))))) (Mul ((Const 91.000000), (Mul ((Neg (X)), (Mul ((Add ((Const 28.000000), X)), (Const 4.000000))))))) "Gary's Generated test 16_1645860446"
      test ((Neg((Mul((Add((Add(X, Y)), X)), (Neg(Y))))))) (Neg ((Mul ((Add ((Add (X, Y)), X)), (Neg (Y)))))) "Gary's Generated test 17_1645860446"
      test ((Mul((Const -40.0), X))) (Mul ((Const -40.000000), X)) "Gary's Generated test 18_1645860446"
      test ((Sub((Mul((Neg(X)), (Sub(Y, Y)))), (Mul((Neg((Const 12.0))), (Const -41.0)))))) (Const -492.000000) "Gary's Generated test 19_1645860446"
      test ((Mul((Neg((Const 3.0))), (Mul((Neg((Const 23.0))), X))))) (Mul ((Const -3.000000), (Mul ((Const -23.000000), X)))) "Gary's Generated test 20_1645860446"
      test ((Add((Sub((Mul((Neg((Add(Y, X)))), (Const 44.0))), (Add((Mul((Sub(Y, (Neg((Const 24.0))))), X)), Y)))), (Add((Sub(X, (Add((Add((Const -41.0), X)), (Const -31.0))))), (Add(X, Y))))))) (Add ((Sub ((Mul ((Neg ((Add (Y, X)))), (Const 44.000000))), (Add ((Mul ((Sub (Y, (Const -24.000000))), X)), Y)))), (Add ((Sub (X, (Add ((Add ((Const -41.000000), X)), (Const -31.000000))))), (Add (X, Y)))))) "Gary's Generated test 21_1645860446"
      test ((Sub((Sub((Neg((Add((Const 46.0), Y)))), Y)), (Neg((Mul((Const 9.0), Y))))))) (Sub ((Sub ((Neg ((Add ((Const 46.000000), Y)))), Y)), (Neg ((Mul ((Const 9.000000), Y)))))) "Gary's Generated test 22_1645860446"
      test ((Neg((Mul((Neg((Sub(Y, (Const -29.0))))), (Add(X, Y))))))) (Neg ((Mul ((Neg ((Sub (Y, (Const -29.000000))))), (Add (X, Y)))))) "Gary's Generated test 23_1645860446"
      test ((Add((Sub(X, (Mul(Y, X)))), (Add((Neg((Sub(X, Y)))), Y))))) (Add ((Sub (X, (Mul (Y, X)))), (Add ((Neg ((Sub (X, Y)))), Y)))) "Gary's Generated test 24_1645860446"
      test ((Mul((Sub((Sub((Const 8.0), (Const 7.0))), Y)), (Neg(X))))) (Mul ((Sub ((Const 1.000000), Y)), (Neg (X)))) "Gary's Generated test 25_1645860446"
      test ((Sub((Const -36.0), (Const 41.0)))) (Const -77.000000) "Gary's Generated test 26_1645860446"
      test ((Mul((Mul((Const -38.0), X)), (Add((Const 43.0), (Const 36.0)))))) (Mul ((Mul ((Const -38.000000), X)), (Const 79.000000))) "Gary's Generated test 27_1645860446"
      test ((Add((Sub((Add((Const 4.0), (Mul(X, X)))), Y)), (Mul((Sub((Add((Neg(Y)), (Sub(Y, Y)))), (Const 5.0))), X))))) (Add ((Sub ((Add ((Const 4.000000), (Mul (X, X)))), Y)), (Mul ((Sub ((Neg (Y)), (Const 5.000000))), X)))) "Gary's Generated test 28_1645860446"
      test ((Add((Neg((Mul((Sub((Add(Y, Y)), X)), (Neg(Y)))))), (Mul(Y, (Mul((Sub((Const 50.0), X)), Y))))))) (Add ((Neg ((Mul ((Sub ((Add (Y, Y)), X)), (Neg (Y)))))), (Mul (Y, (Mul ((Sub ((Const 50.000000), X)), Y)))))) "Gary's Generated test 29_1645860446"
      test ((Neg((Neg(Y))))) Y "Gary's Generated test 30_1645860446"
      test ((Add((Sub((Neg((Const 2.0))), (Add(Y, Y)))), (Add((Const 36.0), (Neg((Mul((Add(Y, X)), (Neg(X))))))))))) (Add ((Sub ((Const -2.000000), (Add (Y, Y)))), (Add ((Const 36.000000), (Neg ((Mul ((Add (Y, X)), (Neg (X)))))))))) "Gary's Generated test 31_1645860446"
      test ((Sub((Sub((Mul((Const -30.0), Y)), (Const 15.0))), (Sub((Const 16.0), Y))))) (Sub ((Sub ((Mul ((Const -30.000000), Y)), (Const 15.000000))), (Sub ((Const 16.000000), Y)))) "Gary's Generated test 32_1645860446"
      test ((Neg((Sub((Sub(Y, (Neg((Mul(Y, X)))))), (Mul((Sub((Const -2.0), Y)), Y))))))) (Neg ((Sub ((Sub (Y, (Neg ((Mul (Y, X)))))), (Mul ((Sub ((Const -2.000000), Y)), Y)))))) "Gary's Generated test 33_1645860446"
      test ((Neg((Mul(X, X))))) (Neg ((Mul (X, X)))) "Gary's Generated test 34_1645860446"
      test ((Mul((Neg((Const -35.0))), Y))) (Mul ((Const 35.000000), Y)) "Gary's Generated test 35_1645860446"
      test ((Add((Add((Add(X, (Const -3.0))), (Add(Y, (Const 35.0))))), (Mul((Sub((Const -22.0), Y)), (Sub(X, (Sub(X, (Sub(X, X))))))))))) (Add ((Add (X, (Const -3.000000))), (Add (Y, (Const 35.000000))))) "Gary's Generated test 36_1645860446"
      test ((Sub((Mul((Add((Const -19.0), (Mul(Y, X)))), (Const 34.0))), (Sub((Neg(Y)), (Mul((Neg(Y)), (Sub(Y, (Const 41.0)))))))))) (Sub ((Mul ((Add ((Const -19.000000), (Mul (Y, X)))), (Const 34.000000))), (Sub ((Neg (Y)), (Mul ((Neg (Y)), (Sub (Y, (Const 41.000000))))))))) "Gary's Generated test 37_1645860446"
      test ((Add((Mul((Mul(X, (Neg(Y)))), (Mul(X, (Sub(X, Y)))))), (Neg((Sub((Add(Y, (Const -35.0))), X))))))) (Add ((Mul ((Mul (X, (Neg (Y)))), (Mul (X, (Sub (X, Y)))))), (Neg ((Sub ((Add (Y, (Const -35.000000))), X)))))) "Gary's Generated test 38_1645860446"
      test ((Neg((Add((Sub(X, (Sub(Y, (Mul(X, Y)))))), (Mul((Sub(Y, X)), Y))))))) (Neg ((Add ((Sub (X, (Sub (Y, (Mul (X, Y)))))), (Mul ((Sub (Y, X)), Y)))))) "Gary's Generated test 39_1645860446"
      test (X) X "Gary's Generated test 40_1645860446"
      test ((Sub((Sub((Add(X, (Const -32.0))), (Sub((Mul((Sub(Y, (Const -3.0))), Y)), (Neg((Const 3.0))))))), (Sub((Add(X, X)), (Neg((Sub((Add(Y, Y)), (Const 15.0)))))))))) (Sub ((Sub ((Add (X, (Const -32.000000))), (Sub ((Mul ((Sub (Y, (Const -3.000000))), Y)), (Const -3.000000))))), (Sub ((Add (X, X)), (Neg ((Sub ((Add (Y, Y)), (Const 15.000000))))))))) "Gary's Generated test 41_1645860446"
      test ((Mul((Mul((Const 10.0), (Add((Const -34.0), (Const -48.0))))), (Add((Const -20.0), Y))))) (Mul ((Const -820.000000), (Add ((Const -20.000000), Y)))) "Gary's Generated test 42_1645860446"
      test ((Neg((Neg((Mul(Y, (Sub(X, X))))))))) (Const 0.000000) "Gary's Generated test 43_1645860446"
      test ((Mul(X, (Const 44.0)))) (Mul (X, (Const 44.000000))) "Gary's Generated test 44_1645860446"
      test ((Add((Add((Sub(Y, Y)), (Sub((Sub(Y, Y)), Y)))), (Add((Sub(X, (Sub(X, Y)))), (Add((Const 12.0), Y))))))) (Add ((Neg (Y)), (Add ((Sub (X, (Sub (X, Y)))), (Add ((Const 12.000000), Y)))))) "Gary's Generated test 45_1645860446"
      test ((Neg(X))) (Neg (X)) "Gary's Generated test 46_1645860446"
      test ((Mul((Add(X, X)), (Const 30.0)))) (Mul ((Add (X, X)), (Const 30.000000))) "Gary's Generated test 47_1645860446"
      test ((Mul((Add(Y, X)), (Add(Y, (Const 11.0)))))) (Mul ((Add (Y, X)), (Add (Y, (Const 11.000000))))) "Gary's Generated test 48_1645860446"
      test ((Neg((Const 40.0)))) (Const -40.000000) "Gary's Generated test 49_1645860446"
      test ((Mul((Sub(Y, X)), (Neg((Mul((Neg((Const -1.0))), (Const 14.0)))))))) (Mul ((Sub (Y, X)), (Const -14.000000))) "Gary's Generated test 50_1645860446"
      test ((Mul((Sub((Const -15.0), (Neg(Y)))), (Add((Add((Add(X, Y)), (Const -43.0))), (Mul((Const -48.0), (Const -24.0)))))))) (Mul ((Sub ((Const -15.000000), (Neg (Y)))), (Add ((Add ((Add (X, Y)), (Const -43.000000))), (Const 1152.000000))))) "Gary's Generated test 51_1645860446"
      test ((Mul((Const -48.0), (Add(Y, Y))))) (Mul ((Const -48.000000), (Add (Y, Y)))) "Gary's Generated test 52_1645860446"
      test ((Sub(X, Y))) (Sub (X, Y)) "Gary's Generated test 53_1645860446"
      test ((Sub((Mul(X, (Mul((Const -39.0), Y)))), (Sub((Add((Sub(Y, X)), Y)), X))))) (Sub ((Mul (X, (Mul ((Const -39.000000), Y)))), (Sub ((Add ((Sub (Y, X)), Y)), X)))) "Gary's Generated test 54_1645860446"
      test ((Add((Add((Neg((Sub((Neg(X)), X)))), X)), (Add((Mul((Const -25.0), Y)), (Sub(Y, X))))))) (Add ((Add ((Neg ((Sub ((Neg (X)), X)))), X)), (Add ((Mul ((Const -25.000000), Y)), (Sub (Y, X)))))) "Gary's Generated test 55_1645860446"
      test ((Mul(Y, Y))) (Mul (Y, Y)) "Gary's Generated test 56_1645860446"
      test ((Add((Mul((Sub(X, (Const -46.0))), Y)), X))) (Add ((Mul ((Sub (X, (Const -46.000000))), Y)), X)) "Gary's Generated test 57_1645860446"
      test ((Neg((Neg((Const 32.0)))))) (Const 32.000000) "Gary's Generated test 58_1645860446"
      test ((Add((Add((Sub((Const 45.0), (Const 22.0))), (Mul(Y, X)))), (Neg((Add((Neg(X)), Y))))))) (Add ((Add ((Const 23.000000), (Mul (Y, X)))), (Neg ((Add ((Neg (X)), Y)))))) "Gary's Generated test 59_1645860446"
      test ((Const 39.0)) (Const 39.000000) "Gary's Generated test 60_1645860446"
      test ((Mul((Neg((Sub((Const -46.0), (Const 30.0))))), (Mul((Add(Y, (Const -6.0))), X))))) (Mul ((Const 76.000000), (Mul ((Add (Y, (Const -6.000000))), X)))) "Gary's Generated test 61_1645860446"
      test ((Sub(X, (Const 20.0)))) (Sub (X, (Const 20.000000))) "Gary's Generated test 62_1645860446"
      test ((Add(X, (Const 32.0)))) (Add (X, (Const 32.000000))) "Gary's Generated test 63_1645860446"
      test ((Add((Const 38.0), (Sub(Y, X))))) (Add ((Const 38.000000), (Sub (Y, X)))) "Gary's Generated test 64_1645860446"
      test ((Add((Mul((Add(Y, (Const 35.0))), Y)), (Sub((Const 42.0), (Sub(X, (Neg((Const 16.0)))))))))) (Add ((Mul ((Add (Y, (Const 35.000000))), Y)), (Sub ((Const 42.000000), (Sub (X, (Const -16.000000))))))) "Gary's Generated test 65_1645860446"
      test ((Neg((Sub(X, X))))) (Const -0.000000) "Gary's Generated test 66_1645860446"
      test (Y) Y "Gary's Generated test 67_1645860446"
      test ((Add((Add((Sub((Add((Add(Y, X)), (Const 23.0))), Y)), (Add((Add(X, Y)), (Const 39.0))))), (Add((Sub(X, (Const -20.0))), (Neg((Const -1.0)))))))) (Add ((Add ((Sub ((Add ((Add (Y, X)), (Const 23.000000))), Y)), (Add ((Add (X, Y)), (Const 39.000000))))), (Add ((Sub (X, (Const -20.000000))), (Const 1.000000))))) "Gary's Generated test 68_1645860446"
      test ((Sub(Y, (Neg((Const -45.0)))))) (Sub (Y, (Const 45.000000))) "Gary's Generated test 69_1645860446"
      test ((Neg((Add(Y, Y))))) (Neg ((Add (Y, Y)))) "Gary's Generated test 70_1645860446"
      test ((Mul((Const 32.0), (Mul((Neg(X)), X))))) (Mul ((Const 32.000000), (Mul ((Neg (X)), X)))) "Gary's Generated test 71_1645860446"
      test (X) X "Gary's Generated test 72_1645860446"
      test ((Neg((Neg((Neg((Add(X, (Mul((Const 33.0), (Const -11.0)))))))))))) (Neg ((Add (X, (Const -363.000000))))) "Gary's Generated test 73_1645860446"
      test ((Add((Sub(Y, (Const -31.0))), (Add((Mul((Add(Y, (Mul(X, X)))), Y)), (Const 0.0)))))) (Add ((Sub (Y, (Const -31.000000))), (Mul ((Add (Y, (Mul (X, X)))), Y)))) "Gary's Generated test 74_1645860446"
      test ((Mul((Sub(Y, X)), (Neg((Mul((Sub(Y, (Const -10.0))), X))))))) (Mul ((Sub (Y, X)), (Neg ((Mul ((Sub (Y, (Const -10.000000))), X)))))) "Gary's Generated test 75_1645860446"
      test ((Add((Neg((Const -16.0))), (Neg((Const -44.0)))))) (Const 60.000000) "Gary's Generated test 76_1645860446"
      test ((Add((Mul((Mul(X, X)), Y)), (Mul(Y, (Const -43.0)))))) (Add ((Mul ((Mul (X, X)), Y)), (Mul (Y, (Const -43.000000))))) "Gary's Generated test 77_1645860446"
      test ((Sub((Sub((Add((Const 26.0), (Sub(X, (Const -7.0))))), (Mul(X, (Const -48.0))))), (Neg((Sub((Neg(Y)), Y))))))) (Sub ((Sub ((Add ((Const 26.000000), (Sub (X, (Const -7.000000))))), (Mul (X, (Const -48.000000))))), (Neg ((Sub ((Neg (Y)), Y)))))) "Gary's Generated test 78_1645860446"
      test ((Neg((Add((Sub(Y, X)), (Add((Sub((Const -31.0), X)), X))))))) (Neg ((Add ((Sub (Y, X)), (Add ((Sub ((Const -31.000000), X)), X)))))) "Gary's Generated test 79_1645860446"
      test ((Add((Sub((Add(X, (Mul(Y, (Const 13.0))))), X)), (Neg(X))))) (Add ((Sub ((Add (X, (Mul (Y, (Const 13.000000))))), X)), (Neg (X)))) "Gary's Generated test 80_1645860446"
      test ((Neg((Sub((Sub((Const -10.0), (Const 9.0))), (Sub((Add(X, X)), Y))))))) (Neg ((Sub ((Const -19.000000), (Sub ((Add (X, X)), Y)))))) "Gary's Generated test 81_1645860446"
      test ((Neg((Mul(X, (Add((Neg(Y)), Y))))))) (Neg ((Mul (X, (Add ((Neg (Y)), Y)))))) "Gary's Generated test 82_1645860446"
      test ((Mul((Const 42.0), (Mul(Y, (Neg((Const -43.0)))))))) (Mul ((Const 42.000000), (Mul (Y, (Const 43.000000))))) "Gary's Generated test 83_1645860446"
      test ((Mul((Mul((Add((Add(Y, Y)), (Add((Const 32.0), (Const -37.0))))), X)), (Neg((Add(Y, X))))))) (Mul ((Mul ((Add ((Add (Y, Y)), (Const -5.000000))), X)), (Neg ((Add (Y, X)))))) "Gary's Generated test 84_1645860446"
      test ((Add((Neg((Mul((Neg(X)), X)))), (Neg((Mul(X, Y))))))) (Add ((Neg ((Mul ((Neg (X)), X)))), (Neg ((Mul (X, Y)))))) "Gary's Generated test 85_1645860446"
      test ((Add((Add((Sub((Add((Sub(Y, X)), (Mul(X, X)))), (Const 32.0))), Y)), (Mul((Mul((Mul((Sub(X, X)), (Add(X, (Const -8.0))))), X)), (Mul((Const 20.0), (Add(Y, Y))))))))) (Add ((Sub ((Add ((Sub (Y, X)), (Mul (X, X)))), (Const 32.000000))), Y)) "Gary's Generated test 86_1645860446"
      test ((Add((Sub(Y, Y)), (Sub((Neg(X)), X))))) (Sub ((Neg (X)), X)) "Gary's Generated test 87_1645860446"
      test ((Neg((Sub((Mul((Const -49.0), (Sub(X, (Const -46.0))))), (Const -41.0)))))) (Neg ((Sub ((Mul ((Const -49.000000), (Sub (X, (Const -46.000000))))), (Const -41.000000))))) "Gary's Generated test 88_1645860446"
      test ((Sub((Add((Mul(Y, X)), X)), (Const -18.0)))) (Sub ((Add ((Mul (Y, X)), X)), (Const -18.000000))) "Gary's Generated test 89_1645860446"
      test ((Sub((Sub((Neg((Neg((Const -43.0))))), (Add((Const -24.0), X)))), (Mul((Add((Const -28.0), Y)), (Mul(X, X))))))) (Sub ((Sub ((Const -43.000000), (Add ((Const -24.000000), X)))), (Mul ((Add ((Const -28.000000), Y)), (Mul (X, X)))))) "Gary's Generated test 90_1645860446"
      test ((Sub((Neg(Y)), (Sub((Const 42.0), X))))) (Sub ((Neg (Y)), (Sub ((Const 42.000000), X)))) "Gary's Generated test 91_1645860446"
      test ((Neg((Sub((Neg((Const 21.0))), (Neg((Neg(Y))))))))) (Neg ((Sub ((Const -21.000000), Y)))) "Gary's Generated test 92_1645860446"
      test ((Sub((Add((Const -21.0), X)), (Const 41.0)))) (Sub ((Add ((Const -21.000000), X)), (Const 41.000000))) "Gary's Generated test 93_1645860446"
      test ((Sub((Const 1.0), (Const 14.0)))) (Const -13.000000) "Gary's Generated test 94_1645860446"
      test ((Mul((Neg((Mul(Y, (Sub(X, (Const -22.0))))))), (Neg(X))))) (Mul ((Neg ((Mul (Y, (Sub (X, (Const -22.000000))))))), (Neg (X)))) "Gary's Generated test 95_1645860446"
      test ((Sub((Mul((Sub((Sub((Const 32.0), X)), (Const 33.0))), (Neg((Mul(X, (Neg((Add(Y, Y)))))))))), (Add((Const -18.0), (Const -36.0)))))) (Sub ((Mul ((Sub ((Sub ((Const 32.000000), X)), (Const 33.000000))), (Neg ((Mul (X, (Neg ((Add (Y, Y)))))))))), (Const -54.000000))) "Gary's Generated test 96_1645860446"
      test ((Const -37.0)) (Const -37.000000) "Gary's Generated test 97_1645860446"
      test ((Mul(Y, (Add(Y, (Const 7.0)))))) (Mul (Y, (Add (Y, (Const 7.000000))))) "Gary's Generated test 98_1645860446"
      test ((Sub((Add(X, (Add((Mul((Const 43.0), (Const -6.0))), (Add(X, Y)))))), (Neg((Const -4.0)))))) (Sub ((Add (X, (Add ((Const -258.000000), (Add (X, Y)))))), (Const 4.000000))) "Gary's Generated test 99_1645860446"
    ]

let passes =
    (List.filter (fun bool -> bool) testResults)
        .Length

let failures = testResults.Length - passes

printfn
    "%s"
    (if failures > 0 then
         (sprintf "%d FAILURES!" failures)
     else
         "all tests passed")
