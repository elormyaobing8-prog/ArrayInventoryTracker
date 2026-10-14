# Array Inventory Tracker

A small C++17 console app that demonstrates how an array can organize real
inventory records. Add products, list and find them, update quantities, and
calculate the value of all stock.

## Why an array?

The app stores products in a fixed-size `std::array<Product, 20>`. Each
position holds one product, and an index lets the program visit or find records
with a loop. A separate count tracks how many positions are currently in use.
The program checks the capacity before adding a product and only reads entries
below that count.

The fixed capacity keeps this example focused on arrays. A production system
with a changing number of products would usually use `std::vector` or a
database.

## Build and run

You need a C++17 compiler such as g++ or Clang:

```text
g++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o inventory
```

On Windows with MinGW, run the resulting program with:

```text
.\inventory.exe
```

On macOS or Linux, run:

```text
./inventory
```

## Menu

- Add a product (up to 20 products)
- List all products and their stock values
- Find a product by its exact name
- Update a product's quantity
- Calculate the total value of all stock

Product names must be unique. Quantities and prices cannot be negative.

## Files

- `main.cpp` — the C++ inventory app
- `arrays_explained.pdf` — an introduction to arrays and real-world examples
- `generate_pdf.py` — regenerates the PDF using only Python's standard library
