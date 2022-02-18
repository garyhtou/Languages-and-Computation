// let classify (numbers: int) =
//     let rec helper (numbers: int, neg, zero, pos) =
//         match numbers with
//         | [] -> output
//         | hd :: tl when hd > 0 -> helper (tl, neg, zero, pos+1)
//         | hd :: tl when hd = 0 -> helper (tl, neg, zero +1, pos)
//         | hd :: tl -> helper (tl, neg +1, zero, post)

//     helper numbers 0 0 0


let rec classify list =
    match list with
    | [] -> (0, 0, 0)
    | hd :: tl ->
        let (neg, zero, pos) = classify tl
        if hd < 0 then (neg + 1, zero, pos)
        elif hd = 0 then (neg, zero + 1, pos)
        else (neg, zero, pos + 1)


printfn "%A" (classify [-4; 2; 0; -9; -3; 1; 0; 24; -3])


let rec remove (list, value) =
    match list with
    | [] -> []
    | hd :: tl when hd = value -> remove (tl, value)
    | hd :: tl -> hd :: remove (tl, value)


printfn "%A" (remove ([1; 2; 1; 3; 1; 4; 1; 5], 1))

