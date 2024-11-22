# Be Innovation Tech


## ODOO-DEV | odoo_skeleton

Repositorio base para desarrollos en Odoo.

## Desarrollado por:

   - "Elias Braceras"
   - "Horacio Montaño"

----------------------------------------------------------------------------------------------------------------------------------------------------------

### Descripcion simple:

  Este repositorio debe ser utilizado como molde para cualquier desarrollo de Odoo. El repositorio esta equipado con una serie de herramientas para agilizar el trabajo durante la preparación para el desarrollo.

  - Este entorno de desarrollo esta pensado para quienes desarrollen en sistemas operativos Linux, tales como Ubuntu, Debian, etc. Sin embargo
    para quienes prefieran desarrollar en Windows les sugerimos que instalen en sus máquinas **WSL2** Subsistema de Linux para Windows.
  
  - Usted dispone en esta versión de un lanzador de proyecto CLI, diseñado para facilitar el armado de su proyecto de desarrollo.
  
  - Se utiliza docker para la creación de instancias de Odoo y docker compose para levantarlas junto con una base de datos.

  - Dispone de una serie de configuraciones preparadas para su uso en VScode como configuraciones para depuración y lanzamiento de contenedores.

  - Utiliza Gitman para la descarga e instalación de repositorios externos.
  
  -  Asegúrese de tener instalado **Docker** y **Docker compose** en su computadora, en el caso de no tener instalada dicha herramienta,
 puede servirse de la guia oficial de Docker para instalar, [Guía para la Instalación de Doker](https://docs.docker.com/engine/install/ubuntu/)
 
  - El lanzador permite utilizar repositorios privados, para desarrollo. Para esto, en tu directorio **odoo-skeleton** encontraras una carpeta oculta **.ssh** 
  dentro de la cual, deberás copiar tu llave privada ssh, la misma que tengas configurada en tu repositorio privado de desarollo.
 
------------------------------------------------------------------------------------------------------------------------------------------------------------

### INSTRUCCIONES:
 

 1. Como primer paso usted debe utilizar el repositorio de Be-Innovation-Tech, nuestra plantilla **odoo-skeleton**, creando un repositorio a partir de la misma con el botón
 **use this template** que se encuentra en la esquina superior derecha en color verde.
 
 2. Determinar el nombre que desea para su repositorio de desarrollo, así como también verificar si desea incluir todas las ramas o alguna en especial.
 
 3. Una vez creado su repositorio, debe clonar el mismo:
 
    ```git clone -b "nombre_de_la_rama´ "url_del_repo"``` 
    
> Si quiere clonar el repositorio completo, desestime la bandera "-b y nombre_de_la_rama"

> Si va a desarrollar para edicion Community, utilice la rama **main**

 4. Antes de comenzar con la ejecución del lanzador, ingrese al directorio de su repositorio e instale las dependencias con el comando:
 
    ```sudo pip3 install -r requirements.txt```
 
 5. Ahora puede ejecutar su LANZADOR ejecutando: 
 
    ```./run.sh``` 
    
    o también puede hacerlo de la siguiente forma:
    
    ``` copier copy ./ ./  --trust ```
    
    para indicar que va a trabajar en la ruta donde esta posicionado.
 
> es ideal que la ruta destino, sea la misma donde se encuentra para eso en ruta destino
use el siguiente comando "./"
esto hará que el proyecto de inicio en el directorio de su repositorio.

 6. Siga los pasos indicados por el software de lanzamiento.

 7. La segunda etapa del LANZADOR le ofrece la opcion de usar **GITMAN** para repositorios de terceros, si le indica que sí! Deberá completar las preguntas. Nuestro lanzador se ocupara de modificar la linea de **addons_path** completando con la ruta de los repositorios agregados.

 8. Una vez finalizado su proyecto, debe levantar su ambiente con el comando: 
   
    ```docker compose up``` o 

    ```docker compose up -d```


 9. Puede verificar que su instancia este corriendo con el comando 
    
    ```docker compose ps```
    
 o en su navegador de preferencia colocando la URL **localhost:puerto**
 
 10. Si su proyecto finalizo con éxito, podrá ejecutar el comando:
    
   ```code .```
    
  ¡AHORA PUEDE COMENZAR A DESARROLLAR CON "VISUAL STUDIO CODE"! 

 ------------------------------------------------------------------------------------------------------------------------------------------------------

### Sugerencias y Consideraciones:

 - Recomendamos utilizar Extensiones de Visual Studio Code, como **Docker**, **Dev Container**, y todas aquellas que considere de utilidad
 para poder trabajar en VSCode.
 
  - Si usted necesita ocupar addons de terceros, luego de haber utilizado el lanzador y haberle indicado NO, puede mas tarde agregar sus repositorios a mano o ejecutar nuevamente su lanzador, sin modificar la informacion relevenate para la construccion, pero si determinando que repositorios va a ocupar.
  
  - En el caso de estar corriendo su ambiente y necesitar agregar repositorios publicos de terceros y decide hacerlo a mano, sin el asistente; debe utilizar el siguiente comando para editar su gitman.yml :
  
      ```sudo nano gitman.yml``` 
  
  y completar cada linea, comenzando por la URL del repositorio, la versión
  del mismo, acorde a la versión de su despliegue de desarrollo. Deberá replicar el conjunto de lineas para agregar mas repositorios de terceros.
  Si tiene dudas con el uso, puede revisar la guía oficial de [gitman](https://gitman.readthedocs.io/en/latest/)
  - Todos los repositorios declarados en "gitman" deberán ser declarados en el archivo **odoo.conf** en la linea de **addons_path**
  Ejemplo:
  
      ```addons_path: usr/lib/python/dist-packages/odoo/extra_addons/,usr/lib/python/dist-packages/odoo/external_addons/account-financial-tools```
    
  Siendo la segunda linea declarada, la que corresponde con los paquetes de modulos de ADHOC. 
  
  > Recuerde que cuando inicia su LANZADOR, el mismo le preguntará si desea utlizar gitman, y en esos pasos puede declarar los repositorios necesarios. Como también puede hacerlo
  lugo de haber lanzado su proyecto, editando el archivo "gimtna.yml" como lo especificamos aquí.
  
  - Gitman crea una carpeta donde contendrá todos los módulos declarados con el nombre de **external_addons** los mismos los puede localizar 
  dentro de su contenedor web Odoo en la ruta declarada en el **odoo.conf**
  
  - Todos los paths deberán estar separados por una coma ","
  
  - Una vez declarados los módulos de terceros en "gitman" sera necesario hacer un rebuild de su imagen, respetando el mismo nombre 
  de la imagen creada en un principio, con el comando 
    
      ```docker build . -t nombre-de-mi-imagen```
  
  - Luego reiniciar el serivcio Odoo o el contenedor con el comando 
    
      ```docker compose restart```
  
  y una vez dentro de su instancia Odoo
  actualizar la lista de aplicaciones en modo "desarrollador" para poder tener los módulos nuevos visibles. 

Si usted modifica su archivo **gitman.yml** antes de realizar la construcción con el comando "build" sera mas que suficiente para poder ver los módulos
sin necesidad de reiniciar sus contenedores.

  - Todos los módulos de terceros simples, como el propio en desarrolo aconsejamos que los coloque en la carpeta **addons** que se encuentra dentro del directorio de trabajo.
  
  - Recuerde que puede operar con el comando **scaffold** para la creacion de su propio modulo, ingresando a su contenedor web y dirigirse al directorio de **addons**
  
  	```cd /usr/lib/python3/dist-packages/odoo/extra-addons/```
  	
  Una vez dentro puede ejecutar el comando SCAFFOLD:
  
  	```odoo scaffold nombre_de_su_modulo ./```
  


------------------------------------------------------------------------------------------------------------------------------------------------------

### Soporte Técnico

- Si usted tiene algun problema con el ambiente de desarrollo, revise nuevamente la guia o consulte con su administrador.

