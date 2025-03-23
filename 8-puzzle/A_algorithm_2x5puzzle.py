import heapq

def print_state(state_str):
    """
    (길이 10) 문자열 상태를 2x5 형태로 출력하는 유틸 함수
    예) '2194705368' ->
        2 1 9 4 7
        0 5 3 6 8
    """
    for i in range(0, 10, 5):
        print(" ".join(state_str[i:i+5]))
    print()

def get_neighbors(state_str):
    """
    현재 상태에서 '0'(빈칸)을 상/하/좌/우로 이동해
    만들 수 있는 다음 상태(문자열)들을 반환.
    (2행 × 5열)
    """
    neighbors = []
    zero_index = state_str.index('0')
    
    row = zero_index // 5
    col = zero_index % 5
    
    # 상하좌우
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in directions:
        nr = row + dr
        nc = col + dc
        if 0 <= nr < 2 and 0 <= nc < 5:
            swap_index = nr * 5 + nc
            state_list = list(state_str)
            # '0'과 swap_index 위치 교환
            state_list[zero_index], state_list[swap_index] = state_list[swap_index], state_list[zero_index]
            neighbors.append("".join(state_list))
    
    return neighbors

def manhattan_heuristic(state_str):
    """
    맨해튼 거리(Manhattan distance)를 이용한 휴리스틱 h(n) 계산.
    목표 상태가 "0123456789" 이라고 가정했을 때,
    각 숫자(0~9)가 '자신의 목표 위치'와 얼마나 떨어져 있는지의 합.
    
    - index = 현재 state_str 내 해당 문자의 위치
    - digit = 실제 숫자값
    - (row, col) = index // 5, index % 5
    - (goal_row, goal_col) = digit // 5, digit % 5   (목표 상태에서 'digit'이 위치할 자리)
    - 거리 = abs(row - goal_row) + abs(col - goal_col)
    
    * 보통 '0'(빈 칸)은 휴리스틱 계산에서 제외하기도 하지만
      여기서는 '0'도 하나의 타일로 보고 동일하게 처리해도 무방합니다.
      원하는 대로 조정 가능.
    """
    h = 0
    for i, ch in enumerate(state_str):
        if ch == '0':
            # '0'을 휴리스틱에 포함하지 않으려면 아래 continue
            # 현재 예시에서는 그냥 포함해도 됨
            continue
        
        digit = int(ch)
        # 현재 위치 (i)
        row, col = i // 5, i % 5
        # 목표 위치 (digit)
        goal_row, goal_col = digit // 5, digit % 5
        
        h += abs(row - goal_row) + abs(col - goal_col)
    return h

def a_star_puzzle(start_state, goal_state):
    """
    A* 탐색 알고리즘으로 2x5 퍼즐을 푸는 함수.
    
    - open_list: 우선순위 큐(heapq), 요소 = (f, g, 현재상태, 경로)
      여기서 f = g + h (h = 휴리스틱)
    - g_cost: 각 상태에 도달하기 위한 최적(최소) g 값을 기록하는 dict
    - visited(또는 closed): 이미 '최적 g로' 방문한 상태는 재확장하지 않도록 관리
    """
    # 초기 휴리스틱
    start_h = manhattan_heuristic(start_state)
    
    # 우선순위 큐에 (f, g, state, path) 형태로 저장
    open_list = []
    heapq.heappush(open_list, (start_h, 0, start_state, []))
    
    # 현재까지 알려진 상태별 최소 g값
    g_cost = {start_state: 0}
    
    expand_count = 0
    
    while open_list:
        # f가 가장 작은 요소를 pop
        f, g, current_state, path = heapq.heappop(open_list)
        expand_count += 1
        
        print(f"[A* - Expand #{expand_count}] (g={g}, f={f})")
        print_state(current_state)
        
        # 목표 상태 확인
        if current_state == goal_state:
            print("[A*] 솔루션 찾음!\n")
            solution_path = path + [current_state]
            for idx, st in enumerate(solution_path):
                print(f"Step {idx}:")
                print_state(st)
            return True
        
        # 자식(이웃) 상태 확인
        for neighbor in get_neighbors(current_state):
            new_g = g + 1  # 한 번 이동 비용
            # 휴리스틱 계산
            h = manhattan_heuristic(neighbor)
            new_f = new_g + h
            
            # 아직 방문 안 했거나, 더 적은 g값으로 방문 가능한 경우
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                heapq.heappush(open_list, (new_f, new_g, neighbor, path + [current_state]))
    
    print("[A*] 실패: 목표 상태를 찾지 못했습니다.")
    return False

if __name__ == "__main__":
    # 초기 상태
    start_state = "2194705368"
    # 목표 상태
    goal_state = "0123456789"
    
    print("[A* - 2×5 퍼즐]")
    print("초기 상태:")
    print_state(start_state)
    print("목표 상태:")
    print_state(goal_state)
    
    a_star_puzzle(start_state, goal_state)
