import re
import os

with open('website/admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update confirmDeleteProject for hybrid
hybrid_delete = """
    async function confirmDeleteProject() {
      const id = document.getElementById('delete-project-id').value;
      if (!id) return;
      const btn = document.getElementById('confirm-delete-btn');
      btn.disabled = true;
      btn.innerText = 'Deleting...';

      if (IS_LOCAL) {
        try {
          const res = await fetch('/api/delete-project?id=' + encodeURIComponent(id), { method: 'DELETE' });
          if (res.ok) {
            closeDeleteModal();
            showNotice('✓ Project permanently deleted. Click "Publish to Live Website" to sync with live domain.');
            loadData();
          } else {
            alert('Delete failed on server.');
          }
        } catch (err) {
          alert('Delete error: ' + err.message);
        } finally {
          btn.disabled = false;
          btn.innerText = 'Yes, Delete Forever';
        }
      } else {
        fullData.projects = (fullData.projects || []).filter(p => p.id !== id);
        closeDeleteModal();
        renderProjects(fullData.projects);
        document.getElementById('tab-proj-count').textContent = fullData.projects.length;
        showNotice('✓ Project deleted in studio! Click "Publish to Live Website" to push changes live.');
        btn.disabled = false;
        btn.innerText = 'Yes, Delete Forever';
      }
    }
"""

code = re.sub(
    r'async function confirmDeleteProject\(\).*?btn\.innerText = \'Yes, Delete Forever\';\s*}',
    hybrid_delete.strip(),
    code,
    flags=re.DOTALL
)

# 2. Update handleAvatarUpload & saveArchitectProfile
hybrid_about = """
    async function handleAvatarUpload(e) {
      const file = e.target.files[0];
      if (!file) return;
      const b64 = await readFileAsBase64(file);
      if (IS_LOCAL) {
        const res = await fetch('/api/upload-photos', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ files: [{ name: 'deepti_singh.jpg', data: b64, dir: 'profile' }] })
        });
        const data = await res.json();
        if (data.status === 'ok') {
          const path = data.uploaded[0];
          document.getElementById('about-avatar-path').value = path;
          document.getElementById('avatar-preview').src = '/' + path + '?t=' + Date.now();
          showNotice('✓ Portrait photo updated!');
        }
      } else {
        const relPath = `assets/profile/${Date.now()}_portrait.jpg`;
        uploadedPhotosQueue.push({ path: relPath, data: b64 });
        document.getElementById('about-avatar-path').value = relPath;
        document.getElementById('avatar-preview').src = b64;
        showNotice('✓ Portrait photo selected! Click "Publish to Live Website" to upload and save.');
      }
    }

    async function saveArchitectProfile(e) {
      e.preventDefault();
      const payload = {
        name: document.getElementById('about-name').value,
        title: document.getElementById('about-title').value,
        experience: document.getElementById('about-exp').value,
        location: document.getElementById('about-loc').value,
        avatar: document.getElementById('about-avatar-path').value,
        bio: document.getElementById('about-bio').value,
        philosophy: document.getElementById('about-philosophy').value,
        skills: [
          { name: "AutoCAD 2D/3D", percentage: document.getElementById('skill-autocad').value + "%" },
          { name: "Google SketchUp", percentage: document.getElementById('skill-sketchup').value + "%" },
          { name: "Autodesk 3ds Max", percentage: document.getElementById('skill-3dsmax').value + "%" },
          { name: "Autodesk Revit Architecture", percentage: document.getElementById('skill-revit').value + "%" }
        ]
      };

      if (IS_LOCAL) {
        const res = await fetch('/api/save-architect', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (res.ok) {
          showNotice('✓ Architect Profile saved! Click "Publish to Live Website" to sync with live site.');
          loadData();
        } else {
          alert('Failed to save profile.');
        }
      } else {
        fullData.architect = { ...(fullData.architect || {}), ...payload };
        showNotice('✓ Architect Profile updated in studio! Click "Publish to Live Website" to push live.');
      }
    }
"""

code = re.sub(
    r'async function handleAvatarUpload\(e\).*?loadData\(\);\s*}\s*}',
    hybrid_about.strip(),
    code,
    flags=re.DOTALL
)

# 3. Update saveR2RCases
hybrid_r2r = """
    async function saveR2RCases() {
      const items = (fullData.render_to_real && fullData.render_to_real.items) || [];
      items.forEach((item, idx) => {
        item.title = document.getElementById(`r2r-title-${idx}`).value;
        item.render_img = document.getElementById(`r2r-render-${idx}`).value;
        item.real_img = document.getElementById(`r2r-real-${idx}`).value;
        item.description = document.getElementById(`r2r-desc-${idx}`).value;
      });

      if (IS_LOCAL) {
        const res = await fetch('/api/save-r2r', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ items })
        });
        if (res.ok) {
          showNotice('✓ Render vs Reality cases saved!');
          loadData();
        } else {
          alert('Failed to save cases.');
        }
      } else {
        if (!fullData.render_to_real) fullData.render_to_real = {};
        fullData.render_to_real.items = items;
        showNotice('✓ Render vs Reality cases updated! Click "Publish to Live Website" to push live.');
      }
    }
"""

code = re.sub(
    r'async function saveR2RCases\(\).*?loadData\(\);\s*}\s*}',
    hybrid_r2r.strip(),
    code,
    flags=re.DOTALL
)

# 4. Update saveCADDrawings
hybrid_cad = """
    async function saveCADDrawings() {
      const list = fullData.technical_drawings || [];
      list.forEach((item, idx) => {
        item.title = document.getElementById(`cad-title-${idx}`).value;
        item.category = document.getElementById(`cad-cat-${idx}`).value;
        item.image = document.getElementById(`cad-img-${idx}`).value;
        item.description = document.getElementById(`cad-desc-${idx}`).value;
      });

      if (IS_LOCAL) {
        const res = await fetch('/api/save-blueprints', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ technical_drawings: list })
        });
        if (res.ok) {
          showNotice('✓ CAD Blueprints saved!');
          loadData();
        } else {
          alert('Failed to save blueprints.');
        }
      } else {
        fullData.technical_drawings = list;
        showNotice('✓ CAD Blueprints updated! Click "Publish to Live Website" to push live.');
      }
    }
"""

code = re.sub(
    r'async function saveCADDrawings\(\).*?loadData\(\);\s*}\s*}',
    hybrid_cad.strip(),
    code,
    flags=re.DOTALL
)

# 5. Update saveHeroContact
hybrid_hero = """
    async function saveHeroContact(e) {
      e.preventDefault();
      const p1 = document.getElementById('contact-phone-1').value;
      const p2 = document.getElementById('contact-phone-2').value;
      const payload = {
        phone: [p1, p2].filter(Boolean),
        email: document.getElementById('contact-email').value,
        announcement: document.getElementById('hero-announcement').value,
        headline_1: document.getElementById('hero-headline-1').value,
        headline_2: document.getElementById('hero-headline-2').value,
        paragraph: document.getElementById('hero-paragraph').value,
        stats: {
          years_exp: document.getElementById('stat-years').value,
          projects_count: document.getElementById('stat-projects').value,
          fidelity_rate: document.getElementById('stat-fidelity').value,
          metros_count: document.getElementById('stat-metros').value
        }
      };

      if (IS_LOCAL) {
        const res = await fetch('/api/save-hero-contact', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (res.ok) {
          showNotice('✓ Hero & Contact Settings saved! Click "Publish to Live Website" to sync.');
          loadData();
        } else {
          alert('Failed to save contact settings.');
        }
      } else {
        if (!fullData.architect) fullData.architect = {};
        fullData.architect.phone = payload.phone;
        fullData.architect.primary_phone = p1;
        fullData.architect.secondary_phone = p2;
        fullData.architect.email = payload.email;
        fullData.hero = {
          announcement: payload.announcement,
          headline_1: payload.headline_1,
          headline_2: payload.headline_2,
          paragraph: payload.paragraph
        };
        fullData.stats = payload.stats;
        showNotice('✓ Hero & Contact Settings updated! Click "Publish to Live Website" to push live.');
      }
    }
"""

code = re.sub(
    r'async function saveHeroContact\(e\).*?loadData\(\);\s*}\s*}',
    hybrid_hero.strip(),
    code,
    flags=re.DOTALL
)

with open('website/admin/index.html', 'w', encoding='utf-8') as out:
    out.write(code)

print("index.html fully updated! File size:", len(code))
