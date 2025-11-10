import java.util.ArrayDeque;
import java.util.ArrayList;

class TowerGame{
    int disc_number;
    ArrayDeque<Integer>[] towers;

    TowerGame(int num_discs){
        this.disc_number = num_discs;
        this.towers = new ArrayDeque[]{
                new ArrayDeque<Integer>(),
                new ArrayDeque<Integer>(),
                new ArrayDeque<Integer>(),
        };
        for (int i = num_discs; i > 0; i--) {
//            System.out.println("Attempting to add to towers[0], i=" + i);
            this.towers[0].addLast(i);
        };
//        System.out.println(String.format("Disc number set: %d", this.disc_number));
//        System.out.println(String.format("Tower 0 set: %s", this.towers[0].toString()));
    }

    void move(int from_tower, int to_tower) {
        System.out.println("Before move:");
        this.displayGameState();
        this.towers[to_tower].addLast(this.towers[from_tower].removeLast());
        System.out.println("After move:");
        this.displayGameState();
    }

    void displayGameState() {}
    
    void solve() {
        this.recursive_solver(0, 2, this.disc_number);
    }
    
    protected void recursive_solver(int from_tower, int to_tower, int n_disks) {
        System.out.println("Recursive solver called with from_tower=" + from_tower + ", to_tower=" + to_tower + ", n_disks=" + n_disks);
        System.out.println("Tower state: " + java.util.Arrays.toString(this.towers));
        if (n_disks == 1) {
            this.move(from_tower, to_tower);
            return;
        }
        // TODO: shorten!
        ArrayList<Integer> options = new ArrayList<Integer>();
        options.add(0);
        options.add(1);
        options.add(2);
        options.remove(Integer.valueOf(from_tower));
        options.remove(Integer.valueOf(to_tower));
        int new_target = options.removeLast();
        System.out.println("New target: " + new_target);

        this.recursive_solver(from_tower, new_target, n_disks - 1);
        this.move(from_tower, to_tower);
        this.recursive_solver(new_target, to_tower, n_disks - 1);

    }

}

class towers{
    public static void main (String[] args) {
        TowerGame game = new TowerGame(4);
        System.out.println("Game state after initialization: " + java.util.Arrays.toString(game.towers));
        game.solve();
        System.out.println("Game state after solver finished: " + java.util.Arrays.toString(game.towers));
    }
}
