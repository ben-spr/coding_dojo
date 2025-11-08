import java.util.ArrayDeque;

class TowerGame{
    int disc_number;
    ArrayDeque<Integer>[] slots;

    TowerGame(int num_discs){
        this.disc_number = num_discs;
        this.slots = new ArrayDeque[]{
                new ArrayDeque<Integer>(),
                new ArrayDeque<Integer>(),
                new ArrayDeque<Integer>(),
        };
        for (int i = num_discs; i > 0; i--) {
//            System.out.println("Attempting to add to slots[0], i=" + i);
            this.slots[0].addLast(i);
        };
//      System.out.println(String.format("Disc number set: %d", this.disc_number));
//        System.out.println(String.format("Slot 0 set: %s", this.slots[0].toString()));
    }

}

class towers{
    public static void main (String[] args) {
        TowerGame game = new TowerGame(4);
    }
}
