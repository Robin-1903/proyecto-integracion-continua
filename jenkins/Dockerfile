FROM jenkins/jenkins:lts-jdk21

USER root
COPY --from=docker:cli /usr/local/bin/docker /usr/local/bin/docker
RUN git config --system --add safe.directory '*'

USER jenkins
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt