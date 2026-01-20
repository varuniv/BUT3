package legacy;

import org.junit.jupiter.api.Test;

import library.Book;
import library.Library;
import library.Borrower;
import library.LibraryApp;

public class LibraryTest {
    
    @Test 
    public void CreationLibraryTest() {
        Library library = new Library();
        assert Library.books != null;
        assert Library.loans != null;
        assert Library.books.isEmpty();
        assert Library.loans.isEmpty();
    }

    @Test
    public void ByIsbnTest() {
        Book book = new Book("978-3-16-148410-0", "The Alchimist", "Paulo Coelho", 1988);
        Library.books.add(book);
        Book foundBook = Library.byIsbn("978-3-16-148410-0");
        assert foundBook != null;
        assert foundBook.getTitle().equals("The Alchimist");
    }

    @Test
    public void IsBorrowedTest() {
        Book book = new Book("978-3-16-148410-0", "The Alchimist", "Paulo Coelho", 1988);
        Borrower borrower = new Borrower("Jean Pierre Polnareff");
        Library.books.add(book);
        Library.loans.put(book.getIsbn(), borrower);
        assert Library.isBorrowed("978-3-16-148410-0") == true;
        assert Library.isBorrowed("978-0-14-118263-6") == false;
    }   

    @Test 
    public void DooubleAdditionTest() {
        Book book1 = new Book("978-3-16-148410-0", "The Alchimist", "Paulo Coelho", 1988);
        Book book2 = new Book("978-3-16-148410-0", "The Alchimist", "Paulo Coelho", 1988);
        Library.books.add(book1);
        Library.books.add(book2);
        assert Library.books.size() == 2;
    }

    
}
