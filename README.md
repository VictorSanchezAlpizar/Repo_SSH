# Tarea 4 Verificacion Funcional - Codificación

Autores:
- Víctor Sánchez Alpízar
- Juan Pablo Ureña Madrigal

Profesor:
- Luis Adolfo Alfaro Hidalgo

El presente documento tiene como finalidad:
- Explicar el funcionamiento principal de la interfaz desarrollada para el SSH.
- Explicar el funcionamiento de las funciones de simulación diseñadas para poder generar pruebas y escenarios diferentes en SSH.

## Interfaz principal.

### Menu de Inicio

![Figura Menu Inicio](Figuras\Menu_Inicio.png)

En esta sección el sistema espera por el ingreso de un usuario y su contraseña. De forma predefinida se encuentran los siguientes usuarios:
- Usuario 1. ID: 1. PWD: 1234.
- Usuario 2. ID: 2. PWD: 2341.
- Usuario 3. ID: 3. PWD: 3412.
- Usuario 4. ID: 4. PWD: 4123.
- Usuario 5. ID: 5. PWD: 5555.
Nota: Posteriormente, estos usuarios pueden, y deben, ser modificados para mantener la privacidad del usuario.

Adicionalmente, en esta interfaz se muestra información de importancia para el usuario:
- La fuente de alimentación seleccionada por el módulo.
- El nivel de la batería de respaldo.
- Modo Activo (incialmente será Desarmado).
- Botones "Pánico" y "Bomberos".

Así como los indicadores LED "Batería" y "Alerta", además del nombre del modelo e identificador.

Finalmente, se encuentra el botón "Abrir Interfaz Sim", el cuál no estará disponible en la versión del cliente, pero es importante para ofrecer distintas opciones de simulación.
- Este modo es principalmente útil para técnicos que requieran determinar si el sistema se encuentra funcionando integramente y poder detectar posibles fallas.

Al seleccionar un usuario se presentará la pantalla de Contraseña:

![Figura Menu Inicio](Figuras\Menu_Inicio_Contraseña.png)

A continuación, el sistema le pedirá al usuario que indique el nivel de batería por debajo del cuál se debe alarmar.

![Figura Menu Inicio](Figuras\Menu_Inicio_BatLvl.png)

### Menu Principal

Una vez que la configuración inicial del usuario se encuentra preparada, el sistema entrará al Menu Principal.

![Figura Menu Inicio](Figuras\Menu_Principal.png)

En este menú se despliega información de relevancia tal como:
- Usuario activo.
- Modo Activo.
- Fuente de alimentación seleccionada.
- Nivel de Batería.
- Cerrar Sesión de Usuario.

En esta interfaz el usuario puede interactuar con el sistema de las siguientes formas:
- Ingresar códigos de Modo para poder ingresar a las distintas opciones disponibles.
- Enviar mensajes de auxilio tales como "Pánico" y "Bomberos".

### Modo Admin


### Modo 0


### Modo 1


### Modo Desarmado


### Modo Ahorro


## Interfaz de Simulación

Al presionar el botón "Abrir Interfaz Sim" es posible acceder a opciones para testear diferentes funciones del SSH.

![Figura Menu Inicio](Figuras\Menu_Sim.png)

En este menú se pueden realizar las siguientes opciones:
- Establecer falla en la fuente "Principal" de energía.
- Limpiar falla en la fuente "Principal" de energía.
- Menú para fallas en sensores. Este Menú ofrece opciones para probar los 16 sensores disponibles por el sistema.
- Limpiar fallas (debido a botón de "Pánico", "Bomberos" o "Sensores")
- Nivel. Indicar el nivel actual de la batería. Al mover este indicador de 0-100 se puede probar que sucede cuando una falla en la fuente "Principal" ocurre y el nivel de batería varia.

Para el caso del Menú para fallas en sensores, se tiene la siguiente interfaz:

![Figura Menu Inicio](Figuras\Menu_Sim_2.png)

Cada botón presente en el menú anterior ofrece opciones para alertar cualquiera de los 16 sensores.