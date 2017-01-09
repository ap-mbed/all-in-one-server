/*
 * TestTemperature.cpp
 *
 *  TDD4ES workshop
 *  The MIT License (MIT)
 *
 * Copyright (c) 2013 EP Research
 * [Released under MIT License. Please refer to license.txt for details]
 */

#include "../unity/unity.h"

#include "../src/LED.h"

#include "stdint.h"

#ifndef TEST_ON_HOST
#include <LPC17xx.h>
#endif

void setUp(void) {

}

void tearDown(void) {

}

void LEDTest(void) {

	volatile uint32_t gpio_reg [6] = {0};
	volatile uint32_t *virtualLeds = gpio_reg + 0x05;
	*virtualLeds = 0xFFFFFFFF;
	LED *led_fake = new LED(virtualLeds, 0);
	led_fake->off();
	TEST_ASSERT_EQUAL_HEX32(0xFFFFFFFE, *virtualLeds);
	led_fake->on();
	TEST_ASSERT_EQUAL_HEX32(0xFFFFFFFF, *virtualLeds);
	delete led_fake;
}

#ifndef TEST_ON_HOST
void LED_real_Test(void) {
	LED led_real = LED(&LPC_GPIO1->FIOPIN, 18);
	led_real.on();
	TEST_ASSERT(LPC_GPIO1->FIOPIN & (1 << 18));
}
#endif

void LED_direction_reg_test() {
	volatile uint32_t gpio_reg [6] = {0};
	volatile uint32_t *virtualLeds = gpio_reg + 0x05;
	*virtualLeds = 0xFFFFFFFF;
	LED *led_fake = new LED(virtualLeds, 0);
	TEST_ASSERT_EQUAL_HEX32(0x00000001, gpio_reg[0]);
	delete led_fake;
}

void LED_other_Test(void) {
	volatile uint32_t gpio_reg [6] = {0};
	volatile uint32_t *virtualLeds = gpio_reg + 0x05;
	*virtualLeds = 0xFFFFFFFF;
	LED *led_fake = new LED(virtualLeds, 0);
	LED *led_otherfake = new LED(virtualLeds, 1);
	led_fake->on();
	TEST_ASSERT_EQUAL_HEX32(0xFFFFFFFD, *virtualLeds);
	led_otherfake->on();
	TEST_ASSERT_EQUAL_HEX32(0xFFFFFFFF, *virtualLeds);
	led_fake->off();
	TEST_ASSERT_EQUAL_HEX32(0xFFFFFFFE, *virtualLeds);
	delete led_fake;
	delete led_otherfake;
}



