"""
Resistance Mapper

Classifies stakeholder objections into Goldratt's Six Layers of Resistance
and recommends the appropriate TOC Thinking Process tool for each layer.

If a layer is not provided for an objection, the script auto-classifies using
keyword matching per the Six Layers framework.

Usage:
    python3 scripts/resistance_mapper.py --file input.json
    python3 scripts/resistance_mapper.py '{"proposal": "...", ...}'

Input JSON:
{
  "proposal": "Switch to a pull-based scheduling system by Q3",
  "stakeholders": [
    {"name": "Alice", "role": "VP Operations"},
    {"name": "Bob", "role": "Plant Manager"}
  ],
  "objections": [
    {
      "stakeholder": "Alice",
      "objection": "I don't see why our current scheduling is a problem",
      "layer": null
    },
    {
      "stakeholder": "Bob",
      "objection": "We can't do this — we don't have the software to support it"
    }
  ]
}

Output: classified objections, stakeholder resistance profile,
recommended approach per layer.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from toc_common import parse_input, format_output, require_fields, rank_by

# Keyword patterns for auto-classification — checked in order (layer 1 first)
LAYER_KEYWORDS = {
    1: [
        "not a problem", "don't see the issue", "working fine", "works fine",
        "no problem", "fine as is", "always worked", "don't see why",
        "what problem", "isn't broken", "not broken",
    ],
    2: [
        "wrong approach", "different direction", "won't work because",
        "better way", "different approach", "not the right way",
        "have you considered", "tried before", "other option",
    ],
    3: [
        "doesn't solve", "won't fix", "still have the problem",
        "won't help", "won't address", "doesn't address", "still broken",
        "doesn't work", "not enough", "won't eliminate",
    ],
    4: [
        "but then", "side effect", "what about", "will cause",
        "will break", "create new problems", "yes but",
        "damage", "unintended", "downstream", "ripple",
    ],
    5: [
        "can't because", "impossible", "don't have resources",
        "no budget", "no time", "lack the", "don't have the",
        "need approval", "requires", "would need", "can't afford",
        "no capacity", "no staff",
    ],
}

# Layer 6 is the fallback — vague or unclassifiable objections
DEFAULT_LAYER = 6

LAYER_METADATA = {
    1: {
        "name": "Disagree on the Problem",
        "toc_tool": "Current Reality Tree (CRT)",
        "approach": (
            "Build a shared Current Reality Tree. Start from observable undesirable effects "
            "both parties agree on. Work backward to surface the shared root cause together. "
            "Do not assert — discover."
        ),
        "key_question": "What effects do we both see that we both agree are undesirable?",
        "do_not": "Present your solution — they can't evaluate a fix to a problem they don't believe exists.",
    },
    2: {
        "name": "Disagree on Direction of Solution",
        "toc_tool": "Evaporating Cloud (EC)",
        "approach": (
            "Use the Evaporating Cloud to surface the conflict. Map each party's need and "
            "prerequisite. Identify the assumption that creates the apparent conflict. "
            "Challenge that assumption — often both approaches are partially right."
        ),
        "key_question": "What is the assumption that's creating the conflict between our two approaches?",
        "do_not": "Force your solution through or dismiss their counter-proposal.",
    },
    3: {
        "name": "Disagree That Solution Solves Problem",
        "toc_tool": "Future Reality Tree (FRT)",
        "approach": (
            "Build a Future Reality Tree that explicitly maps the cause-effect chain from "
            "your solution to the desired outcomes. Make every logical step visible. "
            "Invite them to identify where the chain breaks — then address that gap."
        ),
        "key_question": "Where exactly does the cause-effect chain break in your view?",
        "do_not": "Repeat the argument louder or add more features to the solution.",
    },
    4: {
        "name": "Solution Will Cause Negative Side Effects",
        "toc_tool": "Negative Branch (extension of FRT) + Injection design",
        "approach": (
            "Extend your FRT to model the negative branch they're concerned about. "
            "Either show why the negative effect won't occur, or design an injection — "
            "a supplementary action that neutralizes the side effect without undermining the solution."
        ),
        "key_question": "Walk me through exactly what you're worried will happen step by step.",
        "do_not": "Minimize the concern or say 'that won't happen' without showing your reasoning.",
    },
    5: {
        "name": "Obstacles to Implementation",
        "toc_tool": "Prerequisite Tree (PRT)",
        "approach": (
            "Use a Prerequisite Tree to map the path from here to the goal. "
            "Convert each 'we can't because X' into 'to do this, first we need Y'. "
            "Identify intermediate objectives. Treat obstacles as navigation, not blockers."
        ),
        "key_question": "What would we need to have in place first for this to be possible?",
        "do_not": "Dismiss obstacles as excuses or override them with authority.",
    },
    6: {
        "name": "Unverbalized Fear",
        "toc_tool": "Open conversation + psychological safety",
        "approach": (
            "Create a safe space for the real concern to surface. Ask open-ended questions. "
            "Listen without defending. The fear may be personal (job security, looking bad, "
            "past blame) rather than logical. Name the human concern before addressing business logic."
        ),
        "key_question": "What am I missing that you haven't said yet?",
        "do_not": "Push harder or assume agreement because objections stopped surfacing.",
    },
}


def classify_objection(objection_text):
    """Auto-classify an objection to a layer using keyword matching."""
    lower = objection_text.lower()
    for layer in range(1, 6):  # 1-5 first; 6 is default
        for keyword in LAYER_KEYWORDS[layer]:
            if keyword in lower:
                return layer, f"Matched keyword: '{keyword}'"
    return DEFAULT_LAYER, "No keyword match — classified as Layer 6 (unverbalized/vague)"


def build_stakeholder_profile(stakeholders, classified_objections):
    """Summarize each stakeholder's resistance layers."""
    profile = {}
    for s in stakeholders:
        name = s.get("name", "Unknown")
        profile[name] = {
            "name": name,
            "role": s.get("role", ""),
            "layers_active": [],
            "objection_count": 0,
            "highest_layer": 0,
        }
    for obj in classified_objections:
        name = obj.get("stakeholder", "Unknown")
        layer = obj.get("classified_layer", 6)
        if name not in profile:
            profile[name] = {
                "name": name,
                "role": "Unknown",
                "layers_active": [],
                "objection_count": 0,
                "highest_layer": 0,
            }
        p = profile[name]
        if layer not in p["layers_active"]:
            p["layers_active"].append(layer)
        p["objection_count"] += 1
        if layer > p["highest_layer"]:
            p["highest_layer"] = layer

    # Sort layers_active
    for name in profile:
        profile[name]["layers_active"].sort()

    return list(profile.values())


def build_layer_summary(classified_objections):
    """Group objections by layer with recommended approach."""
    layers = {}
    for obj in classified_objections:
        layer = obj.get("classified_layer", 6)
        if layer not in layers:
            meta = LAYER_METADATA[layer]
            layers[layer] = {
                "layer": layer,
                "name": meta["name"],
                "toc_tool": meta["toc_tool"],
                "approach": meta["approach"],
                "key_question": meta["key_question"],
                "do_not": meta["do_not"],
                "objections": [],
            }
        layers[layer]["objections"].append({
            "stakeholder": obj.get("stakeholder", "Unknown"),
            "objection": obj.get("objection", ""),
        })

    return [layers[k] for k in sorted(layers.keys())]


def main():
    data = parse_input()
    if data is None:
        print(__doc__)
        sys.exit(0)

    require_fields(data, ["proposal", "stakeholders", "objections"])

    proposal = data["proposal"]
    stakeholders = data["stakeholders"]
    objections = data["objections"]

    if not isinstance(stakeholders, list):
        print("Error: stakeholders must be a list", file=sys.stderr)
        sys.exit(1)
    if not isinstance(objections, list):
        print("Error: objections must be a list", file=sys.stderr)
        sys.exit(1)

    # Classify each objection
    classified = []
    for obj in objections:
        layer = obj.get("layer")
        classification_method = "provided"
        classification_note = None

        if layer is None or not isinstance(layer, int) or layer < 1 or layer > 6:
            layer, classification_note = classify_objection(obj.get("objection", ""))
            classification_method = "auto-classified"

        meta = LAYER_METADATA[layer]
        classified.append({
            "stakeholder": obj.get("stakeholder", "Unknown"),
            "objection": obj.get("objection", ""),
            "classified_layer": layer,
            "layer_name": meta["name"],
            "classification_method": classification_method,
            "classification_note": classification_note,
            "recommended_tool": meta["toc_tool"],
        })

    stakeholder_profiles = build_stakeholder_profile(stakeholders, classified)
    layer_summary = build_layer_summary(classified)

    # Find the lowest (most fundamental) layer — must be resolved first
    active_layers = sorted(set(obj["classified_layer"] for obj in classified))
    first_layer_to_address = active_layers[0] if active_layers else None
    first_layer_meta = LAYER_METADATA[first_layer_to_address] if first_layer_to_address else None

    result = {
        "proposal": proposal,
        "total_objections": len(classified),
        "layers_active": active_layers,
        "first_layer_to_address": {
            "layer": first_layer_to_address,
            "name": first_layer_meta["name"] if first_layer_meta else None,
            "why": "You must resolve earlier layers before later ones will be receptive.",
            "toc_tool": first_layer_meta["toc_tool"] if first_layer_meta else None,
            "key_question": first_layer_meta["key_question"] if first_layer_meta else None,
        },
        "objections_classified": classified,
        "layer_summary": layer_summary,
        "stakeholder_profiles": stakeholder_profiles,
        "guidance": (
            "Work through layers in sequence from lowest to highest. "
            "A person at Layer 1 cannot process a Layer 3 argument. "
            "Confirm resolution at each layer before advancing."
        ),
    }

    summary_lines = [
        "=== Resistance Mapper ===",
        f"Proposal: {proposal}",
        f"Total objections: {len(classified)}",
        f"Active layers: {active_layers}",
        "",
        f"START HERE: Layer {first_layer_to_address} — {first_layer_meta['name'] if first_layer_meta else 'None'}",
        f"  Tool: {first_layer_meta['toc_tool'] if first_layer_meta else 'N/A'}",
        f"  Ask: \"{first_layer_meta['key_question'] if first_layer_meta else 'N/A'}\"",
        "",
        "Objections by layer:",
    ]
    for layer_data in layer_summary:
        summary_lines.append(f"\n  Layer {layer_data['layer']}: {layer_data['name']}")
        summary_lines.append(f"  Tool: {layer_data['toc_tool']}")
        for obj in layer_data["objections"]:
            method_note = ""
            for c in classified:
                if c["stakeholder"] == obj["stakeholder"] and c["objection"] == obj["objection"]:
                    if c["classification_method"] == "auto-classified":
                        method_note = " [auto-classified]"
                    break
            summary_lines.append(f"    - {obj['stakeholder']}: \"{obj['objection']}\"{method_note}")
    summary_lines.append("")
    summary_lines.append("Stakeholder profiles:")
    for sp in stakeholder_profiles:
        if sp["objection_count"] > 0:
            summary_lines.append(
                f"  {sp['name']} ({sp['role']}): {sp['objection_count']} objection(s), "
                f"layers {sp['layers_active']}, highest layer {sp['highest_layer']}"
            )

    format_output(result, "\n".join(summary_lines))


if __name__ == "__main__":
    main()
