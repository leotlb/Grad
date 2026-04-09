/*SSC0524 - 2024-01 
Exercício -- Teste automatizado
Integrantes do Grupo:
Leonardo Pereira
Murilo R.
*/

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class MainTest {

    @Test
    void testMain_March2024() {
        String[] args = {"3", "2024"};
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outputStream)); //Redireciona a saída padrão do console

        Cal.main(args); //Chama o método main com os dados do args

        // Pegando o output do console
        String consoleOutput = outputStream.toString().trim();

        String expectedOutput = "Março 2024\n" +
                                "Do Se Te Qa Qi Se Sa\n" +
                                "                1  2\n" +
                                " 3  4  5  6  7  8  9\n" +
                                "10 11 12 13 14 15 16\n" +
                                "17 18 19 20 21 22 23\n" +
                                "24 25 26 27 28 29 30\n" +
                                "31";

        assertEquals(expectedOutput, consoleOutput);
    }

    @Test
    void testMain_May1999() {
        String[] args = {"5", "1999"};
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outputStream)); //Redireciona a saída padrão do console

        Cal.main(args); //Chama o método main com os dados do args

        // Pegando o output do console
        String consoleOutput = outputStream.toString().trim();

        String expectedOutput = "Maio 1999\n" +
                                "Do Se Te Qa Qi Se Sa\n" +
                                "                   1\n" +
                                " 2  3  4  5  6  7  8\n" +
                                " 9 10 11 12 13 14 15\n" +
                                "16 17 18 19 20 21 22\n" +
                                "23 24 25 26 27 28 29\n" +
                                "30 31";

        assertEquals(expectedOutput, consoleOutput);
    }

    @Test
    void testMain_February2026() {
        String[] args = {"2", "2026"};
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outputStream)); //Redireciona a saída padrão do console

        Cal.main(args); //Chama o método main com os dados do args

        // Pegando o output do console
        String consoleOutput = outputStream.toString().trim();

        String expectedOutput = "Fevereiro 2026\n" +
                                "Do Se Te Qa Qi Se Sa\n" +
                                " 1  2  3  4  5  6  7\n" +
                                " 8  9 10 11 12 13 14\n" +
                                "15 16 17 18 19 20 21\n" +
                                "22 23 24 25 26 27 28";

        assertEquals(expectedOutput, consoleOutput);
    }

    @Test
    void testMain_February1600() {
        String[] args = {"2", "1600"};
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outputStream)); //Redireciona a saída padrão do console

        Cal.main(args); //Chama o método main com os dados do args

        // Pegando o output do console
        String consoleOutput = outputStream.toString().trim();

        String expectedOutput = "Fevereiro 1600\n" +
                                "Do Se Te Qa Qi Se Sa\n" +
                                "       1  2  3  4  5\n" +
                                " 6  7  8  9 10 11 12\n" +
                                "13 14 15 16 17 18 19\n" +
                                "20 21 22 23 24 25 26\n" +
                                "27 28 29";

        assertEquals(expectedOutput, consoleOutput);
    }

    @Test
    void testMain_November1866() {
        String[] args = {"11", "1866"};
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outputStream)); //Redireciona a saída padrão do console

        Cal.main(args); //Chama o método main com os dados do args

        // Pegando o output do console
        String consoleOutput = outputStream.toString().trim();

        String expectedOutput = "Novembro 1866\n" +
                                "Do Se Te Qa Qi Se Sa\n" +
                                "             1  2  3\n" +
                                " 4  5  6  7  8  9 10\n" +
                                "11 12 13 14 15 16 17\n" +
                                "18 19 20 21 22 23 24\n" +
                                "25 26 27 28 29 30";

        assertEquals(expectedOutput, consoleOutput);
    }

    @Test
    void testMain_July6666() {
        String[] args = {"7", "6666"};
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outputStream)); //Redireciona a saída padrão do console

        Cal.main(args); //Chama o método main com os dados do args

        // Pegando o output do console
        String consoleOutput = outputStream.toString().trim();

        String expectedOutput = "Julho 6666\n" +
                "Do Se Te Qa Qi Se Sa\n" +
                " 1  2  3  4  5  6  7\n" +
                " 8  9 10 11 12 13 14\n" +
                "15 16 17 18 19 20 21\n" +
                "22 23 24 25 26 27 28\n" +
                "29 30 31";

        assertEquals(expectedOutput, consoleOutput);
    }
}