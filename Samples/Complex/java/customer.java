// Clase concreta Customer hereda de User
class Customer extends User {
    private int customerId;

    public Customer(String username, String email, int customerId) {
        super(username, email);
        this.customerId = customerId;
    }

    @Override
    public String getRole() {
        return "Customer";
    }
}
