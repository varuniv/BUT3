package library;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import library.Book;
import library.Library;
import library.Borrower;
import library.LibraryApp;

public class LibraryTest {
    
    @BeforeEach
    public void setup() {
        Library.getBooks().clear();
        Library.getLoans().clear();
    }
    @BeforeAll
    public static void CreationLibraryTest() {
        Library.getBooks().clear();
        Library.getLoans().clear();
        Library library = new Library();
        assert Library.getBooks() != null;
        assert Library.getLoans() != null;
        System.out.println(Library.getBooks());
        assert Library.getBooks().isEmpty();
        assert Library.getLoans().isEmpty();
    }

    @Test
    public void ByIsbnTest() {
        Book book = new Book("978-3-16-148410-0", "The Alchimist", "Paulo Coelho", 1988);
        Library.getBooks().add(book);
        Book foundBook = Library.byIsbn("978-3-16-148410-0");
        Book notFoundBook = Library.byIsbn("000-0-00-000000-0");
        assert notFoundBook == null;
        assert foundBook != null;
        assert foundBook.getTitle().equals("The Alchimist");
    }

    @Test
    public void IsBorrowedTest() {
        Book book = new Book("978-3-16-148410-0", "The Alchimist", "Paulo Coelho", 1988);
        Borrower borrower = new Borrower("Jean Pierre Polnareff");
        Library.getBooks().add(book);
        Library.getLoans().put(book.getIsbn(), borrower);
        assert Library.isBorrowed("978-3-16-148410-0") == true;
        assert Library.isBorrowed("978-0-14-118263-6") == false;
    }   

    @Test 
    public void DooubleAdditionTest() {
        Book book1 = new Book("978-3-16-148410-0", "The Alchimist", "Paulo Coelho", 1988);
        Book book2 = new Book("978-3-16-148410-0", "The Alchimist", "Paulo Coelho", 1988);
        Library.getBooks().add(book1);
        Library.getBooks().add(book2);
        assert Library.getBooks().size() == 2;
    }

    
}
