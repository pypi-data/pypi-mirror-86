# -*- coding: utf-8 -*-

from sys import stdin


def solution():
    N, M = map(int, stdin.readline().split())

    matrix = [[0]*M for _ in range(N)]
    for i in range(N):
        temp = stdin.readline()
        for j in range(M):
            matrix[i][j] = int(temp[j])

    visited = [[0]*M for _ in range(N)]

    dx, dy = [-1,1,0,0], [0,0,-1,1]

    queue = [(0,0)]
    visited[0][0] = 1

    while queue:
        x, y = queue.pop(0)

        if x == N-1 and y == M-1:
            print(visited[x][y])
            break

        for i in range(4):

            nx = x + dx[i]
            ny = y + dy[i]

            if 0 <= nx < N and 0 <= ny < M:
                if visited[nx][ny] == 0 and matrix[nx][ny] == 1:
                    visited[nx][ny] = visited[x][y] + 1
                    queue.append((nx, ny))


if __name__ == "__main__":
    solution()