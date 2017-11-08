import java.util.Random;
import java.util.logging.*;
import java.util.Scanner;
import java.util.concurrent.ExecutionException;
import java.util.ArrayList;

public class GameState {
	
	private ArrayList<Player> playerList;
	private ArrayList<String> drawDeck;
	private ArrayList<String> discardPile;
	private ArrayList<String> policyList;
	private ArrayList<String> toBePresidentList;
	private String president;
	private String chancellor;
	private String previousPresident;
	private String previousChancellor;
	private int electionTrack;
	private int availableBullets;
	private boolean vetoAvailable;
	private boolean peeked;
	private boolean selected;
	private int viewed;
	private String prospectiveChancellor;
	
	public GameState(ArrayList<Player> players) {
		this.setPlayerList(players);
		this.setDrawDeck(new ArrayList<String>());
		this.setDiscardPile(new ArrayList<String>());
		this.setPolicyList(new ArrayList<String>());
		this.setToBePresidentList(new ArrayList<String>());
		this.setPresident(null);
		this.setChancellor(null);
		this.setPreviousPresident(null);
		this.setPreviousChancellor(null);
		this.prospectiveChancellor = null;
		this.setElectionTrack(0);
		this.setAvailableBullets(2);
		this.setVetoAvailable(false);
		this.setPeeked(false);
		this.setSelected(false);
		this.setViewed(0);
	}

	public ArrayList<Player> getPlayerList() {
		return playerList;
	}

	public void setPlayerList(ArrayList<Player> playerList) {
		this.playerList = playerList;
	}

	public ArrayList<String> getDrawDeck() {
		return drawDeck;
	}

	public void setDrawDeck(ArrayList<String> drawDeck) {
		this.drawDeck = drawDeck;
	}

	public ArrayList<String> getDiscardPile() {
		return discardPile;
	}

	public void setDiscardPile(ArrayList<String> discardPile) {
		this.discardPile = discardPile;
	}

	public ArrayList<String> getPolicyList() {
		return policyList;
	}

	public void setPolicyList(ArrayList<String> policyList) {
		this.policyList = policyList;
	}

	public ArrayList<String> getToBePresidentList() {
		return toBePresidentList;
	}

	public void setToBePresidentList(ArrayList<String> toBePresidentList) {
		this.toBePresidentList = toBePresidentList;
	}

	public String getPresident() {
		return president;
	}

	public void setPresident(String president) {
		this.president = president;
	}

	public int getElectionTrack() {
		return electionTrack;
	}

	public void setElectionTrack(int electionTrack) {
		this.electionTrack = electionTrack;
	}

	public int getAvailableBullets() {
		return availableBullets;
	}

	public void setAvailableBullets(int availableBullets) {
		this.availableBullets = availableBullets;
	}

	public String getChancellor() {
		return chancellor;
	}

	public void setChancellor(String chancellor) {
		this.chancellor = chancellor;
	}

	public String getPreviousPresident() {
		return previousPresident;
	}

	public void setPreviousPresident(String previousPresident) {
		this.previousPresident = previousPresident;
	}

	public String getPreviousChancellor() {
		return previousChancellor;
	}

	public void setPreviousChancellor(String previousChancellor) {
		this.previousChancellor = previousChancellor;
	}

	public boolean isVetoAvailable() {
		return vetoAvailable;
	}

	public void setVetoAvailable(boolean vetoAvailable) {
		this.vetoAvailable = vetoAvailable;
	}

	public boolean isPeekAvailable() {
		return peeked;
	}

	public void setPeeked(boolean peeked) {
		this.peeked = peeked;
	}

	public boolean isSelectionAvailable() {
		return selected;
	}

	public void setSelected(boolean selected) {
		this.selected = selected;
	}

	public int getViewed() {
		return this.viewed;
	}

	public void setViewed(int viewed) {
		this.viewed = viewed;
	}
	
	public ArrayList<String> printPlayersForSelection(boolean dontPrint) {
		this.LOGGER.log(Level.INFO, "GameState.printPlayersForSelection() START\nDo NOT Print?:" + dontPrint);
		ArrayList<String> outList = new ArrayList<String>();
		for (int i = 0; i < this.playerList.size(); i++) {
			if (this.playerList.get(i).isAlive()) {
				outList.add(this.playerList.get(i).getName());
			}
		}
		this.LOGGER.log(Level.INFO, "GameState.printPlayersForSelection() - var outList: " + outList.toString());
		if (!dontPrint) {
			for (int i = 0; i < outList.size(); i++) {
				String x = Integer.toString(i);
				System.out.println(x + ": " + outList.get(i));
			}
		}
		return outList;
	}
	
	public void clearAllRoles() {
		this.LOGGER.log(Level.INFO, "GameState.clearAllRoles START");
		for (int i = 0; i < this.playerList.size(); i++) {
			this.playerList.get(i).clearRole();
			this.LOGGER.log(Level.INFO, "GameState.clearAllRoles()\nConfirm info cleared: " + this.playerList.get(i).getName() + ", role:" + this.playerList.get(i).getRole() + ", party: " + this.playerList.get(i).getParty());
		}
	}
	
	public void resetDeck() {
		this.LOGGER.log(Level.INFO, "GameState.resetDeck() START\nCurrent drawDeck: " + this.drawDeck.toString());
		this.LOGGER.log(Level.INFO, "GameState.resetDeck() START\nCurrent discardPile: " + this.discardPile.toString());
		Shuffler shuffler = new Shuffler();
		ArrayList<String> hold = new ArrayList<String>(this.discardPile);
		for (int i = 0; i < this.drawDeck.size(); i++) {
			hold.add(this.drawDeck.get(i));
		}
		ArrayList<String> newDeck = shuffler.shuffle(hold);
		this.drawDeck = newDeck;
		this.discardPile = new ArrayList<String>();
		this.LOGGER.log(Level.INFO, "GameState.resetDeck() END\nFinal drawDeck: " + this.drawDeck.toString());
		this.LOGGER.log(Level.INFO, "GameState.resetDeck() END\nFinal discardPile: " + this.discardPile.toString());
	}
	
	public void setUpPolicyDeck() {
		this.LOGGER.log(Level.INFO, "GameState.setUpPolicyDeck() START\nConfirm deck empty to start: " + this.drawDeck.toString());
		Shuffler shuffler = new Shuffler();
		ArrayList<String> hold = new ArrayList<String>();
		for (int i = 0; i < 6; i++) {
			hold.add("Liberal");
		}
		for (int i = 0; i < 11; i++) {
			hold.add("Fascist");
		}
		ArrayList<String> newDeck = shuffler.shuffle(hold);
		this.drawDeck = newDeck;
		this.LOGGER.log(Level.INFO, "GameState.resetDeck() END\nFinal drawDeck: " + this.drawDeck.toString());
		this.LOGGER.log(Level.INFO, "GameState.setUpPolicyDeck() END\nConfirm discardPile still emptyt: " + this.discardPile.toString());
	}
	
	public Player findPlayer(String playerName) throws IndexOutOfBoundsException {
		this.LOGGER.log(Level.INFO, "GameState.findPlayer START, searching for \"" + playerName + "\"");
		for (int i = 0; i < this.playerList.size(); i++) {
			Player test = this.playerList.get(i);
			this.LOGGER.log(Level.INFO, "GameState.setUpMatch() looking at " + test.getName());
			this.LOGGER.log(Level.WARNING, "comparing: " + test.getName() + " to " + playerName + "\n" + Boolean.toString(test.getName() == playerName));
			if (test.getName().equals(playerName)) {
				return test;
			}
		}
		throw new IndexOutOfBoundsException();
	}
	
	public void setUpMatch() {
		this.LOGGER.log(Level.INFO, "GameState.setUpMatch() START\n");
		ArrayList<String> rolesList = new ArrayList<String>();
		int libs;
		int fasc;
		if (this.playerList.size() == 5) {
			libs = 3;
			fasc = 1;
		} else if (this.playerList.size() == 6) {
			libs = 4;
			fasc = 1;
		} else if (this.playerList.size() == 7) {
			libs = 4;
			fasc = 2;
		} else if (this.playerList.size() == 8) {
			libs = 5;
			fasc = 2;
		} else if (this.playerList.size() == 9) {
			libs = 5;
			fasc = 3;
		} else {
			libs = 6;
			fasc = 3;
		}
		for (int i = 0; i < libs; i++) {
			rolesList.add("Liberal");
		}
		for (int i = 0; i < fasc; i++) {
			rolesList.add("Fascist");
		}
		this.LOGGER.log(Level.INFO, "GameState.setUpMatch() \nConfirm available roles correct for " + this.playerList.size() + " players: " + rolesList.toString());
		rolesList.add("Hitler");
		Shuffler shuffler = new Shuffler();
		ArrayList<String> rolesListShuffled = shuffler.shuffle(rolesList);
		for (int i = 0; i < this.playerList.size(); i++) {
			this.playerList.get(i).assignRole(rolesListShuffled.get(i));
			this.LOGGER.log(Level.INFO, "GameState.setUpMatch() END\nRoles assigned. " + this.playerList.get(i).getName() + ", " + this.playerList.get(i).getParty() + ", " + this.playerList.get(i).getRole());
		}
	}
	
	public int getSurvivingPlayerCount() {
		int counter = 0;
		for (int i = 0; i < this.playerList.size(); i++) {
			Player current = playerList.get(i);
			if (current.isAlive()) {
				counter++;
			}
		}
		return counter;
	}
	
	public int policyCounterLiberal() {
		int lib = 0;
		for (int i = 0; i < this.policyList.size(); i++) {
			if (this.policyList.get(i) == "Liberal") {
				lib++;
			}
		}
		return lib;
	}
	
	public int policyCounterFascist() {
		int lib = 0;
		for (int i = 0; i < this.policyList.size(); i++) {
			if (this.policyList.get(i) != "Liberal") {
				lib++;
			}
		}
		return lib;
	}
	
	public boolean fascistElectionWin() {
		if (this.policyCounterFascist() >= 3) {
			return this.findPlayer(this.chancellor).playerShotOrElected(); 
		}
		return false;
	}
	
	public boolean fascistPolicyWin() {
		return this.policyCounterFascist() >= 6;
	}
	
	public boolean liberalPolicyWin() {
		return this.policyCounterLiberal() >= 5;
	}
	
	public boolean liberalAssassinateHilterWin() {
		for (int i = 0; i < this.playerList.size(); i++) {
			if (!this.playerList.get(i).isAlive() && this.playerList.get(i).getRole() == "Hitler") {
				return true;
			}
		}
		return false;
	}
	
	public boolean electionTracker(ArrayList<Boolean> voteList) {
		int ja = 0;
		int nien = 0;
		for (int i = 0; i < voteList.size(); i++) {
			if (voteList.get(i)) {
				ja++;
			} else {
				nien++;
			}
		}
		return ja > nien;
	}
	
	public void electedChancellor(String newChancellor) {
		this.previousChancellor = this.chancellor = newChancellor;
		if (this.president.endsWith("*")) {
			this.previousPresident = this.president.substring(0, this.president.length() - 2);
		} else {
			this.previousPresident = this.president;
		}
	}
	
	public boolean canBeChancellor(String selectedChancellor) {
		int currentPlayers = this.getSurvivingPlayerCount();
		if (currentPlayers <= 5) {
			return selectedChancellor != this.previousChancellor && selectedChancellor != this.president && selectedChancellor != this.president + "*";
		} else {
			return selectedChancellor != this.previousChancellor && selectedChancellor != this.previousPresident && 
					selectedChancellor != this.president && selectedChancellor != this.president + "*";
		}
	}
	
	public void canVeto() {
		if (this.policyCounterFascist() >= 5) {
			this.vetoAvailable = true;
		}
	}
	
	public void policyHandling() {
		this.LOGGER.log(Level.INFO,  "START policyHandling");
		//TODO: Need to try/catch user input.
		if (this.drawDeck.size() < 3) {
			this.resetDeck();
		}
		ArrayList<String> hand = new ArrayList<String>(3);
		for (int i = 0; i < 3; i++) {
			hand.add(this.drawDeck.get(0));
			this.drawDeck.remove(0);
		}
		// to the current President
		for (int i = 0; i < 3; i++) {
			String x = Integer.toString(i);
			System.out.println(x + ": " + hand.get(i));
		}
		int toDiscard;
		this.LOGGER.log(Level.INFO,  "policyHandling, President selects: " + hand.toString());
		while (true) {
			System.out.println("Select a card to discard.");
			Scanner user_input = new Scanner(System.in);
			toDiscard = Integer.parseInt(user_input.next());
			if (toDiscard >= 0 && toDiscard <= 2) {
				this.LOGGER.log(Level.INFO,  "START selection number: " + toDiscard);
				break;
			} else {
				System.out.println("must enter number from 0 to 2");
			}
		}
		this.discardPile.add(hand.get(toDiscard));
		hand.remove(toDiscard);
		this.LOGGER.log(Level.INFO,  "policyHandling, Confirm correct card discarded.\nHand: " + hand.toString() + "\n discardPile: " + this.discardPile.toString());
		// to Chancellor
		this.LOGGER.log(Level.INFO,  "policyHandling, Chancellor chooses.");
		for (int i = 0; i < 2; i++) {
			String x = Integer.toString(i);
			System.out.println(x + ": " + hand.get(i));
		}
		int toPlay = 100; // set to impossible number. In line 374, if variable is not reset due to veto, asks for President confirmation.
		if (this.vetoAvailable) {
			this.LOGGER.log(Level.INFO,  "policyHandling, Veto active.");
			String vetoGuard;
			while (true) {
				System.out.println("Select a card to play. You have the option to veto these policies.");
				Scanner user_input = new Scanner(System.in);
				vetoGuard = user_input.next();
				if (vetoGuard == "veto") {
					break;
				} else {
					toPlay = Integer.parseInt(vetoGuard);
					if (toPlay == 0 || toPlay == 1) {
						this.LOGGER.log(Level.INFO,  "policyHandling, Selected card: " + toPlay);
						break;
					} else {
						System.out.println("Number must be a number 1 or 2. You may also enter 'veto' to veto current agendas.");
					}
				}
			}
			this.LOGGER.log(Level.INFO,  "policyHandling, Chancellor choice, veto active: " + toPlay);
			if (toPlay == 100) {
				this.LOGGER.log(Level.INFO,  "policyHandling, Chancellor request veto:");
				System.out.println("The Chancellor has chosen to veto the current set of agendas.");
				//Back to President
				System.out.println("Will you accept the motion to veto?");
				Scanner user_input = new Scanner(System.in);
				String choice = user_input.next();
				if (choice.contains("y") || choice.contains("Y")) {
					System.out.println("The President has accepted the veto motion and no policy was passed.");
					for (int i = 0; i < 2; i++) {
						this.discardPile.add(hand.get(i));
					}
				} else {
					System.out.println("The President has rejected the motion to veto. A policy must now be selected.");
					while (true) {
						// back to Chancellor
						System.out.println("Select a card to play. You now must select a policy to enact.");
						user_input = new Scanner(System.in);
						toPlay = Integer.parseInt(user_input.next());
						if (toPlay == 0 || toPlay == 1) {
							this.LOGGER.log(Level.INFO,  "policyHandling, Selected card: " + toPlay);
							break;
						} else {
							System.out.println("Number must be a number 1 or 2.");

						}
					}
				}
			}
			if (toPlay == 100) {
				System.out.println("Current policy choices have been successfully vetoed.\n Election Tracker increases by 1.");
				this.electionTrack++;
			} else {
				System.out.println("A " + hand.get(toPlay) + " policy was enacted.");
				this.policyList.add(hand.get(toPlay));
				hand.remove(toPlay);
				this.discardPile.add(hand.get(0));
				this.LOGGER.log(Level.INFO,  "policyHandling, END VETO Check all\npolicyList: : " + this.policyList.toString() + "\nDiscardPile: " + this.discardPile.toString());
			}
		} else {
			while (true) {
				// to Chancellor
				this.LOGGER.log(Level.INFO,  "policyHandling, Chancellor choosing.");
				System.out.println("Select a card to play.");
				Scanner user_input = new Scanner(System.in);
				toPlay = Integer.parseInt(user_input.next());
				if (toPlay == 0 || toPlay == 1) {
					this.LOGGER.log(Level.INFO,  "policyHandling, Chancellor playing " + toPlay);
					break;
				} else {
					System.out.println("Number must be a number 1 or 2.");
				}
			}
			System.out.println("A " + hand.get(toPlay) + " policy was enacted.");
			this.policyList.add(hand.get(toPlay));
			hand.remove(toPlay);
			this.discardPile.add(hand.get(0));
			this.LOGGER.log(Level.INFO,  "policyHandling, END Check all\npolicyList: : " + this.policyList.toString() + "\nDiscardPile: " + this.discardPile.toString());
		}
	}
	
	public void showPartyCard(String showing) {
		// to this.president
		Player outed = this.findPlayer(showing);
		System.out.println(outed.getName() + " is a filthy " + outed.getParty() + "!!!");
	}
	
	public void executePlayer() {
		//TODO - check user inputs.
		if (this.policyCounterFascist() > 3 && this.availableBullets > 0) {
			this.LOGGER.log(Level.INFO,  "executePlayer, START:");
			System.out.println("The President must now execute a player of their choice.");
			// to this.president
			System.out.println("Select a player.");
			ArrayList<String> livingPlayers = this.printPlayersForSelection(false);
			Scanner user_input = new Scanner(System.in);
			String choice = user_input.next();
			int toKill = Integer.parseInt(choice);
			System.out.println(this.president + " has formally executed " + livingPlayers.get(toKill) + ".");
			Player isDead = this.findPlayer(livingPlayers.get(toKill));
			isDead.setAlive(false);
			this.LOGGER.log(Level.INFO,  "executePlayer, END, " + isDead.getName() + " should be dead: "  + this.findPlayer(isDead.getName()).isAlive());
		}
	}
	
	public boolean electionSetup() {
		boolean success = false;
		int toChoose;
		System.out.println(this.president + " will now nominate a Chancellor.");
		while (true) {
			// to this.president
			System.out.println("Select a running mate.");
			ArrayList<String> selection = this.printPlayersForSelection(false);
			while (true) {
				Scanner user_input = new Scanner(System.in);
				String choice = user_input.next();
				toChoose = Integer.parseInt(choice);
				if (toChoose >= 0 && toChoose < selection.size()) {
					break;
				} else { 
					System.out.println("must enter number corresponding with nominated player.");
				}
			}
			if (this.canBeChancellor(selection.get(toChoose))) {
				System.out.println(selection.get(toChoose) + " has been nominated for Chancellor.");
				this.prospectiveChancellor = selection.get(toChoose);
				if (this.electionTracker(this.getVotes())) {
					this.electedChancellor(this.prospectiveChancellor);
					System.out.println("President " + this.president + " and Chancellor " + this.chancellor + " have been successfully elected.");
					success = true;
					this.electionTrack = 0;
					break;
				} else {
					System.out.println("President " + this.president + " and Chancellor " + this.chancellor + " have NOT been elected.");
					this.electionTrack++;
					this.president = this.previousPresident;
					break;
				}
			} else {
				System.out.println("This candidate can not be nominated.");
			}
		}
		this.citizensFrustrated();
		return success;
	}
	
	public ArrayList<Boolean> getVotes() {
		ArrayList<Boolean> voteList = new ArrayList<Boolean>();
		ArrayList<String> playersVoting = this.printPlayersForSelection(true);
		for (int i = 0; i < playersVoting.size(); i++) {
			Scanner user_input = new Scanner(System.in);
			System.out.println(playersVoting.get(i) + ", cast your vote.");
			String vote = user_input.next();
			if (vote.contains("j") || vote.contains("J") ||vote.contains("y") ||vote.contains("Y")) {
				voteList.add(true);
			} else {
				voteList.add(false);
			}
		}
		return voteList;
	}
	
	public void viewPartyAffiliation() {
		// to this.president
		if ((this.policyCounterFascist() == 2 && (this.playerList.size() == 7 || this.playerList.size() == 8) && this.viewed < 1) || 
				((this.policyCounterFascist() != 0 && (this.playerList.size() == 9 || this.playerList.size() == 10) && this.viewed < 2))) {
			this.viewed++;
			System.out.println("The President may now view the party affiliation card of another player.");
			while (true) {
				ArrayList<String> selection = this.printPlayersForSelection(false);
				System.out.println("Select a player to view their affiliation.");
				Scanner user_input = new Scanner(System.in);
				String choice = user_input.next();
				int chosen = Integer.parseInt(choice);
				if (chosen >= 0 && chosen < selection.size()) {
					this.showPartyCard(selection.get(chosen));
					break;
				} else {
					System.out.println("You must select the number corresponding to the player who's party membership card you would like to see.");
				}
			}
		}
	}
	
	public void policyPeek() {
		if (this.policyCounterFascist() == 3 && this.playerList.size() < 7 && !this.peeked) {
			//to this.president
			System.out.println("The President may now view the top 3 cards on the policy deck.");
			if (this.drawDeck.size() < 3) {
				this.resetDeck();
			}
			for (int i = 0; i < 3; i++) {
				System.out.println(this.drawDeck.get(i));
			}
		}
	}
	
	public void nextPresident() {
		//TODO check handling of * in appointed president. need to remove * for other checks to work
		//TODO selectNextPresident not making appointed president next president
		while (true) {
			this.LOGGER.log(Level.INFO, "GameState.nextPresident() \"START\" \nPrevious President: " + this.previousPresident + "\nCurrent President: " + this.president + "\nList of presidents: " + this.toBePresidentList.toString());
			if (!this.toBePresidentList.get(0).contains("*")) {
				this.LOGGER.log(Level.INFO, "GameState.nextPresident() - Regular presidential transition.");
		        this.previousPresident = this.president;
		        String hold = this.toBePresidentList.get(0);
		        this.president = hold;
		        this.toBePresidentList.remove(0);
		        this.toBePresidentList.add(hold);
			} else {
				this.LOGGER.log(Level.INFO, "GameState.nextPresident() - Dealing with appointed president");
				this.previousPresident = this.president;
				int x = toBePresidentList.get(0).length();
				this.president = this.toBePresidentList.get(0).substring(0, x - 1);
				this.toBePresidentList.remove(0);
				this.LOGGER.log(Level.INFO, "GameState.nextPresident() - appointed END, toBePresident: " + this.toBePresidentList.toString() + "\nPresident: " + this.president);
			}
			
			if (this.findPlayer(this.president).isAlive()) {
				break;
			}
		this.LOGGER.log(Level.INFO, "GameState.nextPresident() \"END\" \nPrevious President: " + this.previousPresident + "\nCurrent President: " + this.president + "\nList of presidents: " + this.toBePresidentList.toString());
		}
	}
	
	public void selectNextPresident() {
		if (this.policyCounterFascist() == 3 && this.playerList.size() >= 7 && !this.selected) {
			this.selected = true;
	        System.out.println("The President may now select the next Presidential Candidate.");
	        while (true) {
	        	//to this.president
	        	System.out.println("Please select a candidate: ");
	        	ArrayList<String> selection = this.printPlayersForSelection(false);
				System.out.println("Select a player to be president next round.");
				Scanner user_input = new Scanner(System.in);
				String choice = user_input.next();
				int chosen = Integer.parseInt(choice);
				if (chosen >= 0 && chosen <= selection.size() - 1) {
	                System.out.println("President " + this.president + " has selected " + selection.get(chosen) + " to be the next Presidential Candidate.");
	                this.toBePresidentList.add(0, selection.get(chosen) + "*"); 
					break;
				} else {
					System.out.println("You must select the number corresponding to the player you wish to nominate.");
				} 
	        }
		}
	}
	
	public void citizensFrustrated() {
	    if (this.electionTrack >= 4) {
	        System.out.println("The people are unhappy and have forced a policy through.");
	        String forced = this.drawDeck.get(0);
	        this.drawDeck.remove(0);
	        System.out.println("It was a " + forced + " policy!");
	        this.policyList.add(forced);
	        this.electionTrack = 0;
	    }
	}

	public void everyoneUp() {
		for (int i = 0; i < this.playerList.size(); i++) {
			this.playerList.get(i).setAlive(true);
		}
	}
	
	public void wantLogging(boolean yeah) {
		if (!yeah) {
			this.LOGGER.setLevel(Level.SEVERE);
		}
	}
	private final static Logger LOGGER = Logger.getLogger("gamestateLog");

}
