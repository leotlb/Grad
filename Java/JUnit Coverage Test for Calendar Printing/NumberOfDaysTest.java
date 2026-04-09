/*SSC0524 - 2024-01 
Exercício -- Teste automatizado
Integrantes do Grupo:
Leonardo Pereira
Murilo R.
*/

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

public class NumberOfDaysTest {

    private static Cal myCal;

    @BeforeAll
    static void setUp() {
        myCal = new Cal();
    }

    @Test
    public void testNumberOfDaysFebruary2024() {
        // Testa o número de dias em Fevereiro de 2024 (ano bissexto)
        assertEquals(29, myCal.numberOfDays(2, 2024));
    }

    @Test
    public void testNumberOfDaysSeptember1752() {
        // Testa o número de dias em Setembro de 1752 (após a mudança de calendário)
        assertEquals(19, myCal.numberOfDays(9, 1752));
    }

    @Test
    public void testNumberOfDaysApril2023() {
        // Testa o número de dias em Abril de 2023
        assertEquals(30, myCal.numberOfDays(4, 2023));
    }

    @Test
    public void testNumberOfDaysFebruary2100() {
        // Testa o número de dias em Fevereiro de 2100 (ano não bissexto)
        assertEquals(28, myCal.numberOfDays(2, 2100));
    }

    @Test
    public void testNumberOfDaysAugust1500() {
        // Testa o número de dias em Agosto de 1500
        assertEquals(31, myCal.numberOfDays(8, 1500));
    }

    @Test
    public void testNumberOfDaysJanuary3511() {
        // Testa o número de dias em Janeiro de 3511
        assertEquals(31, myCal.numberOfDays(1, 3511));
    }

    @Test
    public void testNumberOfDaysOctober7777() {
        // Testa o número de dias em Outubro de 7777
        assertEquals(31, myCal.numberOfDays(10, 7777));
    }
}
