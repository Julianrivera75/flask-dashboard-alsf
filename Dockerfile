# Usar imagen base más ligera y estable
FROM tomcat:9-jdk11-openjdk

# Variables de entorno optimizadas para Railway
ENV GEOSERVER_VERSION=2.24.0
ENV JAVA_OPTS="-Xms1024m -Xmx2048m -XX:MaxPermSize=512m -XX:+UseG1GC -XX:+UseStringDeduplication"
ENV GEOSERVER_DATA_DIR="/app/geoserver_data"
ENV CATALINA_OPTS="-Djava.awt.headless=true -Dfile.encoding=UTF-8"

# Crear usuario no-root para seguridad
RUN groupadd -r geoserver && useradd -r -g geoserver geoserver

# Instalar dependencias y limpiar cache en una sola capa
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gdal-bin \
    proj-bin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*

# Crear directorios necesarios
RUN mkdir -p /app/geoserver_data \
    && mkdir -p /usr/local/tomcat/webapps/geoserver \
    && chown -R geoserver:geoserver /app/geoserver_data \
    && chown -R geoserver:geoserver /usr/local/tomcat/webapps

# Descargar GeoServer desde mirror más rápido
RUN wget -O /tmp/geoserver.zip \
    "https://github.com/geoserver/geoserver/releases/download/${GEOSERVER_VERSION}/geoserver-${GEOSERVER_VERSION}-war.zip" \
    && unzip /tmp/geoserver.zip -d /tmp/ \
    && cp /tmp/geoserver.war /usr/local/tomcat/webapps/ \
    && rm -rf /tmp/*

# Configurar Tomcat para Railway
RUN echo "export JAVA_OPTS=\"$JAVA_OPTS\"" >> /usr/local/tomcat/bin/setenv.sh \
    && echo "export CATALINA_OPTS=\"$CATALINA_OPTS\"" >> /usr/local/tomcat/bin/setenv.sh \
    && chmod +x /usr/local/tomcat/bin/setenv.sh

# Configurar GeoServer para Railway
RUN mkdir -p /usr/local/tomcat/webapps/geoserver/WEB-INF \
    && echo '<?xml version="1.0" encoding="UTF-8"?>' > /usr/local/tomcat/webapps/geoserver/WEB-INF/web.xml \
    && echo '<web-app xmlns="http://java.sun.com/xml/ns/javaee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd" version="3.0">' >> /usr/local/tomcat/webapps/geoserver/WEB-INF/web.xml \
    && echo '  <display-name>GeoServer</display-name>' >> /usr/local/tomcat/webapps/geoserver/WEB-INF/web.xml \
    && echo '  <welcome-file-list>' >> /usr/local/tomcat/webapps/geoserver/WEB-INF/web.xml \
    && echo '    <welcome-file>web/index.html</welcome-file>' >> /usr/local/tomcat/webapps/geoserver/WEB-INF/web.xml \
    && echo '  </welcome-file-list>' >> /usr/local/tomcat/webapps/geoserver/WEB-INF/web.xml \
    && echo '</web-app>' >> /usr/local/tomcat/webapps/geoserver/WEB-INF/web.xml

# Configurar health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/geoserver/web/ || exit 1

# Exponer puerto
EXPOSE 8080

# Cambiar a usuario no-root
USER geoserver

# Comando de inicio optimizado
CMD ["catalina.sh", "run"] 