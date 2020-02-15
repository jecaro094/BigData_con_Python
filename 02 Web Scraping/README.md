**Comando para acceder al servidor de AWS por ssh**
```
 ssh -i Servertutorial.pem ubuntu@ec2-54-162-25-214.compute-1.amazonaws.com
```
**Hay que usar el certificado que se detalla como argumento <span style="color:red">(Servertutorial.pem)</span>, que estará guardado en mi nube <span style="color:red">(Master_Big_Data/Seminario_02_Web_Scraping)</span>**

---

**Una vez en el servidor, se usa este comando**
```
python -u  datos_diarios.py > data/datos_salida.txt &
```

**para ejecutar el código de python añadido en el background, como un proceso independiente <span style="color:green">(&)**

**Pongo en <span style="color:red">data/datos_salida.txt</span> la salida por pantalla con <span style="color:red">print</span>. Hay que crear la carpeta <span style="color:red">data</span> al principio, aunque esté vacía.**

---

**Para comprobar los procesos que se encuentran ejecutándose en ese momento:**

```
ps -aux | less
```

**y busco aquel que detalle el comando de python que he puesto en la sección anterior. Cuando lo encuentre, si lo quiero borrar, <span style="color:red">mato el proceso con kill**

```
kill -9 _PID_
```
---

**Cada vez que quiera ejecutar el fichero en python con**

```
python -u datos_diarios.py > data/datos_salida.txt &
```

**Para WHATSAPP, poner estas credenciales por terminal:**

- <span style="color:green">**GOOGLE_DRIVE/MASTER_BIG_DATA/02_WEB_SCRAPING/credenciales.txt**

**Y activar/[desactivar] el entorno de python**



```
source ./pywhatsapp/bin/activate
```
```
deactivate
```


---

**<span style="color:red">Para acabar de implementar la transferencia de fotos a amazon ws:**

- **<span style="color:green">pip install boto3**
