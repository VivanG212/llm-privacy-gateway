import time
from redactor import PrivacyRedactor

# Initialize the redactor
redactor = PrivacyRedactor()

# Synthetic test dataset with expected entities
TEST_DATASET = [
    {
        "input": "Sarah Connor called from Los Angeles regarding the $500,000 transfer to Cyberdyne Systems on October 12th.",
        "expected_entities": ["Sarah Connor", "Los Angeles", "$500,000", "Cyberdyne Systems", "October 12th"]
    },
    {
        "input": "Contact Tony Stark at Stark Industries in New York before December 1st.",
        "expected_entities": ["Tony Stark", "Stark Industries", "New York", "December 1st"]
    },
    {
        "input": "Schedule a meeting with Alice Johnson at Google headquarters in Mountain View.",
        "expected_entities": ["Alice Johnson", "Google", "Mountain View"]
    }
]

def run_benchmark():
    print("=== DOOM PRIVACY GATEWAY: EXPERIMENTAL EVALUATION ===")
    total_time_ms = 0
    total_expected = 0
    total_detected = 0

    for idx, item in enumerate(TEST_DATASET, 1):
        raw_text = item["input"]
        expected = item["expected_entities"]
        
        # Measure processing speed
        start_time = time.perf_counter()
        sanitized, vault = redactor.sanitize(raw_text)
        end_time = time.perf_counter()
        
        latency_ms = (end_time - start_time) * 1000
        total_time_ms += latency_ms
        
        detected_values = list(vault.values())
        total_expected += len(expected)
        total_detected += len(detected_values)
        
        print(f"\n--- Test Sample {idx} ---")
        print(f"Raw Input:       {raw_text}")
        print(f"Sanitized Text:  {sanitized}")
        print(f"Vault Contents:  {vault}")
        print(f"Execution Speed: {latency_ms:.2f} ms")

    avg_latency = total_time_ms / len(TEST_DATASET)
    recall_rate = (total_detected / total_expected) * 100

    print("\n================ BENCHMARK METRICS SUMMARY ================")
    print(f"Total Test Cases Processed: {len(TEST_DATASET)}")
    print(f"Average Processing Latency: {avg_latency:.2f} ms")
    print(f"Entity Detection Recall:    {recall_rate:.1f}%")
    print("===========================================================")

if __name__ == "__main__":
    run_benchmark()
