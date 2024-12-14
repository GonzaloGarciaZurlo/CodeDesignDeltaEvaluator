// Clase Order tiene una agregación con Customer y DiscountManager
import java.util.ArrayList;
import java.util.List;

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
