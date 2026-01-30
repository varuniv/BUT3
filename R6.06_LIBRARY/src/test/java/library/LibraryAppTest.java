package library;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.assertNull;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.PrintStream;
import java.util.*;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import library.Book;
import library.Library;
import library.Borrower;
import library.LibraryApp;


class LibraryAppTest {

    @BeforeEach
    void reset() {
        Library.getBooks().clear();
        Library.getLoans().clear();
    }

    private void runApp(String input) {
        InputStream in = new ByteArrayInputStream(input.getBytes());
        System.setIn(in);
        LibraryApp.main(new String[]{});
    }

    @Test
    void addAndListBook() {
        runApp(
                "1\n123\nJava\nBob\n2020\n" +
                "2\n" +
                "6\n"
        );

        assertEquals(1, Library.getBooks().size());
        assertEquals("123", Library.getBooks().get(0).getIsbn());
    }

    @Test
    void borrowAndReturnBook() {
        Library.getBooks().add(new Book("1", "Test", "Me", 2022));

        runApp(
                "3\nAlice\n1\n" +
                "4\n1\n" +
                "6\n"
        );

        assertFalse(Library.isBorrowed("1"));
    }

    @Test
    void borrowUnknownBook() {
        runApp(
                "3\nBob\n999\n" +
                "6\n"
        );

        assertTrue(Library.getLoans().isEmpty());
    }

    @Test
    void invalidYearHandled() {
        runApp(
                "1\n1\nTitle\nAuth\nabc\n" +
                "6\n"
        );

        assertEquals(0, Library.getBooks().get(0).getYear());
    }

    @Test
    void unknownMenuOption() {
        runApp(
                "42\n6\n"
        );

        assertTrue(Library.getBooks().isEmpty());
    }
}
