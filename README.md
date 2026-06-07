# TurtleBot3 — Guía de Mapeo y Trayectorias

## Configuración del entorno

En **cada terminal** que abras (robot o PC) ejecuta primero:

```bash
source /opt/ros/humble/setup.bash
source ~/turtlebot3_ws/install/setup.bash
export ROS_DOMAIN_ID=2
export TURTLEBOT3_MODEL=burger
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_LOCALHOST_ONLY=0
```

---

## 1. Mapeo con SLAM

El mapeo requiere tres terminales: una en el **robot** y dos en la **PC**.

### Terminal 1 — Robot (Raspberry Pi)

Debemos conectarnos por SSH al robot, para esto hay que descubrir el robot dentro de la red y luego conectamos con el equipo por medio de la IP descubierta. En el caso de nosotros lo podemos averiguar porque la IP va alineada a la siguiente MAC Address `d8:3a:dd:14:cc:9d` y la red debe ser descubrible para el robot, en otras palabras debe tener las credenciales para conectarse a la red conectada.. 

Lanza el bringup completo del robot:

```bash
source ~/.bashrc
ros2 launch turtlebot3_bringup robot.launch.py
```


### Terminal 2 — PC (SLAM)

Instala el paquete si no lo tienes:

```bash
sudo apt install ros-humble-slam-toolbox
```

Lanza el SLAM en modo online:

```bash
ros2 launch slam_toolbox online_async_launch.py \
  slam_params_file:=/opt/ros/humble/share/slam_toolbox/config/mapper_params_online_async.yaml \
  use_sim_time:=false
```

### Terminal 3 — PC (Teleop)

Maneja el robot con el teclado para construir el mapa:

```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

Controles:
```
       w
  a    s    d
       x

w/x : avanzar/retroceder
a/d : girar izquierda/derecha
s   : parar
```

### Guardar el mapa

Cuando el mapa esté completo, en una **nueva terminal en la PC**:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/maps/mi_mapa
```

Esto genera dos archivos:
- `mi_mapa.pgm` — imagen del mapa
- `mi_mapa.yaml` — metadatos (resolución, origen, etc.)

### Visualizar en RViz2 (opcional)

```bash
ros2 run rviz2 rviz2
```

Agrega los displays:
- `Map` → topic `/map`
- `LaserScan` → topic `/scan`
- `TF`

---

## 2. Trayectorias Autónomas

### Compilar el paquete (solo la primera vez)

```bash
cd ~/lab_sessions/lab2
colcon build --packages-select lab_2_tb
source install/setup.bash
```

El robot debe tener el bringup corriendo antes de ejecutar cualquier trayectoria.

### Prerequisito — Robot corriendo

**Robot (Raspberry Pi):**
```bash
ros2 launch turtlebot3_bringup robot.launch.py
```

---

### Trayectoria Circular

El robot describe círculos continuos. El radio depende de la relación entre velocidades:

```
radio (m) = linear_speed / angular_speed
```

**PC:**
```bash
ros2 run lab_2_tb circle_trajectory
```

Con parámetros personalizados:
```bash
ros2 run lab_2_tb circle_trajectory --ros-args -p linear_speed:=0.15 -p angular_speed:=0.3
```

| Parámetro       | Default   | Descripción                         |
|-----------------|-----------|-------------------------------------|
| `linear_speed`  | 0.2 m/s   | Velocidad de avance                 |
| `angular_speed` | 0.5 rad/s | Velocidad de giro (define el radio) |

Presiona `Ctrl+C` para detener. El robot frena automáticamente.

---

### Trayectoria en S

El robot alterna arcos a izquierda y derecha formando una S continua.

**PC:**
```bash
ros2 run lab_2_tb s_trajectory
```

Con parámetros personalizados:
```bash
ros2 run lab_2_tb s_trajectory --ros-args -p linear_speed:=0.15 -p arc_duration:=5.0
```

| Parámetro       | Default   | Descripción                              |
|-----------------|-----------|------------------------------------------|
| `linear_speed`  | 0.2 m/s   | Velocidad de avance                      |
| `angular_speed` | 0.5 rad/s | Amplitud del giro en cada arco           |
| `arc_duration`  | 3.0 s     | Duración de cada arco antes de invertir  |

Presiona `Ctrl+C` para detener. El robot frena automáticamente.

---

## Resumen de terminales por tarea

### Mapeo

| Terminal | Máquina       | Comando                                                              |
|----------|---------------|----------------------------------------------------------------------|
| 1        | Robot (RPi)   | `ros2 launch turtlebot3_bringup robot.launch.py`                     |
| 2        | PC            | `ros2 launch slam_toolbox online_async_launch.py use_sim_time:=false` |
| 3        | PC            | `ros2 run turtlebot3_teleop teleop_keyboard`                         |
| 4        | PC (al final) | `ros2 run nav2_map_server map_saver_cli -f ~/maps/mi_mapa`           |

### Trayectorias

| Terminal | Máquina     | Comando                                          |
|----------|-------------|--------------------------------------------------|
| 1        | Robot (RPi) | `ros2 launch turtlebot3_bringup robot.launch.py` |
| 2        | PC          | `ros2 run lab_2_tb circle_trajectory`            |
|          |             | o `ros2 run lab_2_tb s_trajectory`               |
