#include <array>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

namespace {

constexpr std::size_t MAX_PRODUCTS = 20;

struct Product {
    std::string name;
    int quantity = 0;
    double unitPrice = 0.0;
};

using Inventory = std::array<Product, MAX_PRODUCTS>;

std::string readText(const std::string& prompt) {
    std::string value;
    while (true) {
        std::cout << prompt;
        std::getline(std::cin, value);
        if (!value.empty()) {
            return value;
        }
        std::cout << "Please enter a value.\n";
    }
}

int readInteger(const std::string& prompt, int minimum) {
    while (true) {
        std::cout << prompt;
        std::string input;
        std::getline(std::cin, input);

        std::istringstream stream(input);
        int value = 0;
        char extra = '\0';
        if ((stream >> value) && !(stream >> extra) && value >= minimum) {
            return value;
        }
        std::cout << "Enter a whole number that is at least " << minimum << ".\n";
    }
}

double readPrice(const std::string& prompt) {
    while (true) {
        std::cout << prompt;
        std::string input;
        std::getline(std::cin, input);

        std::istringstream stream(input);
        double value = 0.0;
        char extra = '\0';
        if ((stream >> value) && !(stream >> extra) && std::isfinite(value)
            && value >= 0.0) {
            return value;
        }
        std::cout << "Enter a valid price of zero or more.\n";
    }
}

std::size_t findProduct(const Inventory& inventory, std::size_t count,
                        const std::string& name) {
    for (std::size_t index = 0; index < count; ++index) {
        if (inventory[index].name == name) {
            return index;
        }
    }
    return count;
}

void addProduct(Inventory& inventory, std::size_t& count) {
    if (count == inventory.size()) {
        std::cout << "Inventory is full. The limit is " << inventory.size()
                  << " products.\n";
        return;
    }

    const std::string name = readText("Product name: ");
    if (findProduct(inventory, count, name) != count) {
        std::cout << "That product is already in the inventory.\n";
        return;
    }

    Product product;
    product.name = name;
    product.quantity = readInteger("Quantity: ", 0);
    product.unitPrice = readPrice("Unit price: ");
    inventory[count] = product;
    ++count;
    std::cout << "Product added.\n";
}

void listProducts(const Inventory& inventory, std::size_t count) {
    if (count == 0) {
        std::cout << "The inventory is empty.\n";
        return;
    }

    std::cout << std::left << std::setw(24) << "Product"
              << std::right << std::setw(10) << "Quantity"
              << std::setw(14) << "Unit price"
              << std::setw(16) << "Stock value" << '\n';
    std::cout << std::string(64, '-') << '\n';
    for (std::size_t index = 0; index < count; ++index) {
        const Product& product = inventory[index];
        std::cout << std::left << std::setw(24) << product.name
                  << std::right << std::setw(10) << product.quantity
                  << std::setw(13) << std::fixed << std::setprecision(2)
                  << product.unitPrice
                  << std::setw(15) << product.quantity * product.unitPrice
                  << '\n';
    }
}

void searchProduct(const Inventory& inventory, std::size_t count) {
    const std::string name = readText("Product name to find: ");
    const std::size_t index = findProduct(inventory, count, name);
    if (index == count) {
        std::cout << "Product not found.\n";
        return;
    }

    const Product& product = inventory[index];
    std::cout << product.name << ": " << product.quantity << " in stock at "
              << std::fixed << std::setprecision(2) << product.unitPrice
              << " each.\n";
}

void updateQuantity(Inventory& inventory, std::size_t count) {
    const std::string name = readText("Product name to update: ");
    const std::size_t index = findProduct(inventory, count, name);
    if (index == count) {
        std::cout << "Product not found.\n";
        return;
    }

    inventory[index].quantity = readInteger("New quantity: ", 0);
    std::cout << "Quantity updated.\n";
}

void printStockValue(const Inventory& inventory, std::size_t count) {
    double total = 0.0;
    for (std::size_t index = 0; index < count; ++index) {
        total += inventory[index].quantity * inventory[index].unitPrice;
    }
    std::cout << "Total value of all stock: " << std::fixed
              << std::setprecision(2) << total << '\n';
}

void printMenu() {
    std::cout << "\n=== Array Inventory Tracker ===\n"
              << "1. Add a product\n"
              << "2. List products\n"
              << "3. Find a product\n"
              << "4. Update a product quantity\n"
              << "5. Show total stock value\n"
              << "0. Exit\n";
}

}  // namespace

int main() {
    Inventory inventory{};
    std::size_t count = 0;

    while (true) {
        printMenu();
        const int choice = readInteger("Choose an option: ", 0);
        switch (choice) {
            case 0:
                std::cout << "Goodbye!\n";
                return 0;
            case 1:
                addProduct(inventory, count);
                break;
            case 2:
                listProducts(inventory, count);
                break;
            case 3:
                searchProduct(inventory, count);
                break;
            case 4:
                updateQuantity(inventory, count);
                break;
            case 5:
                printStockValue(inventory, count);
                break;
            default:
                std::cout << "Choose a menu option from 0 to 5.\n";
                break;
        }
    }
}
