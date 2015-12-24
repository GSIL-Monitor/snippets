package net.momoka;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.util.HashMap;
import java.util.Map;

import org.msgpack.jackson.dataformat.MessagePackFactory;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MsgpackExample {

	private static final Logger logger = LoggerFactory
	  .getLogger(MsgpackExample.class);

	public static void main(String[] args) throws Exception {

		File f = new File("input.msgpack");
		FileInputStream fis = new FileInputStream(f);

		byte[] data = new byte[(int) f.length()];
		fis.read(data);

		logger.info(data.toString());

		ObjectMapper mapper = new ObjectMapper(new MessagePackFactory());

		Object _ = mapper.readValue(data, new TypeReference<Map<String, Object>>() {
		});
		
		logger.info(_.toString());
	}
}
