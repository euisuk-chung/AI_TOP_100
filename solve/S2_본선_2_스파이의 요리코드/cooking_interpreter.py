"""
요리코드(Cooking Code) 인터프리터
Q9 스파이의 요리코드 문제 해결용
"""
import re
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


class CookingInterpreter:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.containers: Dict[str, int] = defaultdict(int)  # 식기 (변수)
        self.ingredients: Dict[str, int] = {}  # 재료 (상수)
        self.recipes: Dict[str, List[str]] = {}  # 레시피 (함수)
        self.output: List[int] = []  # 출력 결과

    def log(self, msg: str):
        if self.debug:
            print(f"[DEBUG] {msg}")

    def parse_calories_table(self, lines: List[str]) -> int:
        """칼로리 테이블 파싱, 파싱된 줄 수 반환"""
        idx = 0
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            if "칼로리 테이블" in line or "Kcal" in line:
                continue
            # 재료 = 값 형식
            match = re.match(r'(\S+)\s*=\s*(\d+)', line)
            if match:
                name, val = match.groups()
                self.ingredients[name] = int(val)
                self.log(f"재료 등록: {name} = {val}")
                idx = i + 1
            else:
                break
        return idx

    def parse_recipes(self, lines: List[str]) -> int:
        """레시피 파싱, 파싱된 줄 수 반환"""
        idx = 0
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # 레시피 시작: "XXX 레시피:" 형식
            match = re.match(r'(\S+)\s*레시피\s*:', line)
            if match:
                recipe_name = match.group(1)
                recipe_lines = []
                i += 1
                while i < len(lines):
                    rline = lines[i].strip()
                    if rline == "끝.":
                        i += 1
                        break
                    if rline:
                        recipe_lines.append(rline)
                    i += 1
                self.recipes[recipe_name] = recipe_lines
                self.log(f"레시피 등록: {recipe_name} -> {recipe_lines}")
                idx = i
            elif "요리시작:" in line or "요리시작" in line:
                return idx
            else:
                i += 1
                idx = i
        return idx

    def normalize(self, text: str) -> str:
        """조사 제거 (를, 을, 가, 이 등)"""
        # 끝에 붙은 조사 제거
        text = re.sub(r'(를|을|가|이|의|에|로|으로)$', '', text)
        return text

    def execute_line(self, line: str) -> bool:
        """단일 명령어 실행, 계속 진행 여부 반환"""
        line = line.strip()
        if not line or line == "끝.":
            return True

        # 1. 재료 넣기: "식기에 재료를 N번 넣는다." 또는 "식기에 재료를 넣는다."
        match = re.match(r'(\S+)에\s+(\S+?)(를|을)?\s*(\d+)?번?\s*넣는다\.?', line)
        if match:
            container, ingredient, _, count = match.groups()
            container = self.normalize(container)
            ingredient = self.normalize(ingredient)
            count = int(count) if count else 1
            if ingredient in self.ingredients:
                val = self.ingredients[ingredient] * count
                self.containers[container] += val
                self.log(f"넣기: {container} += {ingredient}({self.ingredients[ingredient]}) * {count} = {self.containers[container]}")
            else:
                self.log(f"WARNING: 알 수 없는 재료: {ingredient}")
            return True

        # 2. 내용물 옮기기: "A의 내용물을 B로 옮긴다."
        match = re.match(r'(\S+?)의\s*내용물을\s+(\S+?)(로|으로)\s*옮긴다\.?', line)
        if match:
            src, dst, _ = match.groups()
            src = self.normalize(src)
            dst = self.normalize(dst)
            self.containers[dst] += self.containers[src]
            self.log(f"옮기기: {dst} += {src}({self.containers[src]}) -> {dst}={self.containers[dst]}, {src}=0")
            self.containers[src] = 0
            return True

        # 3. 가열 (분): "식기를 N분간 가열한다."
        match = re.match(r'(\S+?)(를|을)?\s*(\d+)분간?\s*가열한다\.?', line)
        if match:
            container, _, minutes = match.groups()
            container = self.normalize(container)
            minutes = int(minutes)
            self.containers[container] *= minutes
            self.log(f"가열(분): {container} *= {minutes} -> {self.containers[container]}")
            return True

        # 4. 가열 (초): "식기를 N초간 가열한다."
        match = re.match(r'(\S+?)(를|을)?\s*(\d+)초간?\s*가열한다\.?', line)
        if match:
            container, _, seconds = match.groups()
            container = self.normalize(container)
            seconds = int(seconds)
            divisor = 60 // seconds
            self.containers[container] //= divisor
            self.log(f"가열(초): {container} //= {divisor} -> {self.containers[container]}")
            return True

        # 5. 출력: "식기를 식탁 위에 올려두었다."
        match = re.match(r'(\S+?)(를|을)?\s*식탁\s*위에\s*올려두었다\.?', line)
        if match:
            container = match.group(1)
            container = self.normalize(container)
            val = self.containers[container]
            self.output.append(val)
            self.log(f"출력: {container} = {val}")
            return True

        # 6. 레시피 호출: "XXX를 N번 만든다." 또는 "XXX를 만든다." 또는 "XXX 레시피를 N번 만든다."
        match = re.match(r'(.+?)(\s*레시피)?(를|을)\s*(\d+)?번?\s*만든다\.?', line)
        if match:
            recipe_name = match.group(1).strip()
            has_recipe_keyword = match.group(2) is not None
            count = match.group(4)
            recipe_name = self.normalize(recipe_name)
            count = int(count) if count else 1
            if recipe_name in self.recipes:
                for _ in range(count):
                    self.execute_block(self.recipes[recipe_name])
                self.log(f"레시피 호출: {recipe_name} * {count}")
            else:
                self.log(f"WARNING: 알 수 없는 레시피: {recipe_name}")
            return True

        self.log(f"알 수 없는 명령어: {line}")
        return True

    def execute_block(self, lines: List[str]):
        """명령어 블록 실행 (조건문 처리 포함)"""
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            # 조건문 처리: "만약 A가 B보다 내용물이 많으면:" 또는 "만약 A와 B의 내용물이 같으면:"
            if line.startswith("만약"):
                # 조건 파싱 - 패턴 1: A가 B보다
                condition_match = re.match(r'만약\s+(\S+)가?\s+(\S+)보다\s+내용물이\s+(많으면|적으면|같으면|다르면|많거나\s*같으면|적거나\s*같으면)\s*:?', line)
                # 조건 파싱 - 패턴 2: A와 B의 내용물이 같으면/다르면
                if not condition_match:
                    condition_match = re.match(r'만약\s+(\S+)와?\s+(\S+)의\s+내용물이\s+(같으면|다르면)\s*:?', line)

                if condition_match:
                    a, b, comp = condition_match.groups()
                    val_a = self.containers[a]
                    val_b = self.containers[b]

                    condition_met = False
                    if "많으면" in comp and "같으면" not in comp:
                        condition_met = val_a > val_b
                    elif "적으면" in comp and "같으면" not in comp:
                        condition_met = val_a < val_b
                    elif "같으면" in comp and "많거나" not in comp and "적거나" not in comp:
                        condition_met = val_a == val_b
                    elif "다르면" in comp:
                        condition_met = val_a != val_b
                    elif "많거나" in comp and "같으면" in comp:
                        condition_met = val_a >= val_b
                    elif "적거나" in comp and "같으면" in comp:
                        condition_met = val_a <= val_b

                    self.log(f"조건: {a}({val_a}) {comp} {b}({val_b}) -> {condition_met}")

                    # 조건문 블록 추출
                    i += 1
                    true_block = []
                    false_block = []
                    in_else = False
                    depth = 1

                    while i < len(lines) and depth > 0:
                        sub_line = lines[i].strip()
                        if sub_line.startswith("만약"):
                            depth += 1
                        if sub_line == "끝.":
                            depth -= 1
                            if depth == 0:
                                i += 1
                                break
                        if "그렇지 않으면" in sub_line and depth == 1:
                            in_else = True
                            i += 1
                            continue
                        if depth > 0:
                            if in_else:
                                false_block.append(sub_line)
                            else:
                                true_block.append(sub_line)
                        i += 1

                    if condition_met:
                        self.execute_block(true_block)
                    else:
                        self.execute_block(false_block)
                    continue
                else:
                    # 단순 조건문: 같은 줄에 명령어가 있는 경우
                    self.log(f"복잡한 조건문: {line}")
                    i += 1
                    continue

            self.execute_line(line)
            i += 1

    def run(self, code: str) -> List[int]:
        """전체 코드 실행"""
        lines = code.split('\n')

        # 1. 칼로리 테이블 파싱
        cal_idx = 0
        for i, line in enumerate(lines):
            if "칼로리 테이블" in line or "Kcal" in line:
                cal_idx = i
                break

        # 칼로리 테이블 파싱
        table_lines = []
        for i in range(cal_idx + 1, len(lines)):
            line = lines[i].strip()
            if not line:
                continue
            match = re.match(r'(\S+)\s*=\s*(\d+)', line)
            if match:
                name, val = match.groups()
                self.ingredients[name] = int(val)
                self.log(f"재료 등록: {name} = {val}")
            else:
                break

        # 2. 레시피 파싱
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            match = re.match(r'(.+?)\s*레시피\s*:', line)
            if match:
                recipe_name = match.group(1).strip()
                recipe_lines = []
                i += 1
                while i < len(lines):
                    rline = lines[i].strip()
                    if rline == "끝.":
                        i += 1
                        break
                    if rline:
                        recipe_lines.append(rline)
                    i += 1
                self.recipes[recipe_name] = recipe_lines
                self.log(f"레시피 등록: {recipe_name} -> {len(recipe_lines)}줄")
            else:
                i += 1

        # 3. 요리시작 블록 찾기 및 실행
        main_block = []
        in_main = False
        depth = 0  # 조건문/레시피 깊이 추적
        for line in lines:
            line_stripped = line.strip()
            if "요리시작:" in line_stripped or "요리시작" == line_stripped:
                in_main = True
                continue
            if in_main:
                # 조건문 시작 추적
                if line_stripped.startswith("만약"):
                    depth += 1
                # 끝. 처리
                if line_stripped == "끝.":
                    if depth > 0:
                        depth -= 1
                        main_block.append(line_stripped)
                        continue
                    else:
                        break  # 메인 블록 종료
                if line_stripped:
                    main_block.append(line_stripped)

        self.log(f"메인 블록: {len(main_block)}줄")
        self.execute_block(main_block)

        return self.output


def solve_q1():
    """Q1: 불향가득 단짠 제육볶음"""
    code = open("/home/euisuk.chung/repo/AI_TOP_100/source/q9/1.txt").read()
    interp = CookingInterpreter(debug=False)
    result = interp.run(code)
    print(f"Q1 결과: {result}")
    # 선택지: 1) 3, 89, 6  2) 6, 78, 14  3) 9, 83, 12  4) 12, 96, 24
    return result


def solve_q3():
    """Q3: 행사용 사리곰탕"""
    code = open("/home/euisuk.chung/repo/AI_TOP_100/source/q9/3.txt").read()
    interp = CookingInterpreter(debug=False)
    result = interp.run(code)
    print(f"Q3 결과: {result}")
    return result


def solve_q4():
    """Q4: 긴 요리코드"""
    code = open("/home/euisuk.chung/repo/AI_TOP_100/source/q9/4.txt").read()
    interp = CookingInterpreter(debug=False)
    result = interp.run(code)
    print(f"Q4 결과: {result}")
    return result


def solve_q5():
    """Q5: 스파이의 결행일"""
    code = open("/home/euisuk.chung/repo/AI_TOP_100/source/q9/5.txt").read()
    interp = CookingInterpreter(debug=False)
    result = interp.run(code)
    print(f"Q5 결과: {result}")
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        q = sys.argv[1]
        if q == "1":
            solve_q1()
        elif q == "3":
            solve_q3()
        elif q == "4":
            solve_q4()
        elif q == "5":
            solve_q5()
        elif q == "debug":
            # 디버그 모드로 Q1 실행
            code = open("/home/euisuk.chung/repo/AI_TOP_100/source/q9/1.txt").read()
            interp = CookingInterpreter(debug=True)
            result = interp.run(code)
            print(f"결과: {result}")
    else:
        print("Q1:")
        solve_q1()
        print("\nQ3:")
        solve_q3()
        print("\nQ5:")
        solve_q5()
