import os
import subprocess
import sys
import time
import webbrowser
import signal
from pathlib import Path
from datetime import datetime

class ServerManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.project_root = Path(__file__).parent
        self.log_file = self.project_root / 'server.log'

    def log_message(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        print(message)
        with open(self.log_file, 'a') as f:
            f.write(log_entry)

    def check_requirements(self):
        """Check if all required software is installed"""
        try:
            # Check Python version
            python_version = sys.version_info
            if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
                raise RuntimeError("Python 3.8 or higher is required")

            # Check Node.js installation
            npm_cmd = 'npm.cmd' if sys.platform.startswith('win') else 'npm'
            subprocess.run([npm_cmd, '--version'], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE,
                         check=True)

            # Check if virtual environment exists
            venv_path = self.project_root / 'backend' / 'venv'
            if not venv_path.exists():
                raise RuntimeError("Virtual environment not found. Please set up the backend first.")

            return True
        except subprocess.CalledProcessError:
            self.log_message("Error: Node.js and npm are required but not found.")
            return False
        except Exception as e:
            self.log_message(f"Error during requirements check: {str(e)}")
            return False

    def get_python_venv_path(self):
        if sys.platform.startswith('win'):
            return str(self.project_root / 'backend' / 'venv' / 'Scripts' / 'python.exe')
        return str(self.project_root / 'backend' / 'venv' / 'bin' / 'python')

    def get_npm_command(self):
        return 'npm.cmd' if sys.platform.startswith('win') else 'npm'

    def start_backend(self):
        self.log_message("Starting Django backend server...")
        python_path = self.get_python_venv_path()
        
        try:
            # Check if port 8000 is available
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if sock.connect_ex(('localhost', 8000)) == 0:
                self.log_message("Error: Port 8000 is already in use. Please stop any running Django servers.")
                return False
            
            # Apply migrations
            subprocess.run([python_path, 'backend/manage.py', 'migrate'], 
                         check=True,
                         cwd=self.project_root)
            
            # Start Django server
            self.backend_process = subprocess.Popen(
                [python_path, 'backend/manage.py', 'runserver'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                cwd=self.project_root
            )
            return True
        except Exception as e:
            self.log_message(f"Error starting backend: {str(e)}")
            return False
        finally:
            sock.close()

    def start_frontend(self):
        self.log_message("Starting React frontend server...")
        npm = self.get_npm_command()
        frontend_path = self.project_root / 'frontend'
        
        try:
            # Check if port 3000 is available
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if sock.connect_ex(('localhost', 3000)) == 0:
                self.log_message("Error: Port 3000 is already in use. Please stop any running React servers.")
                return False

            # Install dependencies if needed
            if not (frontend_path / 'node_modules').exists():
                self.log_message("Installing frontend dependencies...")
                subprocess.run([npm, 'install'], 
                             cwd=frontend_path, 
                             check=True)
            
            # Start React development server
            self.frontend_process = subprocess.Popen(
                [npm, 'start'],
                cwd=frontend_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            return True
        except Exception as e:
            self.log_message(f"Error starting frontend: {str(e)}")
            return False
        finally:
            sock.close()

    def stop_servers(self):
        self.log_message("Shutting down servers...")
        
        if self.backend_process:
            if sys.platform.startswith('win'):
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.backend_process.pid)])
            else:
                os.killpg(os.getpgid(self.backend_process.pid), signal.SIGTERM)
        
        if self.frontend_process:
            if sys.platform.startswith('win'):
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.frontend_process.pid)])
            else:
                os.killpg(os.getpgid(self.frontend_process.pid), signal.SIGTERM)

    def run(self):
        os.chdir(self.project_root)
        
        if not self.check_requirements():
            return
        
        try:
            if not self.start_backend():
                return
            self.log_message("Backend server started at http://localhost:8000")
            
            time.sleep(2)  # Wait for backend to initialize
            
            if not self.start_frontend():
                self.stop_servers()
                return
            self.log_message("Frontend server started at http://localhost:3000")
            
            # Open the frontend in the default browser
            webbrowser.open('http://localhost:3000')
            
            self.log_message("\nPress Ctrl+C to stop both servers...")
            
            while True:
                if self.backend_process.poll() is not None:
                    self.log_message("Backend server stopped unexpectedly!")
                    break
                if self.frontend_process.poll() is not None:
                    self.log_message("Frontend server stopped unexpectedly!")
                    break
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.log_message("\nReceived shutdown signal...")
        except Exception as e:
            self.log_message(f"An error occurred: {str(e)}")
        finally:
            self.stop_servers()
            self.log_message("Servers stopped.")

def main():
    manager = ServerManager()
    manager.run()

if __name__ == "__main__":
    main() 