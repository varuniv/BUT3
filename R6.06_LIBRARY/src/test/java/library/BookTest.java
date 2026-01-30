package library;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import library.Book;


public class BookTest {
    
    @Test
    void CreationBookTest() {
        Book book = new Book("978-3-16-148410-0", "The Alchimist", "Paulo Coelho", 1988);
        assertEquals("978-3-16-148410-0", book.getIsbn());
        assertEquals("The Alchimist", book.getTitle());
        assertEquals("Paulo Coelho", book.getAuthor());
        assertEquals(1988, book.getYear());
    }

    @Test
    void ToStringBookTest() {
        Book book = new Book("978-3-16-148410-0", "The Alchimist", "Paulo Coelho", 1988);
        String expected = "[978-3-16-148410-0] The Alchimist - Paulo Coelho (1988)";
        assert book.toString().equals(expected);    
        assert !book.toString().equals("Incorrect String");
    }

    @Test
    void MultipleBooksTest() {
        Book book1 = new Book("978-3-16-148410-0", "The Alchimist", "Paulo Coelho", 1925);
        Book book2 = new Book("978-0-14-118263-6", "1984", "George Orwell", 1949);
        assert !book1.getIsbn().equals(book2.getIsbn());
        assert !book1.getTitle().equals(book2.getTitle());  
    }

}
