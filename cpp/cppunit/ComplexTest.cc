#include <cppunit/Test.h>
#include <cppunit/TestFixture.h>
#include <cppunit/TestSuite.h>
#include <cppunit/extensions/HelperMacros.h>
#include "Complex.hpp"

class ComplexTest : public CppUnit::TestFixture {
private:
  Complex *m_10_1, *m_1_1, *m_11_2;
public:
  void setUp()
  {
    m_10_1 = new Complex( 10, 1 );
    m_1_1 = new Complex( 1, 1 );
    m_11_2 = new Complex( 11, 2 );
  }

  void tearDown()
  {
    delete m_10_1;
    delete m_1_1;
    delete m_11_2;
  }

	void testEquality()
  {
    CPPUNIT_ASSERT( *m_10_1 == *m_10_1 );
    CPPUNIT_ASSERT( !(*m_10_1 == *m_11_2) );
  }

	// suite
  static CppUnit::Test *suite() {
    CppUnit::TestSuite *suiteOfTests =
			new CppUnit::TestSuite( "ComplexTest" );
    suiteOfTests->addTest( new CppUnit::TestCaller<ComplexTest>(
                                   "testEquality",
                                   &ComplexTest::testEquality ) );
    return suiteOfTests;
  }

};
