import subprocess
import json
import re

def run_ab_and_extract_codes():
    post_data = {"original_url": "https://www.example.com/test/performance/load"}
    with open("post_data.json", "w") as f:
        json.dump(post_data, f)

    command = [
        "ab",
        "-n", "100",
        "-c", "10",
        "-p", "post_data.json",
        "-T", "application/json",
        "-v","4",
        "http://127.0.0.1:8000/urls/"
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    output = stdout.decode()
    print(output)
    # json_responses = [line.strip() for line in output.split('\n') if line.startswith('{')] #Find all lines that start with a curly brace.
    # print(json_responses)
    short_urls = []
    with open("../django.log", "r") as f:  # Go up one directory to the project root
        for line in f:
            if "short_url" in line and "INFO shortener.views" in line:
                try:
                    json_start_index = line.find('{')
                    if json_start_index != -1:
                        json_string = line[json_start_index:].strip()
                        # print(type(json_string))
                        response_json = json.loads(json_string)
                        short_urls.append(response_json["short_url"])
                    else:
                        print(f"Error: Could not find JSON start in log line: {line.strip()}")
                except json.JSONDecodeError as e:  # Capture the JSONDecodeError as 'e'
                    print(f"Error parsing JSON: {line.strip()} - {e}")
                except KeyError as e:  # Capture the KeyError as 'e'
                    print(f"Error: 'short_url' key not found in JSON: {line.strip()} - {e}")
    # for response_str in json_responses:
    #     try:
    #         response_json = json.loads(response_str)
    #         # print("In try")
    #         # print(response_json)
    #         short_codes.append(response_json["short_url"])
    #     except (json.JSONDecodeError, KeyError):
    #         print(f"Error parsing JSON: {response_str}")

    requests_per_second = re.search(r"Requests per second:\s+([\d.]+)", output).group(1)
    time_per_request = re.search(r"Time per request:\s+([\d.]+)\s+\[ms\]", output).group(1)
    failed_requests = re.search(r"Failed requests:\s+([\d]+)", output).group(1)

    return short_urls, requests_per_second, time_per_request, failed_requests

if __name__ == "__main__":
    short_codes, requests_per_second, time_per_request, failed_requests = run_ab_and_extract_codes()

    # print("Extracted Short Urls:")
    with open ("short_Urls.txt","a") as f:
        for code in short_codes:
            # print(code)
            f.write(code + "\n")

    print("\nPerformance Metrics:")
    print(f"Requests per second: {requests_per_second}")
    print(f"Time per request: {time_per_request} ms")
    print(f"Failed requests: {failed_requests}")
    with open("Performance Metrics.txt","a") as pm:
        pm.write("While creating short URLS:\n")
        pm.write("Requests per second:"+requests_per_second+"\n")
        pm.write("Time per request:"+time_per_request+"\n")
        pm.write("Failed requests:"+failed_requests+"\n")