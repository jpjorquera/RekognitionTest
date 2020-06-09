# Pruebas servicio Rekognition AWS
Se busca verificar si el texto en las imágenes de prueba se encuentra en la imagen de control haciendo uso de Rekognition de Amazon Web Services.

## Instrucciones de uso
### Precondiciones
El programa está desarrollado en python 3.

Es necesario tener los archivos de prueba y control que se incluyen en las carpetas respectivas en un AWS S3 bucket. En el bucket los archivos deben estar sueltos, en la carpeta de raíz.

En el archivo `bucket.txt`se debe escribir el nombre del bucket en el que se encuentran los archivos.

Es necesario tener las credenciales y configuración de AWS ingresadas en la configuración del AWS-CLI.

### Instalar librerías necesarias
`pip install boto3`

### Ejecutar
`python identificar.py`

### Resultados
Los resultados obtenidos se muestran en el archivo `LogsPruebas.txt`.