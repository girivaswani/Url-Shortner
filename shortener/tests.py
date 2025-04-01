# from django.test import TestCase
# import json


# # Create your tests here.
# def get_Urls():
#     short_urls=[]
#     with open("../django.log", "r") as f:  # Go up one directory to the project root
#         for line in f:
#             if "short_url" in line and "INFO shortener.views" in line:
#                 try:
#                     json_start_index = line.find('{')
#                     if json_start_index != -1:
#                         json_string = line[json_start_index:].strip()
#                         # print(type(json_string))
#                         response_json = json.loads(json_string)
#                         short_urls.append(response_json["short_url"])
#                     else:
#                         print(f"Error: Could not find JSON start in log line: {line.strip()}")
#                 except json.JSONDecodeError as e:  # Capture the JSONDecodeError as 'e'
#                     print(f"Error parsing JSON: {line.strip()} - {e}")
#                 except KeyError as e:  # Capture the KeyError as 'e'
#                     print(f"Error: 'short_url' key not found in JSON: {line.strip()} - {e}")

#     return short_urls
# if __name__=="__main__":
#     short_urls=get_Urls()
#     print(len(short_urls))


import subprocess
import json
import re

def parse_django_log_and_get_short_urls():
    short_urls = []
    with open("../django.log", "r") as f:
        for line in f:
            if "short_url" in line and "INFO shortener.views" in line:
                try:
                    json_start_index = line.find('{')
                    if json_start_index != -1:
                        json_string = line[json_start_index:].strip()
                        response_json = json.loads(json_string)
                        short_urls.append(response_json["short_url"])
                except (json.JSONDecodeError, KeyError):
                    pass
    return short_urls

def run_ab_redirection_test(short_url):
    command = [
        "ab",
        "-n", "100",
        "-c", "10",
        short_url
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    output = stdout.decode()
    requests_per_second = re.search(r"Requests per second:\s+([\d.]+)", output).group(1)
    time_per_request = re.search(r"Time per request:\s+([\d.]+)\s+\[ms\]", output).group(1)
    failed_requests = re.search(r"Failed requests:\s+([\d]+)", output).group(1)
    return requests_per_second, time_per_request, failed_requests

if __name__ == "__main__":
    short_urls = parse_django_log_and_get_short_urls()

    if short_urls:
        print("\nPerformance Metrics for Redirection:")
        total_rps = 0
        total_time_per_request = 0
        total_failed = 0

        for short_url in short_urls[:25]:  # Test with the first few short URLs
            rps, tpr, fr = run_ab_redirection_test(short_url)
            print(f"\nTesting redirection for: {short_url}")
            print(f"  Requests per second: {rps}")
            print(f"  Time per request: {tpr} ms")
            print(f"  Failed requests: {fr}")
            total_rps += float(rps)
            total_time_per_request += float(tpr)
            total_failed += int(fr)

        avg_rps = total_rps / len(short_urls[:25])
        avg_tpr = total_time_per_request / len(short_urls[:25])

        print("\nAverage Redirection Performance:")
        print(f"  Average Requests per second: {avg_rps:.2f}")
        print(f"  Average Time per request: {avg_tpr:.2f} ms")
        print(f"  Total Failed requests: {total_failed}")
    else:
        print("No short URLs found in django.log to test redirection.")

