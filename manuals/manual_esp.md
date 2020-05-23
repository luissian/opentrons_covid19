## Manual de usuario para robots OT-2 covid19 ISCIII

Este manual está diseñado para guiar al operador de los robots OT-2 instalados en el ISCIII durante la epidemia de covid19 y utilizar correctamente los protocolos diseñados para nuestras configuraciones y protocolos particulares.

## Configuración de los robots

Los 8 robots son en principio idénticos entre ellos, y se diferencian únicamente por las distintas pipetas y módulos montados en cada una de las 3 configuraciones:

- **A**: Los robots **A1 y A2** montan una pipeta de 300µl y otra de 1000µl, sin ningún módulo adicional.
- **B**: Los robots **B1, B2, B3 y B4** montan una multi pipeta de 8 canales de 300µl y una pipeta de 1000µl, junto con un móculo magnético.
- **C**: Los robots **C1 y C2** montan una pipeta de 300µl y otra de 20µl, junto con un módulo térmico. Estos robots no tienen luz interna como medida de precaución ya que van a usar compuestos fotosensibles.

Los robots se encuentran localizados en 2 laboratorios diferentes, distinguiendo entre:

- **Sala de extracción**: Situada en Orientación Diagnóstica, encontramos en una misma sala los robots **A1, A2, B1, B2, B3 y B4** junto con un PC para su operación.

![extraction_room_setup.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/extraction_room_setup.jpg?raw=true)

- **Sala de preparación de PCR**: En Virus Respiratorios se encuentran lo robots **C1 y C2** junto a un otro PC para su operación.

![pcrprep_room_setup.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/pcrprep_room_setup.jpg?raw=true)

## Encender los robots

Antes de enceder el robot, asegúrate de que no hay puntas en las pipetas ni objetos dentro de la cabina que puedan entrometerse en el recorrido del brazo y las pipetas durante la vuelta a la posición de origen.

Para encender los robots, utiliza el botón de encendido que se encuentra al fondo del panel lateral izquierdo, justo sobre la toma de corriente del robot.

![robot_power_button.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/robot_power_button.jpg?raw=true)

El robot emitirá unos sonidos de engranajes y es posible que el brazo se mueva hasta la posición de inicio unas cuantas veces. El botón frontal del aparato parpadeará en color azul durante el proceso.

Una vez se paren los ruidos y el brazo del robot esté detenido, el led del botón frontal pasará a brillar en color azul de forma fija indicando que el robot está listo para ser utilizado.

![robot_front_led.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/robot_front_led.jpg?raw=true)

Finalmente, en el caso de los robots tipo **B** y **C** tendremos que encender los módulos magnético y de temperatura respectivamente. Para ello, presiona le botón de encendido de cada módulo situado en la parte trasera del mismo. Cuando la luz trasera se encienda y el módulo deje de emitir sonidos estará listo para usarse.

![tempdeck_power_button.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/tempdeck_power_button.jpg?raw=true)
![magdeck_power_button.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/magdeck_power_button.jpg?raw=true)

**Nota**: En el robot **A2** el led del botón frontal no funciona en color azul, por lo que no nos indicará que está en proceso de arranque con parpadeos ni que está listo para su uso brillando fijo en color azul, deberemos comprobarlo a través de la aplicación como explicaremos más adelante.

**Le doy al botón de encendido del robot/módulo pero no responde**: Comprueba que el cable de corriente está bien conectado al robot/módulo, que la fuente y el cable de corriente están bien encajados y que finalmente el cable de corriente esté conectado a un enchufe que funcione.

**Huele a quemado o veo humo**: Apaga rápidamente el robot o módulo del que procede el olor/humo pulsando rápidamente el botón de apagado del robot al fondo del panel lateral izquierdo. Comprueba que los conectores de corriente están correctamente conectados haciendo coincidir la parte plana del conector macho con la parte plana del hembra y lo mismo con la muesca interna. Si observas que alguno de los pines se ha vuelto negro o estaba bien conectado, no vuelvas a encender el robot y llama a soporte.

![power_connector_frontal_male.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/power_connector_frontal_male.jpg?raw=true)
![power_connector_frontal_female.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/power_connector_frontal_female.jpg?raw=true)

**Se me ha olvidado quitar la punta de la pipeta antes de encenderlo y ...**: Apaga el robot de nuevo pulsando rápidamente el botón de apagado del robot al fondo del panel lateral izquierdo. Una vez se haya detenido, recoge cualquier líquido que pueda haberse derramado y pide soperte para poder evaluar posibles daños o desajustes producisdos por las colisiones.

**Se me ha olvidado quitar la punta de la pipeta antes de encenderlo pero ha terminado de volver a la posición de inicio sin colisionar con nada**: Cuidadosamente retira la punta de la pipeta antes de ejecutar ninguna orden sobre el robot. Una vez retirada, puedes seguir trabajando con normalidad.

## Encender la aplicación de Opentrons

Los PCs instalados en las mismas salas que los robots tienen un usuario común que permite acceder al equipo con todos los programas que necesitarás. Logueate siguiendo las instrucciones que te habrá proporcionado el administrador o ponte en contacto con soporte.

Una vez en el escritorio del equipo, busca el logo de la aplicación Opentrons y ábrela.

![opentrons_app_icon.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_icon.jpg?raw=true)

La aplicación se abre en modo desarrollador, ya que de otra forma no tendríamos acceso a algunas características necesarias para el correcto funcionamiento de nustros robots, pero a cambio produce efectos en la interfaz que la pueden hacer menos amigable. Cierra el modo debug de la aplicación y podemos continuar.

Cierra también las peticiones de actualización. Cada actualización debe ser testada a fondo antes de ser instalada, ya que también actualizará los robots y puede modificar su funcionamiento.

![close_debug_mode.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/close_debug_mode.jpg?raw=true)

La ventana de la aplicación se divide en 3 secciones verticales:

![opentrons_app_mainwindow.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_mainwindow.jpg?raw=true)

- A la izquierda del todo tenemos un menú que nos permite cambiar entre las ventanas de robot, protocolo, calibración y ejecución.

![opentrons_app_leftmenu.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_leftmenu.jpg?raw=true)

- En el panel del medio tenemos las posibles órdenes que podemos dar al robot desde la ventana en la que nos encontramos.

![opentrons_app_middlemenu.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_middlemenu.jpg?raw=true)

- En el panel de la derecha, el más grande de los tres, se presenta la información para el usuario así como opciones de configuración e interacción con el robot. Como la anterior, depende de la ventana en la que nos encontremos el contenido de este panel variará.

![opentrons_app_rightmenu.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_rightmenu.jpg?raw=true)

## Conectar un robot

En la aplicación hacemos click en la primera opción del menú lateral de la izquierda: `Robot`. Veremos que en el panel del medio se muestran los diferentes robots disponibles para operar. Si haces click en cualquiera de ellos verás en el panel lateral de la derecha información y opciones de configuración para dicho robot, como la opción de encender las luces internas con el botón `Lights`.

**Nota**: Enceder las luces es recomendable para localizar fácilmente el robot que vas a utilizar. También son de ayuda a la hora de colocar y sacar el material de la cabina.

**Nota**: Los robots tipo **C** no tienen luces internas.

![opentrons_app_mainrobot.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_mainrobot.jpg?raw=true)

Para poder operar el robot, tendemos que dar la orden de conectarnos a él. Para ello, haz click en la pequeña palanca a la dereha del nombre del robot en el panel de en medio o en el botón `Connect` en el panel de la derecha tras haber seleccionado el robot en el del medio.

 ![opentrons_app_connecttorobot.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_connecttorobot.jpg?raw=true)

 Un baner verde en la parte superior del tercer panel nos confirmará a qué robot nos hemos conectado con éxito.

 ![opentrons_app_connectedrobot.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_connectedrobot.jpg?raw=true)

 **Nota**: Solo puedes estar conectado a un robot al mismo tiempo. Los demás seguirán ejecutando sus órdenes aunque te desconectes de ellos, pero cualquier configuración hecha en un robot corre el riesgo de perderse si te desconectas antes de ejecutar una orden, por lo que es recomendable que en caso de desconexión vuelvas a empezar la configuración de tu protocolo desde el principio.

 **Nota**: Si te conectas a un robot que está en funcionamiento, el baner superior en color amarillo te lo indicará cuando te conectes. Mientras está en funcionamiento no podrás darle nuevas órdenes, solo ver su información y seguir la ejecución actual como veremos más adelante.

 **Nota**: Aunque desde ambos PCs puedes conectarte a todos los robots (estén o no en tu misma sala), nunca debes operar un robot fuera de tu campo visual. No sabes qué hay dentro de la cabina o si hay alguien manipulándolo en ese momento. Asegúrate siempre a qué robot estás conectando antes de hacer nada.

## Cargar un protocolo

Esta es la segunda opción del panel de la izquierda: `Protocol`. Cuando accedas a esta ventana, en el panel de la derecha verás el protocolo que se encuentra actualmente cargado en el robot de la última ejecución.

![opentrons_app_mainprotocol.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_mainprotocol.jpg?raw=true)

Si quieres cargar un nuevo protocolo, tan solo busca el archivo `.py` correspondiente y arrástralo al panel del medio o haz click en el botón `Open` del mismo panel y selecciona el archivo deseado.

En el panel de la derecha podemos ver el nombre del protocolo, versión, autores y versión de la API requerida, seguido de las pipetas y módulos que debe haber instalados en el robot, y finalmente una lista del labware que se necesitará.

**Nota**: Si las pipetas y módulos requeridos no correpsonden con las presentes en el robot o las que esperas para el protocolo (cruz roja junto a su numbre en lugar de un check negro), asegúrate de que estás cargando el protocolo correcto en el robot deseado e inténtalo de nuevo.

**Nota**: Si el módulo requerido aparece como no detectado (círculo vacío donde debería estar un check negro), revisa que el robot al que estás conectado tiene el módulo instalado, que el módulo está conectado a la corriente y al robot, y que el módulo está encendido.

**Nota**: Si quieres reejecutar el mismo protocolo que ya estaba cargado en el robot, no necesitas volver a cargarlo o calibrarlo.

**Nota**: La codificación de los nombres del labware se puede consultar en la tabla de inventario de los robots, o puedes consultarlo en nuestra web.

**Nota**: Aunque el robot pida menos cajas de puntas de las esperadas, ignóralo, siempre hay que poner tantas como se ha diseñado en el protocolo para máximo número de muestras. No te preocupes de rellenar cajas que queden a medias, el robot seguirá usando las cajas que quedan a medias hasta que termine contodas y entonces parará a pedirte que repongas las cajas vacías por nuevas.

## Calibrar un protocolo

En la tercera opción del menú del panel de la izquierda, `Calibrate`, podremos ajustar la posición del brazo del robot y sus movimientos para que se mueva por la cabina correctamente y reconozca el labware al milímetro.

![opentrons_app_maincalibrate.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_maincalibrate.jpg?raw=true)

**Solo es necesario calibrar un protocolo si:**
- es la primera vez que se ejecuta ese protocolo en este robot
- se han modificado las opciones labware utilizado respecto a ejecuciones previas del protocolo en este robot
- se ha observado que el robot empieza a fallar a la hora de coger puntas, golpea o roza el labware al moverse, o no baja hasta la altura correcta dentro de los pocillos/tubos para realizar su programa.

**Nota**: Si tras calibrar el protocolo varias veces el brazo y las pipetas siguieran rozando o golpeando el labware al moverse por la cabina, realiza una calibración del deck. Si esto tampoco solucionara el problema, contaca a soporte.

**No es necesario realizar una calibración si:**
- estás volviendo a ejecutar el mismo protocolo que se ha ejecutado previamente en el robot.
- el único cambio en el protocolo ha sido el número de muestras.

En el panel central se muestra una lista del labware requerido para ejecutar el protocolo. Para que aparezca todo el labware y poder calibrarlo de una sola vez, es recomendable calibrarlo para una ejecución con el máximo número de muestras y con todos los pasos a posibles realizar.

Hay que iniciar la calibración con la cabina vacía (a exepción de los módulos requeridos, que tienen que estar conectados y encendidos) y las pipetas sin puntas, y es necesario que el deck haya sido calibrado previamente.

Al iniciar la calibración se empezará por las pipetas. Te pedirá paso a paso que quites el cubo de basura de las puntas y pongas una punta en las pipetas, y él solo tocará unos sensores normalemente ocultos bajo el cubo para comprobar el movimiento y posicionamiento de las puntas. Una vez termine el proceso para ambas pipetas, vuelve a poner cuidadosamente el cubo para cubrir los sonsores.

![opentrons_calibration_metalpins.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_calibration_metalpins.jpg?raw=true)

**Nota**: Los sensores son unas plaquitas de metal muy delicadas y sensibles. Ten mucho cuidado al quitar y poner el cubo de basura o podrías dañarlos.

**Nota**: En caso de que uno de los sensores resulte dañado o el posicionamiento de la pipeta sea incorrecto debido a una mala calibración del deck, el brazo del robot no se detendrá y podrá causar daños. Si esto ocurre, apaga el robot rápidamente pulsando el botón de apagado situado al fondo de la parte inferior del panel laterla izquierdo del robot.

**Nota**: En caso de que haya habido una colisión o los sensores no hayan funcionado o hayan resultado dañados, ponte en contacto con soporte.

**Nota**: Cuando el protocolo solo necesita una pipeta, el proceso de calibrado puede entrar en bucle y pedirte varias veces que calibres la misma pipeta. Si esto ocurre, una vez hayas terminado de calibrar la pipeta y aparezca el botón `Next pipette` no pulses en él. En su lugar pulsa en el primer tiprack en el panel del medio para continuar con la calibración.

Una vez acabes de calibrar las pipetas y pases al primer labware, las puntas, te aparecerá una plantilla con la colocación en el deck de los módulos (si los hubiera) y del labware. Es hora de colocarlo todo tal y como se indica en la plantilla, pero todo vacío. Sigue las instrucciones de la sección `Colocar el labware en la cabina` de este manual para hacerlo correctamente. Solo estamos calibrando por el momento y si hubiera líquidos se podría salpicar, manchar o contaminar el labware y la cabina.

![opentrons_calibration_labwarelayout.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_calibration_labwarelayout.jpg?raw=true)

Ahora vamos a comenzar a calibrar las cajas de puntas. El robot desplazará la pipeta correspondiente sobre la punta superior izquierda de cada caja, y usando los controles de la aplicación debe colocarse la pipeta centrada sobre la punta y a ras de su parte superior (a la altura donde acaba la punta debe comenzar la pipeta). Cuando estemos en posición probaremos a coger la punta con la pipeta y si la ha cogido correctamente ese tiprack estará calibrado. Si falla habrá que repetir el proceso hasta que lo haga correctamente.

![opentrons_calibration_controls.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_calibration_controls.jpg?raw=true)

**Nota**: La pipeta monocanal de 1000µl puede hacer sacudidas extrañas al recoger la punta. Esto es un comportamiento que no depende del robot sino de la aplicación, y puede desactivarse dentro de la aplicacción en la ventana `Robot`, en la sección `PIPETTES & MODULES` del panel central. Selecciona el botón `SETTINGS` correspondiente a la pipeta y habrá un checkbox con la opción de `shaking` que se puede desactivar.

**Nota**: Las pipetas multicanal no pueden calibrarse usando solo una punta, tienes que mirar toda la primera fila de puntas y asegurarte de que no solo una pipeta está centrada y a la altura correcta, sino que de media todas lo están.

Finalmente calibraremos el resto del labware. La pipeta monocanal de la derecha habrá cogido una punta del último tiprack calibrado y la usará para este paso. Uno por uno, la pipeta se desplazará al primer pocillo o tubo de cada labware y deberemos calibrarla usando los controles de la aplicación. El extremo inferior de la punta deberá quedar centrada en el pocillo o tubo y a la altura que este comienza en su parte superior.

**Nota**: Cuanto más larga sea la punta, más imprecisa será la calibración, ya que hay mayores posibilidades de que la punta esté ligeramente desviada o la pipeta la haya cogido algo torcida. Se especialmente cuidadoso su utilizas la pipeta monocanal de 1000µl.

**Nota**: No se pueden usar pipetas multicanal para calibrar labware.

Cuando hayamos terminado de calibrar el labware, la pipeta devolverá la punta a su posición y estaremos listos para ejecutar el protocolo.

## Colocar el labware en la cabina

Para colocar el labware dentro de la cabina, sigue las instrucciones que te han sido porporcionadas por el administrador para cada protocolo siguiendo las siguientes recomendaciones:
- Asegúrate de que el robot está detenido.
- Empieza siempre a colocar labware por las casillas del fondo (10 y 11), luego la tercera fila (7, 8 y 9), el medio (4, 5 y 6) y termina con la fila frontal (1, 2 y 3).
- Coloca los botes y cajas tapados siempre que sea posible, y ábrelos solo en el momento antes de la ejecución.
- Cuando montes un rack de Opentrons, asegúrate que la esquina marcada del rack coincide con la marca en el soporte. Esa esquina corresponderá con la esquina superior izquierda de la casilla en el deck.

![opentrons_labware_opentronsrack.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_labware_opentronsrack.jpg?raw=true)

- Para colocar una pieza de labware en su casilla, asegurate de que primero colocas la esquina inferior derecha bien encajada en las pestañas de sujección. El resto debería encajar solo al soltarlo suavemente.

![opentrons_labware_deckslot.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_labware_deckslot.jpg?raw=true)

- Asegurate de que colocas los tubos correspondientes en sus posiciones correctas.
- Coloca todas las cajas de puntas como si el protocolo se fuera a ejecutar para el máximo de muestras y pasos.

## Ejecutar un protocolo

La última opción del menú de la izquierda, `Run`, nos permite darle la orden de ejecución al robot y monitorizar su progreso. En esta ventana veremos en el panel del medio un cronómetro que contabilizará el tiempo de ejecución y los botones de inicio (`START`), pausa (`PAUSE`), reanudar (`RESUME`), cancelar ejecución (`CANCEL RUN`) y resetear protocolo (`RESET RUN`), dependiendo del estado del robot:

- Inicio (`START`):

Esta orden iniciará la ejecución del protocolo cargado. Asegúrate de que el protocolo cargado es el adecuado, de que estás operando el robot correcto, que el labware está colocado y destapado, los módulos requeridos encendidos y las pipetas sin puntas puestas antes de iniciar la ejecución.

![opentrons_run_start.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_run_start.jpg?raw=true)

- Pausa (`PAUSE`):

Detiene temporalmente la ejecución del protocolo. Puede tardar unos segundos en hacer efecto, ya que tendrá que terminar la orden en curso antes de detenerse.

**Nota**: En caso de que el robot encuentre un error subsanable, como por ejemplo apertura de la puerta, falta de puntas o basura llena, detendrá la ejecución como si el botón pausa (`PAUSE`) se hubiera pulsado. Esta situación se notifica al operador tanto por texto en el log como con un mensaje sonoro. Una vez el problema ha sido resuelto, pulsando el botón reanudar (`RESUME`) retomará la ejecución.

![opentrons_run_pause.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_run_pause.jpg?raw=true)

- Reanudar (`RESUME`):

Retoma la ejecución tras una parada.

![opentrons_run_pauserestart.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_run_pauserestart.jpg?raw=true)

- Cancelar ejecución (`CANCEL RUN`):

Aborta la ejecución del protocolo. Esta orden requiere confirmación y no es recuperable.

**Nota**: Tras una cancelación, el robot borrará toda información sobre la ejecución fallida, por lo que es recomendable recargar todas las puntas antes de volver a ejecutar.

![opentrons_run_cancelrunconfirmation.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_run_cancelrunconfirmation.jpg?raw=true)

- Resetear protocolo (`RESET RUN`):

Después de terminar una ejecución el robot se detendrá. El color del baner superior y su mensaje nos indicarán si terminó con éxito (verde), quedo pausada (amarillo) o fue abortada por el usuario o un error irrecuperable (rojo). Para ejecutar de nuevo el mismo protocolo no es necesario volver a subir el protocolo, basta con pulsar este botón y preparará el robot para una nueva ejecución del mismo protocolo.

![opentrons_run_resetrun.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_run_resetrun.jpg?raw=true)

En todo momento, en el panel de la derecha de esta ventana veremos un log de los pasos del protocolo. Cuando esté en ejecución, el log irá acanzando y resaltará en azul la orden que se encuentra realizando el robot en ese momento, en gris las ya realizadas y en negro las que quedan para terminar la ejecución.

**Nota**: Este log corresponde con una simulación previa a la ejecución, por lo que puede ser ligeramente diferente de la realidad o ir a una velocidad distinta a la de ejecución real, por lo que debe tomarse con cautela su información.

## Limpieza del robot
