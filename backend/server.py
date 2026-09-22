import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

from db import(
    create_task,
    get_all_tasks,
    get_task,
    mark_completed,
    delete_task
)

# ================================================================================================
#Helpers
# ================================================================================================

def task_to_dict(task):
    """تبدیل یک ردیف دیتابیس به دیکشنری قابل تبدیل به json"""
    if not task:
        return None
    task_id, title, description, completed,created_at = task
    return {
        'id': task_id,
        'title': title,
        'description': description,
        'completed': completed,
        'created_at': created_at.isoformat() if created_at else None
    }

# ================================================================================================
#HTTP Request handler
# ================================================================================================

class TaskApiHandler(BaseHTTPRequestHandler):
    # ========================
    # Utils
    # ========================
    def send_json(self, data, status=200):
        """یک پاسخ جسشون میفرستد"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def read_body(self):
        """بدنه request را میخواند و به دیکشنری تبدیل میکند"""
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return {}
        body = self.rfile.read(length)
        try:
            return json.loads(body.decode('utf-8'))
        except json.JSONDecodeError:
            return {}

    def log_message(self, format, *args):
        """لاگ های http را قشنگتر نشون بده"""
        print(f"[{self.command}] {self.path} -> {args[1]} ")

    # ==================================
    # GET
    # ==================================

    def do_GET(self):
        # GET/tasks
        if self.path == '/tasks':
            tasks = get_all_tasks()
            data = [task_to_dict(t) for t in tasks]
            self.send_json(data)
            return

        #GET/tasks/{id}
        match = re.match(r'^/tasks/(\d+)$', self.path)
        if match:
            task_id = int(match.group(1))
            task = get_task(task_id)
            if task:
                self.send_json(task_to_dict(task))
            else:
                self.send_json({"error": "task not found"})
            return

        # مسیر ناشناخته
        self.send_json({"error": "not found"}, 404)

    # ---------------------------------------
    # POST
    # ---------------------------------------

    def do_POST(self):
        # POST/tasks
        if self.path == '/tasks':
            body = self.read_body()
            title = body.get('title', "").strip()
            description = body.get('description', "").strip()

            if not title:
                self.send_json({"error": "title is required"}, 400)
                return

            task_id = create_task(title, description)
            task = get_task(task_id)
            self.send_json(task_to_dict(task), 201)
            return

        self.send_json({"error": "not found"}, 404)

    #----------------------------------------------
    # PUT
    #----------------------------------------------

    def do_PUT(self):
        # PUT/tasks/{id}/complete
        match = re.match(r"^/tasks/(\d+)/complete$", self.path)
        if match:
            task_id = int(match.group(1))
            task = get_task(task_id)
            if not task:
                self.send_json({"error": "task not found"}, 404)
                return

            mark_completed(task_id)
            task = get_task(task_id)
            self.send_json(task_to_dict(task))
            return
        self.send_json({"error": "not found"}, 404)

    #-------------------------------------------------
    # DELETE
    #-------------------------------------------------

    def do_DELETE(self):
        match = re.match(r"^/tasks/(\d+)$", self.path)
        if match:
            task_id = int(match.group(1))
            task = get_task(task_id)
            if not task:
                self.send_json({"error": "task not found"}, 404)
                return

            delete_task(task_id)
            self.send_json({"message": "Task deleted"}, 200)
            return
        self.send_json({"error": "not found"}, 404)

    def do_OPTIONS(self):
        """پاسخ به preflight request برای cors"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'content-type')
        self.end_headers()
    #---------------------------------------------------------
    # Run Server
    #---------------------------------------------------------

def run_server(port=8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, TaskApiHandler)
    print(f"sever running on http://localhost:{port}")
    print(f"test: http://localhost:{port}/tasks")
    print(" press ctrl-c to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("server stopped")
        httpd.server_close()


if __name__ == "__main__":
    run_server()