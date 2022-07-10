T_KEY = "T_KEY"
T_STR = "T_STR"
T_SYM = "T_SYM"
T_ID = "T_ID"
T_DEC = "T_DEC"
T_HEX = "T_HEX"

TF_ID = {
    0: {
        "a-z": 1,
        "A-Z": 1,
        "_": 1,
    },
    1: {
        "a-z": 1,
        "A-Z": 1,
        "0-9": 1,
        "_": 1,
    },
}

FS_ID = {
    1: T_ID,
}

TF_DEC = {
    0: {
        "0-9": 1,
    },
    1: {
        "0-9": 1,
        ".": 2,
    },
    2: {
        "0-9": 3,
    },
    3: {
        "0-9": 3,
    },
}

FS_DEC = {
    1: T_DEC,
    3: T_DEC,
}

TF_HEX = {
    0: {
        "0": 1,
    },
    1: {
        "x": 2,
        "X": 2,
    },
    2: {
        "0-9": 3,
        "a-f": 3,
        "A-F": 3,
    },
    3: {
        "0-9": 3,
        "a-f": 3,
        "A-F": 3,
    },
}

FS_HEX = {
    3: T_HEX,
}

RULES = [
    "Program -> P1 Program | #",
    "P1 -> VarDecl | FuncDecl",

    "VarDecl -> Type T_ID V1 V2 ;",
    "V1 -> [ T_DEC ] | #",
    "V2 -> = Lit | #",

    "Type -> int | bool | void",

    "FuncDecl -> def Type T_ID ( F1 ) Block",
    "F1 -> Params | #",

    "Params -> Type T_ID P3",
    "P3 -> , Type T_ID P3 | #",

    "Block -> { B1 B2 }",
    "B1 -> VarDecl B1 | #",
    "B2 -> Stmt B2 | #",

    "Stmt -> T_ID X2 | if ( Expr ) Block S1 | while ( Expr ) Block | return S2 ; | break ; | continue ; ",
    "S1 -> else Block | #",
    "S2 -> Expr | #",

    "Expr -> UnOp BaseExpr E1 | BaseExpr E1 ",

    "E1 -> BinOp Expr E1 | #",

    "BinOp -> && | || | == | > | < | >= | <= | * | + | != | - | % | / ",

    "UnOp -> - | ! ",

    "BaseExpr -> ( Expr ) | T_ID X1 | Lit ",

    "Loc -> L1",
    "L1 -> [ Expr ] | #",

    "FuncCall -> ( C1 )",
    "C1 -> Args | #",

    "X1 -> Loc | FuncCall",
    "X2 -> Loc = Expr ; | FuncCall ;",

    "Args -> Expr A1",
    "A1 -> , Expr A1 | #",

    "Lit -> T_DEC | T_HEX | T_STR | true | false",
]

VARIABLES = ["Program", "P1", "P2", "VarDecl", "V1", "Type", "FuncDecl", "F1", "P3", "Block", "B1", "B2", "Stmt", "S1", "S2", "Expr", "BaseExpr", "Loc", "L1", "FuncCall", "C1", "Args", "A1", "Lit", "BinOp", "UnOp", "X1", "X2"]
TERMINALS = ["def", "if", "else", "while", "return", "break", "continue", "int", "bool", "void", "true", "false", "*", "+", "-", "||", "&&", "=", "==", ">", "<", ">=", "<=", "/", "%", "!", "!=", "(", ")", "[", "]", "{", "}", ";", "//", "/*", "*/", "\"", ",", "#", "T_KEY", "T_STR", "T_SYM", "T_ID", "T_DEC", "T_HEX",]
