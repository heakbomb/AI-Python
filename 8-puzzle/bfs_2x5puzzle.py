############################
# bfs_2x5puzzle.py
############################

from collections import deque

def print_state(state_str):
    """
    현재 상태(길이 10 문자열)를 2×5 형태로 출력하는 유틸 함수.
    예) '2194705368'
       => 2 1 9 4 7
          0 5 3 6 8
    """
    for i in range(0, 10, 5):
        print(" ".join(state_str[i:i+5]))
    print()

def get_neighbors(state_str):
    """
    현재 상태에서 '0'(빈칸)을 상/하/좌/우로 이동해
    생성할 수 있는 다음 상태(문자열)들을 반환.
    
    퍼즐 형태: 2행 × 5열 = 총 10칸
    인덱스 -> (row, col)
      row = index // 5 (0~1)
      col = index % 5  (0~4)
    """
    neighbors = []
    zero_index = state_str.index('0')
    
    row = zero_index // 5
    col = zero_index % 5
    
    # 상하좌우 이동 정의
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in directions:
        nr = row + dr
        nc = col + dc
        # 유효 범위 (row: 0~1, col: 0~4)
        if 0 <= nr < 2 and 0 <= nc < 5:
            swap_index = nr * 5 + nc
            state_list = list(state_str)
            # '0'과 swap_index 위치의 문자 교환
            state_list[zero_index], state_list[swap_index] = state_list[swap_index], state_list[zero_index]
            neighbors.append("".join(state_list))
    
    return neighbors

def bfs_puzzle(start_state, goal_state):
    """
    너비 우선 탐색(BFS)을 이용해 퍼즐을 푸는 함수.
    - queue(덱) 사용
    - (상태, 경로)를 튜플로 저장
    - 방문 집합(visited)을 사용해 중복 상태 방지
    - 해를 찾으면 '최단 경로' 보장
    """
    queue = deque([(start_state, [])])
    visited = set([start_state])
    
    expand_count = 0
    
    while queue:
        current_state, path = queue.popleft()
        expand_count += 1
        
        print(f"[BFS - Expand #{expand_count}] (깊이={len(path)})")
        print_state(current_state)
        
        if current_state == goal_state:
            print("[BFS] 솔루션 찾음!\n")
            solution_path = path + [current_state]
            for idx, st in enumerate(solution_path):
                print(f"Step {idx}:")
                print_state(st)
            return True
        
        # 이웃 상태 확장
        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [current_state]))
    
    print("[BFS] 실패: 목표 상태를 찾지 못했습니다.")
    return False

if __name__ == "__main__":
    # 초기 상태
    start_state = "2194705368"
    # 목표 상태
    goal_state = "0123456789"
    
    print("[BFS 2x5 퍼즐 시작]")
    bfs_puzzle(start_state, goal_state)
