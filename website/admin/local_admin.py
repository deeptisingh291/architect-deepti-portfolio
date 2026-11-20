#!/usr/bin/env python3
"""
LOCAL ARCHITECTURAL PORTFOLIO ADMIN & PROJECT MANAGER
For Ar. Deepti Singh Portfolio
Run locally on Mac: python3 website/admin/local_admin.py
"""

import http.server
import socketserver
import json
import os
import shutil
import urllib.parse
from PIL import Image

PORT = 9000
DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/projects.json')
JS_DATA_FILE = os.path.join(os.path.dirname(__file__), '../js/data.js')
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '../assets/projects')

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Local Portfolio Manager &bull; Ar. Deepti Singh</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=Cinzel:wght@700&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; background: #0a0a0c; color: #f5f5f7; }
    .gold-border { border-color: rgba(197, 168, 128, 0.4); }
  </style>
</head>
<body class="p-6 sm:p-10 max-w-6xl mx-auto">
  
  <!-- Header -->
  <header class="flex flex-col sm:flex-row justify-between items-start sm:items-center pb-8 border-b border-white/10 gap-4">
    <div>
      <div class="text-xs font-mono text-[#c5a880] uppercase tracking-wider">LOCAL PORTFOLIO CONTROL PANEL</div>
      <h1 class="text-3xl font-bold font-['Cinzel'] text-white mt-1">Ar. Deepti Singh &bull; Project Manager</h1>
      <p class="text-xs text-zinc-400 mt-1">Upload new projects, edit specifications, and manage portfolio renders without coding.</p>
    </div>
    <div class="flex items-center gap-3">
      <a href="http://localhost:8080" target="_blank" class="px-4 py-2 bg-[#16161c] border border-white/20 text-xs rounded hover:border-[#c5a880] transition-colors">
        View Live Website &rarr;
      </a>
      <button onclick="openNewModal()" class="px-5 py-2.5 bg-[#c5a880] text-black font-semibold text-xs tracking-wider uppercase rounded hover:bg-[#dfc8a5] transition-colors">
        + Add New Project
      </button>
    </div>
  </header>

  <!-- Flash Notice -->
  <div id="notice" class="hidden mt-6 p-4 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-mono"></div>

  <!-- Projects List -->
  <main class="mt-10">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-lg font-bold text-white">Current Projects in Portfolio (<span id="count">0</span>)</h2>
      <div class="text-xs text-zinc-500 font-mono">Real-time sync with projects.json & data.js</div>
    </div>

    <div id="project-list" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Loaded dynamically via JavaScript -->
    </div>
  </main>

  <!-- Add / Edit Project Modal -->
  <div id="modal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-[#121216] border border-white/20 rounded-xl max-w-2xl w-full p-6 sm:p-8 max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-center pb-4 border-b border-white/10 mb-6">
        <h3 id="modal-heading" class="text-xl font-bold text-white font-['Cinzel']">Add New Architectural Project</h3>
        <button onclick="closeModal()" class="text-zinc-400 hover:text-white text-2xl">&times;</button>
      </div>

      <form id="project-form" onsubmit="handleFormSubmit(event)" class="space-y-4 text-xs">
        <input type="hidden" id="edit-id" value="">

        <div>
          <label class="block font-mono text-zinc-300 mb-1">PROJECT TITLE *</label>
          <input type="text" id="title" required placeholder="e.g. Modern Minimalist Duplex" class="w-full p-3 bg-black border border-white/15 rounded text-white focus:border-[#c5a880] outline-none">
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block font-mono text-zinc-300 mb-1">CATEGORY *</label>
            <select id="category" class="w-full p-3 bg-black border border-white/15 rounded text-white focus:border-[#c5a880] outline-none">
              <option value="residential">Residential Architecture</option>
              <option value="commercial">Commercial & Institutional</option>
              <option value="interior">Luxury Interiors</option>
            </select>
          </div>
          <div>
            <label class="block font-mono text-zinc-300 mb-1">LOCATION *</label>
            <input type="text" id="location" required placeholder="e.g. Raipur, C.G." class="w-full p-3 bg-black border border-white/15 rounded text-white focus:border-[#c5a880] outline-none">
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block font-mono text-zinc-300 mb-1">CLIENT NAME</label>
            <input type="text" id="client" placeholder="e.g. Shri Rajesh Sharma" class="w-full p-3 bg-black border border-white/15 rounded text-white focus:border-[#c5a880] outline-none">
          </div>
          <div>
            <label class="block font-mono text-zinc-300 mb-1">AREA / DIMENSIONS</label>
            <input type="text" id="area" placeholder="e.g. 4,500 Sq. Ft. (G+2)" class="w-full p-3 bg-black border border-white/15 rounded text-white focus:border-[#c5a880] outline-none">
          </div>
        </div>

        <div>
          <label class="block font-mono text-zinc-300 mb-1">PHOTO FILE PATH OR FILENAME *</label>
          <input type="text" id="image-path" required placeholder="e.g. assets/projects/my_new_render.jpg" class="w-full p-3 bg-black border border-white/15 rounded text-white focus:border-[#c5a880] outline-none">
          <span class="text-[10px] text-zinc-500 mt-1 block">Place new high-res image into website/assets/projects/ and paste filename here.</span>
        </div>

        <div>
          <label class="block font-mono text-zinc-300 mb-1">ARCHITECTURAL TAGLINE</label>
          <input type="text" id="tagline" placeholder="e.g. Clean geometric volumes with Italian marble and sunken courtyards" class="w-full p-3 bg-black border border-white/15 rounded text-white focus:border-[#c5a880] outline-none">
        </div>

        <div>
          <label class="block font-mono text-zinc-300 mb-1">FULL SCOPE & ARCHITECTURAL DESCRIPTION</label>
          <textarea id="description" rows="3" placeholder="Describe the design concept, ventilation zoning, materials used..." class="w-full p-3 bg-black border border-white/15 rounded text-white focus:border-[#c5a880] outline-none"></textarea>
        </div>

        <div class="pt-4 flex justify-end gap-3 border-t border-white/10">
          <button type="button" onclick="closeModal()" class="px-5 py-2.5 bg-zinc-800 text-zinc-300 rounded hover:bg-zinc-700">Cancel</button>
          <button type="submit" class="px-6 py-2.5 bg-[#c5a880] text-black font-semibold rounded hover:bg-[#dfc8a5]">Save Project</button>
        </div>
      </form>
    </div>
  </div>

  <script>
    let projectsData = [];

    async function loadData() {
      const res = await fetch('/api/projects');
      const data = await res.json();
      projectsData = data.projects || [];
      document.getElementById('count').textContent = projectsData.length;
      renderProjects();
    }

    function renderProjects() {
      const container = document.getElementById('project-list');
      container.innerHTML = '';
      projectsData.forEach(p => {
        const card = document.createElement('div');
        card.className = 'bg-[#141418] border border-white/10 rounded-lg overflow-hidden flex flex-col justify-between';
        card.innerHTML = `
          <div class="relative aspect-[16/10] bg-black">
            <img src="/${p.image}" class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/400x250?text=Render+Preview'">
            <span class="absolute top-2 left-2 px-2 py-0.5 rounded text-[10px] font-mono bg-black/70 text-[#c5a880] border border-[#c5a880]/30 uppercase">\${p.category}</span>
          </div>
          <div class="p-4 flex-1 flex flex-col justify-between">
            <div>
              <div class="text-[11px] font-mono text-zinc-400">\${p.location} &bull; \${p.client || 'Commission'}</div>
              <h4 class="font-bold text-white text-sm mt-1">\${p.title}</h4>
              <p class="text-xs text-zinc-400 mt-2 line-clamp-2">\${p.tagline || p.description}</p>
            </div>
            <div class="pt-4 mt-4 border-t border-white/5 flex justify-between items-center text-xs">
              <button onclick="editProject('\${p.id}')" class="text-[#c5a880] hover:underline">Edit Details</button>
              <button onclick="deleteProject('\${p.id}')" class="text-red-400 hover:underline">Delete</button>
            </div>
          </div>
        `;
        container.appendChild(card);
      });
    }

    function openNewModal() {
      document.getElementById('modal-heading').textContent = 'Add New Architectural Project';
      document.getElementById('project-form').reset();
      document.getElementById('edit-id').value = '';
      document.getElementById('modal').classList.remove('hidden');
    }

    function editProject(id) {
      const p = projectsData.find(item => item.id === id);
      if (!p) return;
      document.getElementById('modal-heading').textContent = 'Edit Architectural Project';
      document.getElementById('edit-id').value = p.id;
      document.getElementById('title').value = p.title || '';
      document.getElementById('category').value = p.category || 'residential';
      document.getElementById('location').value = p.location || '';
      document.getElementById('client').value = p.client || '';
      document.getElementById('area').value = (p.details && p.details['Area']) || '';
      document.getElementById('image-path').value = p.image || '';
      document.getElementById('tagline').value = p.tagline || '';
      document.getElementById('description').value = p.description || '';
      document.getElementById('modal').classList.remove('hidden');
    }

    function closeModal() {
      document.getElementById('modal').classList.add('hidden');
    }

    async function handleFormSubmit(e) {
      e.preventDefault();
      const editId = document.getElementById('edit-id').value;
      const cat = document.getElementById('category').value;
      const catLabel = cat === 'residential' ? 'Residential Architecture' : cat === 'commercial' ? 'Commercial & Institutional' : 'Luxury Interiors';
      
      const payload = {
        id: editId || ('proj-' + Date.now()),
        title: document.getElementById('title').value,
        category: cat,
        category_label: catLabel,
        location: document.getElementById('location').value,
        client: document.getElementById('client').value,
        image: document.getElementById('image-path').value,
        gallery: [document.getElementById('image-path').value],
        tagline: document.getElementById('tagline').value,
        description: document.getElementById('description').value,
        details: {
          'Area': document.getElementById('area').value || 'Custom'
        }
      };

      const res = await fetch('/api/save-project', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        closeModal();
        showNotice('Project successfully saved and synchronized!');
        loadData();
      } else {
        alert('Failed to save project.');
      }
    }

    async function deleteProject(id) {
      if (!confirm('Are you sure you want to remove this project from the portfolio?')) return;
      const res = await fetch('/api/delete-project?id=' + encodeURIComponent(id), { method: 'DELETE' });
      if (res.ok) {
        showNotice('Project deleted.');
        loadData();
      }
    }

    function showNotice(msg) {
      const el = document.getElementById('notice');
      el.textContent = '✓ ' + msg;
      el.classList.remove('hidden');
      setTimeout(() => el.classList.add('hidden'), 4000);
    }

    loadData();
  </script>
</body>
</html>
"""

class AdminRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Serve from website root directory
        website_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        super().__init__(*args, directory=website_root, **kwargs)

    def do_GET(self):
        if self.path == '/' or self.path == '/admin' or self.path == '/admin/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_DASHBOARD.encode('utf-8'))
            return
        elif self.path == '/api/projects':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            with open(DATA_FILE, 'r') as f:
                self.wfile.write(f.read().encode('utf-8'))
            return
        else:
            return super().do_GET()

    def do_POST(self):
        if self.path == '/api/save-project':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            new_proj = json.loads(body)

            with open(DATA_FILE, 'r') as f:
                data = json.load(f)

            # check if updating or adding
            found = False
            for idx, p in enumerate(data['projects']):
                if p['id'] == new_proj['id']:
                    data['projects'][idx] = new_proj
                    found = True
                    break
            if not found:
                data['projects'].insert(0, new_proj)

            # Save projects.json
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=2)

            # Save data.js
            with open(JS_DATA_FILE, 'w') as f:
                f.write('window.__PORTFOLIO_DATA__ = ' + json.dumps(data, indent=2) + ';')

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return

    def do_DELETE(self):
        if self.path.startswith('/api/delete-project'):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            proj_id = query.get('id', [None])[0]
            if proj_id:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)

                data['projects'] = [p for p in data['projects'] if p['id'] != proj_id]

                with open(DATA_FILE, 'w') as f:
                    json.dump(data, f, indent=2)

                with open(JS_DATA_FILE, 'w') as f:
                    f.write('window.__PORTFOLIO_DATA__ = ' + json.dumps(data, indent=2) + ';')

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status":"deleted"}')
                return

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), AdminRequestHandler) as httpd:
        print(f"============================================================")
        print(f" PORTFOLIO ADMIN MANAGER RUNNING AT: http://localhost:{PORT}")
        print(f" Open http://localhost:{PORT} in your browser to manage projects!")
        print(f"============================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nAdmin Server stopped.")

