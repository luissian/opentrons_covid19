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

Los PCs instalados en las mismas salas que los robots tienen un usuario común que permite acceder al equipo con todos los programas que necesitarás. Logueate siguiendo las instrucciones que te habrá proporcionado el administrador o ponte en contacto con soporte.

Una vez en el escritorio del equipo, busca el logo de la aplicación Opentrons y ábrela.

![opentrons_app_icon.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/opentrons_app_icon.jpg?raw=true)

La aplicación se abre en modo desarrollador, ya que de otra forma no tendríamos acceso a algunas características necesarias para el correcto funcionamiento de nustros robots, pero a cambio produce efectos en la interfaz que la pueden hacer menos amigable. Cierra el modo debug de la aplicación y podemos continuar.

![close_debug_mode.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/close_debug_mode.jpg?raw=true)

La ventana de la aplicación se divide en 3 secciones verticales:

![opentrons_app_mainwindow.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/opentrons_app_mainwindow.jpg?raw=true)

- A la izquierda del todo tenemos un menú que nos permite cambiar entre las ventanas de robot, protocolo, calibración y ejecución.

![opentrons_app_leftmenu.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/opentrons_app_leftmenu.jpg?raw=true)

- En el panel del medio tenemos las posibles órdenes que podemos dar al robot desde la ventana en la que nos encontramos.

![opentrons_app_middlemenu.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/opentrons_app_middlemenu.jpg?raw=true)

- En el panel de la derecha, el más grande de los tres, se presenta la información para el usuario así como opciones de configuración e interacción con el robot. Como la anterior, depende de la ventana en la que nos encontremos el contenido de este panel variará.

![opentrons_app_rightmenu.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/opentrons_app_rightmenu.jpg?raw=true)

## Conectar un robot

En la aplicación hacemos click en la primera opción del menú lateral de la izquierda: `Robot`. Veremos que en el panel del medio se muestran los diferentes robots disponibles para operar. Si haces click en cualquiera de ellos verás en el panel lateral de la derecha información y opciones de configuración para dicho robot, como la opción de encender las luces internas con el botón `Lights`.

**Nota**: Enceder las luces es recomendable para localizar fácilmente el robot que vas a utilizar. También son de ayuda a la hora de colocar y sacar el material de la cabina.

**Nota**: Los robots tipo **C** no tienen luces internas.

![opentrons_app_mainrobot.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/opentrons_app_mainrobot.jpg?raw=true)

Para poder operar el robot, tendemos que dar la orden de conectarnos a él. Para ello, haz click en la pequeña palanca a la dereha del nombre del robot en el panel de en medio o en el botón `Connect` en el panel de la derecha tras haber seleccionado el robot en el del medio.

 ![opentrons_app_connectedrobot.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/opentrons_app_connectedrobot.jpg?raw=true)

 Un baner verde en la parte superior del tercer panel nos confirmará a qué robot nos hemos conectado con éxito.

 **Nota**: Solo puedes estar conectado a un robot al mismo tiempo. Los demás seguirán ejecutando sus órdenes aunque te desconectes de ellos, pero cualquier configuración hecha en un robot corre el riesgo de perderse si te desconectas antes de ejecutar una orden, por lo que es recomendable que en caso de desconexión vuelvas a empezar la configuración de tu protocolo desde el principio.

 **Nota**: Si te conectas a un robot que está en funcionamiento, el baner superior en color amarillo te lo indicará cuando te conectes. Mientras está en funcionamiento no podrás darle nuevas órdenes, solo ver su información y seguir la ejecución actual como veremos más adelante.

 **Nota**: Aunque desde ambos PCs puedes conectarte a todos los robots (estén o no en tu misma sala), nunca debes operar un robot fuera de tu campo visual. No sabes qué hay dentro de la cabina o si hay alguien manipulándolo en ese momento. Asegúrate siempre a qué robot estás conectando antes de hacer nada.

## Cargar un protocolo

Esta es la segunda opción del panel de la izquierda: `Protocol`. Cuando accedas a esta ventana, en el panel de la derecha verás el protocolo que se encuentra actualmente cargado en el robot de la última ejecución.

![opentrons_app_mainprotocol.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/opentrons_app_mainprotocol.jpg?raw=true)

Si quieres cargar un nuevo protocolo, tan solo busca el archivo `.py` correspondiente y arrástralo al panel del medio o haz click en el botón `Open` del mismo panel y selecciona el archivo deseado.

En el panel de la derecha podemos ver el nombre del protocolo, versión, autores y versión de la API requerida, seguido de las pipetas y módulos que debe haber instalados en el robot, y finalmente una lista del labware que se necesitará.

**Nota**: Si las pipetas y módulos requeridos no correpsonden con las presentes en el robot o las que esperas para el protocolo (cruz roja junto a su numbre en lugar de un check negro), asegúrate de que estás cargando el protocolo correcto en el robot deseado e inténtalo de nuevo.

**Nota**: Si el módulo requerido aparece como no detectado (círculo vacío donde debería estar un check negro), revisa que el robot al que estás conectado tiene el módulo instalado, que el módulo está conectado a la corriente y al robot, y que el módulo está encendido.

**Nota**: Si quieres reejecutar el mismo protocolo que ya estaba cargado en el robot, no necesitas volver a cargarlo o calibrarlo.

**Nota**: La codificación de los nombres del labware se puede consultar en la tabla de inventario de los robots, o puedes consultarlo en nuestra web.

**Nota**: Aunque el robot pida menos cajas de puntas de las esperadas, ignóralo, siempre hay que poner tantas como se ha diseñado en el protocolo para máximo número de muestras. No te preocupes de rellenar cajas que queden a medias, el robot seguirá usando las cajas que quedan a medias hasta que termine contodas y entonces parará a pedirte que repongas las cajas vacías por nuevas.

## Calibrar un protocolo

## Ejecutar un protocolo
