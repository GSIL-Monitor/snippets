#include <cppunit/ui/text/TestRunner.h>
#include "ComplexTest.hpp"

int main(int argc, char** argv) {

  CppUnit::TextUi::TestRunner runner;
  runner.addTest(ComplexTest::suite());
  runner.run();
  return 0;

}
