#include "printk.h"
#include "sbi.h"

extern void test();

int start_kernel() {
    // printk("2021");
    // printk(" Hello \n");

    test(); // DO NOT DELETE !!!

	return 0;
}
