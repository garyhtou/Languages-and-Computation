let rec doubleNeg values =
    match values with
    | [] -> []
    | hd :: tl when hd < 0 -> hd :: hd :: doubleNeg tl
    | hd :: tl -> hd :: doubleNeg tl

printfn "%A" (doubleNeg [ 3; -1; 4; -2; -5; 7 ])
