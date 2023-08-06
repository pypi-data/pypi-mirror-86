# -*- coding: utf-8 -*-

import sys


def solution():
    N = int(sys.stdin.readline())
    qu = [];
    for _ in range(N):
        arr = sys.stdin.readline().split()
        if arr[0] == 'push':
            qu.append(arr[1])
        elif arr[0] == 'pop':
            if qu: print(qu.pop(0))
            else: print(-1)
        elif arr[0] == 'size':
            print((len(qu)))
        elif arr[0] == 'empty':
            print(1-int(bool(qu)))
        elif arr[0] == 'front':
            if qu: print(qu[0])
            else: print(-1)
        elif arr[0] == 'back':
            if qu: print(qu[-1])
            else: print(-1)
        else:
            pass


if __name__ == "__main__":
    solution();