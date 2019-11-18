#include <stddef.h>
#include <stdio.h>


#include "ad7124.h"      /* AD7124 definitions */
#include "ad7124_regs.h" /* Get register struct. */
 
void main(void)
{
    struct ad7124_dev *device = NULL;    /* A new driver instance */
    struct ad7124_init_param init_param; /* Initialisation params */
    enum ad7124_registers regNr;         /* Variable to iterate through registers */
    uint32_t timeout = 1000;             /* Number of tries before a function times out */
    int32_t ret = 0;                     /* Return value */
    int32_t sample;                      /* Stores raw value read from the ADC */
    struct ad7124_st_reg *reg;           /* Pointer to the register structure */
 
    /* Initialize AD7124 device. */
    init_param.spi_init = NULL;
    init_param.spi_rdy_poll_cnt = 10;
    ret = ad7124_setup(&device, &init_param);
    if (ret < 0)
    {
        /* AD7124 initialization failed, check the value of ret! */
        printf("Initialise failed, %d\n", ret);
    }
    else
    {
        /* AD7124 initialization OK */
        printf("Initialised OK\n");
    } 
 
    /* Read all registers */
    for (regNr = AD7124_Status; (regNr < AD7124_REG_NO) && !(ret < 0); regNr++)
    {
        reg = ad7124_get_reg(regNr);
        ret = ad7124_read_register(device, reg);
        printf("Register: %d, %d\n", regNr, ret);
    }
 
    /* Read data from the ADC */
    ret = ad7124_wait_for_conv_ready(device, timeout);
    if (ret < 0)
    {
        /* Something went wrong, check the value of ret! */
        printf("Wait failed, %d\n", ret);
    }
 
    ret = ad7124_read_data(device, &sample);
    if (ret < 0)
    {
        /* Something went wrong, check the value of ret! */
        printf("Read failed, %d\n", ret);
    }
    
    printf("Remove\n");
    ad7124_remove(device);
    printf("Done!\n");
}
