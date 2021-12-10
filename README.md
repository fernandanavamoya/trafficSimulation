# Reto-Movilidad-Urbana

## Pre Requisitos:
### Mesa
**Lo siguiente es para crear un ambiente virutal, en caso de querer intalar mesa en tu propio computadora ve salta lo siguiente y solo instala mesa**

Descargar Miniconda
> https://docs.conda.io/en/latest/miniconda.html

Crear un ambiente virtual desde terminal
```
conda create --nombreambiente
conda activate nombreambiente
```

**Instalación de mesa**
```
pip intall mesa
```
**Instalación de Flask**
```
pip intall Flask
```

Verifica que estas dentro del ambiente
> Python 3.8.12 64-bits ('nombreambiente': conda)

### Unity
Instalar Unity HUB
> https://unity3d.com/es/get-unity/download

Instalar Unity version
> 2020.3.22f1


### IBM Cloud
Seguir documentación
> https://github.com/IBM-Cloud/get-started-python


## Instalación
Clonar repositorio desde GIT Bash
```
git clone https://github.com/adriabellak/Reto-Movilidad-Urbana.git

```

**Si estas utilizando un ambiente virtual**, verifica que estes dentro del ambiente virtual de conda
> Python 3.8.12 64-bits ('nombreambiente': conda)

Dentro de los archivos del repositorio ve a:
> /Unity/Traffic

Abre una terminal desde ahí, **si estas usando un ambiente virtual debaría aparecerte lo siguiente** en caso de que no activa tu ambiente virtual
```
conda activate nombreambiente
```

Corre el siguiente archivo desde la terminal, esto va a abrir el puerto 8586 para poder correr la simulación
```
python unity.py
```
Abre el proyecto de unity y ponle play a la simulación







