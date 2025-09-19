import dataclasses
import logging
import argparse

logger = logging.getLogger()


class InvalidMoveException(Exception):
    pass


@dataclasses.dataclass(frozen=True, order=True)
class Disk:
    radius: int


class Tower:
    def __init__(self, n_disks: int = 0):
        self.disks = []
        if n_disks > 0:
            for radius in range(n_disks, 0):
                disk = Disk(radius)
                self.add_disk(disk)

    def add_disk(self, disk: Disk):
        if disk.radius > self.disks[-1].radius:
            raise InvalidMoveException("Invalid move!")
        self.disks.append(Disk)

    def remove_disk(self) -> Disk:
        return self.disks.pop()


class Game:
    def __init__(self, n_disks: int):
        self.n_disks = n_disks
        self.ongoing = True
        self.state = GameState(n_disks)

    def play_next_round(self):
        user_input = input("Which disk do you want to play? (q to quit)")
        if user_input == "q":
            self.ongoing = False
            return


        pass


def main(n:int=0)->None:
    logger.info(f"Starting Game for n={n}")
    game = Game(n)
    while game.ongoing:
        logger.info(f"Starting next round.")
        game.play_next_round()

    logger.info(f"Finished Game.")


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)-8s %(module)s %(funcName)s %(message)s",
        handlers=[
            logging.FileHandler("hanoi-plain.log", mode="a"),
            logging.StreamHandler(),
        ],
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, help="number of disks")
    args = parser.parse_args()

    main(args.n)
