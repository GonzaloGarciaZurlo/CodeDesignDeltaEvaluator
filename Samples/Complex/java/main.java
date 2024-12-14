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
