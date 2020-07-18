FROM centos:7
MAINTAINER zhoujl<ajldaydayup000@163.com>

ADD jdk-8u251-linux-x64.tar.gz /usr/local/

ENV MYPATH /usr/local
WORKDIR $MYPATH

RUN yum -y install vim
RUN yum -y install net-tools

ENV JAVA_HOME /usr/local/jdk1.8.0_251
#ENV PATH $JAVA_HOME/bin:$PATH
ENV CLASSPATH $JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar

# Install necessary tools
RUN yum install -y pcre-devel wget net-tools gcc zlib zlib-devel make openssl-devel
# Install Nginx
ADD http://nginx.org/download/nginx-1.16.1.tar.gz .
RUN tar zxvf nginx-1.16.1.tar.gz
RUN mkdir -p /usr/local/nginx
RUN cd nginx-1.16.1 && ./configure --prefix=/usr/local/nginx && make && make install
ADD elasticsearch-7.6.1-linux-x86_64.tar.gz /usr/local/

EXPOSE 80
CMD /bin/bash