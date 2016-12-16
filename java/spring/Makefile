default: run

clean:
	mvn clean

compile: clean
	mvn compile

package: compile
	mvn package

dist: package

run: compile
	mvn exec:java -Dconfig=production.properties
