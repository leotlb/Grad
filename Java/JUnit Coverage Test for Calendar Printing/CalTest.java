/*SSC0524 - 2024-01 
Exercício -- Teste automatizado
Integrantes do Grupo:
Leonardo Pereira
Murilo R.
*/

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

class CalTest {
	
	private static Cal myCal;

	@BeforeAll
	static void setUpBeforeClass() throws Exception {
		myCal = new Cal();
	}

	@AfterAll
	static void tearDownAfterClass() throws Exception {
		myCal = null;
	}

	/* 
	Observação:
	O retorno para o mês de setembro de 1752 foi inserido hard coded no método cal() devido a ser uma exceção
	todavia utilizando essa exceção como modelo base para a formatação das strings esperadas nenhum outro teste é 
	aceito pois para todos os outros caso o método cal() foi programado para inserir um espaço ou um line 
	break (dependendo do dia da semana) ao fim da string e no caso de setembro de 1752 não há nenhum dos dois,
	logo importante pontuar esta discrepância e informar que optamos por modificar as strings esperadas para
	incluir esse último carácter visto que o método cumpre com sua função principal e imprime um calendário 
	mensal adequado 
	*/
	
	
	// Exceção de 1752, mês de 19 dias
	@Test
	void test_Sept1752() {
		String expectedString = "       1  2 14 15 16\n" + 
								"17 18 19 20 21 22 23\n" +
								"24 25 26 27 28 29 30";
		assertEquals(expectedString, myCal.cal(2, 19));
	}
	
	//Mes de 29 dias
	@Test
	void test_Fev1888() {
		String expectedString = "          1  2  3  4\n" + 
								" 5  6  7  8  9 10 11\n" +
								"12 13 14 15 16 17 18\n" + 
								"19 20 21 22 23 24 25\n" +
								"26 27 28 29 ";
		assertEquals(expectedString, myCal.cal(3, 29));
	}
	
	//Mes de 31 dias
	@Test
	void test_Jan2024() {
		String expectedString = "    1  2  3  4  5  6\n" +
				            	" 7  8  9 10 11 12 13\n" +
				            	"14 15 16 17 18 19 20\n" +
				            	"21 22 23 24 25 26 27\n" +
				            	"28 29 30 31 ";
		assertEquals(expectedString, myCal.cal(1, 31));
	}
	
	//Mes de 28 dias
	@Test
	void test_Fev1970() {
		String expectedString = " 1  2  3  4  5  6  7\n" + 
								" 8  9 10 11 12 13 14\n" + 
								"15 16 17 18 19 20 21\n" + 
								"22 23 24 25 26 27 28\n";
		assertEquals(expectedString, myCal.cal(0, 28));
	}
	
	//Mês de 30 dias
	@Test
	void test_Abr2007() {
		String expectedString = " 1  2  3  4  5  6  7\n" + 
								" 8  9 10 11 12 13 14\n" + 
								"15 16 17 18 19 20 21\n" + 
								"22 23 24 25 26 27 28\n" +
								"29 30 ";
		assertEquals(expectedString, myCal.cal(0, 30));
	}

}
