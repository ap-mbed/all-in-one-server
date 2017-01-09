/*
 * TestTemperature_Runner.cpp
 *
 * TDD4ES workshop
 * The MIT License (MIT)
 * 
 * Copyright (c) 2013 EP Research
 * [Released under MIT License. Please refer to license.txt for details]
 */

#include "../unity/unity.h"

extern void setUp(void);
extern void tearDown(void);

extern void LEDTest(void);
extern void LED_other_Test(void);
extern void LED_real_Test(void);
extern void LED_direction_reg_test();

static void runTest(UnityTestFunction test) {
	if (TEST_PROTECT()) {
		setUp();
		test();
	}
	if (TEST_PROTECT() && !TEST_IS_IGNORED) {
		tearDown();
	}
}
void resetTest() {
	tearDown();
	setUp();
}

void unity_run_tests(void) {
	printf("Start testing \r\n");

	Unity.TestFile = "test/Tests.cpp";
	UnityBegin();

	// RUN_TEST calls runTest
	RUN_TEST(LEDTest, 1);
	RUN_TEST(LED_other_Test, 2);
	RUN_TEST(LED_direction_reg_test, 3);
	#ifndef TEST_ON_HOST
	RUN_TEST(LED_real_Test, 4);
	#endif


	UnityEnd();
        printf("DONE!");
}

