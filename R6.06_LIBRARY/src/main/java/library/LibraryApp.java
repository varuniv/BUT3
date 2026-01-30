package library;

import java.util.Locale;
import java.util.Scanner;

/**
 * Application de gestion de bibliothèque refactorée (R6.06).
 * Utilise les méthodes statiques de la classe Library.
 */
public class LibraryApp {

    private static final Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.println("Welcome to Library v1.2");

        boolean running = true;
        while (running) {
            displayMenu();
            String choice = sc.nextLine();

            if ("1".equals(choice)) {
                uiAddBook();
            } else if ("2".equals(choice)) {
                uiListBooks();
            } else if ("3".equals(choice)) {
                uiBorrowBook();
            } else if ("4".equals(choice)) {
                uiReturnBook();
            } else if ("5".equals(choice)) {
                uiFindByAuthor();
            } else if ("6".equals(choice)) {
                running = false;
            } else {
                System.out.println("Unknown option.");
            }
        }
        System.out.println("Bye.");
    }

    private static void displayMenu() {
        System.out.println("\n1) Add book  2) List books  3) Borrow  4) Return  5) Find by author  6) Exit");
        System.out.print("> ");
    }

    /**
     * Ajoute un livre en utilisant Library.addBook
     */
    private static void uiAddBook() {
        System.out.print("ISBN? ");
        String isbn = sc.nextLine();
        System.out.print("Title? ");
        String title = sc.nextLine();
        System.out.print("Author? ");
        String author = sc.nextLine();
        System.out.print("Year? ");
        int year = parseYear(sc.nextLine());

        // Création de l'objet Book et ajout via la nomenclature de Library
        Book newBook = new Book(isbn, title, author, year);
        Library.addBook(newBook);
        
        System.out.println("Book added successfully.");
    }

    /**
     * Liste les livres en utilisant Library.getBooks et Library.isBorrowed
     */
    private static void uiListBooks() {
        if (Library.getBooks().isEmpty()) {
            System.out.println("No books in library.");
            return;
        }
        for (Book b : Library.getBooks()) {
            // Utilise Library.isBorrowed(isbn) pour vérifier le statut
            String status = Library.isBorrowed(b.getIsbn()) ? " [BORROWED]" : "";
            System.out.println(b + status);
        }
    }

    
    /**
     * Emprunte un livre en utilisant Library.byIsbn et Library.borrowBook
     */
    private static void uiBorrowBook() {
        System.out.print("ISBN to borrow? ");
        String isbn = sc.nextLine();
        
        Book book = Library.byIsbn(isbn);
        if (book == null) {
            System.out.println("Error: Book not found.");
            return;
        }

        if (Library.isBorrowed(isbn)) {
            System.out.println("Error: Already borrowed.");
        } else {
            System.out.print("Borrower name? ");
            String name = sc.nextLine();
            // Utilise la nomenclature Library.borrowBook(String, String)
            Library.borrowBook(isbn, name);
            System.out.println("Loan registered.");
        }
    }

    /**
     * Retourne un livre en utilisant Library.removeLoan
     */
    private static void uiReturnBook() {
        System.out.print("ISBN to return? ");
        String isbn = sc.nextLine();
        
        if (Library.isBorrowed(isbn)) {
            // Utilise la nomenclature Library.removeLoan(String)
            Library.removeLoan(isbn);
            System.out.println("Book returned.");
        } else {
            System.out.println("Error: This book was not borrowed.");
        }
    }

    /**
     * Recherche par auteur via Library.getBooks
     */
    private static void uiFindByAuthor() {
        System.out.print("Author contains? ");
        String filter = sc.nextLine().toLowerCase(Locale.ROOT);
        
        boolean found = false;
        for (Book b : Library.getBooks()) {
            if (b.getAuthor().toLowerCase(Locale.ROOT).contains(filter)) {
                String status = Library.isBorrowed(b.getIsbn()) ? " [BORROWED]" : "";
                System.out.println(b + status);
                found = true;
            }
        }
        if (!found) System.out.println("No books found for this author.");
    }

    private static int parseYear(String yearStr) {
        try {
            return Integer.parseInt(yearStr);
        } catch (NumberFormatException ex) {
            System.out.println("Invalid year, defaulting to 0");
            return 0;
        }
    }
}