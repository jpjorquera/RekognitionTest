import os
import datetime
# librería requerida por aws cli
import boto3

# Parámetros
CONFIDENCE = 97
CARPETA_CONTROL = "control"
CARPETA_PRUEBAS = "pruebas"

# Leer nombre de bucket en archivo separado
def readBucketName():
    archivo = open("./bucket.txt", "r")
    bucketName = archivo.readline().strip()
    archivo.close()
    return bucketName

# Filtrar texto de otros atributos y con confianza > 97%
def filtrarTexto(textDetections):
    newTextDetections = []
    # Ver en cada objeto detectado
    for text in textDetections:
        # Filtrar parámetros
        if text['Type'] == "WORD":
            if (text['Confidence'] > CONFIDENCE):
                texto = text['DetectedText']
                # Estandarizar
                texto = str.lower(texto).strip()
                newTextDetections.append(texto)
    return newTextDetections

# Buscar y aplicar rekognition a imagen en bucket, luego filtrar
# las respuestas
def detect_text(photo, bucket):
    # Hacer request en aws bucket
    client=boto3.client('rekognition')
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
    # Extraer respuestas y filtrar
    textDetections=response['TextDetections']
    texto = filtrarTexto(textDetections)
    return texto

# Armar lista con archivos en la carpeta especificada
def listarArchivos(carpeta):
     lista = os.listdir("./"+carpeta)
     return lista

# Agregar log en el archivo para la prueba del archivo indicado
def imprimirLog(archivo, nombrePrueba, resultado):
    # Formato: [DD/MM/YYYY HH:MM:SS] Caso de prueba id #id - Resultado: “True/False”
    tiempo_actual = datetime.datetime.now()
    tiempo_a_imprimir = tiempo_actual.strftime("[%d/%m/%Y %H:%M:%S]")
    linea_a_escribir = tiempo_a_imprimir+' Prueba archivo: "'+str(nombrePrueba)+'" - Resultado: '+str(resultado)+"\n"
    archivo.write(linea_a_escribir)

# Función para verificar si el texto de prueba se encuentra contenido en el texto de control
# los textos vienen en minúsculas
def compararPrueba(control, prueba):
    control = " ".join(control)
    prueba = " ".join(prueba)
    resultado = prueba in control
    return resultado

def main():
    bucket=readBucketName()
    # Identificar archivos
    archivos_control = listarArchivos(CARPETA_CONTROL)
    archivos_prueba = listarArchivos(CARPETA_PRUEBAS)
    # Extraer texto y probar
    texto_control = detect_text(archivos_control[0], bucket)
    # Imprimir en archivo de logs
    salida = open("LogsPruebas.txt", mode="w")
    for prueba in archivos_prueba:
        texto_prueba = detect_text(prueba, bucket)
        resultado = compararPrueba(texto_control, texto_prueba)
        imprimirLog(salida, prueba, resultado)

    salida.close()

if __name__ == "__main__":
    main()
