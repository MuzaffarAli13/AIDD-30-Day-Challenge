import sys

def add(x, y):
    """Adds two numbers"""
    return x + y

def subtract(x, y):
    """Subtracts two numbers"""
    return x - y

def multiply(x, y):
    """Multiplies two numbers"""
    return x * y

def divide(x, y):
    """Divides two numbers"""
    if y == 0:
        return "Error! Division by zero."
    return x / y

def main():
    print("Simple Calculator")
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")

    while True:
        choice = input("Enter choice(1/2/3/4): ")

        if choice in ('1', '2', '3', '4'):
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
            except ValueError:
                print("Invalid input. Please enter numbers only.")
                continue

            if choice == '1':
                print(num1, "+", num2, "=", add(num1, num2))
            elif choice == '2':
                print(num1, "-", num2, "=", subtract(num1, num2))
            elif choice == '3':
                print(num1, "*", num2, "=", multiply(num1, num2))
            elif choice == '4':
                print(num1, "/", num2, "=", divide(num1, num2))

            next_calculation = input("Let's do next calculation? (yes/no): ")
            if next_calculation.lower() == "no":
                break
        else:
            print("Invalid Input")

if __name__ == "__main__":
    if sys.argv[1:]: # Check if command-line arguments are provided
        try:
            num1 = float(sys.argv[1])
            operator = sys.argv[2]
            num2 = float(sys.argv[3])

            if operator == '+':
                print(add(num1, num2))
            elif operator == '-':
                print(subtract(num1, num2))
            elif operator == '*':
                print(multiply(num1, num2))
            elif operator == '/':
                print(divide(num1, num2))
            else:
                print("Invalid operator.")
        except (ValueError, IndexError):
            print("Usage: python calculator.py <number1> <operator> <number2>")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        main()
