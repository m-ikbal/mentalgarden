def map_emotion_to_tree(emotion: str):
    return {
        "joy": {"leaf_color": "green", "has_flowers": True, "falling_leaves": False},
        "love": {"leaf_color": "lightgreen", "has_flowers": True, "falling_leaves": False},
        "neutral": {"leaf_color": "yellow", "has_flowers": False, "falling_leaves": False},
        "sadness": {"leaf_color": "brown", "has_flowers": False, "falling_leaves": True},
        "fear": {"leaf_color": "gray", "has_flowers": False, "falling_leaves": True},
        "anger": {"leaf_color": "red", "has_flowers": False, "falling_leaves": True},
        "surprise": {"leaf_color": "orange", "has_flowers": True, "falling_leaves": False}
    }.get(emotion, {
        "leaf_color": "yellow", "has_flowers": False, "falling_leaves": False
    })
