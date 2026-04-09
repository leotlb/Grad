/*SSC0524 - 2024-01 
Exercício -- Teste automatizado
Integrantes do Grupo:
Leonardo Pereira
Murilo R.
*/

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;


public class IsLeapTest {

    private static Cal myCal;

    @BeforeAll
    static void setUp() {
        myCal = new Cal();
    }

    @Test
    public void testIsLeapYear2024() {
        assertTrue(myCal.isLeap(2024)); // Testa se 2024 é bissexto
    }

    @Test
    public void testIsLeapYear1752() {
        assertTrue(myCal.isLeap(1752)); // Testa se 1752 é bissexto (antes da mudança de calendário)
    }

    @Test
    public void testIsNotLeapYear1800() {
        assertFalse(myCal.isLeap(1800)); // Testa se 1800 não é bissexto
    }

    @Test
    public void testIsLeapYear2000() {
        assertTrue(myCal.isLeap(2000)); // Testa se 2000 é bissexto (ano divisível por 400)
    }

    @Test
    public void testIsLeapYear2032() {
        assertTrue(myCal.isLeap(2032)); // Testa se 2032 é bissexto
    }

    @Test
    public void testIsNotLeapYear2100() {
        assertFalse(myCal.isLeap(2100)); // Testa se 2100 não é bissexto
    }

    @Test
    public void testIsLeapYear3004() {
        assertTrue(myCal.isLeap(3004)); // Testa se 3004 é bissexto
    }

    @Test
    public void testIsLeapYear1700() {
        assertTrue(myCal.isLeap(1700)); // Testa se 1700 é bissexto
    }

    @Test
    public void testIsLeapYear1900() {
        assertFalse(myCal.isLeap(1900)); // Testa se 1900 não é bissexto
    }

    @Test
    public void testIsLeapYear2008() {
        assertTrue(myCal.isLeap(2008)); // Testa se 2008 é bissexto
    }

    @Test
    public void testIsLeapYear2017() {
        assertFalse(myCal.isLeap(2017)); // Testa se 2017 não é bissexto
    }

    @Test
    public void testIsLeapYear2200() {
        assertFalse(myCal.isLeap(2200)); // Testa se 2200 não é bissexto (divisível por 100, mas não por 400)
    }
}

