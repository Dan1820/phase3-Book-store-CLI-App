# import csv
# import os

# # Function to load books from a CSV file


# def load_books():
#     with open('lib/books.csv', 'r') as file:
#         reader = csv.DictReader(file)
#         books = list(reader)
#     return books

# # Function to save books to a CSV file


# def save_books(books):
#     fieldnames = books[0].keys()
#     with open('lib/books.csv', 'w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(books)

# # Function to display the main menu


# def display_menu():
#     print("Welcome to the Book Store Management App!")
#     print("1. Add Book")
#     print("2. Update Book")
#     print("3. Search Books")
#     print("4. Process Sale")
#     print("5. Generate Report")
#     print("6. Quit")

# # Function to add a book to the inventory


# def add_book(books):
#     book = {}
#     book['Title'] = input("Enter the book title: ")
#     book['Author'] = input("Enter the author name: ")
#     book['Price'] = float(input("Enter the price: "))
#     book['Quantity'] = int(input("Enter the quantity: "))
#     books.append(book)
#     save_books(books)
#     print("Book added successfully!")

# # Function to update a book in the inventory


# def update_book(books):
#     title = input("Enter the book title to update: ")
#     for book in books:
#         if book['Title'] == title:
#             book['Author'] = input("Enter the author name: ")
#             book['Price'] = float(input("Enter the price: "))
#             book['Quantity'] = int(input("Enter the quantity: "))
#             save_books(books)
#             print("Book updated successfully!")
#             return
#     print("Book not found!")

# # Function to search books by title or author


# def search_books(books):
#     keyword = input("Enter the book title or author name: ")
#     results = []
#     for book in books:
#         if keyword.lower() in book['Title'].lower() or keyword.lower() in book['Author'].lower():
#             results.append(book)
#     if results:
#         print("Search Results:")
#         for book in results:
#             print(
#                 f"Title: {book['Title']}, Author: {book['Author']}, Price: {book['Price']}, Quantity: {book['Quantity']}")
#     else:
#         print("No books found!")

# # Function to process a sale and update the inventory


# def process_sale(books):
#     title = input("Enter the book title to sell: ")
#     for book in books:
#         if book['Title'] == title:
#             quantity = int(input("Enter the quantity to sell: "))
#             if quantity <= book['Quantity']:
#                 book['Quantity'] -= quantity
#                 save_books(books)
#                 print("Sale processed successfully!")
#             else:
#                 print("Insufficient quantity!")
#             return
#     print("Book not found!")

# # Function to generate a report of the current inventory


# def generate_report(books):
#     print("Inventory Report:")
#     for book in books:
#         print(
#             f"Title: {book['Title']}, Author: {book['Author']}, Price: {book['Price']}, Quantity: {book['Quantity']}")

# # Main function to run the application


# def main():
#     books = load_books()
#     while True:
#         display_menu()
#         choice = input("Enter your choice (1-6): ")
#         if choice == '1':
#             add_book(books)
#         elif choice == '2':
#             update_book(books)
#         elif choice == '3':
#             search_books(books)
#         elif choice == '4':
#             process_sale(books)
#         elif choice == '5':
#             generate_report(books)
#         elif choice == '6':
#             print("Thank you for using the Book Store Management App!")
#             break
#         else:
#             print("Invalid choice. Please try again.")


# if __name__ == '__main__':
#     main()
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    quantity = Column(Integer)

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}', quantity='{self.quantity}')>"


class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    quantity = Column(Integer)
    total_price = Column(Integer)

    book = relationship("Book", backref="sales")

    def __repr__(self):
        return f"<Sale(book='{self.book}', quantity='{self.quantity}', total_price='{self.total_price}')>"


class StoreManagementApp:
    def __init__(self):
        self.engine = create_engine('sqlite:///bookstore.db')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add_book(self, title, author, quantity):
        book = Book(title=title, author=author, quantity=quantity)
        self.session.add(book)
        self.session.commit()
        print("Book added successfully.")

    def update_book(self, book_id, title=None, author=None, quantity=None):
        book = self.session.query(Book).get(book_id)
        if not book:
            print("Book not found.")
            return

        if title:
            book.title = title
        if author:
            book.author = author
        if quantity:
            book.quantity = quantity

        self.session.commit()
        print("Book updated successfully.")

    def search_books(self, keyword):
        books = self.session.query(Book).filter(
            Book.title.ilike(f"%{keyword}%") | Book.author.ilike(
                f"%{keyword}%")
        ).all()

        if books:
            print("Search results:")
            for book in books:
                print(book)
        else:
            print("No books found.")

    def process_sale(self, book_id, quantity):
        book = self.session.query(Book).get(book_id)
        if not book:
            print("Book not found.")
            return

        if book.quantity < quantity:
            print("Insufficient stock.")
            return

        total_price = quantity * 10  # Assuming each book costs $10

        sale = Sale(book_id=book_id, quantity=quantity,
                    total_price=total_price)
        self.session.add(sale)
        self.session.commit()

        book.quantity -= quantity
        self.session.commit()
        print("Sale processed successfully.")

    def generate_report(self):
        total_sales = self.session.query(Sale).count()
        total_books = self.session.query(Book).count()

        print("-------- Report --------")
        print(f"Total Sales: {total_sales}")
        print(f"Total Books: {total_books}")


if __name__ == '__main__':
    app = StoreManagementApp()

    while True:
        print("\n--- Book Store Management App ---")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Search Books")
        print("4. Process Sale")
        print("5. Generate Report")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            quantity = int(input("Enter book quantity: "))
            app.add_book(title, author, quantity)

        elif choice == '2':
            book_id = int(input("Enter book ID: "))
            title = input("Enter new title (press Enter to skip): ")
            author = input("Enter new author (press Enter to skip): ")
            quantity = input("Enter new quantity (press Enter to skip): ")

            if not any([title, author, quantity]):
                print("No updates specified.")
                continue

            if quantity:
                quantity = int(quantity)

            app.update_book(book_id, title, author, quantity)

        elif choice == '3':
            keyword = input("Enter book title or author: ")
            app.search_books(keyword)

        elif choice == '4':
            book_id = int(input("Enter book ID: "))
            quantity = int(input("Enter quantity sold: "))
            app.process_sale(book_id, quantity)

        elif choice == '5':
            app.generate_report()

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")
