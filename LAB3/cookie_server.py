import socket
import threading
import random
import time

# Server configuration
HOST = '127.0.0.1'
PORT = 8080

# Dictionary to store active sessions by cookie value
sessions = {}

def generate_user_id():
    """Generate a unique user ID for new visitors"""
    return f"User{random.randint(1000, 9999)}"

def parse_http_request(request):
    """Parse HTTP request and extract headers"""
    lines = request.split('\r\n')
    request_line = lines[0] if lines else ""
    
    headers = {}
    for line in lines[1:]:
        if line == '':  # Empty line marks end of headers
            break
        if ': ' in line:
            key, value = line.split(': ', 1)
            headers[key] = value
    
    return request_line, headers

def extract_cookie_value(cookie_header, cookie_name):
    """Extract specific cookie value from Cookie header"""
    for cookie in cookie_header.split('; '):
        if cookie.startswith(f'{cookie_name}='):
            return cookie.split('=', 1)[1]
    return None

def create_http_response(status, headers, body):
    """Create properly formatted HTTP response"""
    response_lines = [status]
    for header_name, header_value in headers.items():
        response_lines.append(f"{header_name}: {header_value}")
    response_lines.append('')  # Empty line before body
    response_lines.append(body)
    return '\r\n'.join(response_lines)

def handle_client(conn, addr):
    """Handle individual client connection"""
    print(f"New connection from {addr}")
    
    try:
        # Receive and decode HTTP request
        request = conn.recv(4096).decode('utf-8')
        print(f"Request from {addr}:\n{request}")
        
        # Parse the HTTP request
        request_line, headers = parse_http_request(request)
        
        # Check for existing cookie
        cookie_value = None
        if 'Cookie' in headers:
            cookie_value = extract_cookie_value(headers['Cookie'], 'user')
            print(f"Found cookie: user={cookie_value}")
        
        # Determine if this is a new or returning visitor
        if cookie_value and cookie_value in sessions:
            # Returning visitor
            print(f"Returning visitor: {cookie_value}")
            
            html_body = f"""
            <html>
            <head><title>Welcome Back!</title></head>
            <body>
                <h1>Welcome back, {cookie_value}!</h1>
                <p>We remember you from your previous visit.</p>
                <p>Your session is active.</p>
                <hr>
                <small>This is a cookie-based session management demo</small>
            </body>
            </html>
            """
            
            response_headers = {
                'Content-Type': 'text/html; charset=utf-8',
                'Content-Length': str(len(html_body)),
                'Set-Cookie': f'user={cookie_value}; Path=/',  # Refresh cookie
                'Connection': 'close'
            }
            
            response = create_http_response('HTTP/1.1 200 OK', response_headers, html_body)
            
        else:
            # First-time visitor
            new_user_id = generate_user_id()
            sessions[new_user_id] = {
                'created': time.time(),
                'last_seen': time.time()
            }
            
            print(f"New visitor assigned ID: {new_user_id}")
            
            html_body = f"""
            <html>
            <head><title>Welcome New User!</title></head>
            <body>
                <h1>Welcome, new user {new_user_id}!</h1>
                <p>This is your first visit to our server.</p>
                <p>We've created a session for you using cookies.</p>
                <p>Refresh the page to see the returning visitor experience.</p>
                <hr>
                <small>This is a cookie-based session management demo</small>
            </body>
            </html>
            """
            
            response_headers = {
                'Content-Type': 'text/html; charset=utf-8',
                'Content-Length': str(len(html_body)),
                'Set-Cookie': f'user={new_user_id}; Path=/',  # Set new cookie
                'Connection': 'close'
            }
            
            response = create_http_response('HTTP/1.1 200 OK', response_headers, html_body)
        
        # Send response back to client
        conn.sendall(response.encode('utf-8'))
        print(f"Response sent to {addr}")
        
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
        # Send error response
        error_body = "<html><body><h1>500 Internal Server Error</h1></body></html>"
        error_headers = {
            'Content-Type': 'text/html',
            'Content-Length': str(len(error_body)),
            'Connection': 'close'
        }
        error_response = create_http_response('HTTP/1.1 500 Internal Server Error', error_headers, error_body)
        try:
            conn.sendall(error_response.encode('utf-8'))
        except:
            pass
    finally:
        conn.close()

def run_server():
    """Main server loop"""
    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind and listen
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        
        print(f"HTTP Server running on http://{HOST}:{PORT}")
        print("Press Ctrl+C to stop the server")
        print(f"Active sessions: {len(sessions)}")
        
        while True:
            # Accept new connection
            client_conn, client_addr = server_socket.accept()
            
            # Handle each client in a separate thread
            client_thread = threading.Thread(
                target=handle_client, 
                args=(client_conn, client_addr)
            )
            client_thread.daemon = True  # Thread dies when main program exits
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()
        print("Server stopped.")

# Additional utility function to view active sessions
def show_sessions():
    """Display all active sessions"""
    print(f"\nActive Sessions ({len(sessions)}):")
    for user_id, session_data in sessions.items():
        if isinstance(session_data, dict):
            created = time.ctime(session_data['created'])
            print(f"  {user_id}: Created at {created}")
        else:
            print(f"  {user_id}: Simple session")

if __name__ == "__main__":
    print("Cookie Management HTTP Server")
    print("============================")
    run_server()
