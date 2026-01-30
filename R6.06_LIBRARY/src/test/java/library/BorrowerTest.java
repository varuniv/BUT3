package library;

import org.junit.jupiter.api.Test;

import library.Borrower;


public class BorrowerTest {
    
    @Test
    public void CreationBorrowerTest() {
        Borrower borrower = new Borrower("Jean Pierre Polnareff");
        assert borrower.name.equals("Jean Pierre Polnareff");
    }
}
