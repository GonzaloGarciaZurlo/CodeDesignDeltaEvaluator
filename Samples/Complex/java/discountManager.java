// Clase DiscountManager para gestionar descuentos
class DiscountManager {
    public float calculateDiscount(float total) {
        if (total > 50.0f) {
            return total * 0.1f; // 10% de descuento si el total es mayor a 50 USD
        }
        return 0.0f;
    }
}
