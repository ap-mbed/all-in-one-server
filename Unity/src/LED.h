/*
 * LED.h
 *
 * TDD4ES workshop
 * The MIT License (MIT)
 * 
 * Copyright (c) 2013 EP Research
 * [Released under MIT License. Please refer to license.txt for details]
 */

#ifndef LED_H_
#define LED_H_

#include <stdint.h>

class LED {
public:
	LED(volatile uint32_t* address, uint8_t pin);
	virtual ~LED();
	void on();
	void off();

private:
	volatile uint32_t* address;
	uint8_t pin;

};

#endif /* LED_H_ */
