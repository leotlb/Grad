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

class Jan1Test {
	
	private static Cal myCal;

	@BeforeAll
	static void setUpBeforeClass()  throws Exception {
		myCal = new Cal();
	}
	
	@AfterAll
	static void tearDownAfterClass()  throws Exception {
		myCal = null;
	}

	// Teste para limite inferior
	@Test
	void test_jan1_1() {
		assertEquals(6, myCal.jan1(1));
	}
	
	// Teste para ano anterior a 1752
	@Test
	void test_jan1_1500() {
		assertEquals(3, myCal.jan1(1500));
	}
	
	// Teste para ano posterior a 1752 e anterior a 1800
	@Test
	void test_jan1_1792() {
		assertEquals(0, myCal.jan1(1792));
	}
	
	// Teste para ano posterior a 1800
	@Test
	void test_jan1_2024() {
		assertEquals(1, myCal.jan1(2024));
	}
	
	// Teste para limite superior
	@Test
	void test_jan1_9999() {
		assertEquals(5, myCal.jan1(9999));
	}

}