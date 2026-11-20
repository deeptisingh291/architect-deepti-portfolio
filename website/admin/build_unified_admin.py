import re
import os

with open('website/admin/studio.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Studio Passcode Protection for Live Site
auth_modal = """
  <!-- Passcode Protection Modal for Live Site -->
  <div id="auth-gate-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90 backdrop-blur-md">
    <div class="bg-[#121216] border border-[#c5a880]/40 rounded-2xl max-w-md w-full p-8 shadow-2xl text-center space-y-6">
      <div class="w-16 h-16 mx-auto border-2 border-[#c5a880] flex items-center justify-center text-[#c5a880] font-serif font-bold text-2xl">DS</div>
      <div>
        <h2 class="text-xl font-bold font-serif text-white tracking-wide">Studio Content Manager</h2>
        <p class="text-xs font-mono text-[#c5a880] mt-1 uppercase tracking-wider">Ar. Deepti Singh &bull; Confidential</p>
      </div>
      <p class="text-xs text-zinc-400">Please enter your studio passcode to access portfolio controls.</p>
      <form onsubmit="verifyStudioPasscode(event)" class="space-y-4">
        <input type="password" id="studio-passcode-input" placeholder="Enter Studio Passcode" class="w-full px-4 py-3 bg-black border border-white/20 rounded-lg text-sm text-white text-center focus:outline-none focus:border-[#c5a880] tracking-widest font-mono" required autofocus>
        <button type="submit" class="w-full py-3 bg-[#c5a880] text-black font-bold text-xs uppercase tracking-widest rounded-lg hover:bg-[#dfc8a5] transition-all">Enter Studio</button>
      </form>
      <p id="auth-error-msg" class="text-xs text-red-400 hidden font-mono">Incorrect passcode. Try again.</p>
    </div>
  </div>

  <!-- GitHub Token Configuration Modal for Direct Live Publishing -->
  <div id="gh-token-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-sm">
    <div class="bg-[#121216] border border-[#c5a880]/30 rounded-2xl max-w-lg w-full p-8 shadow-2xl space-y-5">
      <div class="flex items-center justify-between pb-3 border-b border-white/10">
        <h3 class="text-base font-bold font-serif text-white flex items-center gap-2">
          <svg class="w-5 h-5 text-[#c5a880]" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
          Direct Live Publishing Setup
        </h3>
        <button onclick="document.getElementById('gh-token-modal').classList.add('hidden')" class="text-zinc-400 hover:text-white">&times;</button>
      </div>
      <p class="text-xs text-zinc-300 leading-relaxed">
        Live website par direct save karne ke liye GitHub Personal Access Token (PAT) enter karein. Ye aapke browser me securely save ho jayega taaki aap jab bhi "Publish" click karein, Netlify turant live deploy kar de.
      </p>
      <div class="space-y-2">
        <label class="block text-xs font-mono uppercase text-[#c5a880]">GitHub Token (Classic or Fine-grained with repo write)</label>
        <input type="password" id="gh-token-input" placeholder="ghp_xxxxxxxxxxxxxxxxxxxx" class="w-full px-4 py-2.5 bg-black border border-white/20 rounded text-sm text-white font-mono focus:border-[#c5a880] outline-none">
      </div>
      <div class="pt-2 flex justify-between items-center text-xs">
        <a href="https://github.com/settings/tokens/new?scopes=repo" target="_blank" class="text-[#c5a880] hover:underline font-mono">Create token on GitHub &rarr;</a>
        <button onclick="saveGitHubToken()" class="px-5 py-2.5 bg-[#c5a880] text-black font-bold uppercase tracking-wider rounded hover:bg-[#dfc8a5]">Save Token</button>
      </div>
    </div>
  </div>
"""

# Insert modals right before closing </body>
content = content.replace('</body>', auth_modal + '\n</body>')

# 2. Add Export / Backup Button in top bar
top_bar_actions = """
      <div class="flex items-center gap-3">
        <button onclick="downloadDataBackup()" class="px-3 py-2 rounded bg-[#16161c] border border-white/10 hover:border-[#c5a880] text-zinc-300 hover:text-[#c5a880] text-xs font-mono flex items-center gap-1.5 transition-all" title="Download backup of all current data">
          <svg class="w-3.5 h-3.5 text-[#c5a880]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
          Backup JSON
        </button>
        <a href="/" target="_blank" class="px-3 py-2 rounded bg-[#16161c] border border-white/10 hover:border-[#c5a880] text-zinc-300 hover:text-[#c5a880] text-xs font-mono flex items-center gap-1 transition-all">
          View Live Site &nearr;
        </a>
        <button id="publish-live-btn" onclick="publishToLiveSite()" class="px-5 py-2 rounded bg-[#c5a880] hover:bg-[#dfc8a5] text-black font-bold text-xs uppercase tracking-wider flex items-center gap-2 transition-all shadow-lg shadow-[#c5a880]/10">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/></svg>
          <span id="publish-btn-text">Publish to Live Website</span>
        </button>
      </div>
"""

content = re.sub(
    r'<div class="flex items-center gap-3">.*?<button id="publish-live-btn".*?</div>',
    top_bar_actions.strip(),
    content,
    flags=re.DOTALL
)

# 3. Add Hybrid Sync & GitHub API Script
hybrid_script = """
    const IS_LOCAL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    let uploadedPhotosQueue = []; // For online uploads

    // Check Authentication on Live Site
    function initSecurity() {
      if (IS_LOCAL) return;
      const authed = sessionStorage.getItem('deepti_studio_authed');
      if (!authed) {
        document.getElementById('auth-gate-modal').classList.remove('hidden');
      }
    }

    function verifyStudioPasscode(e) {
      e.preventDefault();
      const input = document.getElementById('studio-passcode-input').value.trim();
      // Studio Passcode: deepti2026 or admin
      if (input === 'deepti2026' || input === 'admin2026' || input === 'deeptisingh') {
        sessionStorage.setItem('deepti_studio_authed', 'true');
        document.getElementById('auth-gate-modal').classList.add('hidden');
      } else {
        const err = document.getElementById('auth-error-msg');
        err.classList.remove('hidden');
      }
    }

    // Hybrid loadData: Local API or Live Static JSON
    async function loadData() {
      try {
        const ts = Date.now();
        if (IS_LOCAL) {
          const res = await fetch('/api/projects');
          fullData = await res.json();
        } else {
          // Fetch live projects.json with cache buster
          const pRes = await fetch('../data/projects.json?t=' + ts);
          fullData = await pRes.json();
          // Also fetch profile.json
          try {
            const profRes = await fetch('../data/profile.json?t=' + ts);
            if (profRes.ok) {
              const prof = await profRes.json();
              fullData.architect = { ...(fullData.architect || {}), ...prof };
            }
          } catch (e) {}
        }

        const projects = fullData.projects || [];
        document.getElementById('tab-proj-count').textContent = projects.length;
        renderProjects(projects);
        populateAboutTab();
        populateR2RTab();
        populateCADTab();
        populateHeroTab();
      } catch (err) {
        console.error("Error loading data:", err);
      }
    }

    // Backup Download
    function downloadDataBackup() {
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(fullData, null, 2));
      const downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", `projects_backup_${new Date().toISOString().slice(0,10)}.json`);
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    }

    // GitHub Token Handling
    function saveGitHubToken() {
      const token = document.getElementById('gh-token-input').value.trim();
      if (!token) return alert('Please enter token');
      localStorage.setItem('studio_gh_token', token);
      document.getElementById('gh-token-modal').classList.add('hidden');
      publishToLiveSite();
    }

    // Hybrid Publish to Live
    async function publishToLiveSite() {
      const btn = document.getElementById('publish-live-btn');
      const text = document.getElementById('publish-btn-text');
      btn.disabled = true;
      text.textContent = 'Publishing Live...';

      if (IS_LOCAL) {
        try {
          const res = await fetch('/api/publish-live', { method: 'POST' });
          const data = await res.json();
          if (data.status === 'ok') {
            showNotice('✓ ' + (data.message || 'Successfully published to live website! Netlify is updating architectdeepti.in'));
          } else {
            alert('Publish failed: ' + (data.error || 'Check internet/git connection'));
          }
        } catch (err) {
          alert('Publish error: ' + err.message);
        } finally {
          btn.disabled = false;
          text.textContent = 'Publish to Live Website';
        }
        return;
      }

      // Online Direct Publish via GitHub API
      let ghToken = localStorage.getItem('studio_gh_token');
      if (!ghToken) {
        btn.disabled = false;
        text.textContent = 'Publish to Live Website';
        document.getElementById('gh-token-modal').classList.remove('hidden');
        return;
      }

      try {
        const repo = 'deeptisingh291/architect-deepti-portfolio';
        const headers = {
          'Authorization': `Bearer ${ghToken}`,
          'Accept': 'application/vnd.github.v3+json',
          'Content-Type': 'application/json'
        };

        // 1. Upload any queued photos
        for (const item of uploadedPhotosQueue) {
          try {
            const pathUrl = `https://api.github.com/repos/${repo}/contents/website/${item.path}`;
            let sha = null;
            const check = await fetch(pathUrl, { headers });
            if (check.ok) {
              const d = await check.json();
              sha = d.sha;
            }
            const b64Data = item.data.includes(',') ? item.data.split(',')[1] : item.data;
            await fetch(pathUrl, {
              method: 'PUT',
              headers,
              body: JSON.stringify({
                message: `Upload image ${item.path}`,
                content: b64Data,
                sha: sha || undefined
              })
            });
          } catch (e) {
            console.warn('Image upload failed:', item.path, e);
          }
        }
        uploadedPhotosQueue = [];

        // 2. Commit website/data/projects.json
        const projUrl = `https://api.github.com/repos/${repo}/contents/website/data/projects.json`;
        let projSha = null;
        const pCheck = await fetch(projUrl, { headers });
        if (pCheck.ok) {
          const d = await pCheck.json();
          projSha = d.sha;
        }

        const projContentB64 = btoa(unescape(encodeURIComponent(JSON.stringify(fullData, null, 2))));
        const pPut = await fetch(projUrl, {
          method: 'PUT',
          headers,
          body: JSON.stringify({
            message: 'Studio Dashboard live update: projects.json',
            content: projContentB64,
            sha: projSha || undefined
          })
        });

        if (!pPut.ok) {
          const errData = await pPut.json();
          throw new Error(errData.message || 'GitHub commit failed');
        }

        // 3. Commit website/data/profile.json if architect data present
        if (fullData.architect) {
          const profUrl = `https://api.github.com/repos/${repo}/contents/website/data/profile.json`;
          let profSha = null;
          const profCheck = await fetch(profUrl, { headers });
          if (profCheck.ok) {
            const d = await profCheck.json();
            profSha = d.sha;
          }
          const profContentB64 = btoa(unescape(encodeURIComponent(JSON.stringify(fullData.architect, null, 2))));
          await fetch(profUrl, {
            method: 'PUT',
            headers,
            body: JSON.stringify({
              message: 'Studio Dashboard live update: profile.json',
              content: profContentB64,
              sha: profSha || undefined
            })
          });
        }

        showNotice('✓ Published directly to GitHub! Netlify is updating architectdeepti.in right now.');
      } catch (err) {
        alert('Publish failed: ' + err.message + '. Tip: verify your token or download JSON backup.');
      } finally {
        btn.disabled = false;
        text.textContent = 'Publish to Live Website';
      }
    }
"""

# Replace existing loadData and publishToLiveSite in content
content = re.sub(r'async function loadData\(\).*?async function publishToLiveSite\(\).*?}\s*}', hybrid_script.strip(), content, flags=re.DOTALL)

# Add initSecurity call
content = content.replace('window.onload = function() {', 'window.onload = function() {\n      initSecurity();')

# Update file upload logic to handle online queueing
online_upload_patch = """
        if (IS_LOCAL) {
          const res = await fetch('/api/upload-photos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ files: payloadFiles })
          });
          const result = await res.json();
          if (result.status === 'ok') {
            result.uploaded.forEach(path => {
              if (!currentGallery.includes(path)) currentGallery.push(path);
            });
            if (!currentCover && currentGallery.length) currentCover = currentGallery[0];
            renderPhotoPreviews();
            statusText.textContent = `✓ Uploaded ${result.uploaded.length} photo(s)!`;
            setTimeout(() => statusBox.classList.add('hidden'), 2500);
          }
        } else {
          // Online Mode: queue photos in memory
          payloadFiles.forEach(f => {
            const cleanName = f.name.replace(/[^a-zA-Z0-9_\-\.]/g, '_').toLowerCase();
            const relPath = `assets/projects/${Date.now()}_${cleanName}`;
            uploadedPhotosQueue.push({ path: relPath, data: f.data });
            if (!currentGallery.includes(relPath)) currentGallery.push(relPath);
          });
          if (!currentCover && currentGallery.length) currentCover = currentGallery[0];
          renderPhotoPreviews();
          statusText.textContent = `✓ Added ${payloadFiles.length} photo(s) to gallery! Click Publish to sync.`;
          setTimeout(() => statusBox.classList.add('hidden'), 2500);
        }
"""

content = re.sub(
    r'const res = await fetch\(\'/api/upload-photos\'.*?setTimeout\(\(\) => statusBox\.classList\.add\(\'hidden\'\), 2500\);\s*}',
    online_upload_patch.strip(),
    content,
    flags=re.DOTALL
)

# Hybrid handleFormSubmit for project save
project_save_patch = """
        if (IS_LOCAL) {
          const res = await fetch('/api/save-project', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          if (res.ok) {
            closeModal();
            showNotice('✓ Project saved! Click "Publish to Live Website" upar right side me jab live bhejna ho.');
            loadData();
          } else {
            alert('Failed to save project.');
          }
        } else {
          // Online Mode: update in memory
          const existingIdx = (fullData.projects || []).findIndex(p => p.id === payload.id);
          if (existingIdx >= 0) {
            fullData.projects[existingIdx] = payload;
          } else {
            if (!fullData.projects) fullData.projects = [];
            fullData.projects.unshift(payload);
          }
          closeModal();
          showNotice('✓ Project updated in studio! Click "Publish to Live Website" to push changes live.');
          renderProjects(fullData.projects);
          document.getElementById('tab-proj-count').textContent = fullData.projects.length;
        }
"""

content = re.sub(
    r'const res = await fetch\(\'/api/save-project\'.*?alert\(\'Failed to save project\.\'\);\s*}',
    project_save_patch.strip(),
    content,
    flags=re.DOTALL
)

# Save to website/admin/index.html
with open('website/admin/index.html', 'w', encoding='utf-8') as out:
    out.write(content)

print("Unified website/admin/index.html successfully created! Size:", len(content))
