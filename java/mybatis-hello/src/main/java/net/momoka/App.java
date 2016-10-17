package net.momoka;

import javax.sql.DataSource;

import net.momoka.mapper.UserMapper;
import net.momoka.model.User;
import org.apache.ibatis.datasource.pooled.PooledDataSource;
import org.apache.ibatis.mapping.Environment;
import org.apache.ibatis.session.Configuration;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.apache.ibatis.transaction.TransactionFactory;
import org.apache.ibatis.transaction.jdbc.JdbcTransactionFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Hello world!
 * 
 */
public class App {

    private static final Logger LOGGER = LoggerFactory.getLogger(App.class);

    public static void main(String[] args) {

        DataSource dataSource =
            new PooledDataSource("com.mysql.jdbc.Driver",
                "jdbc:mysql://localhost:3306/mysql", "root", "");

        TransactionFactory transactionFactory = new JdbcTransactionFactory();
        Environment environment =
            new Environment("development", transactionFactory, dataSource);
        Configuration configuration = new Configuration(environment);
        configuration.addMapper(UserMapper.class);
        SqlSessionFactory sqlSessionFactory =
            new SqlSessionFactoryBuilder().build(configuration);

        SqlSession session = sqlSessionFactory.openSession();

        UserMapper mapper = session.getMapper(UserMapper.class);

        LOGGER.debug("{}", mapper);
        User user = mapper.getUser("localhost", "root");

        LOGGER.debug("{}", user);

        session.commit();
        session.close();

    }
}
