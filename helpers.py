def load_into_array(dest: [], dest_idx: int, src: []):
    print(src)
    offset = 0
    for bit in src:
        dest[dest_idx + offset] = src[offset]
        offset += 1
            