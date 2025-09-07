import dns.resolver
import logging


logging.basicConfig(
    filename='dns_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filemode='w'
)

def query_dns_records(domain):
   
    print(f"Querying DNS records for: {domain} ")
    logging.info(f"Querying DNS records for: {domain} ")
    
    record_types = ['A', 'MX', 'CNAME']
    
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            
            message = f"Found {len(answers)} {rtype} record(s):"
            print(f"\n{message}")
            logging.info(message)
            
            for record in answers:
                record_text = f"  -> {record.to_text()}"
                print(record_text)
                logging.info(record_text)
                
        except dns.resolver.NoAnswer:
            message = f"  No {rtype} records found."
            print(f"\n{message}")
            logging.info(message)
        except dns.resolver.NXDOMAIN:
            message = f"  The domain '{domain}' does not exist (NXDOMAIN)."
            print(f"\n{message}")
            logging.error(message)
            break 
        except Exception as e:
            message = f"  An unexpected error occurred: {e}"
            print(f"\n{message}")
            logging.error(message)

if __name__ == "__main__":
    query_dns_records("iitp.ac.in")
    print("\n" + "="*50)
    query_dns_records("google.com")
    print("\n" + "="*50)
    query_dns_records("mail.google.com")
    print("\n" + "="*50)
    query_dns_records("this-domain-does-not-exist-12345.com")