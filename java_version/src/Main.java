import java.util.*;
import java.util.logging.*;
public class Main {

	public static void main(String[] args) {
		System.out.println("number of players");
		Scanner scanner = new Scanner(System.in);
		String strOfPlayers = scanner.next();
		int numOfPlayers = Integer.parseInt(strOfPlayers);
		ArrayList<Player> playerNames = new ArrayList<Player>();
		for (int i = 0; i < numOfPlayers; i++) {
			String x = Integer.toString(i);
			System.out.println("Player " + x + ", enter your name.");
			scanner = new Scanner(System.in);
			String name = scanner.next();
			playerNames.add(new Player(name));
		}
		boolean keepPlaying = true;
		while (keepPlaying) {
			GameState game = new GameState(playerNames);
			game.wantLogging(false);
			game.everyoneUp();
			System.out.println("Who will be president first?");
			ArrayList<String> playersList = game.printPlayersForSelection(false);
			scanner = new Scanner(System.in);
			String toGo = scanner.next();
			int selectedFirst =  Integer.parseInt(toGo);
			ArrayList<String> presidentList = new ArrayList<String>();
			for (int i = 0; i < game.getPlayerList().size(); i++) {
				int index = i + selectedFirst;
				index = index % game.getPlayerList().size();
				presidentList.add(playersList.get(index));
			}
			game.setToBePresidentList(presidentList);
			game.setUpMatch();
			game.setUpPolicyDeck();
			while (true) {
				game.nextPresident();
				if (game.electionSetup()) {
					if (game.fascistElectionWin()) {
						System.out.println("The Fascists Win");
						break;
					}
					game.policyHandling();
					if (game.fascistPolicyWin()) {
						System.out.println("The Fascists Win");
						break;
					} else if (game.liberalPolicyWin()) {
						System.out.println("The Liberals Win");
						break;
					}
					game.policyPeek();
					game.viewPartyAffiliation();
					game.selectNextPresident();
					game.executePlayer();
					if (game.liberalAssassinateHilterWin()) {
						System.out.println("The Liberals Win");
						break;
					}
				}
			}
			for (int i = 0; i < game.getPlayerList().size(); i++) {
				Player player = game.getPlayerList().get(i);
				System.out.println(player.getName() + " - " + player.getRole() + " - " + player.isAlive());
			}
			System.out.println("Play again?");
			scanner = new Scanner(System.in);
			String playAgain = scanner.next();
			if (playAgain.contains("n") || playAgain.contains("N")) {
				keepPlaying = false;
			}
		}
	}
	
}
