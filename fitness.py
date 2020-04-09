from snek import *

offsets = [(1, 0), (-1, 0), (0, -1), (0, 1)]


def is_blocked(r, c, occ):
    return r < 0 or r >= BOARD_SIZE or c < 0 or c >= BOARD_SIZE or occ[r][c] == 1


def get_sur_cnt(r, c, hr, hc, occ):
    cnt = 0

    for dr, dc in offsets:
        nr = r + dr
        nc = c + dc

        if is_blocked(nr, nc, occ) and (nr, nc) != (hr, hc):
            cnt += 1

    return cnt


def dfs(r, c, occ, visited):
    visited[r][c] = True

    for dr, dc in offsets:
        nr = r + dr
        nc = c + dc

        if not is_blocked(nr, nc, occ) and not visited[nr][nc]:
            dfs(nr, nc, occ, visited)


def mark_failures(hr, hc, occ):
    q = set()

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if occ[r][c] == 0:
                cnt = get_sur_cnt(r, c, hr, hc, occ)

                if cnt >= 3:
                    q.add((r, c))

    while q:
        r, c = q.pop()

        cnt = get_sur_cnt(r, c, hr, hc, occ)

        if cnt >= 3:
            occ[r][c] = 1
            for dr, dc in offsets:
                nr = r + dr
                nc = c + dc

                if not is_blocked(nr, nc, occ):
                    q.add((nr, nc))

    visited = [[False] * BOARD_SIZE for i in range(BOARD_SIZE)]
    dfs(hr, hc, occ, visited)

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if not visited[i][j]:
                occ[i][j] = 1


def get_fitness(hr, hc, occ):
    tmp = [[occ[i][j] for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

    mark_failures(hr, hc, tmp)

    fitness = 0

    for i in range(len(tmp)):
        for j in range(len(tmp[i])):
            if tmp[i][j] == 0:
                fitness += 1

    return fitness

