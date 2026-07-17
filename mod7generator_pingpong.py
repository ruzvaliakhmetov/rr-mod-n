# Mod 7 font machine — ping-pong edition
font = Glyphs.font
digits = ["zero","one","two","three","four","five",
          "six","seven","eight","nine"]
MOD = 7
PASSES = 8

# --- 1. Two register sets: st.* and su.* ---
for prefix_name in ("st", "su"):
    for s in range(MOD):
        name = "%s.%d" % (prefix_name, s)
        g = font.glyphs[name]
        if g is None:
            g = GSGlyph(name)
            font.glyphs.append(g)
        for master in font.masters:
            g.layers[master.id].width = 0
        g.category = "Letter"
        g.subCategory = None
        g.storeCategory = True

# --- 2. Prefix ---
lines = []
lines.append("@digit = [%s];" % " ".join(digits))
lines.append("@stateA = [%s];" % " ".join("st.%d" % s for s in range(MOD)))
lines.append("@stateB = [%s];" % " ".join("su.%d" % s for s in range(MOD)))
lines.append("")

lines.append("lookup toState {")
for d in range(10):
    lines.append("  sub %s by st.%d;" % (digits[d], d % MOD))
lines.append("} toState;")
lines.append("")

lines.append("lookup calcState {")
lines.append("  ignore sub [@digit @stateA @stateB] @digit';")
lines.append("  sub @digit' lookup toState @digit;")
lines.append("} calcState;")
lines.append("")

def step_rules(src, dst):
    out = []
    for s in range(MOD):
        for d in range(10):
            new = (s * 10 + d) % MOD
            out.append("  sub %s.%d %s by %s.%d;" % (src, s, digits[d], dst, new))
    return out

for p in range(1, PASSES + 1):
    src, dst = ("st", "su") if p % 2 == 1 else ("su", "st")
    lines.append("lookup step%d {" % p)
    lines.extend(step_rules(src, dst))
    lines.append("} step%d;" % p)
    lines.append("")

lines.append("lookup render {")
for s in range(MOD):
    lines.append("  sub st.%d by %s;" % (s, digits[s]))
    lines.append("  sub su.%d by %s;" % (s, digits[s]))
for d in range(MOD, 10):
    lines.append("  sub %s by %s;" % (digits[d], digits[d % MOD]))
lines.append("} render;")

prefix_code = "\n".join(lines)
prefix = font.featurePrefixes["mod7"]
if prefix is None:
    prefix = GSFeaturePrefix("mod7", prefix_code)
    font.featurePrefixes.append(prefix)
else:
    prefix.code = prefix_code

# --- 3. Feature ---
calls = ["lookup calcState;"]
calls += ["lookup step%d;" % p for p in range(1, PASSES + 1)]
calls.append("lookup render;")
fea_code = "\n".join(calls)
feature = font.features["ss01"]
if feature is None:
    feature = GSFeature("ss01", fea_code)
    font.features.append(feature)
else:
    feature.code = fea_code
feature.automatic = False

print("Ping-pong generated. Compile, export, test in AI")