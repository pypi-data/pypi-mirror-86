from photons_messages_generator import errors

valid_enum_types = ["uint8", "uint16", "uint32", "uint64", "int8", "int16", "int32", "int64"]
valid_struct_types = valid_enum_types + ["bool", "float32", "float64", "byte"]


def snake_to_camel(s):
    uppercase = False
    final = []
    for i, ch in enumerate(s):
        if ch == "_":
            uppercase = True
            continue

        if uppercase or i == 0:
            ch = ch.upper()
            uppercase = False

        final.append(ch)
    return "".join(final)


def camel_to_snake(s):
    parts = []
    buf = []

    for i, ch in enumerate(s):
        if i == 0:
            buf.append(ch.lower())
            continue

        if ch.isupper():
            parts.append("".join(buf))
            buf = []

        buf.append(ch.lower())

    if buf:
        parts.append("".join(buf))

    return "_".join(parts)


def convert_type(name, size_bits):
    broken = size_bits % 8 != 0

    if name in ("string", "byte"):
        if broken:
            raise errors.BadSizeBytes(
                "Only basic types and reserved may be a partial byte",
                name=name,
                size_bits=size_bits,
            )

        num_bytes = int(size_bits / 8)
        if name == "string":
            return f"T.String({num_bytes} * 8)"
        elif name == "byte":
            return f"T.Bytes({num_bytes} * 8)"

    if name == "reserved":
        return f"T.Reserved({size_bits})"

    if name == "bit" or size_bits == 1:
        return "T.Bool"
    elif name == "bool":
        return "T.BoolInt"
    elif name == "float32":
        return "T.Float"
    elif name == "float64":
        return "T.Double"
    else:
        return f"T.{name.capitalize()}"
