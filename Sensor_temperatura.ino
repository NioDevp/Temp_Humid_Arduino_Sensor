//Incluir librerias

#include <DHT.h>
#include <DHT_U.h>

//Definimos

#define DHT_PIN  2

#define DHTTYPE DHT11

DHT dht(DHT_PIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();

}


void loop() {
  delay (2000);

  float t = dht.readTemperature();
  float h = dht.readHumidity();

   if (isnan(h) || isnan(t)) {
    Serial.println("Error obteniendo los datos del sensor DHT11");
    return; 
    }

  float hif = dht.computeHeatIndex(t, h);

 //Serial.print("Humedad: ");
  Serial.print(h);
  Serial.print(" ");
  //Serial.print(" %\t");
  //Serial.print("Temperatura: ");
  Serial.print(t);
  Serial.print(" ");
  //Serial.print(" *C ");
  //Serial.print("Índice de calor: ");
  Serial.println(hif);
  //Serial.println(" *C ");


}
