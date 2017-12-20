#include <libxml/xmlversion.h>
#include <libxml/parser.h>

int
main(void)
{
    LIBXML_TEST_VERSION
    xmlCleanupParser();
		printf("Ok\n");
    return 0;
}
