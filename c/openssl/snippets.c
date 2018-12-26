#include <stdio.h>
#include <string.h>
#include <time.h>
#include <openssl/err.h>
#include <openssl/pem.h>
#include <openssl/x509.h>
#include <openssl/x509v3.h>
#include <openssl/x509_vfy.h>
#include <openssl/cms.h>

BIO * mem2bio(BIO * berr, const char * in, int insize) {
	BIO * rv = NULL;
	rv = BIO_new(BIO_s_mem());

	if (BIO_write(rv, in, insize) <= 0) {
		BIO_printf(berr, "cannot read mem");
		rv = NULL;
		goto end;
	}
end:
	return rv;
}

int main() {
	int i = CMS_ContentInfo_print_ctx(NULL, NULL, 0, NULL);
	printf("i: %d\n", i);

	BIO * berr = BIO_new(BIO_s_mem());
	const char * in = "";

	char * out = calloc(1024, 1);

	int insize = 0;
	PKCS7 * rv = NULL;
	BIO * bin = mem2bio(berr, in, insize);
	if (bin == NULL) {
		printf("mem2bio is null\n");
		goto end;
	}

	rv = d2i_PKCS7_bio(bin, NULL);
	if (rv == NULL) {
		// BIO_puts(berr, "cannot load p7 object");
		printf("cannot load p7 object\n");
		goto end;
	}

	printf("rv: %p\n", rv);


end:
	if (bin != NULL) BIO_free(bin);
	// return rv;
	BIO_gets(berr, out, 1024);
	printf("berr: %s\n", out);
	return 0;
}
