/*
 * LED.cpp
 *
 * TDD4ES workshop
 * The MIT License (MIT)
 * 
 * Copyright (c) 2013 EP Research
 * [Released under MIT License. Please refer to license.txt for details]
 */

#include "LED.h"

LED::LED(volatile uint32_t* address, uint8_t pin) {
	this->address = address;
	this->pin = pin;

	*(address-5) |= (1<<pin);

	off();		// by default, turn led off
}

LED::~LED() {

}

void LED::on() {
	*address |= (1 << pin);
}

void LED::off(){
	*address &= ~(1 << pin);
}

