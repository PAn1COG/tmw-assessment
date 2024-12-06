import time
import json
import sys

def count_alphabets(file_content):
    return sum(char.isalpha() for char in file_content)

if __name__ == "__main__":
    try:
        # Read arguments
        input_data = json.loads(sys.argv[1])
        file_content = input_data.get("file_content", "")

        # Simulate delay
        time.sleep(15)  

        # Count
        result = count_alphabets(file_content)

        # Return result as JSON
        print(json.dumps({"status": "completed", "result": result}))
    except Exception as e:
        print(json.dumps({"status": "error", "result": None, "error": str(e)}))
