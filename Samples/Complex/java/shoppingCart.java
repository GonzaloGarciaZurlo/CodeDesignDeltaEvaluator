// Clase ShoppingCart tiene una composición con Customer
import java.util.ArrayList;
import java.util.List;

class ShoppingCart {
    private Customer customer;
    private List<String> items;

    public ShoppingCart(Customer customer) {
        this.customer = customer;
        this.items = new ArrayList<>();
    }

    public void addItem(String item) {
        items.add(item);
    }

    public float getTotal() {
        return items.size() * 10.0f; // Por simplicidad, cada artículo cuesta 10 USD
    }
}
