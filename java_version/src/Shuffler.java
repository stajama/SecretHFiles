import java.util.Random;
import java.util.ArrayList;

public class Shuffler {
	
	public Shuffler() {
		
	}
	
	public ArrayList<String> shuffle(ArrayList<String> shuffleDeck) {
		ArrayList<String> returnList = new ArrayList<String>();
		Random generator = new Random();
		while (! shuffleDeck.isEmpty()) {
			int len = shuffleDeck.size();
			int select = generator.nextInt(len);
			returnList.add(shuffleDeck.get(select));
			shuffleDeck.remove(select);
		}
		return returnList;
	}

}
