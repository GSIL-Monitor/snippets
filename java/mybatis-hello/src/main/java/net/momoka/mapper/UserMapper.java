package net.momoka.mapper;

import net.momoka.model.User;
import org.apache.ibatis.annotations.Param;

public interface UserMapper {

    public User getUser(@Param("host") String host, @Param("user") String user);

}
