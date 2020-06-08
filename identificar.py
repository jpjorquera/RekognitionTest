# librería requerida por aws cli
import boto3

# Filtrar atributos importantes con texto y confianza > 97%
CONFIDENCE = 97
def filtrarTexto(textDetections):
    newTextDetections = []
    # Ver en cada objeto detectado
    for text in textDetections:
        # Filtrar parámetros
        if text['Type'] == "WORD":
            if (text['Confidence'] > CONFIDENCE):
                texto = text['DetectedText']
                newTextDetections.append(texto)
    return newTextDetections


def detect_text(photo, bucket):
    # Hacer request en aws bucket
    client=boto3.client('rekognition')
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
    # Extraer respuestas y filtrar
    textDetections=response['TextDetections']
    texto = filtrarTexto(textDetections)
    return texto

def main():

    photo='control.png'
    #photo='prueba.jpg'
    bucket='rekogtestusm'

    texto=detect_text(photo,bucket)
    print("Text detected: " + str(texto))


if __name__ == "__main__":
    main()
