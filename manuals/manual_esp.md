## Manual de usuario para robots OT-2 covid19 ISCIII

Este manual está diseñado para guiar al operador de los robots OT-2 instalados en el ISCIII durante la epidemia de covid19 y utilizar correctamente los protocolos diseñados para nuestras configuraciones y protocolos particulares.

## Configuración de los robots

Los 8 robots son en principio idénticos entre ellos, y se diferencian únicamente por las distintas pipetas y módulos montados en cada una de las 3 configuraciones:

- **A**: Los robots **A1 y A2** montan una pipeta de 300µl y otra de 1000µl, sin ningún módulo adicional.
- **B**: Los robots **B1, B2, B3 y B4** montan una multi pipeta de 8 canales de 300µl y una pipeta de 1000µl, junto con un móculo magnético.
- **C**: Los robots **C1 y C2** montan una pipeta de 300µl y otra de 20µl, junto con un módulo térmico. Estos robots no tienen luz interna como medida de precaución ya que van a usar compuestos fotosensibles.

Los robots se encuentran localizados en 2 laboratorios diferentes, distinguiendo entre:

- **Sala de extracción**: Situada en Orientación Diagnóstica, encontramos en una misma sala los robots **A1, A2, B1, B2, B3 y B4** junto con un PC para su operación.

![extraction_room_setup.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/extraction_room_setup.jpg?raw=true)

- **Sala de preparación de PCR**: En Virus Respiratorios se encuentran lo robots **C1 y C2** junto a un otro PC para su operación.

![pcrprep_room_setup.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/pcrprep_room_setup.jpg?raw=true)

## Encender los robots

Antes de enceder el robot, asegúrate de que no hay puntas en las pipetas ni objetos dentro de la cabina que puedan entrometerse en el recorrido del brazo y las pipetas durante la vuelta a la posición de origen.

Para encender los robots, utiliza el botón de encendido que se encuentra al fondo del panel lateral izquierdo, justo sobre la toma de corriente del robot.

![robot_power_button.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/robot_power_button.jpg?raw=true)

El robot emitirá unos sonidos de engranajes y es posible que el brazo se mueva hasta la posición de inicio unas cuantas veces. El botón frontal del aparato parpadeará en color azul durante el proceso.

Una vez se paren los ruidos y el brazo del robot esté detenido, el led del botón frontal pasará a brillar en color azul de forma fija indicando que el robot está listo para ser utilizado.

![robot_front_led.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/robot_front_led.jpg?raw=true)

Finalmente, en el caso de los robots tipo **B** y **C** tendremos que encender los módulos magnético y de temperatura respectivamente. Para ello, presiona le botón de encendido de cada módulo situado en la parte trasera del mismo. Cuando la luz trasera se encienda y el módulo deje de emitir sonidos estará listo para usarse.

![tempdeck_power_button.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/tempdeck_power_button.jpg?raw=true)
![magdeck_power_button.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/magdeck_power_button.jpg?raw=true)

**Nota**: En el robot **A2** el led del botón frontal no funciona en color azul, por lo que no nos indicará que está en proceso de arranque con parpadeos ni que está listo para su uso brillando fijo en color azul, deberemos comprobarlo a través de la aplicación como explicaremos más adelante.

**Le doy al botón de encendido del robot/módulo pero no responde**: Comprueba que el cable de corriente está bien conectado al robot/módulo, que la fuente y el cable de corriente están bien encajados y que finalmente el cable de corriente esté conectado a un enchufe que funcione.

**Huele a quemado o veo humo**: Apaga rápidamente el robot o módulo del que procede el olor/humo pulsando rápidamente el botón de apagado del robot al fondo del panel lateral izquierdo. Comprueba que los conectores de corriente están correctamente conectados haciendo coincidir la parte plana del conector macho con la parte plana del hembra y lo mismo con la muesca interna. Si observas que alguno de los pines se ha vuelto negro o estaba bien conectado, no vuelvas a encender el robot y llama a soporte.

![power_connector_frontal_male.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/power_connector_frontal_male.jpg?raw=true)
![power_connector_frontal_female.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/power_connector_frontal_female.jpg?raw=true)

**Se me ha olvidado quitar la punta de la pipeta antes de encenderlo y ...**: Apaga el robot de nuevo pulsando rápidamente el botón de apagado del robot al fondo del panel lateral izquierdo. Una vez se haya detenido, recoge cualquier líquido que pueda haberse derramado y pide soperte para poder evaluar posibles daños o desajustes producisdos por las colisiones.

**Se me ha olvidado quitar la punta de la pipeta antes de encenderlo pero ha terminado de volver a la posición de inicio sin colisionar con nada**: Cuidadosamente retira la punta de la pipeta antes de ejecutar ninguna orden sobre el robot. Una vez retirada, puedes seguir trabajando con normalidad.

## Encender la aplicación de Opentrons

## Conectar un robot

## Cargar un protocolo

## Calibrar un protocolo

## Ejecutar un protocolo
