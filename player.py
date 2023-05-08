import physical_obj
import item

class Player(physical_obj.PhysObj):
    
    def __init__(self) -> None:
        super().__init__()

        self.max_health: int = 100
        self.health = self.max_health
        self.inventory: list[item.Item] = []

        self.player_visible = False
