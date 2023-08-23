import physical_obj

class Object(physical_obj.PhysObj):
    def __init__(self, object_id: str) -> None:
        super().__init__(object_id)
        
