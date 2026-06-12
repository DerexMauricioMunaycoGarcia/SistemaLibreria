CREATE DATABASE LibreriaDB;
GO

USE LibreriaDB;
GO

------Creamos tabla Producto
CREATE TABLE Productos (
    IdProducto INT IDENTITY(1,1) PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Precio DECIMAL(10,2) NOT NULL,
    Stock INT NOT NULL,
    Estado BIT DEFAULT 1
);

------Creamos tabla Clientes 
   CREATE TABLE Clientes (
    IdCliente INT IDENTITY(1,1) PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    DNI CHAR(8) NOT NULL,
    Telefono VARCHAR(15),
    Estado BIT DEFAULT 1
);

------Creamos la tabla Ventas 
CREATE TABLE Ventas (
    IdVenta INT IDENTITY(1,1) PRIMARY KEY,
    Fecha DATETIME DEFAULT GETDATE(),
    Total DECIMAL(10,2) NOT NULL,
    IdCliente INT NOT NULL,

    CONSTRAINT FK_Ventas_Clientes
    FOREIGN KEY (IdCliente)
    REFERENCES Clientes(IdCliente)
);

------Creamos la tabla detalle venta
CREATE TABLE DetalleVenta (
    IdDetalle INT IDENTITY(1,1) PRIMARY KEY,
    IdVenta INT NOT NULL,
    IdProducto INT NOT NULL,
    Cantidad INT NOT NULL,
    Precio DECIMAL(10,2) NOT NULL,
    Subtotal DECIMAL(10,2) NOT NULL,

    CONSTRAINT FK_DetalleVenta_Ventas
    FOREIGN KEY (IdVenta)
    REFERENCES Ventas(IdVenta),

    CONSTRAINT FK_DetalleVenta_Productos
    FOREIGN KEY (IdProducto)
    REFERENCES Productos(IdProducto)
);
------- creacion de la tabla login
CREATE TABLE Usuarios(
    IdUsuario INT IDENTITY(1,1) PRIMARY KEY,
    Usuario VARCHAR(50),
    Clave VARCHAR(100),
    Rol VARCHAR(20)
);
-------Insertamos datos
INSERT INTO Productos(Nombre, Precio, Stock)
VALUES
('Libro SQL Server', 50.00, 20),
('Libro Python', 70.00, 15),
('Cuaderno Universitario', 12.00, 50),
('Lapicero Azul', 2.50, 100);

INSERT INTO Clientes(Nombre, DNI, Telefono)
VALUES
('Juan Perez', '12345678', '987654321'),
('Maria Lopez', '87654321', '999888777');

INSERT INTO Usuarios
VALUES
('admin','123456','Administrador');


Select * from Productos;
select * from Clientes;
SELECT * FROM Ventas;
SELECT * FROM DetalleVenta;
SELECT * FROM Usuarios;

SELECT 
    V.Fecha, 
    C.Nombre AS 'Cliente', 
    C.DNI, 
    P.Nombre AS 'Producto', 
    DV.Cantidad, 
    DV.Subtotal
FROM Ventas V
JOIN Clientes C ON V.IdCliente = C.IdCliente
JOIN DetalleVenta DV ON V.IdVenta = DV.IdVenta
JOIN Productos P ON DV.IdProducto = P.IdProducto
ORDER BY V.Fecha DESC;