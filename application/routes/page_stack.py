class PageStack:
    stack = []

    @staticmethod
    def stack_page(func):
        ''' Decorate a view function with this to att to stack. '''
        def wrapper(*args, **kwargs):
            # Add page to stack
            page = {'func': func, 'args': args, 'kwargs': kwargs}
            PageStack.stack.append(page)
            print("hallloooo")
            # Run page as normal
            return func(*args, **kwargs)
        return wrapper
    
    @staticmethod
    def previous():
        ''' Pops the most recent view function from the stack and runs it. '''
        # Get most previous page
        page = PageStack.stack.pop()
        func = page['func']
        args = page['args']
        kwargs = page['kwargs']
        # Run function again
        func(*args, **kwargs)
        # Add to 

    @staticmethod
    def clear():
        PageStack.stack = []


    

if __name__ == '__main__':
    
    @PageStack.stack_page
    def say_hello(name, is_old=True):
        hello_str = f'Hello {name}'
        if is_old:
            hello_str += ' you oldie'
        print(hello_str)

    say_hello('Ronja', True)

    PageStack.previous()
    print()
    PageStack.previous()
    PageStack.previous()

