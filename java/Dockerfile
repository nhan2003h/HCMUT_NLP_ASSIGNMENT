FROM maven:3.6.0-jdk-8-slim AS build
COPY nlp-assignment-222/src /home/app/src
COPY nlp-assignment-222/pom.xml /home/app
RUN mvn -f /home/app/pom.xml clean package

#
# final image
#
FROM openjdk:8-jre-slim
COPY --from=build /home/app/target/nlp-assignment-222-1.0-SNAPSHOT.jar /usr/local/lib/nlp-assignment-222-1.0-SNAPSHOT.jar
# COPY --from=build /home/app/target/* /test/

ENTRYPOINT ["java","-jar","/usr/local/lib/nlp-assignment-222-1.0-SNAPSHOT.jar"]
#ENTRYPOINT ["ls","-lat","/test"]
