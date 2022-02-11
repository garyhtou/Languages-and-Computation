// Gary Tou
// CPSC 3400, HW 4 - F# Exercises
// 2/7/2022
// https://seattleu.instructure.com/courses/1602042/assignments/6989794

let volume dimension =
    let (radius: float, height) = dimension
    System.Math.PI * (radius ** 2) * height


// Custom map function since we are not allowed to use `List` for this assignment
let rec map values func =
    match values with
    | [] -> []
    | hd :: tl -> func hd :: map tl func

let rec max values funcComp =
    match values with
    | hd :: tl when tl = [] -> hd
    | hd :: tl ->
        let tlMax = max tl funcComp
        funcComp hd tlMax
    | _ -> failwith "max: empty list"

let v = volume (0.5, 1)
printf v







// let mapCylinderVolume dimensions =
//     max (map dimensions volume) (fun a b -> if volume a > volume b then a else b)



// let maxCylinderVolume dimensions =
//     let hd :: tl = dimensions

//     match tl with
//     | [] -> hd
//     | let currRadius :: currHeight = hd
//     let currVolume = volume currRadius currHeight

//     let next = maxCylinderVolume tl
//     let nextRadius :: nextHeight = next
//     let nextVolume = volume nextRadius nextHeight




//     let currRadius :: currHeight = hd
//     let currVolume = volume currRadius currHeight

//     let next = maxCylinderVolume tl
//     let nextRadius :: nextHeight = next
//     let nextVolume = volume nextRadius nextHeight









// elimDuplicates







// BST
