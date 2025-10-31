# File Name: router.py
# Implements Part 2 of the Computer Networks Lab assignment.

# We must import the helper functions from Part 1
try:
    from ip_utils import ip_to_binary, get_network_prefix
except ImportError:
    print("\n--- ERROR ---")
    print("Could not find 'ip_utils.py' in the same directory.")
    print("Please make sure 'ip_utils.py' is present before running 'router.py'.")
    print("-------------\n")
    exit()

class Router:
    """
    Implements a router with a forwarding table that uses the
    Longest Prefix Match (LPM) algorithm.
    """
    def __init__(self, routes: list):
        """
        Initializes the router with a list of routes.
        
        Args:
            routes (list): A list of tuples, where each tuple contains
                           a CIDR prefix string and an output link string.
                           e.g., [("223.1.1.0/24", "Link 0"), ...]
        """
        # This list will store our "optimized" forwarding table
        self.forwarding_table = []
        
        # Call the helper method to process the routes as required [cite: 34]
        self._build_forwarding_table(routes)

    def _build_forwarding_table(self, routes: list):
        """
        A private method to process the human-readable routes list into
        an internal format optimized for LPM.
        
        The internal table will store tuples of:
        (binary_prefix, prefix_length, output_link)
        """
        print("Building forwarding table...")
        temp_table = []
        for (cidr_prefix, output_link) in routes:
            # 1. Convert the CIDR prefix (e.g., "223.1.1.0/24") into
            #    its binary prefix (e.g., "110111110000000100000001") [cite: 38]
            binary_prefix = get_network_prefix(cidr_prefix)
            
            # 2. Get the length of that binary prefix (e.g., 24)
            prefix_length = len(binary_prefix)
            
            # 3. Store this processed information
            temp_table.append((binary_prefix, prefix_length, output_link))
        
        # 4. **CRUCIAL HINT:** Sort the table by prefix length in
        #    DESCENDING order (longest to shortest).
        #    We use a lambda function to tell `sorted` to use the
        #    second element of our tuple (prefix_length) as the sort key.
        self.forwarding_table = sorted(temp_table, 
                                       key=lambda item: item[1], 
                                       reverse=True)
        print("Forwarding table built and sorted.")

    def route_packet(self, dest_ip: str) -> str:
        """
        Performs the Longest Prefix Match algorithm to find the
        correct output link for a given destination IP.
        
        Args:
            dest_ip (str): The destination IP address (e.g., "223.1.1.100")
            
        Returns:
            str: The corresponding output link string or a default route.
        """
        
        # (a) Convert the destination IP to its 32-bit binary representation [cite: 44]
        binary_dest_ip = ip_to_binary(dest_ip)
        
        # (b) Iterate through the sorted internal forwarding table [cite: 45]
        for (binary_prefix, prefix_len, output_link) in self.forwarding_table:
            
            # (c) Check if the binary destination IP *starts with* the binary prefix [cite: 46]
            #     This is the core prefix match logic.
            if binary_dest_ip.startswith(binary_prefix):
                
                # (d) The first match IS the longest match because we sorted the table.
                #     Return the corresponding output link immediately. [cite: 47, 48]
                return output_link
                
        # (e) If the loop finishes with no matches, return the default route [cite: 49]
        return "Default Gateway"


# --- Main execution block for testing ---
if __name__ == "__main__":
    
    print("--- Testing Part 2: router.py ---")

    # 1. Define the routes for the test case [cite: 50-52]
    routes_list = [
        ("223.1.1.0/24", "Link 0"),
        ("223.1.2.0/24", "Link 1"),
        ("223.1.3.0/24", "Link 2"),
        ("223.1.0.0/16", "Link 4 (ISP)")
    ]
    
    # 2. Initialize the Router
    my_router = Router(routes_list)

    # (Optional) Print the sorted internal table to verify the hint
    print("\n--- Internal Forwarding Table (Sorted Longest-to-Shortest) ---")
    for (prefix, length, link) in my_router.forwarding_table:
        print(f"  Prefix: {prefix:<24} (Len: {length}) -> {link}")
    print("---------------------------------------------------------------")

    # 3. Verify the test cases [cite: 53]
    
    print("\n--- Running Routing Tests ---")
    
    # Test 1: Should match "223.1.1.0/24"
    ip_1 = "223.1.1.100"
    link_1 = my_router.route_packet(ip_1)
    print(f"Routing '{ip_1}':\t -> {link_1} \t(Expected: Link 0)") # [cite: 54]

    # Test 2: Should match "223.1.2.0/24"
    ip_2 = "223.1.2.5"
    link_2 = my_router.route_packet(ip_2)
    print(f"Routing '{ip_2}':\t\t -> {link_2} \t(Expected: Link 1)") # [cite: 57]
    
    # Test 3: Should fail /24 matches, but match "223.1.0.0/16"
    ip_3 = "223.1.250.1"
    link_3 = my_router.route_packet(ip_3)
    print(f"Routing '{ip_3}':\t -> {link_3} \t(Expected: Link 4 (ISP))") # [cite: 58]

    # Test 4: Should match nothing
    ip_4 = "198.51.100.1"
    link_4 = my_router.route_packet(ip_4)
    print(f"Routing '{ip_4}':\t -> {link_4} (Expected: Default Gateway)") # [cite: 59]