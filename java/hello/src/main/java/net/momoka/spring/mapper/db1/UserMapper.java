package net.momoka.spring.mapper.db1;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Update;
import net.momoka.spring.model.User;


@Mapper
public interface UserMapper {

  @Select("SELECT * FROM user WHERE id = #{id}")
  User select(@Param("id") long id);

  @Select("SELECT * FROM user")
  List<User> all();

  @Insert("INSERT INTO user (id, username) VALUES (#{id}, #{username})")
  int insert(User user);

  @Update("UPDATE user SET username = #{username} WHERE id = #{id}")
  int update(User user);

}
