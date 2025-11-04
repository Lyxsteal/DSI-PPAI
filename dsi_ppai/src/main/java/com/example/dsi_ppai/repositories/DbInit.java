package com.example.dsi_ppai.repositories;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public final class DbInit {
    private static final String URL = "jdbc:h2:file:estacionSismo;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE"; //jdcb // dmbs q laburamos // q este en memoria // asi se llama la bd // no se cierra la conexion
    private static final String USER = "sa";
    private static final String PASS = "";

    private DbInit() {
    }

    public static void run() throws SQLException, IOException {
        try (Connection conn = DriverManager.getConnection(URL, USER, PASS)) {
            exec(conn, "src/main/resources/sql/ddl.sql");
        }
    }

    private static void exec(Connection conn, String file) throws IOException, SQLException {
        String sql = Files.readString(Path.of(file), StandardCharsets.UTF_8);
        try (Statement st = conn.createStatement()) {
            if (st == null) {
                throw new IOException("Archivo no encontrado" + file);
            }
            st.execute(sql);
        }
    }
}
