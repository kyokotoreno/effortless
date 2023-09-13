package edu.usta.configuracion;

import java.sql.*;
import java.util.logging.*;

public class MiConexion {
    private String url, clave, usuario, driver;
    protected String cadenaSql;
    protected ResultSet registros;
    protected Connection conexion;
    protected Integer cantidad;
    protected PreparedStatement consulta;

    public MiConexion() {
        this.usuario = "%user%";
        this.clave = "%pass%";
        this.driver = "org.mariadb.jdbc.Driver";
        this.url = "jdbc:mariadb://localhost:3306/%basedatos%";
        
        this.conectarse();
    }
    
    private void conectarse() {
        try {
            Class.forName(this.driver);
            this.conexion = DriverManager.getConnection(this.url, this.usuario, this.clave);
            System.out.printf(%conexion_establecida%);
        } catch (ClassNotFoundException | SQLException ex) {
            Logger.getLogger(MiConexion.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}
