import os
# librería requerida por aws cli
import boto3

# Parámetros
NOMBRE_BUCKET = "rekogtestusm"
CONFIDENCE = 97
CARPETA_CONTROL = "control"
CARPETA_PRUEBAS = "pruebas"

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

def main():
    bucket=NOMBRE_BUCKET
    # Identificar archivos
    archivos_control = listarArchivos(CARPETA_CONTROL)
    archivos_prueba = listarArchivos(CARPETA_PRUEBAS)
    # Extraer texto y probar
    control = detect_text(archivos_control[0], bucket)
    print(str(control))
    for prueba in archivos_prueba:
        prueba = detect_text(prueba, bucket)
        print(str(prueba))

        

if __name__ == "__main__":
    main()
