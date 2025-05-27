import traceback

def func1():
    try:
        raise ValueError("Error occured")
    except Exception as e:
        stack_trace = traceback.extract_stack()

    last_caller = stack_trace[-2].name
    print(f"Last caller before exception : {last_caller} ")
        
def func2():
    func1()

def func3():
    func2()

func3()