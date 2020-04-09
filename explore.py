from fitness import get_fitness
from collections import deque
from snek import *

offsets = [(1, 0), (-1, 0), (0, -1), (0, 1)]


class QueryResult:
    def __init__(self, reachable, fitness, moves):
        self.reachable = reachable
        self.fitness = fitness
        self.moves = moves

    def __gt__(self, other):
        if self.reachable == other.reachable:
            return self.fitness > other.fitness
        else:
            return self.reachable


def map_snake(snake):
    ret = [[0 for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
    for r, c in snake:
        ret[r][c] = 1
    return ret


def get_num_moves(r, c, prev):
    cnt = 0

    while r != -1:
        r, c = prev[r][c]
        cnt += 1

    return cnt - 1


def get_moves(r, c, prev):
    moves = deque()

    while r != -1:
        moves.appendleft((r, c))
        r, c = prev[r][c]

    moves.popleft()
    return moves


def is_valid(r, c):
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE


def explore_bfs(snake, tr, tc):
    hr, hc = snake[-1]

    visited = [[False for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
    prev = [[(-1, -1) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

    for r, c in snake:
        visited[r][c] = True

    q = deque()
    q.append((hr, hc))

    while q:
        r, c = q.popleft()

        for dr, dc in offsets:
            nr = r + dr
            nc = c + dc

            if is_valid(nr, nc) and not visited[nr][nc]:
                visited[nr][nc] = True
                prev[nr][nc] = (r, c)
                q.append((nr, nc))

    for r, c in snake:
        visited[r][c] = False

    total_dist = (LIMIT + get_num_moves(tr, tc, prev)) if visited[tr][tc] else -1

    if visited[tr][tc] and total_dist < TIME_OUT:
        moves = get_moves(tr, tc, prev)
        tmp_snake = (snake + moves)

        while len(tmp_snake) != len(snake) + 1:
            tmp_snake.popleft()

        hr, hc = tmp_snake[-1]
        return QueryResult(True, get_fitness(hr, hc, map_snake(tmp_snake)), moves)
    else:
        return QueryResult(False, get_fitness(hr, hc, map_snake(snake)), deque())


def explore_aux(snake, blocks, tr, tc, step):
    hr, hc = snake[-1]

    if (hr, hc) == (tr, tc):
        return QueryResult(True, get_fitness(hr, hc, map_snake(snake)), deque([(hr, hc)]))
    elif step == LIMIT:
        if tr == -1:
            return QueryResult(False, get_fitness(hr, hc, map_snake(snake)), deque([(hr, hc)]))
        else:
            ret = explore_bfs(snake, tr, tc)
            ret.moves.appendleft((hr, hc))
            return ret

    tail = snake[0]
    snake.popleft()
    ret = QueryResult(False, -1, deque())
    blocks.remove(tail)

    for dr, dc in offsets:
        nr = hr + dr
        nc = hc + dc

        if is_valid(nr, nc) and (nr, nc) not in blocks:
            snake.append((nr, nc))
            blocks.add((nr, nc))

            if (nr, nc) == (tr, tc):
                snake.appendleft(tail)
                blocks.add(tail)

            ret = max(ret, explore_aux(snake, blocks, tr, tc, step + 1))

            if (nr, nc) == (tr, tc):
                snake.popleft()
                blocks.remove(tail)

            snake.pop()
            blocks.remove((nr, nc))

    blocks.add(tail)
    snake.appendleft(tail)
    ret.moves.appendleft((hr, hc))

    return ret


def explore(snake, tr, tc):
    blocks = set(snake)
    return explore_aux(snake, blocks, tr, tc, 0)

