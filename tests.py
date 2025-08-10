from functions.write_file import write_file


def test():
    response=write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(response)
    response=write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(response)
    response=write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(response)
    
if __name__ == "__main__":
    test()
