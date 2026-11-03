#!/usr/bin/env python3
"""Builds one .glb per Run My Agents cook: a rounded body in the avatar's shape and colour, its face wrapped onto the
front, and a chef hat. Reads cooks.json and face/<slug>.png (the face without its body) from the folder given."""
import json, math, struct, sys, os

out = sys.argv[1]
cooks = json.load(open(os.path.join(out, "cooks.json")))
# Body half-sizes (x, y, z) in units where the 64 px avatar is 2 wide, and how square the corners are (1 = round).
SHAPES = {"circle": (0.875, 0.875, 0.78, 1.0), "blob": (0.86, 0.88, 0.74, 0.92), "square": (0.84, 0.84, 0.7, 0.32),
          "pill": (0.94, 0.625, 0.6, 0.55), "tall": (0.625, 0.94, 0.6, 0.4)}

def sgnpow(v, p): return math.copysign(abs(v) ** p, v)

def superellipsoid(a, b, c, e, nu=48, nv=32):
    P, N, I = [], [], []
    for i in range(nv + 1):
        v = -math.pi / 2 + math.pi * i / nv
        for j in range(nu + 1):
            u = -math.pi + 2 * math.pi * j / nu
            cv, sv, cu, su = math.cos(v), math.sin(v), math.cos(u), math.sin(u)
            x, y, z = a * sgnpow(cv, e) * sgnpow(su, e), b * sgnpow(sv, e), c * sgnpow(cv, e) * sgnpow(cu, e)
            nx, ny, nz = sgnpow(cv, 2 - e) * sgnpow(su, 2 - e) / a, sgnpow(sv, 2 - e) / b, sgnpow(cv, 2 - e) * sgnpow(cu, 2 - e) / c
            l = math.sqrt(nx * nx + ny * ny + nz * nz) or 1
            P.append((x, y, z)); N.append((nx / l, ny / l, nz / l))
    for i in range(nv):
        for j in range(nu):
            k = i * (nu + 1) + j
            I += [k, k + nu + 1, k + 1, k + 1, k + nu + 1, k + nu + 2]
    return P, N, None, I

def front_z(x, y, a, b, c, e):
    p = 2 / e
    r = 1 - abs(x / a) ** p - abs(y / b) ** p
    return c * r ** (1 / p) if r > 0 else None

def face_grid(vb, a, b, c, e, n=40):
    """The face texture on a grid that follows the body's front surface; parts outside the body sit just in front."""
    x0, y0, w, h = vb
    P, N, U, I = [], [], [], []
    for i in range(n + 1):
        for j in range(n + 1):
            sx, sy = x0 + w * j / n, y0 + h * i / n
            x, y = (sx - 32) / 32, -(sy - 32) / 32
            z = front_z(x, y, a, b, c, e)
            z = (z if z is not None else c * 0.35) + 0.012
            P.append((x, y, z)); N.append((0, 0, 1)); U.append((j / n, i / n))
    for i in range(n):
        for j in range(n):
            k = i * (n + 1) + j
            I += [k, k + n + 1, k + 1, k + 1, k + n + 1, k + n + 2]
    return P, N, U, I

def cylinder(r, h, y0, n=40):
    P, N, I = [], [], []
    for j in range(n + 1):
        t = 2 * math.pi * j / n
        for y in (y0, y0 + h):
            P.append((r * math.sin(t), y, r * math.cos(t))); N.append((math.sin(t), 0, math.cos(t)))
    for j in range(n):
        k = 2 * j
        I += [k, k + 1, k + 2, k + 2, k + 1, k + 3]
    return P, N, None, I

def sphere(r, cx, cy, cz):
    P, N, _, I = superellipsoid(r, r, r, 1.0, 32, 20)
    return [(x + cx, y + cy, z + cz) for x, y, z in P], N, None, I

def merge(parts):
    P, N, I = [], [], []
    for p, n, _, i in parts:
        base = len(P); P += p; N += n; I += [base + k for k in i]
    return P, N, None, I

def hexrgb(h):
    h = h.lstrip("#"); return [int(h[k:k + 2], 16) / 255 for k in (0, 2, 4)]

def to_linear(c): return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]

def build(cook):
    a, b, c, e = SHAPES[cook["shape"]]
    vb = (-6, -6, 76, 76) if cook["extra"] else (0, 0, 64, 64)
    top = b
    hat = merge([cylinder(0.46, 0.34, top - 0.06), sphere(0.3, -0.27, top + 0.42, 0), sphere(0.3, 0.27, top + 0.42, 0), sphere(0.36, 0, top + 0.56, 0)])
    meshes = [("body", superellipsoid(a, b, c, e), 0), ("face", face_grid(vb, a, b, c, e), 1), ("hat", hat, 2)]
    png = open(os.path.join(out, "face", cook["slug"] + ".png"), "rb").read()
    blob, views, accessors, prims = bytearray(), [], [], []

    def view(data, target=None):
        while len(blob) % 4: blob.append(0)
        off = len(blob); blob.extend(data)
        v = {"buffer": 0, "byteOffset": off, "byteLength": len(data)}
        if target: v["target"] = target
        views.append(v); return len(views) - 1

    def acc(vals, kind, comps):
        flat = [x for v in vals for x in (v if comps > 1 else (v,))]
        if kind == "idx":
            vi = view(struct.pack(f"<{len(flat)}I", *flat), 34963)
            accessors.append({"bufferView": vi, "componentType": 5125, "count": len(flat), "type": "SCALAR"})
        else:
            vi = view(struct.pack(f"<{len(flat)}f", *flat), 34962)
            a_ = {"bufferView": vi, "componentType": 5126, "count": len(vals), "type": {2: "VEC2", 3: "VEC3"}[comps]}
            if kind == "pos":
                a_["min"] = [min(v[k] for v in vals) for k in range(3)]; a_["max"] = [max(v[k] for v in vals) for k in range(3)]
            accessors.append(a_)
        return len(accessors) - 1

    for name, (P, N, U, I), mat in meshes:
        attrs = {"POSITION": acc(P, "pos", 3), "NORMAL": acc(N, "n", 3)}
        if U: attrs["TEXCOORD_0"] = acc(U, "uv", 2)
        prims.append({"attributes": attrs, "indices": acc(I, "idx", 1), "material": mat})
    img_view = view(png)
    gltf = {
        "asset": {"version": "2.0", "generator": "flisk-emoji cooks/glb.py"},
        "scene": 0, "scenes": [{"nodes": [0]}],
        "nodes": [{"name": cook["role"] + " cook", "mesh": 0}],
        "meshes": [{"name": cook["role"], "primitives": prims}],
        "materials": [
            {"name": "body", "pbrMetallicRoughness": {"baseColorFactor": to_linear(hexrgb(cook["color"])) + [1], "metallicFactor": 0, "roughnessFactor": 0.5}},
            {"name": "face", "pbrMetallicRoughness": {"baseColorTexture": {"index": 0}, "metallicFactor": 0, "roughnessFactor": 0.4}, "alphaMode": "MASK", "alphaCutoff": 0.5, "doubleSided": True},
            {"name": "hat", "pbrMetallicRoughness": {"baseColorFactor": [0.95, 0.95, 0.96, 1], "metallicFactor": 0, "roughnessFactor": 0.75}},
        ],
        "textures": [{"source": 0, "sampler": 0}], "samplers": [{"magFilter": 9729, "minFilter": 9987}],
        "images": [{"bufferView": img_view, "mimeType": "image/png"}],
        "buffers": [{"byteLength": 0}], "bufferViews": views, "accessors": accessors,
    }
    while len(blob) % 4: blob.append(0)
    gltf["buffers"][0]["byteLength"] = len(blob)
    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * ((4 - len(js) % 4) % 4)
    total = 12 + 8 + len(js) + 8 + len(blob)
    data = struct.pack("<III", 0x46546C67, 2, total) + struct.pack("<II", len(js), 0x4E4F534A) + js + struct.pack("<II", len(blob), 0x004E4942) + bytes(blob)
    os.makedirs(os.path.join(out, "3d"), exist_ok=True)
    open(os.path.join(out, "3d", cook["slug"] + ".glb"), "wb").write(data)
    return len(data)

for ck in cooks: print(ck["slug"], build(ck))
