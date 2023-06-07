import csv
import os

# Function to load books from a CSV file


def load_books():
    with open('lib/books.csv', 'r') as file:
        reader = csv.DictReader(file)
        books = list(reader)
    return books

# Function to save books to a CSV file


def save_books(books):
    fieldnames = books[0].keys()
    with open('lib/books.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)

# Function to display the main menu


def display_menu():
    print("Welcome to the Book Store Management App!")
    print("1. Add Book")
    print("2. Update Book")
    print("3. Search Books")
    print("4. Process Sale")
    print("5. Generate Report")
    print("6. Quit")

# Function to add a book to the inventory


def add_book(books):
    book = {}
    book['Title'] = input("Enter the book title: ")
    book['Author'] = input("Enter the author name: ")
    book['Price'] = float(input("Enter the price: "))
    book['Quantity'] = int(input("Enter the quantity: "))
    books.append(book)
    save_books(books)
    print("Book added successfully!")

# Function to update a book in the inventory


def update_book(books):
    title = input("Enter the book title to update: ")
    for book in books:
        if book['Title'] == title:
            book['Author'] = input("Enter the author name: ")
            book['Price'] = float(input("Enter the price: "))
            book['Quantity'] = int(input("Enter the quantity: "))
            save_books(books)
            print("Book updated successfully!")
            return
    print("Book not found!")

# Function to search books by title or author


def search_books(books):
    keyword = input("Enter the book title or author name: ")
    results = []
    for book in books:
        if keyword.lower() in book['Title'].lower() or keyword.lower() in book['Author'].lower():
            results.append(book)
    if results:
        print("Search Results:")
        for book in results:
            print(
                f"Title: {book['Title']}, Author: {book['Author']}, Price: {book['Price']}, Quantity: {book['Quantity']}")
    else:
        print("No books found!")

# Function to process a sale and update the inventory


def process_sale(books):
    title = input("Enter the book title to sell: ")
    for book in books:
        if book['Title'] == title:
            quantity = int(input("Enter the quantity to sell: "))
            if quantity <= book['Quantity']:
                book['Quantity'] -= quantity
                save_books(books)
                print("Sale processed successfully!")
            else:
                print("Insufficient quantity!")
            return
    print("Book not found!")

# Function to generate a report of the current inventory


def generate_report(books):
    print("Inventory Report:")
    for book in books:
        print(
            f"Title: {book['Title']}, Author: {book['Author']}, Price: {book['Price']}, Quantity: {book['Quantity']}")

# Main function to run the application


def main():
    books = load_books()
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ")
        if choice == '1':
            add_book(books)
        elif choice == '2':
            update_book(books)
        elif choice == '3':
            search_books(books)
        elif choice == '4':
            process_sale(books)
        elif choice == '5':
            generate_report(books)
        elif choice == '6':
            print("Thank you for using the Book Store Management App!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
