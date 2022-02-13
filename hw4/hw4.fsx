// Gary Tou
// CPSC 3400, HW 4 - F# Exercises
// 2/7/2022
// https://seattleu.instructure.com/courses/1602042/assignments/6989794


// Helper functions for maxCylinderVolume
let rec map (values, fn) =
    match values with
    | [] -> []
    | hd :: tl -> fn hd :: map (tl, fn)

let rec max (values, compFn) =
    match values with
    | hd :: tl when tl = [] -> hd
    | hd :: tl ->
        let tlMax = max (tl, compFn)
        compFn hd tlMax
    | _ -> failwith "max: empty list"

let volume dimension =
    let (radius: float, height) = dimension
    System.Math.PI * (radius ** 2) * height

// Write a function maxCylinderVolume that takes a list of floating-point tuples
// that represent dimensions of a cylinder and returns the volume of the
// cylinder that has the largest volume. Each tuple has two floating point
// values that are both greater than zero. The first value is the radius r and
// the second value is the height h. The volume of the cylinder is computed
// using 𝜋𝑟2h. The value π is represented in F# with System.Math.PI. If the
// list is empty, return 0.0.
let maxCylinderVolume dimensions =
    max (map (dimensions, volume), (fun a b -> if a > b then a else b))


// Write a function elimDuplicates that takes a list of integers and eliminates
// consecutive duplicates; replacing them with a single instance of the value.
// Order is preserved and non- consecutive duplicates are unaffected.
let rec elimDuplicates (values: list<int>) =
    match values with
    | [] -> []
    | hd :: tl when tl = [] -> [ hd ]
    | hd :: tl ->
        let tlElim = elimDuplicates tl

        match tlElim with
        | [] -> [ hd ]
        | hd' :: tl' when hd = hd' -> hd :: elimDuplicates tl' // Removes duplicate
        | hd' :: tl' -> hd :: hd' :: elimDuplicates tl'


// Tree definition for problem 3
type BST =
    | Empty
    | TreeNode of int * BST * BST

// Returns true if the value is in the tree and false otherwise
let rec search (value: int, tree: BST) =
    match tree with
    | Empty -> false
    | TreeNode (nodeVal, _, _) when value = nodeVal -> true
    | TreeNode (_, left, right) -> search (value, left) || search (value, right)

// Inserts the value into the tree and returns the resulting tree. The resulting
// tree does NOT need to be balanced. If the value already exists in the tree,
// return the tree without inserting the value.
let rec insert (value: int, tree: BST) =
    match tree with
    // Create node
    | Empty -> TreeNode(value, Empty, Empty)
    // Return existing tree if it exists
    | TreeNode (nodeVal, _, _) when nodeVal = value -> tree
    // Handle branch node
    | TreeNode (nodeVal, left, right) ->
        if value < nodeVal then
            TreeNode(nodeVal, insert (value, left), right)
        else
            TreeNode(nodeVal, left, insert (value, right))


// The parameter `func` is a Boolean function that takes a single parameter and
// returns true or false. The function tests the value of each node with func
// and returns the number of nodes that evaluate to true.
let rec count (func: (int -> bool), tree: BST) =
    match tree with
    | Empty -> 0
    | TreeNode (nodeVal, left, right) ->
        (if func nodeVal then 1 else 0)
        + count (func, left)
        + count (func, right)


// Returns the number of nodes that contain even integers. REQUIREMENT: This
// function must be a single call to `count` (part 3C) using a lambda function.
let evenCount (tree: BST) = count ((fun x -> x % 2 = 0), tree)
