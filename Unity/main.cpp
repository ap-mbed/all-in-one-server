extern void unity_run_tests();


int main() {

	unity_run_tests();

#ifndef TEST_ON_HOST
	while (1) {
	}
#endif //TEST_ON_HOST
	return 0;

}
