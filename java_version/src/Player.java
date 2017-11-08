
public class Player {

	private String name;
	private String party;
	private String role;
	private boolean alive;
	
	public Player() {
		
	}
	public Player(String name) {
		this.name = name;
	}
	
	public String getName() {
		return name;
	}

	public String getParty() {
		return party;
	}

	public String getRole() {
		return role;
	}

	public boolean isAlive() {
		return alive;
	}

	public void setAlive(boolean alive) {
		this.alive = alive;
	}
	
	public void assignRole(String role) {
		this.role = role;
		if (this.role == "Hitler") {
			this.party = "Fascist";
		} else {
			this.party = role;
		}
	}
	
	public void clearRole() {
		this.role = null;
	}
	
	public boolean playerShotOrElected() {
		return this.role == "Hitler";
	}
	
}

