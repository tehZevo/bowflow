from math import log10, floor

from pygame.math import Vector2

def round_sigfigs(x, figs):
    return int(round(x, figs - (1 + floor(log10(abs(x))))))

def point_in_aabb(point, min, max):
    return point.x >= min.x and point.x < max.x and point.y >= min.y and point.y < max.y

def intersect(p1, p2, p3, p4):
    denom = (p4.y - p3.y) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.y-p1.y)
    if denom == 0:
        return None

    ua = ((p4.x - p3.x) * (p1.y - p3.y) - (p4.y - p3.y) * (p1.x - p3.x)) / denom
    if ua < 0 or ua > 1:
        return None
    
    ub = ((p2.x - p1.x) * (p1.y - p3.y) - (p2.y - p1.y) * (p1.x - p3.x)) / denom
    if ub < 0 or ub > 1:
        return None

    x = p1.x + ua * (p2.x - p1.x)
    y = p1.y + ua * (p2.y - p1.y)

    return Vector2(x, y)

def project_onto_foothold(point, fh_start, fh_end):
    return (point - fh_start).length() / (fh_end - fh_start).length() #TODO: not entirely correct, assumes point is already within segment