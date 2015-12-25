package net.momoka.jdbc;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;

import com.mchange.v2.c3p0.ComboPooledDataSource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MySQLExample {
	
	private static final Logger logger = LoggerFactory.getLogger(MySQLExample.class);

	public static void main(String[] args) throws Exception {
		
		ComboPooledDataSource ds = new ComboPooledDataSource();
		
		ds.setDriverClass("com.mysql.jdbc.Driver");
		ds.setUser("root");
		ds.setPassword("");
		ds.setJdbcUrl("jdbc:mysql://127.0.0.1:3306/test?charset=utf8");
		
		Connection conn = ds.getConnection();
		
		Statement stmt = conn.createStatement();
		
		ResultSet rs = stmt.executeQuery("SELECT 1");
		
		if (rs.next()) {
			int result = rs.getInt(1);
			logger.info("{}", result);
		}
		
		rs.close();
		stmt.close();
		
		PreparedStatement _ = conn.prepareStatement("UPDATE user SET id = 10 WHERE id = ?");
		_.setInt(1, 2);
		int affectedRows = _.executeUpdate();
		
		logger.info("{}", affectedRows);
		
		_.close();
		
		conn.close();
		ds.close();
		
		return;
	}
}
