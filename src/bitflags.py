# Blocks a player from using any verb that doesn't have the VERB_OVERRIDE_LAYDOWN flag
PLAYER_LAYING_DOWN = (1 << 0)  # DEPRECATED


# If a verb should ignore the player laying down
VERB_IGNORE_LAYDOWN = (1 << 0)
# If a verb should ignore the player sitting down
VERB_IGNORE_SITDOWN = (1 << 1)

# The base examine component shouldn't print anything on examine. Use only if a different component is taking its place
BASEOBJ_BASE_EXAMINE_OVERRIDDEN = (1 << 0)
