from PositionVector import Position, Size


# Collision System
def RectangleCollision(r1_pos, r1_size, r2_pos, r2_size) -> bool:
    if r1_pos.x + r1_size.w > r2_pos.x and r1_pos.x < r2_pos.x + r2_size.w:
        if r1_pos.y + r1_size.h > r2_pos.y and r1_pos.y < r2_pos.y + r2_size.h:
            return True
    return False


def PointRectCollision(r1_pos, r1_size, p_pos) -> bool:
    if r1_pos.x < p_pos.x < r1_pos.x + r1_size.w:
        if r1_pos.y + r1_size.h > p_pos.y > r1_pos.y:
            return True
    return False


# Combat System
class Hurtbox:
    def __init__(self, position, size):
        self.pos = Position(*position)
        self.size = Size(*size)
        self.active = False
        self.collision = "A"
        self.solid = True
        self.dealKnockback = self.size / 4
