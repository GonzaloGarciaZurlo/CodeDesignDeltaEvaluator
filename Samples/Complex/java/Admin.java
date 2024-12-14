// Clase concreta Admin hereda de User
class Admin extends User {
    private int adminLevel;

    public Admin(String username, String email, int adminLevel) {
        super(username, email);
        this.adminLevel = adminLevel;
    }

    @Override
    public String getRole() {
        return "Admin";
    }
}
