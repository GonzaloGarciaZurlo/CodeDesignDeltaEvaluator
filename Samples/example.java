import java.util.ArrayList;
import java.util.List;

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

// Nueva clase DiscountManager para gestionar descuentos
class DiscountManager {
    public float calculateDiscount(float total) {
        if (total > 50.0f) {
            return total * 0.1f; // 10% de descuento si el total es mayor a 50 USD
        }
        return 0.0f;
    }
}

// Clase ShoppingCart tiene una composición con Customer
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

// Clase Order tiene una agregación con Customer y DiscountManager
class Order {
    private Customer customer;
    private DiscountManager discountManager;
    private List<String> items;

    public Order(Customer customer, DiscountManager discountManager) {
        this.customer = customer;
        this.discountManager = discountManager;
        this.items = new ArrayList<>();
    }

    public void addItem(String item) {
        items.add(item);
    }

    public void processOrder() {
        System.out.println("Processing order for " + customer.getRole() + " with items:");
        for (String item : items) {
            System.out.println("- " + item);
        }
        float total = items.size() * 10.0f;
        float discount = discountManager.calculateDiscount(total);
        float finalTotal = total - discount;
        System.out.println("Total: " + total + " USD");
        System.out.println("Discount: " + discount + " USD");
        System.out.println("Final total after discount: " + finalTotal + " USD");
    }
}

// Clase principal
public class Main {
    public static void main(String[] args) {
        Customer customer = new Customer("JaneDoe", "jane@example.com", 456);
        DiscountManager discountManager = new DiscountManager();

        // Creando el carrito de compras y agregando items
        ShoppingCart cart = new ShoppingCart(customer);
        cart.addItem("Tablet");
        cart.addItem("Headphones");

        // Creando la orden y procesándola
        Order order = new Order(customer, discountManager);
        order.addItem("Tablet");
        order.addItem("Headphones");
        order.processOrder();
    }
}
