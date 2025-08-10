from functions.get_file_content import get_file_content


def test():
    calcmain=get_file_content("calculator", "main.py")
    print (calcmain)
    calc=get_file_content("calculator", "pkg/calculator.py")
    print(calc)
    cat=get_file_content("calculator", "/bin/cat") 
    print(cat)
    miss=get_file_content("calculator", "pkg/does_not_exist.py") 
    print(miss)

if __name__ == "__main__":
    test()
