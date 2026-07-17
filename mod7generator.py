# Mod 7 font machine — full generator
font = Glyphs.font
digits = ["zero","one","two","three","four","five",
          "six","seven","eight","nine"]
MOD = 7
PASSES = 8   # supports up to 9-digit numbers

# --- 1. State glyphs: empty, zero-width, forced Letter category ---
for s in range(MOD):
    name = "st.%d" % s
    g = font.glyphs[name]
    if g is None:
        g = GSGlyph(name)
        font.glyphs.append(g)
    for master in font.masters:
        g.layers[master.id].width = 0
    g.category = "Letter"
    g.subCategory = None
    g.storeCategory = True

# --- 2. Prefix: all definitions, in execution order ---
lines = []
lines.append("@digit = [%s];" % " ".join(digits))
lines.append("@state = [%s];" % " ".join("st.%d" % s for s in range(MOD)))
lines.append("")

lines.append("lookup toState {")
for d in range(10):
    lines.append("  sub %s by st.%d;" % (digits[d], d % MOD))
lines.append("} toState;")
lines.append("")

lines.append("lookup calcState {")
lines.append("  ignore sub [@digit @state] @digit';")
lines.append("  sub @digit' lookup toState @digit;")
lines.append("} calcState;")
lines.append("")

step_rules = []
for s in range(MOD):
    for d in range(10):
        new = (s * 10 + d) % MOD
        step_rules.append("  sub st.%d %s by st.%d;" % (s, digits[d], new))

for p in range(1, PASSES + 1):
    lines.append("lookup step%d {" % p)
    lines.extend(step_rules)
    lines.append("} step%d;" % p)
    lines.append("")

lines.append("lookup render {")
for s in range(MOD):
    lines.append("  sub st.%d by %s;" % (s, digits[s]))
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

# --- 3. Feature: calls only ---
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

print("Generated. Now: Font Info > Features > Compile")