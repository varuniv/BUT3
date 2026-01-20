
package library;

import java.util.*;

/**
 * Console app for a tiny library.
 * 
 */
public class LibraryApp {

    public static void main(String[] args) {
        System.out.println("Welcome to Library v1.0");
        Scanner sc = new Scanner(System.in);
        while (true) {
            System.out.println("\n1) Add book  2) List books  3) Borrow  4) Return  5) Find by author  6) Exit");
            System.out.print("> ");
            String choice = sc.nextLine();
            if ("1".equals(choice)) {
               
                System.out.print("ISBN? ");
                String isbn = sc.nextLine();
                System.out.print("Title? ");
                String title = sc.nextLine();
                System.out.print("Author? ");
                String author = sc.nextLine();
                System.out.print("Year? ");
                String yearStr = sc.nextLine();
                int year = 0;
                try {
                    year = Integer.parseInt(yearStr);
                } catch (Exception ex) {
                    System.out.println("Invalid year, defaulting to 0");
                }
                
                for (Book b : Library.books) {
                    if (b.getIsbn().equals(isbn) || b.getTitle().equalsIgnoreCase(title)) {
                        System.out.println("Warning: similar book already exists.");
                    }
                }
                Book b = new Book(isbn, title, author, year);
                Library.books.add(b);
                System.out.println("Added: " + b);
            } else if ("2".equals(choice)) {
               
                for (Book b : Library.books) {
                    System.out.println(b + (Library.loans.containsKey(b.getIsbn()) ? " [BORROWED]" : ""));
                }
            } else if ("3".equals(choice)) {
                System.out.print("Borrower name? ");
                String n = sc.nextLine();
                System.out.print("ISBN to borrow? ");
                String ib = sc.nextLine();
                
                Book found = null;
                for (Book x : Library.books) {
                    if (x.getIsbn().equals(ib)) { found = x; break; }
                }
                if (found == null) {
                    System.out.println("Not found.");
                } else if (Library.loans.containsKey(ib)) {
                    System.out.println("Already borrowed.");
                } else {
                    Library.loans.put(ib, new Borrower(n));
                    System.out.println("OK.");
                }
            } else if ("4".equals(choice)) {
                System.out.print("ISBN to return? ");
                String ib = sc.nextLine();
                if (Library.loans.remove(ib) != null) {
                    System.out.println("Returned.");
                } else {
                    System.out.println("Not borrowed.");
                }
            } else if ("5".equals(choice)) {
                System.out.print("Author contains? ");
                String a = sc.nextLine().toLowerCase(Locale.ROOT);
                
                for (Book b : Library.books) {
                    if (b.getAuthor().toLowerCase(Locale.ROOT).contains(a)) {
                        System.out.println(b + (Library.loans.containsKey(b.getIsbn()) ? " [BORROWED]" : ""));
                    }
                }
            } else if ("6".equals(choice)) {
                break;
            } else {
                System.out.println("Unknown option.");
            }
        }
      
        System.out.println("Bye.");
    }
}
