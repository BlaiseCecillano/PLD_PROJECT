def search(numbers, target):
    count = numbers.count(target)
    

    if count > 0:
        return count
    else:
        return "NO SUCH NUMBER!"
print("NUMBER OCCURENCE SEARCH")
def main():
    numbers = []
    
    
    while True:
        num = int(input("Enter a number (enter 0 or a negative number to stop): "))
        
        if num <= 0:
            break
        
        numbers.append(num)
    
    while True:
    
        target = int(input("Search for number: "))
        
        result = search(numbers, target)
        #TEST
    
        if isinstance(result, int):
            print(f"The number {target} occurred {result} time(s).")
        else:
            print(result)
        
        try_again = input("Would you like to try another number? (y/n): ").strip().lower()
        if try_again != 'y':
            print("Goodbye!")
            break  


if __name__ == "__main__":
    main()
