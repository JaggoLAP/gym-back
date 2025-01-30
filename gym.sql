-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS gym_management;
USE gym_management;

-- Tabla de socios
CREATE TABLE socios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(15),
    direccion VARCHAR(255),
    password VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    estado ENUM('activo', 'vencida', 'gracia') DEFAULT 'vencida'--
);

-- Tabla de cuotas
CREATE TABLE cuotas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    socio_id INT NOT NULL,
    fecha_pago DATE NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado ENUM('activa', 'vencida', 'gracia') DEFAULT 'vencida',
    monto DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (socio_id) REFERENCES socios(id)
);

-- Tabla de actividades
CREATE TABLE actividades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    dias_habilitados VARCHAR(50) DEFAULT NULL, 
    horario TIME DEFAULT NULL,                 
    sesiones_por_mes INT DEFAULT NULL,         
    max_participantes INT DEFAULT NULL,        
    participantes_actuales INT DEFAULT 0,
    precio DECIMAL(10, 2) DEFAULT NULL,        -- O
    activo BOOLEAN DEFAULT TRUE                
);

-- Insertar actividades iniciales
INSERT INTO actividades (nombre)
VALUES
    ('Zumba'),
    ('Cycle'),
    ('Functional Boxing'),
    ('Dodgeball');

-- Tabla de inscripciones a actividades
CREATE TABLE inscripciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    socio_id INT NOT NULL,
    actividad_id INT NOT NULL,
    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sesiones_restantes INT NOT NULL,
    FOREIGN KEY (socio_id) REFERENCES socios(id),
    FOREIGN KEY (actividad_id) REFERENCES actividades(id)
);

-- Tabla de asistencias
CREATE TABLE asistencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    socio_id INT NOT NULL,
    fecha DATE NOT NULL,
    tipo_ingreso ENUM('normal', 'gracia') DEFAULT 'normal',
    FOREIGN KEY (socio_id) REFERENCES socios(id)
);

-- Tabla de empleados
CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(15),
    direccion VARCHAR(255),
    puesto VARCHAR(50),
    password VARCHAR(255) NOT NULL
);

-- Tabla de configuración de precios
CREATE TABLE configuracion_precios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('cuota', 'actividad') NOT NULL, -- Puede ser 'cuota' o 'actividad'
    referencia_id INT DEFAULT NULL,           -- ID de la actividad (si aplica) o NULL para cuotas generales
    precio DECIMAL(10, 2) NOT NULL,           -- Precio actual
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insertar precio inicial de la cuota
INSERT INTO configuracion_precios (tipo, referencia_id, precio)
VALUES
    ('cuota', NULL, 2000.00); -- Precio inicial de la cuota

-- Insertar precios iniciales de actividades en configuración
INSERT INTO configuracion_precios (tipo, referencia_id, precio)
VALUES
    ('actividad', 1, 1000.00), -- Zumba
    ('actividad', 2, 1200.00), -- Cycle
    ('actividad', 3, 1500.00), -- Functional Boxing
    ('actividad', 4, 1100.00); -- Dodgeball