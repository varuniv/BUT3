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

    private final PrintStream originalOut = System.out;
    private final InputStream originalIn = System.in;

    private ByteArrayOutputStream out;

    @BeforeEach
    void setUp() {
        Library.books.clear();
        Library.loans.clear();
        out = new ByteArrayOutputStream();
        System.setOut(new PrintStream(out));
    }

    @AfterEach
    void tearDown() {
        System.setOut(originalOut);
        System.setIn(originalIn);
    }

    private void runApp(String input) {
        System.setIn(new ByteArrayInputStream(input.getBytes()));
        LibraryApp.main(new String[]{});
    }

    @Test
    void creationLibraryAppTest() {
        LibraryApp app = new LibraryApp();
        assert app != null;
    }

    @Test
    void ajouterLivreAvecAnneeInvalide() {
        String input =
                "1\n" +
                "123\n" +
                "Test\n" +
                "Author\n" +
                "abc\n" +   // année invalide
                "6\n";

        runApp(input);

        assertEquals(1, Library.books.size());
        assertEquals(0, Library.books.get(0).getYear());
        assertTrue(out.toString().contains("Invalid year"));
    }

    @Test
    void avertissementLivreExistant() {
        Library.books.add(new Book("1", "Java", "Author", 2000));

        String input =
                "1\n" +
                "1\n" +
                "Java\n" +
                "Author\n" +
                "2000\n" +
                "6\n";

        runApp(input);

        assertTrue(out.toString().contains("Warning: similar book already exists"));
    }


    @Test
    void listerLivresAvecEmprunt() {
        Book b = new Book("10", "JUnit", "Kent Beck", 2004);
        Library.books.add(b);
        Library.loans.put("10", new Borrower("Alice"));

        runApp("2\n6\n");

        assertTrue(out.toString().contains("[BORROWED]"));
    }



    @Test
    void emprunterLivreInexistant() {
        runApp("3\nBob\n999\n6\n");

        assertTrue(out.toString().contains("Not found"));
    }

    @Test
    void emprunterLivreDejaEmprunte() {
        Library.books.add(new Book("2", "Clean Code", "Martin", 2008));
        Library.loans.put("2", new Borrower("Bob"));

        runApp("3\nAlice\n2\n6\n");

        assertTrue(out.toString().contains("Already borrowed"));
    }

    @Test
    void emprunterLivreOK() {
        Library.books.add(new Book("3", "DDD", "Evans", 2003));

        runApp("3\nAlice\n3\n6\n");

        assertEquals("Alice", Library.loans.get("3").name);
    }


    @Test
    void retourLivreOK() {
        Library.loans.put("4", new Borrower("Bob"));

        runApp("4\n4\n6\n");

        assertTrue(out.toString().contains("Returned"));
    }

    @Test
    void retourLivreNonEmprunte() {
        runApp("4\n5\n6\n");

        assertTrue(out.toString().contains("Not borrowed"));
    }


    @Test
    void rechercheParAuteurIgnoreCase() {
        Library.books.add(new Book("1", "Refactoring", "Martin Fowler", 1999));
        Library.books.add(new Book("2", "Java", "Gosling", 1995));

        runApp("5\nFOWLER\n6\n");

        assertTrue(out.toString().contains("Martin Fowler"));
        assertFalse(out.toString().contains("Gosling"));
    }


    @Test
    void optionInconnue() {
        runApp("42\n6\n");

        assertTrue(out.toString().contains("Unknown option"));
    }


    @Test
    void quitterApplication() {
        runApp("6\n");

        assertTrue(out.toString().contains("Bye."));
    }


    @Test
    void testByIsbn() {
        Book b = new Book("99", "Test", "Author", 2020);
        Library.books.add(b);

        assertEquals(b, Library.byIsbn("99"));
        assertNull(Library.byIsbn("404"));
    }

    @Test
    void testIsBorrowed() {
        Library.loans.put("88", new Borrower("Alice"));

        assertTrue(Library.isBorrowed("88"));
        assertFalse(Library.isBorrowed("77"));
    }
}

