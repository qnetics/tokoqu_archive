from src.apis.id import generate_id

class assert_methods :

    def assert_equals_test(self, test_name, expectation, reality) -> None :

        if expectation == reality :

            print(f"{test_name} .............. [ SUCCESS ]")

        else :

            print(f"{test_name} .............. [ FAILED ]")


    def assert_not_equals_test(self, test_name, expectation, reality) -> None :

        if expectation != reality :

            print(f"{test_name} .............. [ SUCCESS ]")

        else :

            print(f"{test_name} .............. [ FAILED ]")


    def assert_boolean_test(self, test_name, expectation) -> None :

        if expectation :

            print(f"{test_name} .............. [ SUCCESS ]")

        else :

            print(f"{test_name} .............. [ FAILED ]")



class testing_units(assert_methods, generate_id) :

    def __init__(self) -> None :

        super().__init__()


    # apis testing
    def id_generate_tests(self) -> None :

        expectation = 32

        reality = len( self.id_generate() )

        self.assert_equals_test( test_name = "id_generate_tests()", expectation = expectation, reality = reality )

    def all_tests(self) :

        tests = [

            self.id_generate_tests()

        ]

        for test in tests :

            test

        

