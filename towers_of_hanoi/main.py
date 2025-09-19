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
    def __init__(self, id: str, n_disks: int = 0):
        self.id = id
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
        try:
            self.disks.pop()
        except IndexError:
            raise InvalidMoveException(f"Invalid move! Tower {self.id} is empty!")


class Game:
    def __init__(self, n_disks: int):
        self.n_disks = n_disks
        self.ongoing = True
        # self.state = GameState(n_disks)
        self.towers = {
                "1": Tower(id="1", n_disks=self.n_disks),
                "2": Tower(id="2"),
                "3": Tower(id="3"),
        }

    def play_next_round(self):
        def get_user_input(msg: str, valid_input: list):
            while True:
                user_input = input(msg)
                if not user_input in valid_input:
                    logger.error(f"Invalid user input detected: {user_input}")
                    print(f"Invalid input! Valid options: {valid_input}")
                    continue

                return user_input

        valid_input = list(self.towers.keys())
        user_input = get_user_input(
                "Which disk do you want to play? (q to quit) ",
                valid_input + ["q"],
        )

        if user_input == "q":
            logger.info("User decided to quit, ending game...")
            self.ongoing = False
            self.debug(f"Set {self.ongoing=}.")
            return

        valid_input.remove(user_input)

        user_input = get_user_input(
                "Where do you want to place the disk?",
                valid_input,
        )
        
        # check for validity, error message and return if invalid

        


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
