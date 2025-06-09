from hdfs import InsecureClient
import time
import sys
import requests

def wait_for_hdfs(max_retries=10, delay=15):
    """Wait for HDFS to be ready by checking the web interface"""
    for attempt in range(max_retries):
        try:
            response = requests.get('http://namenode:9870', timeout=10)
            if response.status_code == 200:
                print(f"HDFS is ready after {attempt + 1} attempts")
                return True
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries}: HDFS not ready yet ({e})")
            time.sleep(delay)
    
    print("HDFS failed to become ready")
    return False

def test_hdfs_operations():
    # Connect to HDFS
    try:
        client = InsecureClient('http://namenode:9870', user='root')
        print("Connected to HDFS successfully!")
        
        # Test write operation
        test_file_path = '/test_file.txt'
        test_content = "Hello HDFS! This is a test file created by Python client."
        
        print(f"Writing to {test_file_path}...")
        with client.write(test_file_path, encoding='utf-8') as writer:
            writer.write(test_content)
        print("Write operation completed successfully!")
        
        # Test read operation
        print(f"Reading from {test_file_path}...")
        with client.read(test_file_path, encoding='utf-8') as reader:
            read_content = reader.read()
        print(f"Read content: {read_content}")
        
        # List files in root directory
        print("Listing files in root directory:")
        files = client.list('/')
        for file in files:
            print(f"  {file}")
            
        # Get file status
        file_status = client.status(test_file_path)
        print(f"File status: {file_status}")
        
        # Test directory operations
        test_dir = '/test_directory'
        print(f"Creating directory {test_dir}...")
        client.makedirs(test_dir)
        
        # Write a file in the directory
        dir_file_path = f"{test_dir}/nested_file.txt"
        with client.write(dir_file_path, encoding='utf-8') as writer:
            writer.write("This is a nested file in HDFS directory.")
        
        # List contents of the directory
        print(f"Contents of {test_dir}:")
        dir_contents = client.list(test_dir)
        for item in dir_contents:
            print(f"  {item}")
        
        print("All HDFS operations completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    print("Waiting for HDFS to be ready...")
    if wait_for_hdfs():
        test_hdfs_operations()
    else:
        print("Failed to connect to HDFS")
        sys.exit(1)
