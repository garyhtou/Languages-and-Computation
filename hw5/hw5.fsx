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
      test
          (Mul(Add(X, Const 1.0), Neg(Sub(Mul(Const 2.0, Y), X))))
          (Mul(Add(X, Const 1.0), Neg(Sub(Mul(Const 2.0, Y), X))))
          "t20" ]

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
