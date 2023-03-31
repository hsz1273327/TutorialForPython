
import sys

def main():
    print("你是谁?")
    sys.stdin.readline()
    while True:
        line = sys.stdin.readline() 
        if not line: 
            break 
        who = line.strip()
        print(f"hello world {who}!")
        
    
if __name__ == "__main__":
    main()
