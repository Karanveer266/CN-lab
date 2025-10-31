# File Name: scheduler.py
# Implements Part 3 of the Computer Networks Lab assignment.

from dataclasses import dataclass

# 1. Class: Packet [cite: 65]
# Using a dataclass is a clean, modern way to
# implement this simple data container.
@dataclass
class Packet:
    """
    A simple class to represent a network packet.
    """
    source_ip: str   # [cite: 67]
    dest_ip: str     # [cite: 68]
    payload: str     # [cite: 69]
    priority: int    # [cite: 70] (0=High, 1=Medium, 2=Low)

# 2. Function: fifo_scheduler [cite: 71]
def fifo_scheduler(packet_list: list) -> list:
    """
    Simulates a First-Come, First-Served (FCFS/FIFO) scheduler.
    
    Input: A list of Packet objects in the order they arrived. [cite: 73]
    Output: A new list of Packet objects in the order they would be sent. [cite: 74]
    """
    # Since the input list is already in arrival order,
    # a FIFO scheduler will process them in that exact order.
    # We return a copy to avoid modifying the original list by accident.
    return packet_list.copy()

# 3. Function: priority_scheduler [cite: 76]
def priority_scheduler(packet_list: list) -> list:
    """
    Simulates a Priority Scheduler.
    
    Input: A list of Packet objects that have arrived at the queue. [cite: 78]
    Output: A new list of Packet objects, ordered by priority (lower number first). [cite: 79-80]
    """
    # We can use Python's built-in `sorted` function.
    # We provide a `key` to tell `sorted` to use the 'priority'
    # attribute of each Packet object for comparison.
    # The default sort is ascending (0, 1, 2), which is exactly
    # what we need for (High, Medium, Low) priority.
    return sorted(packet_list, key=lambda packet: packet.priority)


# --- Main execution block for testing --- [cite: 84]
if __name__ == "__main__":
    
    print("--- Testing Part 3: scheduler.py ---")

    # 1. Create the list of Packet objects in their arrival order [cite: 85]
    # (Using dummy IPs as they are not specified for the test)
    
    p1 = Packet(source_ip="10.1.1.2", dest_ip="192.168.1.10", 
                payload="Data Packet 1", priority=2) # [cite: 87] Priority Low
                
    p2 = Packet(source_ip="10.1.1.3", dest_ip="192.168.1.11", 
                payload="Data Packet 2", priority=2) # [cite: 89] Priority Low
                
    p3 = Packet(source_ip="172.16.0.5", dest_ip="192.168.1.12", 
                payload="VOIP Packet 1", priority=0) # [cite: 91] Priority High
                
    p4 = Packet(source_ip="10.1.1.4", dest_ip="192.168.1.13", 
                payload="Video Packet 1", priority=1) # [cite: 93] Priority Medium
                
    p5 = Packet(source_ip="172.16.0.6", dest_ip="192.168.1.14", 
                payload="VOIP Packet 2", priority=0) # [cite: 94] Priority High

    # This is the list in arrival order
    arrival_list = [p1, p2, p3, p4, p5]
    
    print("\n--- Testing FIFO Scheduler ---")
    print("Arrival Order:\t [Data 1 (P2), Data 2 (P2), VOIP 1 (P0), Video 1 (P1), VOIP 2 (P0)]")
    
    # Run the FIFO scheduler
    fifo_result = fifo_scheduler(arrival_list)
    
    # Get just the payloads for easy verification
    fifo_payloads = [p.payload for p in fifo_result]
    
    print(f"FIFO Send Order: {fifo_payloads}")
    
    # Verify the result [cite: 96-97]
    expected_fifo = ["Data Packet 1", "Data Packet 2", "VOIP Packet 1", "Video Packet 1", "VOIP Packet 2"]
    print(f"Test Passed:     {fifo_payloads == expected_fifo}")


    print("\n--- Testing Priority Scheduler ---")
    print("Arrival Order:\t [Data 1 (P2), Data 2 (P2), VOIP 1 (P0), Video 1 (P1), VOIP 2 (P0)]")
    
    # Run the Priority scheduler
    priority_result = priority_scheduler(arrival_list)
    
    # Get just the payloads for easy verification
    priority_payloads = [p.payload for p in priority_result]
    
    print(f"Priority Send Order: {priority_payloads}")
    
    # Verify the result [cite: 99-101]
    # Note: Both VOIP packets have P0. The sort algorithm is "stable",
    # meaning it keeps them in their original relative order (VOIP 1, then VOIP 2).
    expected_priority = ["VOIP Packet 1", "VOIP Packet 2", "Video Packet 1", "Data Packet 1", "Data Packet 2"]
    print(f"Test Passed:         {priority_payloads == expected_priority}")