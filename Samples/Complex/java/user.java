// Clase abstracta User
abstract class User {
    protected String username;
    protected String email;

    public User(String username, String email) {
        this.username = username;
        this.email = email;
    }

    public abstract String getRole();
}