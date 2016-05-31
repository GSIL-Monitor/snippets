#include <stdint.h>
typedef uint8_t u_char;

#include <bsd/stdlib.h>
#include <openssl/evp.h>
#include <stdint.h>
#include <string.h>
#include <inttypes.h>

#define MAX_PADDING 8192;

void sha1()
{
	EVP_MD_CTX ctx;

	char buffer[] = "123456";
	uint8_t md_output[EVP_MAX_MD_SIZE];
	unsigned int md_len;

	EVP_DigestInit(&ctx, EVP_sha1());
	EVP_DigestUpdate(&ctx, buffer, sizeof(buffer));
	EVP_DigestFinal(&ctx,  md_output, &md_len);

	for (int i = 0; i < 6000; i++) {
		EVP_DigestInit(&ctx, EVP_sha1());
		EVP_DigestUpdate(&ctx, md_output, md_len);
		EVP_DigestFinal(&ctx,  md_output, &md_len);
	}

	printf("%s\n", md_output);
}


int main(int argc, char** argv)
{
	u_int32_t rnd = arc4random();

	unsigned int padding_length = rnd % MAX_PADDING;

	printf("%u\n", padding_length);

	return 0;
}
