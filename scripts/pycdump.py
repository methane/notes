# pyc ファイルの中身を確認するためのスクリプト
# 未完成

class TYPE:
    NULL              = b'0'
    NONE              = b'N'
    FALSE             = b'F'
    TRUE              = b'T'
    STOPITER          = b'S'
    ELLIPSIS          = b'.'
    INT               = b'i'
    INT64             = b'I'
    FLOAT             = b'f'
    BINARY_FLOAT      = b'g'
    COMPLEX           = b'x'
    BINARY_COMPLEX    = b'y'
    LONG              = b'l'
    STRING            = b's'
    INTERNED          = b't'
    REF               = b'r'
    TUPLE             = b'('
    LIST              = b'['
    DICT              = b'{'
    CODE              = b'c'
    UNICODE           = b'u'
    UNKNOWN           = b'?'
    SET               = b'<'
    FROZENSET         = b'>'
    ASCII             = b'a'
    ASCII_INTERNED    = b'A'
    SMALL_TUPLE       = b')'
    SHORT_ASCII       = b'z'
    SHORT_ASCII_INTERNED = b'Z'


def dump_marshal(m: bytes):
    i = 0

    def read_int4():
        nonlocal i
        x = int.from_bytes(m[i:i+4], "little")
        i += 4
        return x
    
    def read_string(n):
        nonlocal i
        x = m[i:i+n]
        i += n
        return x.decode()
    
    def dump_object():
        nonlocal i
        c = m[i] & 0x7f
        i += 1
        match bytes([c]):
            case TYPE.NULL:
                print("NULL")
            case TYPE.NONE:
                print("None")
            case TYPE.FALSE:
                print("False")
            case TYPE.TRUE:
                print("True")
            case TYPE.ELLIPSIS:
                print("...")
            case TYPE.INT:
                print("INT")
                i += 4
            case TYPE.INT64:
                print("INT64")
                i += 8
            case TYPE.LONG:
                n = read_int4()
                i += n
                print(f"LONG {n}")
            case TYPE.FLOAT:
                print("FLOAT")
                i += 8
            case TYPE.STRING:  # bytes
                n = read_int4()
                s = m[i:i+n]
                i += n
                print(f"BYTES {n} {s!r}")
            case TYPE.ASCII_INTERNED | TYPE.ASCII | TYPE.UNICODE | TYPE.INTERNED:
                n = read_int4()
                s = read_string(n)
                print(f"STR {n} {s!r}")
            case TYPE.SHORT_ASCII | TYPE.SHORT_ASCII_INTERNED:
                n = m[i]
                i += 1
                s = read_string(n)
                print(f"STR {n} {s!r}")
            case TYPE.TUPLE:
                n = read_int4()
                print(f"TUPLE {n}")
                for _ in range(n):
                    dump_object()
            case TYPE.SMALL_TUPLE:
                n = m[i]
                i += 1
                print(f"TUPLE {n}")
                for _ in range(n):
                    dump_object()
            case TYPE.LIST:
                n = read_int4()
                print(f"LIST {n}")
            case TYPE.SET | TYPE.FROZENSET:
                n = read_int4()
                print("SET {n}")
            case TYPE.REF:
                read_int4()
                print("REF")
            case TYPE.CODE:
                print("CODE START")
                x = read_int4() # argcount
                x = read_int4() # posonlyargcount
                x = read_int4() # kwonlyargcount
                x = read_int4() # nlocals
                x = read_int4() # stacksize
                x = read_int4() # flags
                dump_object() # code
                dump_object() # consts
                dump_object() # names
                dump_object() # varnames
                dump_object() # freevars
                dump_object() # cellvars
                dump_object() # filename
                dump_object() # name
                read_int4() # firstlineno
                dump_object() # linetable
                print("CODE END")
            case x:
                print(f"unknown {x}")

    while i < len(m):
        dump_object()

def main():
    import sys
    with open(sys.argv[1], "rb") as f:
        #f.read(16)  # skip header
        data = f.read()
    dump_marshal(data)

main()
