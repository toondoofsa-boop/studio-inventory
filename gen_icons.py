import zlib, struct

def png_chunk(tag, data):
    body = tag + data
    return struct.pack('>I', len(data)) + body + struct.pack('>I', zlib.crc32(body) & 0xffffffff)

def make_png(w, h, pixels):
    raw = b''
    for row in pixels:
        raw += b'\x00'
        for r, g, b in row:
            raw += bytes([r, g, b])
    return (
        b'\x89PNG\r\n\x1a\n' +
        png_chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)) +
        png_chunk(b'IDAT', zlib.compress(raw, 6)) +
        png_chunk(b'IEND', b'')
    )

def draw_icon(size):
    BG  = (10, 10, 10)
    GOLD = (245, 200, 66)
    px = [[list(BG) for _ in range(size)] for _ in range(size)]

    def sp(x, y, c):
        if 0 <= x < size and 0 <= y < size:
            px[y][x] = list(c)

    def hline(x1, x2, y, c, w):
        for t in range(-w//2, w//2+1):
            for x in range(x1, x2+1): sp(x, y+t, c)

    def vline(x, y1, y2, c, w):
        for t in range(-w//2, w//2+1):
            for y in range(y1, y2+1): sp(x+t, y, c)

    def rect(x1, y1, x2, y2, c, w):
        hline(x1, x2, y1, c, w); hline(x1, x2, y2, c, w)
        vline(x1, y1, y2, c, w); vline(x2, y1, y2, c, w)

    lw  = max(2, size // 40)
    m   = size // 8
    mid = size // 2

    # Lid
    lid_t = m
    lid_b = m + size // 4
    # Body
    bod_t = lid_b
    bod_b = size - m

    # Body outline
    rect(m, bod_t, size - m, bod_b, GOLD, lw)
    # Lid outline (narrower)
    pad = size // 8
    rect(m + pad, lid_t, size - m - pad, lid_b, GOLD, lw)
    # Vertical tape stripe
    vline(mid, bod_t, bod_b, GOLD, lw)
    # Horizontal tape on lid
    hline(m + pad, size - m - pad, (lid_t + lid_b) // 2, GOLD, lw)

    return [(tuple(px[y][x]) for x in range(size)) for y in range(size)]

for size, name in [(192, 'icon-192.png'), (512, 'icon-512.png')]:
    rows = [list(draw_icon(size)[y]) for y in range(size)]
    data = make_png(size, size, rows)
    with open(name, 'wb') as f:
        f.write(data)
    print(f'Created {name} ({len(data):,} bytes)')
