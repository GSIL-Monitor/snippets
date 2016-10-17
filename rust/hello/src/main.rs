extern crate redis;
use redis::Commands;

fn fetch_an_integer() -> redis::RedisResult<isize> {
    // connect to redis
    let client = try!(redis::Client::open("redis://127.0.0.1/"));
    let con = try!(client.get_connection());

    let _ : () = try!(con.set("my_key", 42));

    con.get("my_key");
}

fn main() {
    println!("Hello, world!");
    let c = fetch_an_integer();
    println!("{}", c);
}
