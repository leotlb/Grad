/*SSC0524 - 2024-01 
Exercício -- Teste automatizado
Integrantes do Grupo:
Leonardo Pereira
Murilo R.
*/

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

public class FirstOfMonthTest {

    private static Cal myCal;

    @BeforeAll
    static void setUp() {
        myCal = new Cal();
    }

    @Test
    public void testFirstOfMonthJanuary2024() {
        // Testa o dia da semana inicial de Janeiro de 2024
        assertEquals(1, myCal.firstOfMonth(1, 2024));
    }

    @Test
    public void testFirstOfMonthFebruary2019() {
        // Testa o dia da semana inicial de Fevereiro de 2019
        assertEquals(5, myCal.firstOfMonth(2, 2019));
    }

    @Test
    public void testFirstOfMonthSeptember1752() {
        // Testa o dia da semana inicial de Setembro de 1752 (após a mudança de calendário, 11 dias)
        assertEquals(2, myCal.firstOfMonth(9, 1752));
    }

    @Test
    public void testFirstOfMonthOctober1752() {
        // Testa o dia da semana inicial de Outubro de 1752
        assertEquals(0, myCal.firstOfMonth(10, 1752));
    }

    @Test
    public void testFirstOfMonthDecember2030() {
        // Testa o dia da semana inicial de Dezembro de 2030
        assertEquals(0, myCal.firstOfMonth(12, 2030));
    }

    @Test
    public void testFirstOfMonthApril200() {
        // Testa o dia da semana inicial de Abril de 200
        assertEquals(2, myCal.firstOfMonth(4, 200));
    }

    @Test
    public void testFirstOfMonthOctober1200() {
        // Testa o dia da semana inicial de Outubro de 1200
        assertEquals(0, myCal.firstOfMonth(10, 1200));
    }

    @Test
    public void testFirstOfMonthMay1500() {
        // Testa o dia da semana inicial de Maio de 1500
        assertEquals(5, myCal.firstOfMonth(5, 1500));
    }

    @Test
    public void testFirstOfMonthJuly2019() {
        // Testa o dia da semana inicial de Julho de 2019
        assertEquals(1, myCal.firstOfMonth(7, 2019));
    }

    @Test
    public void testFirstOfMonthNovember1752() {
        // Testa o dia da semana inicial de Novembro de 1752
        assertEquals(3, myCal.firstOfMonth(11, 1752));
    }

    @Test
    public void testFirstOfMonthJanuary5032() {
        // Testa o dia da semana inicial de Janeiro de 5032
        assertEquals(0, myCal.firstOfMonth(1, 5032));
    }

    @Test
    public void testFirstOfMonthFebruary9999() {
        // Testa o dia da semana inicial de Fevereiro de 9999
        assertEquals(1, myCal.firstOfMonth(2, 9999));
    }
}
