# 10.10.2025 - Türme von Hanoi - https://de.wikipedia.org/wiki/T%C3%BCrme_von_Hanoi
import itertools
import pytest


class Game:
    def __init__(self, disc_number: int = 1):
        self.disc_number = disc_number
        self.slot = [
            [size for size in range(disc_number, 0, -1)],
            [],
            [],
        ]

    def __str__(self) -> str:
        cell_length = self.disc_number * 2 + 1
        rows = []
        for (cell1, cell2, cell3) in itertools.zip_longest(*self.slot, fillvalue=None):
            str1 = f"{'-' * (cell1 * 2 - 1)}" if cell1 else ""
            str2 = f"{'-' * (cell2 * 2 - 1)}" if cell2 else ""
            str3 = f"{'-' * (cell3 * 2 - 1)}" if cell3 else ""

            rows.append(f"|{str1:^{cell_length}}|{str2:^{cell_length}}|{str3:^{cell_length}}|")

        empty_cell = f"{' '*cell_length}"
        empty_line = empty_cell.join("|" * 4)
        for _ in range(self.disc_number - len(rows)):
            rows.append(empty_line)

        result = "\n".join(reversed(rows))
        return result

    def move(self, from_slot:int, to_slot:int)->None:
        print(f"before move")
        print(self)
        self.slot[to_slot].append(self.slot[from_slot].pop())
        print(f"after move")
        print(self)

    def solve(self)->None:
        self._solve(0, 2, self.disc_number)
        # Ziel: Alle scheiben "sortiert" auf letzten Slot bewegen (0->2)

    def _solve(self, from_slot:int, to_slot:int, n_disks:int):
        if n_disks == 1:
            self.move(from_slot=from_slot, to_slot=to_slot)
            return
        new_target = 3 ^ (from_slot | to_slot)
        self._solve(from_slot=from_slot, to_slot=new_target, n_disks=n_disks-1)
        self.move(from_slot=from_slot, to_slot=to_slot)
        self._solve(from_slot=new_target, to_slot=to_slot, n_disks=n_disks-1)



def test_game_solver_with_3_disks():
    disc_num = 3
    game = Game(disc_num)
    game.solve()
    assert str(game) =="""
|       |       |   -   |
|       |       |  ---  |
|       |       | ----- |""".strip()

def test_game_state_after_two_moves():
    disc_num = 3
    game = Game(disc_num)
    game.move(from_slot=0, to_slot=1)
    game.move(from_slot=0, to_slot=2)
    assert str(game) =="""
|       |       |       |
|       |       |       |
| ----- |   -   |  ---  |""".strip()

def test_game_state_after_one_move():
    disc_num = 2
    game = Game(disc_num)
    game.move(from_slot=0, to_slot=1)
    assert str(game) =="""
|     |     |     |
| --- |  -  |     |""".strip()

def test_initial_state_with_four_disks():
    disc_num = 4
    game = Game(disc_num)
    assert str(game) == """
|    -    |         |         |
|   ---   |         |         |
|  -----  |         |         |
| ------- |         |         |""".strip()

def test_initial_state_with_three_disks():
    assert str(Game(3)) == """
|   -   |       |       |
|  ---  |       |       |
| ----- |       |       |""".strip()

def test_initial_state_with_two_disks():
    assert str(Game(2)) == """
|  -  |     |     |
| --- |     |     |""".strip()

if __name__ == "__main__":
    pytest.main()
