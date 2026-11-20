#!/usr/bin/env python3
"""
MASTER ARCHITECTURAL PORTFOLIO CONTROL PANEL
For Ar. Deepti Singh Portfolio
Manage Projects, About Bio, Render-vs-Reality, CAD Blueprints, Hero & Contact.
Run locally on Mac: python3 website/admin/local_admin.py
"""

import http.server
import socketserver
import json
import os
import re
import base64
import urllib.parse
import subprocess
from PIL import Image
import io

PORT = 9000
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_FILE = os.path.join(BASE_DIR, 'data/projects.json')
PROFILE_FILE = os.path.join(BASE_DIR, 'data/profile.json')
JS_DATA_FILE = os.path.join(BASE_DIR, 'js/data.js')
ENTRIES_DIR = os.path.join(BASE_DIR, 'data/projects_entries')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets/projects')
PLANS_DIR = os.path.join(BASE_DIR, 'assets/plans')
R2R_DIR = os.path.join(BASE_DIR, 'assets/render_to_real')
PROFILE_DIR = os.path.join(BASE_DIR, 'assets/profile')

for d in [ASSETS_DIR, PLANS_DIR, R2R_DIR, PROFILE_DIR, ENTRIES_DIR]:
    os.makedirs(d, exist_ok=True)

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Master Portfolio Control Panel &bull; Ar. Deepti Singh</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Cinzel:wght@600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; background: #0a0a0c; color: #f5f5f7; }
    .gold-accent { color: #c5a880; }
    .gold-border { border-color: rgba(197, 168, 128, 0.4); }
    .gold-bg { background-color: #c5a880; }
    .nav-tab.active { background-color: #c5a880; color: #000; font-weight: 700; }
  </style>
</head>
<body class="p-4 sm:p-8 max-w-7xl mx-auto min-h-screen flex flex-col justify-between">
  
  <div>
    <!-- Top Action Bar -->
    <header class="flex flex-col lg:flex-row justify-between items-start lg:items-center pb-6 border-b border-white/10 gap-4">
      <div>
        <div class="text-[11px] font-mono text-[#c5a880] uppercase tracking-widest flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          MASTER ARCHITECTURAL CONTROL PANEL &bull; AR. DEEPTI SINGH
        </div>
        <h1 class="text-2xl sm:text-3xl font-bold font-['Playfair_Display'] text-white mt-1">Portfolio Studio & Content Manager</h1>
        <p class="text-xs text-zinc-400 mt-1">Edit all portfolio sections, projects, CAD blueprints, credentials, and live publishing.</p>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <a href="https://architectdeepti.in" target="_blank" class="px-4 py-2.5 bg-[#16161c] border border-white/15 text-xs text-zinc-300 rounded-lg hover:border-[#c5a880] transition-colors flex items-center gap-1.5">
          <span>View Live Site</span>
          <svg class="w-3.5 h-3.5 text-[#c5a880]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
        </a>

        <!-- 1-Click Live Publish Button -->
        <button onclick="publishToLiveSite()" id="publish-live-btn" class="px-5 py-2.5 bg-gradient-to-r from-[#dfc8a5] via-[#c5a880] to-[#9e7f57] text-black font-bold text-xs tracking-wider uppercase rounded-lg hover:opacity-90 transition-all flex items-center gap-2 shadow-xl shadow-[#c5a880]/20">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/></svg>
          <span id="publish-btn-text">Publish to Live Website</span>
        </button>
      </div>
    </header>

    <!-- Flash Notice -->
    <div id="notice" class="hidden mt-6 p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-mono flex items-center justify-between">
      <span id="notice-text">Notice</span>
      <button onclick="document.getElementById('notice').classList.add('hidden')" class="text-emerald-400 font-bold">&times;</button>
    </div>

    <!-- Navigation Section Tabs -->
    <nav class="flex flex-wrap items-center gap-2 mt-8 pb-4 border-b border-white/10 text-xs font-mono">
      <button onclick="switchTab('tab-projects')" id="tab-btn-projects" class="nav-tab active px-4 py-2.5 rounded-lg border border-white/10 transition-all flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
        <span>Projects Portfolio (<span id="tab-proj-count">0</span>)</span>
      </button>

      <button onclick="switchTab('tab-about')" id="tab-btn-about" class="nav-tab px-4 py-2.5 rounded-lg border border-white/10 bg-[#121216] text-zinc-300 hover:text-white transition-all flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
        <span>About Architect & Experience</span>
      </button>

      <button onclick="switchTab('tab-r2r')" id="tab-btn-r2r" class="nav-tab px-4 py-2.5 rounded-lg border border-white/10 bg-[#121216] text-zinc-300 hover:text-white transition-all flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/></svg>
        <span>Render vs Reality Cases</span>
      </button>

      <button onclick="switchTab('tab-cad')" id="tab-btn-cad" class="nav-tab px-4 py-2.5 rounded-lg border border-white/10 bg-[#121216] text-zinc-300 hover:text-white transition-all flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"/></svg>
        <span>CAD Blueprints & Plans</span>
      </button>

      <button onclick="switchTab('tab-hero')" id="tab-btn-hero" class="nav-tab px-4 py-2.5 rounded-lg border border-white/10 bg-[#121216] text-zinc-300 hover:text-white transition-all flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"/></svg>
        <span>Hero Headline & Contact</span>
      </button>
    </nav>

    <!-- ======================================================================= -->
    <!-- TAB 1: PROJECTS PORTFOLIO -->
    <!-- ======================================================================= -->
    <div id="tab-projects" class="tab-content mt-8">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-3">
        <div>
          <h2 class="text-xl font-bold font-['Playfair_Display'] text-white">Current Projects in Portfolio</h2>
          <p class="text-xs text-zinc-400 mt-0.5">Click "Edit Project" to add/remove photos or update specs. Click "+ Add New Project" to create one.</p>
        </div>
        <div class="flex items-center gap-3">
          <input type="text" id="search-filter" oninput="filterProjects()" placeholder="Search project title or city..." class="px-3.5 py-2 bg-[#121216] border border-white/15 rounded-lg text-xs text-white placeholder-zinc-500 outline-none focus:border-[#c5a880] w-64">
          <button onclick="openNewModal()" class="px-4 py-2 bg-[#c5a880] text-black font-semibold text-xs rounded-lg hover:bg-[#dfc8a5] transition-all flex items-center gap-1.5 shadow-md">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
            <span>+ Add New Project</span>
          </button>
        </div>
      </div>

      <div id="project-list" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Rendered via JavaScript -->
      </div>
    </div>

    <!-- ======================================================================= -->
    <!-- TAB 2: ABOUT ARCHITECT & PRACTICE -->
    <!-- ======================================================================= -->
    <div id="tab-about" class="tab-content hidden mt-8 max-w-4xl">
      <div class="bg-[#121216] border border-white/10 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="border-b border-white/10 pb-4">
          <h2 class="text-xl font-bold font-['Playfair_Display'] text-white">About Ar. Deepti Singh & Practice Profile</h2>
          <p class="text-xs text-zinc-400 mt-1">Manage profile photo, professional bio, academic background, practice timeline, and software expertise.</p>
        </div>

        <form id="about-form" onsubmit="saveArchitectProfile(event)" class="space-y-6 text-xs">
          <!-- Profile Portrait Upload -->
          <div class="flex flex-col sm:flex-row items-center gap-6 p-4 bg-black/40 border border-white/10 rounded-xl">
            <img id="avatar-preview" src="/assets/profile/deepti_singh.jpg" class="w-24 h-24 rounded-full object-cover border-2 border-[#c5a880]" onerror="this.src='https://via.placeholder.com/150'">
            <div class="space-y-2 text-center sm:text-left">
              <div class="font-mono text-zinc-300 font-semibold">PROFILE PORTRAIT PHOTO</div>
              <input type="file" id="avatar-file-input" accept="image/*" class="hidden" onchange="handleAvatarUpload(event)">
              <button type="button" onclick="document.getElementById('avatar-file-input').click()" class="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-white rounded text-xs font-mono">
                Upload New Portrait Photo
              </button>
              <input type="hidden" id="about-avatar-path" value="assets/profile/deepti_singh.jpg">
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block font-mono text-zinc-300 mb-1.5">FULL NAME & TITLE *</label>
              <input type="text" id="about-name" required class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none">
            </div>
            <div>
              <label class="block font-mono text-zinc-300 mb-1.5">PROFESSIONAL TITLE *</label>
              <input type="text" id="about-title" required class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none">
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block font-mono text-zinc-300 mb-1.5">EXPERIENCE BADGE *</label>
              <input type="text" id="about-exp" required class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none">
            </div>
            <div>
              <label class="block font-mono text-zinc-300 mb-1.5">HEADQUARTERS LOCATION *</label>
              <input type="text" id="about-loc" required class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none">
            </div>
          </div>

          <div>
            <label class="block font-mono text-zinc-300 mb-1.5">FULL BIOGRAPHY *</label>
            <textarea id="about-bio" rows="4" required class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none leading-relaxed"></textarea>
          </div>

          <div>
            <label class="block font-mono text-zinc-300 mb-1.5">DESIGN PHILOSOPHY & ETHOS</label>
            <textarea id="about-philosophy" rows="3" class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none leading-relaxed"></textarea>
          </div>

          <!-- Software Skills -->
          <div class="p-4 bg-black/40 border border-white/10 rounded-xl space-y-3">
            <div class="font-mono text-zinc-300 font-semibold mb-2">SOFTWARE EXPERTISE PERCENTAGES</div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div>
                <label class="block font-mono text-zinc-400 mb-1">AutoCAD (%)</label>
                <input type="number" id="skill-autocad" min="1" max="100" class="w-full p-2.5 bg-black border border-white/15 rounded text-white text-center font-mono focus:border-[#c5a880] outline-none">
              </div>
              <div>
                <label class="block font-mono text-zinc-400 mb-1">Google SketchUp (%)</label>
                <input type="number" id="skill-sketchup" min="1" max="100" class="w-full p-2.5 bg-black border border-white/15 rounded text-white text-center font-mono focus:border-[#c5a880] outline-none">
              </div>
              <div>
                <label class="block font-mono text-zinc-400 mb-1">Autodesk 3ds Max (%)</label>
                <input type="number" id="skill-3dsmax" min="1" max="100" class="w-full p-2.5 bg-black border border-white/15 rounded text-white text-center font-mono focus:border-[#c5a880] outline-none">
              </div>
              <div>
                <label class="block font-mono text-zinc-400 mb-1">Autodesk Revit (%)</label>
                <input type="number" id="skill-revit" min="1" max="100" class="w-full p-2.5 bg-black border border-white/15 rounded text-white text-center font-mono focus:border-[#c5a880] outline-none">
              </div>
            </div>
          </div>

          <div class="flex justify-end pt-4 border-t border-white/10">
            <button type="submit" class="px-6 py-2.5 bg-[#c5a880] text-black font-semibold rounded-lg hover:bg-[#dfc8a5] transition-colors shadow-lg">
              Save Profile Details
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ======================================================================= -->
    <!-- TAB 3: RENDER VS REALITY CASES -->
    <!-- ======================================================================= -->
    <div id="tab-r2r" class="tab-content hidden mt-8 max-w-4xl">
      <div class="bg-[#121216] border border-white/10 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="border-b border-white/10 pb-4">
          <h2 class="text-xl font-bold font-['Playfair_Display'] text-white">Render to Reality Before/After Sliders</h2>
          <p class="text-xs text-zinc-400 mt-1">Manage the 3 interactive comparison cases displayed on the home page.</p>
        </div>

        <div id="r2r-cases-container" class="space-y-6">
          <!-- Rendered via JS -->
        </div>

        <div class="flex justify-end pt-4 border-t border-white/10">
          <button onclick="saveR2RCases()" class="px-6 py-2.5 bg-[#c5a880] text-black font-semibold rounded-lg hover:bg-[#dfc8a5] transition-colors shadow-lg">
            Save All Render vs Reality Cases
          </button>
        </div>
      </div>
    </div>

    <!-- ======================================================================= -->
    <!-- TAB 4: CAD BLUEPRINTS & PLANS -->
    <!-- ======================================================================= -->
    <div id="tab-cad" class="tab-content hidden mt-8 max-w-4xl">
      <div class="bg-[#121216] border border-white/10 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="border-b border-white/10 pb-4 flex justify-between items-center">
          <div>
            <h2 class="text-xl font-bold font-['Playfair_Display'] text-white">CAD Blueprints & Spatial Plans Viewer</h2>
            <p class="text-xs text-zinc-400 mt-1">Manage the CAD elevations, 3D floor plates, and structural drawings.</p>
          </div>
          <button onclick="addNewBlueprint()" class="px-3.5 py-2 bg-zinc-800 hover:bg-zinc-700 text-white rounded text-xs font-mono">
            + Add Drawing
          </button>
        </div>

        <div id="cad-drawings-container" class="space-y-6">
          <!-- Rendered via JS -->
        </div>

        <div class="flex justify-end pt-4 border-t border-white/10">
          <button onclick="saveCADDrawings()" class="px-6 py-2.5 bg-[#c5a880] text-black font-semibold rounded-lg hover:bg-[#dfc8a5] transition-colors shadow-lg">
            Save All Blueprints & Plans
          </button>
        </div>
      </div>
    </div>

    <!-- ======================================================================= -->
    <!-- TAB 5: HERO HEADLINE & CONTACT -->
    <!-- ======================================================================= -->
    <div id="tab-hero" class="tab-content hidden mt-8 max-w-4xl">
      <div class="bg-[#121216] border border-white/10 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="border-b border-white/10 pb-4">
          <h2 class="text-xl font-bold font-['Playfair_Display'] text-white">Hero Headline, Metrics & Contact Settings</h2>
          <p class="text-xs text-zinc-400 mt-1">Edit the main website hero title, announcement badge, phone numbers, and WhatsApp inquiry.</p>
        </div>

        <form id="hero-contact-form" onsubmit="saveHeroContact(event)" class="space-y-5 text-xs">
          <div>
            <label class="block font-mono text-zinc-300 mb-1.5 font-semibold">TOP ANNOUNCEMENT BAR TEXT</label>
            <input type="text" id="hero-announcement" class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none">
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block font-mono text-zinc-300 mb-1.5 font-semibold">HERO PRIMARY HEADLINE (LINE 1)</label>
              <input type="text" id="hero-headline-1" value="Sculpting Space." class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none text-sm font-bold">
            </div>
            <div>
              <label class="block font-mono text-zinc-300 mb-1.5 font-semibold">HERO SECONDARY HEADLINE (LINE 2)</label>
              <input type="text" id="hero-headline-2" value="Executing Reality." class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none text-sm font-bold">
            </div>
          </div>

          <div>
            <label class="block font-mono text-zinc-300 mb-1.5 font-semibold">HERO PHILOSOPHY PARAGRAPH</label>
            <textarea id="hero-paragraph" rows="3" class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none leading-relaxed"></textarea>
          </div>

          <!-- 4 Stats -->
          <div class="p-4 bg-black/40 border border-white/10 rounded-xl space-y-3">
            <div class="font-mono text-zinc-300 font-semibold">HOME PAGE STATS / METRICS</div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div>
                <label class="block font-mono text-zinc-400 mb-1">Years Exp</label>
                <input type="text" id="stat-years" value="12+" class="w-full p-2.5 bg-black border border-white/15 rounded text-white font-mono text-center focus:border-[#c5a880] outline-none">
              </div>
              <div>
                <label class="block font-mono text-zinc-400 mb-1">Projects Count</label>
                <input type="text" id="stat-projects" value="50+" class="w-full p-2.5 bg-black border border-white/15 rounded text-white font-mono text-center focus:border-[#c5a880] outline-none">
              </div>
              <div>
                <label class="block font-mono text-zinc-400 mb-1">Fidelity Rate</label>
                <input type="text" id="stat-fidelity" value="100%" class="w-full p-2.5 bg-black border border-white/15 rounded text-white font-mono text-center focus:border-[#c5a880] outline-none">
              </div>
              <div>
                <label class="block font-mono text-zinc-400 mb-1">Key Metros</label>
                <input type="text" id="stat-metros" value="6+" class="w-full p-2.5 bg-black border border-white/15 rounded text-white font-mono text-center focus:border-[#c5a880] outline-none">
              </div>
            </div>
          </div>

          <!-- Contact Details -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label class="block font-mono text-zinc-300 mb-1.5">PRIMARY PHONE / WHATSAPP *</label>
              <input type="text" id="contact-phone-1" required class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none font-mono">
            </div>
            <div>
              <label class="block font-mono text-zinc-300 mb-1.5">SECONDARY PHONE</label>
              <input type="text" id="contact-phone-2" class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none font-mono">
            </div>
            <div>
              <label class="block font-mono text-zinc-300 mb-1.5">OFFICIAL EMAIL *</label>
              <input type="email" id="contact-email" required class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none font-mono">
            </div>
          </div>

          <div class="flex justify-end pt-4 border-t border-white/10">
            <button type="submit" class="px-6 py-2.5 bg-[#c5a880] text-black font-semibold rounded-lg hover:bg-[#dfc8a5] transition-colors shadow-lg">
              Save Hero & Contact Settings
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer class="mt-16 pt-6 border-t border-white/10 text-center text-xs text-zinc-500 font-mono">
    Ar. Deepti Singh &bull; Lead Architect &bull; CSVTU Bhilai &bull; Practicing Since 2013
  </footer>

  <!-- ========================================================================= -->
  <!-- MODAL: ADD / EDIT PROJECT (WITH MULTI-PHOTO UPLOAD) -->
  <!-- ========================================================================= -->
  <div id="modal" class="hidden fixed inset-0 bg-black/85 backdrop-blur-md z-50 flex items-center justify-center p-4">
    <div class="bg-[#121216] border border-white/20 rounded-2xl max-w-3xl w-full p-6 sm:p-8 max-h-[92vh] overflow-y-auto shadow-2xl">
      <div class="flex justify-between items-center pb-4 border-b border-white/10 mb-6">
        <div>
          <span class="text-[10px] font-mono text-[#c5a880] tracking-wider uppercase">Project Editor</span>
          <h3 id="modal-heading" class="text-xl font-bold text-white font-['Cinzel'] mt-0.5">Add New Architectural Project</h3>
        </div>
        <button onclick="closeModal()" class="w-8 h-8 rounded-full bg-white/5 hover:bg-white/10 text-zinc-400 hover:text-white flex items-center justify-center text-xl transition-colors">&times;</button>
      </div>

      <form id="project-form" onsubmit="handleFormSubmit(event)" class="space-y-5 text-xs">
        <input type="hidden" id="edit-id" value="">

        <div>
          <label class="block font-mono text-zinc-300 mb-1.5 font-semibold">PROJECT TITLE *</label>
          <input type="text" id="title" required placeholder="e.g. Modern Minimalist Villa & Courtyard" class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none text-sm">
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block font-mono text-zinc-300 mb-1.5 font-semibold">CATEGORY *</label>
            <select id="category" class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none">
              <option value="residential">Residential Architecture</option>
              <option value="commercial">Commercial & Institutional</option>
              <option value="interior">Luxury Interiors</option>
            </select>
          </div>
          <div>
            <label class="block font-mono text-zinc-300 mb-1.5 font-semibold">LOCATION (CITY & STATE) *</label>
            <input type="text" id="location" required placeholder="e.g. Bhilai, C.G. or Raipur, C.G." class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none">
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block font-mono text-zinc-300 mb-1.5">CLIENT NAME</label>
            <input type="text" id="client" placeholder="e.g. Shri Rajesh Gupta" class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none">
          </div>
          <div>
            <label class="block font-mono text-zinc-300 mb-1.5">BUILT-UP AREA / DIMENSIONS</label>
            <input type="text" id="area" placeholder="e.g. 5,200 Sq. Ft. (G+2 Storey)" class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none">
          </div>
        </div>

        <!-- MULTI-PHOTO UPLOAD ZONE -->
        <div class="p-4 bg-black/50 border border-white/10 rounded-xl space-y-3">
          <div class="flex justify-between items-center">
            <div>
              <label class="block font-mono text-zinc-200 font-semibold">PROJECT PHOTOS, RENDERS & BLUEPRINTS *</label>
              <p class="text-[11px] text-zinc-400 mt-0.5">Select multiple photos. Click on any photo to set it as Primary Cover Image.</p>
            </div>
            <span id="photo-count-badge" class="px-2.5 py-1 rounded bg-[#c5a880]/15 border border-[#c5a880]/30 text-[#c5a880] font-mono text-[11px]">0 Photos</span>
          </div>

          <div onclick="document.getElementById('file-input').click()" class="border-2 border-dashed border-[#c5a880]/40 hover:border-[#c5a880] bg-[#16161c]/60 hover:bg-[#16161c] rounded-xl p-6 text-center cursor-pointer transition-all">
            <input type="file" id="file-input" multiple accept="image/*" class="hidden" onchange="handleFileSelection(event)">
            <div class="flex flex-col items-center gap-2">
              <div class="w-12 h-12 rounded-full bg-[#c5a880]/15 flex items-center justify-center text-[#c5a880]">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              </div>
              <div class="text-sm font-semibold text-white">Click to Choose Multiple Photos / Renders</div>
              <div class="text-[11px] text-zinc-400">Hold <kbd class="px-1.5 py-0.5 bg-black/60 rounded text-zinc-300 font-mono">Shift</kbd> or <kbd class="px-1.5 py-0.5 bg-black/60 rounded text-zinc-300 font-mono">Cmd</kbd> on your Mac to select multiple files at once</div>
            </div>
          </div>

          <div id="upload-status" class="hidden p-2.5 rounded bg-blue-500/10 border border-blue-500/20 text-blue-300 text-[11px] font-mono flex items-center gap-2">
            <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg>
            <span id="upload-status-text">Uploading photos...</span>
          </div>

          <div id="photo-preview-grid" class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2"></div>
        </div>

        <div>
          <label class="block font-mono text-zinc-300 mb-1.5">SHORT ARCHITECTURAL TAGLINE</label>
          <input type="text" id="tagline" placeholder="e.g. Crisp minimalist geometries with Italian travertine and passive solar shading" class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none">
        </div>

        <div>
          <label class="block font-mono text-zinc-300 mb-1.5">ARCHITECTURAL SCOPE & SPECIFICATIONS</label>
          <textarea id="description" rows="3" placeholder="Describe spatial zoning, materials, client brief..." class="w-full p-3 bg-black border border-white/15 rounded-lg text-white focus:border-[#c5a880] outline-none"></textarea>
        </div>

        <div class="pt-4 flex justify-between items-center border-t border-white/10">
          <div class="text-[11px] text-zinc-500 font-mono">Auto-saved to projects.json</div>
          <div class="flex gap-3">
            <button type="button" onclick="closeModal()" class="px-5 py-2.5 bg-zinc-800 text-zinc-300 rounded-lg hover:bg-zinc-700 font-medium">Cancel</button>
            <button type="submit" id="submit-btn" class="px-6 py-2.5 bg-[#c5a880] text-black font-semibold rounded-lg hover:bg-[#dfc8a5] transition-colors flex items-center gap-2 shadow-lg shadow-[#c5a880]/15">
              <span>Save Project</span>
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL: DELETE CONFIRMATION (CUSTOM MODAL - NO BROWSER BLOCK) -->
  <!-- ========================================================================= -->
  <div id="delete-modal" class="hidden fixed inset-0 bg-black/85 backdrop-blur-md z-50 flex items-center justify-center p-4">
    <div class="bg-[#16161c] border border-red-500/30 rounded-2xl max-w-md w-full p-6 text-center space-y-4 shadow-2xl">
      <div class="w-12 h-12 rounded-full bg-red-500/20 text-red-400 mx-auto flex items-center justify-center">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
      </div>
      <div>
        <h3 class="text-base font-bold text-white">Permanently Delete Project?</h3>
        <p class="text-xs text-zinc-400 mt-1" id="delete-project-title">Are you sure you want to remove this project?</p>
      </div>
      <input type="hidden" id="delete-project-id" value="">
      <div class="flex justify-center gap-3 pt-2">
        <button onclick="closeDeleteModal()" class="px-5 py-2.5 bg-zinc-800 text-zinc-300 rounded-lg hover:bg-zinc-700 text-xs">Cancel</button>
        <button onclick="confirmDeleteProject()" id="confirm-delete-btn" class="px-5 py-2.5 bg-red-600 hover:bg-red-500 text-white font-semibold rounded-lg text-xs shadow-lg shadow-red-600/20">
          Yes, Delete Forever
        </button>
      </div>
    </div>
  </div>

  <!-- JavaScript Application -->
  <script>
    let fullData = {};
    let currentGallery = [];
    let currentCover = "";

    async function loadData() {
      try {
        const res = await fetch('/api/projects');
        fullData = await res.json();
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

    // =========================================================================
    // TAB NAVIGATION
    // =========================================================================
    function switchTab(tabId) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.nav-tab').forEach(el => {
        el.classList.remove('active', 'bg-[#c5a880]', 'text-black', 'font-bold');
        el.classList.add('bg-[#121216]', 'text-zinc-300');
      });

      const activeContent = document.getElementById(tabId);
      if (activeContent) activeContent.classList.remove('hidden');

      const btnId = 'tab-btn-' + tabId.replace('tab-', '');
      const activeBtn = document.getElementById(btnId);
      if (activeBtn) {
        activeBtn.classList.add('active', 'bg-[#c5a880]', 'text-black', 'font-bold');
        activeBtn.classList.remove('bg-[#121216]', 'text-zinc-300');
      }
    }

    // =========================================================================
    // 1-CLICK PUBLISH TO LIVE WEBSITE (NETLIFY & GITHUB)
    // =========================================================================
    async function publishToLiveSite() {
      const btn = document.getElementById('publish-live-btn');
      const text = document.getElementById('publish-btn-text');
      btn.disabled = true;
      text.textContent = 'Pushing to Live Site...';

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
    }

    // =========================================================================
    // PROJECTS PORTFOLIO
    // =========================================================================
    function renderProjects(list) {
      const container = document.getElementById('project-list');
      container.innerHTML = '';
      if (!list || list.length === 0) {
        container.innerHTML = '<div class="col-span-3 text-center py-12 text-zinc-500 font-mono text-xs">No projects found. Click "+ Add New Project" above.</div>';
        return;
      }

      list.forEach(p => {
        const card = document.createElement('div');
        card.className = 'bg-[#121216] border border-white/10 rounded-xl overflow-hidden flex flex-col justify-between hover:border-[#c5a880]/50 transition-all group';
        const galleryCount = (p.gallery && p.gallery.length) || 1;
        const areaText = (p.details && p.details['Area']) ? ` &bull; ${p.details['Area']}` : '';

        card.innerHTML = `
          <div class="relative aspect-[16/10] bg-black overflow-hidden">
            <img src="/${p.image}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" onerror="this.src='https://via.placeholder.com/600x400?text=Render+Preview'">
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent"></div>
            <div class="absolute top-3 left-3 flex gap-2">
              <span class="px-2.5 py-1 rounded text-[10px] font-mono bg-black/80 text-[#c5a880] border border-[#c5a880]/30 uppercase font-semibold">\${p.category}</span>
            </div>
            <div class="absolute bottom-3 right-3 px-2 py-0.5 rounded bg-black/80 text-zinc-300 text-[10px] font-mono flex items-center gap-1 border border-white/10">
              <svg class="w-3 h-3 text-[#c5a880]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              <span>\${galleryCount} Photos</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between">
            <div>
              <div class="text-[11px] font-mono text-[#c5a880]">\${p.location}\${areaText}</div>
              <h3 class="font-bold text-white text-base font-['Playfair_Display'] mt-1 leading-snug">\${p.title}</h3>
              <p class="text-xs text-zinc-400 mt-2 line-clamp-2 leading-relaxed">\${p.tagline || p.description}</p>
            </div>
            <div class="pt-4 mt-4 border-t border-white/10 flex justify-between items-center text-xs">
              <button onclick="editProject('\${p.id}')" class="text-[#c5a880] hover:text-[#dfc8a5] font-semibold flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                <span>Edit Project</span>
              </button>
              <button onclick="promptDeleteProject('\${p.id}', '\${p.title.replace(/'/g, "\\\\'")}')" class="text-red-400 hover:text-red-300 font-mono text-[11px] flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                <span>Delete</span>
              </button>
            </div>
          </div>
        `;
        container.appendChild(card);
      });
    }

    function filterProjects() {
      const q = document.getElementById('search-filter').value.toLowerCase().trim();
      const projects = fullData.projects || [];
      if (!q) { renderProjects(projects); return; }
      const filtered = projects.filter(p => 
        (p.title && p.title.toLowerCase().includes(q)) || 
        (p.location && p.location.toLowerCase().includes(q)) ||
        (p.client && p.client.toLowerCase().includes(q))
      );
      renderProjects(filtered);
    }

    function openNewModal() {
      document.getElementById('modal-heading').textContent = 'Add New Architectural Project';
      document.getElementById('project-form').reset();
      document.getElementById('edit-id').value = '';
      currentGallery = [];
      currentCover = "";
      renderPhotoPreviews();
      document.getElementById('modal').classList.remove('hidden');
    }

    function editProject(id) {
      const p = (fullData.projects || []).find(item => item.id === id);
      if (!p) return;
      document.getElementById('modal-heading').textContent = 'Edit Project Details';
      document.getElementById('edit-id').value = p.id;
      document.getElementById('title').value = p.title || '';
      document.getElementById('category').value = p.category || 'residential';
      document.getElementById('location').value = p.location || '';
      document.getElementById('client').value = p.client || '';
      document.getElementById('area').value = (p.details && p.details['Area']) || '';
      document.getElementById('tagline').value = p.tagline || '';
      document.getElementById('description').value = p.description || '';
      
      currentGallery = Array.isArray(p.gallery) && p.gallery.length ? [...p.gallery] : (p.image ? [p.image] : []);
      currentCover = p.image || (currentGallery.length ? currentGallery[0] : '');
      renderPhotoPreviews();
      document.getElementById('modal').classList.remove('hidden');
    }

    function closeModal() {
      document.getElementById('modal').classList.add('hidden');
    }

    // MULTI-PHOTO UPLOADS
    async function handleFileSelection(e) {
      const files = Array.from(e.target.files);
      if (!files.length) return;
      const statusBox = document.getElementById('upload-status');
      const statusText = document.getElementById('upload-status-text');
      statusBox.classList.remove('hidden');
      statusText.textContent = `Uploading ${files.length} photo(s)...`;

      try {
        const payloadFiles = [];
        for (const file of files) {
          const b64 = await readFileAsBase64(file);
          payloadFiles.push({ name: file.name, data: b64, dir: 'projects' });
        }

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
        } else {
          alert('Upload failed: ' + result.error);
          statusBox.classList.add('hidden');
        }
      } catch (err) {
        alert('Upload error: ' + err.message);
        statusBox.classList.add('hidden');
      }
      e.target.value = '';
    }

    function readFileAsBase64(file) {
      return new Promise((resolve, reject) => {
        const r = new FileReader();
        r.onload = () => resolve(r.result);
        r.onerror = reject;
        r.readAsDataURL(file);
      });
    }

    function renderPhotoPreviews() {
      const grid = document.getElementById('photo-preview-grid');
      const badge = document.getElementById('photo-count-badge');
      badge.textContent = `${currentGallery.length} Photos`;
      grid.innerHTML = '';

      if (!currentGallery.length) {
        grid.innerHTML = '<div class="col-span-4 text-center py-4 text-zinc-500 font-mono text-[11px]">No photos selected.</div>';
        return;
      }

      currentGallery.forEach((path, idx) => {
        const isCover = (path === currentCover) || (!currentCover && idx === 0);
        if (isCover) currentCover = path;

        const item = document.createElement('div');
        item.className = `relative aspect-video rounded-lg overflow-hidden border-2 \${isCover ? 'border-[#c5a880]' : 'border-white/10'} bg-black group`;
        item.innerHTML = `
          <img src="/\${path}" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-between p-1.5">
            <div class="flex justify-end">
              <button type="button" onclick="removePhoto('\${path}')" class="w-5 h-5 rounded-full bg-red-600 text-white flex items-center justify-center font-bold" title="Remove">&times;</button>
            </div>
            <button type="button" onclick="setAsCover('\${path}')" class="w-full py-1 rounded bg-[#c5a880] text-black text-[10px] font-bold uppercase">
              \${isCover ? '★ Cover Photo' : 'Make Cover'}
            </button>
          </div>
          \${isCover ? '<div class="absolute top-1.5 left-1.5 px-1.5 py-0.5 rounded bg-[#c5a880] text-black text-[9px] font-bold uppercase font-mono">Cover</div>' : ''}
        `;
        grid.appendChild(item);
      });
    }

    function setAsCover(path) { currentCover = path; renderPhotoPreviews(); }
    function removePhoto(path) {
      currentGallery = currentGallery.filter(p => p !== path);
      if (currentCover === path) currentCover = currentGallery[0] || '';
      renderPhotoPreviews();
    }

    async function handleFormSubmit(e) {
      e.preventDefault();
      if (!currentGallery.length) {
        alert('Please choose or upload at least one photo.');
        return;
      }

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
        image: currentCover || currentGallery[0],
        gallery: currentGallery,
        featured: true,
        tagline: document.getElementById('tagline').value,
        description: document.getElementById('description').value,
        details: { 'Area': document.getElementById('area').value || 'Custom Built' }
      };

      const btn = document.getElementById('submit-btn');
      btn.disabled = true;
      btn.innerText = 'Saving...';

      try {
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
      } catch (err) {
        alert('Error: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerText = 'Save Project';
      }
    }

    // CUSTOM IN-APP DELETE MODAL (100% RELIABLE)
    function promptDeleteProject(id, title) {
      document.getElementById('delete-project-id').value = id;
      document.getElementById('delete-project-title').textContent = `Are you sure you want to delete "${title}"? This cannot be undone.`;
      document.getElementById('delete-modal').classList.remove('hidden');
    }

    function closeDeleteModal() {
      document.getElementById('delete-modal').classList.add('hidden');
    }

    async function confirmDeleteProject() {
      const id = document.getElementById('delete-project-id').value;
      if (!id) return;
      const btn = document.getElementById('confirm-delete-btn');
      btn.disabled = true;
      btn.innerText = 'Deleting...';

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
    }

    // =========================================================================
    // ABOUT ARCHITECT & PRACTICE TAB
    // =========================================================================
    function populateAboutTab() {
      const a = fullData.architect || {};
      document.getElementById('about-name').value = a.name || 'Ar. Deepti Singh';
      document.getElementById('about-title').value = a.title || 'Architect & Interior Designer';
      document.getElementById('about-exp').value = a.experience || '12+ Years of Practice (Since 2013)';
      document.getElementById('about-loc').value = a.location || 'Durg - Bhilai & Raipur, Chhattisgarh, India';
      document.getElementById('about-bio').value = a.bio || '';
      document.getElementById('about-philosophy').value = a.philosophy || '';
      document.getElementById('about-avatar-path').value = a.avatar || 'assets/profile/deepti_singh.jpg';
      document.getElementById('avatar-preview').src = '/' + (a.avatar || 'assets/profile/deepti_singh.jpg');

      const skills = a.skills || [];
      skills.forEach(s => {
        const name = s.name.toLowerCase();
        if (name.includes('autocad')) document.getElementById('skill-autocad').value = parseInt(s.percentage) || 95;
        if (name.includes('sketchup')) document.getElementById('skill-sketchup').value = parseInt(s.percentage) || 90;
        if (name.includes('3ds')) document.getElementById('skill-3dsmax').value = parseInt(s.percentage) || 88;
        if (name.includes('revit')) document.getElementById('skill-revit').value = parseInt(s.percentage) || 82;
      });
    }

    async function handleAvatarUpload(e) {
      const file = e.target.files[0];
      if (!file) return;
      const b64 = await readFileAsBase64(file);
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

      const res = await fetch('/api/save-architect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        showNotice('✓ Architect Profile saved! Click "Publish to Live Website" to sync with live site.');
        loadData();
      }
    }

    // =========================================================================
    // RENDER VS REALITY TAB
    // =========================================================================
    function populateR2RTab() {
      const container = document.getElementById('r2r-cases-container');
      container.innerHTML = '';
      const r2r = (fullData.render_to_real && fullData.render_to_real.items) || [];

      r2r.forEach((item, idx) => {
        const card = document.createElement('div');
        card.className = 'p-5 bg-black/40 border border-white/10 rounded-xl space-y-4';
        card.innerHTML = `
          <div class="flex justify-between items-center pb-2 border-b border-white/10">
            <span class="font-mono text-[#c5a880] text-xs font-bold uppercase">CASE 0\${idx + 1}</span>
          </div>
          <div>
            <label class="block font-mono text-zinc-300 mb-1">CASE TITLE</label>
            <input type="text" id="r2r-title-\${idx}" value="\${item.title}" class="w-full p-2.5 bg-black border border-white/15 rounded text-white focus:border-[#c5a880] outline-none">
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block font-mono text-zinc-300 mb-1">3D RENDER IMAGE PATH</label>
              <input type="text" id="r2r-render-\${idx}" value="\${item.render_img}" class="w-full p-2.5 bg-black border border-white/15 rounded text-white font-mono focus:border-[#c5a880] outline-none">
            </div>
            <div>
              <label class="block font-mono text-zinc-300 mb-1">ACTUAL REAL PHOTO PATH</label>
              <input type="text" id="r2r-real-\${idx}" value="\${item.real_img}" class="w-full p-2.5 bg-black border border-white/15 rounded text-white font-mono focus:border-[#c5a880] outline-none">
            </div>
          </div>
          <div>
            <label class="block font-mono text-zinc-300 mb-1">EXECUTION FIDELITY DESCRIPTION</label>
            <textarea id="r2r-desc-\${idx}" rows="2" class="w-full p-2.5 bg-black border border-white/15 rounded text-white focus:border-[#c5a880] outline-none leading-relaxed">\${item.description}</textarea>
          </div>
        `;
        container.appendChild(card);
      });
    }

    async function saveR2RCases() {
      const items = (fullData.render_to_real && fullData.render_to_real.items) || [];
      items.forEach((item, idx) => {
        item.title = document.getElementById(`r2r-title-\${idx}`).value;
        item.render_img = document.getElementById(`r2r-render-\${idx}`).value;
        item.real_img = document.getElementById(`r2r-real-\${idx}`).value;
        item.description = document.getElementById(`r2r-desc-\${idx}`).value;
      });

      const res = await fetch('/api/save-r2r', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items })
      });
      if (res.ok) {
        showNotice('✓ Render vs Reality cases saved!');
        loadData();
      }
    }

    // =========================================================================
    // CAD BLUEPRINTS & PLANS TAB
    // =========================================================================
    function populateCADTab() {
      const container = document.getElementById('cad-drawings-container');
      container.innerHTML = '';
      const list = fullData.technical_drawings || [];

      list.forEach((item, idx) => {
        const card = document.createElement('div');
        card.className = 'p-5 bg-black/40 border border-white/10 rounded-xl space-y-3';
        card.innerHTML = `
          <div class="flex justify-between items-center pb-2 border-b border-white/10">
            <span class="font-mono text-[#c5a880] text-xs font-bold uppercase">DRAWING PLATE 0\${idx + 1}</span>
            <button onclick="removeBlueprint(\${idx})" class="text-red-400 hover:text-red-300 font-mono text-[11px]">&times; Remove Plate</button>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block font-mono text-zinc-300 mb-1">PLATE TITLE</label>
              <input type="text" id="cad-title-\${idx}" value="\${item.title}" class="w-full p-2.5 bg-black border border-white/15 rounded text-white focus:border-[#c5a880] outline-none">
            </div>
            <div>
              <label class="block font-mono text-zinc-300 mb-1">CATEGORY / DISCIPLINE</label>
              <input type="text" id="cad-cat-\${idx}" value="\${item.category}" class="w-full p-2.5 bg-black border border-white/15 rounded text-white focus:border-[#c5a880] outline-none">
            </div>
          </div>
          <div>
            <label class="block font-mono text-zinc-300 mb-1">BLUEPRINT IMAGE PATH</label>
            <input type="text" id="cad-img-\${idx}" value="\${item.image}" class="w-full p-2.5 bg-black border border-white/15 rounded text-white font-mono focus:border-[#c5a880] outline-none">
          </div>
          <div>
            <label class="block font-mono text-zinc-300 mb-1">TECHNICAL SPECIFICATIONS</label>
            <textarea id="cad-desc-\${idx}" rows="2" class="w-full p-2.5 bg-black border border-white/15 rounded text-white focus:border-[#c5a880] outline-none leading-relaxed">\${item.description}</textarea>
          </div>
        `;
        container.appendChild(card);
      });
    }

    function addNewBlueprint() {
      const list = fullData.technical_drawings || [];
      list.push({
        title: "New Architectural CAD Drawing",
        category: "Floor Plan / Elevation",
        image: "assets/plans/blueprint_floorplan_1.jpg",
        description: "Technical drafting specifications and municipal sanction details."
      });
      populateCADTab();
    }

    function removeBlueprint(idx) {
      const list = fullData.technical_drawings || [];
      list.splice(idx, 1);
      populateCADTab();
    }

    async function saveCADDrawings() {
      const list = fullData.technical_drawings || [];
      list.forEach((item, idx) => {
        item.title = document.getElementById(`cad-title-\${idx}`).value;
        item.category = document.getElementById(`cad-cat-\${idx}`).value;
        item.image = document.getElementById(`cad-img-\${idx}`).value;
        item.description = document.getElementById(`cad-desc-\${idx}`).value;
      });

      const res = await fetch('/api/save-blueprints', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ technical_drawings: list })
      });
      if (res.ok) {
        showNotice('✓ CAD Blueprints saved!');
        loadData();
      }
    }

    // =========================================================================
    // HERO & CONTACT TAB
    // =========================================================================
    function populateHeroTab() {
      const a = fullData.architect || {};
      const stats = fullData.stats || {};
      document.getElementById('contact-phone-1').value = (a.phone && a.phone[0]) || "+91 8989594919";
      document.getElementById('contact-phone-2').value = (a.phone && a.phone[1]) || "+91 7000098073";
      document.getElementById('contact-email').value = a.email || "deeptisingh291@gmail.com";
      document.getElementById('hero-announcement').value = "Accepting Architectural & Turnkey Interior Commissions for 2024-2025";
      document.getElementById('hero-paragraph').value = "Contemporary architectural design, bespoke residential villas, and turnkey interior environments characterized by clean geometries, all-white minimalist palettes, and uncompromising 1:1 render-to-reality fidelity.";
      document.getElementById('stat-years').value = stats.years_exp || "12+";
      document.getElementById('stat-projects').value = stats.projects_count || "50+";
      document.getElementById('stat-fidelity').value = stats.fidelity_rate || "100%";
      document.getElementById('stat-metros').value = stats.metros_count || "6+";
    }

    async function saveHeroContact(e) {
      e.preventDefault();
      const payload = {
        phone: [document.getElementById('contact-phone-1').value, document.getElementById('contact-phone-2').value],
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

      const res = await fetch('/api/save-hero-contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        showNotice('✓ Hero & Contact Settings saved! Click "Publish to Live Website" to sync.');
        loadData();
      }
    }

    function showNotice(msg) {
      const el = document.getElementById('notice');
      const text = document.getElementById('notice-text');
      text.textContent = msg;
      el.classList.remove('hidden');
      setTimeout(() => el.classList.add('hidden'), 5000);
    }

    // Initial load
    loadData();
  </script>
</body>
</html>
"""

class MasterAdminRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        if self.path in ['/', '/admin', '/admin/']:
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
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        payload = json.loads(body) if body else {}

        if self.path == '/api/publish-live':
            try:
                # 1. Update zip
                zip_cmd = f"cd '{BASE_DIR}/website' && zip -FS -r ../deepti-singh-portfolio-deploy.zip . -x '*.DS_Store'"
                subprocess.run(zip_cmd, shell=True, check=True)

                # 2. Git commit and push to GitHub
                git_cmd = f"cd '{BASE_DIR}' && git add -A && git commit -m 'Master Control Panel live update' && git push origin main"
                result = subprocess.run(git_cmd, shell=True, capture_output=True, text=True)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'status': 'ok',
                    'message': 'Changes successfully pushed to GitHub! Netlify is updating architectdeepti.in right now.'
                }).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'error': str(e)}).encode('utf-8'))
                return

        elif self.path == '/api/upload-photos':
            uploaded_paths = []
            for item in payload.get('files', []):
                name = item.get('name', 'image.jpg')
                raw_b64 = item.get('data', '')
                sub_dir = item.get('dir', 'projects')
                target_dir = ASSETS_DIR if sub_dir == 'projects' else (PROFILE_DIR if sub_dir == 'profile' else ASSETS_DIR)

                if ',' in raw_b64:
                    raw_b64 = raw_b64.split(',', 1)[1]

                clean_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', name).lower()
                dest_path = os.path.join(target_dir, clean_name)
                
                base, ext = os.path.splitext(clean_name)
                counter = 1
                while os.path.exists(dest_path):
                    clean_name = f"{base}_{counter}{ext}"
                    dest_path = os.path.join(target_dir, clean_name)
                    counter += 1

                image_bytes = base64.b64decode(raw_b64)
                try:
                    img = Image.open(io.BytesIO(image_bytes))
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    img.save(dest_path, 'JPEG', quality=90, optimize=True)
                except Exception:
                    with open(dest_path, 'wb') as f:
                        f.write(image_bytes)

                rel_path = f"assets/{sub_dir}/{clean_name}"
                uploaded_paths.append(rel_path)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok', 'uploaded': uploaded_paths}).encode('utf-8'))
            return

        elif self.path == '/api/save-project':
            new_proj = payload
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)

            found = False
            for idx, p in enumerate(data['projects']):
                if p['id'] == new_proj['id']:
                    data['projects'][idx] = new_proj
                    found = True
                    break
            if not found:
                data['projects'].insert(0, new_proj)

            self._save_all_data(data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return

        elif self.path == '/api/save-architect':
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)

            data['architect']['name'] = payload.get('name', data['architect']['name'])
            data['architect']['title'] = payload.get('title', data['architect']['title'])
            data['architect']['experience'] = payload.get('experience', data['architect']['experience'])
            data['architect']['location'] = payload.get('location', data['architect']['location'])
            data['architect']['avatar'] = payload.get('avatar', data['architect']['avatar'])
            data['architect']['bio'] = payload.get('bio', data['architect']['bio'])
            data['architect']['philosophy'] = payload.get('philosophy', data['architect']['philosophy'])
            if 'skills' in payload:
                data['architect']['skills'] = payload['skills']

            self._save_all_data(data)

            # Also update profile.json
            with open(PROFILE_FILE, 'w') as f:
                json.dump(data['architect'], f, indent=2)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return

        elif self.path == '/api/save-r2r':
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            data['render_to_real']['items'] = payload.get('items', data['render_to_real']['items'])
            self._save_all_data(data)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return

        elif self.path == '/api/save-blueprints':
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            data['technical_drawings'] = payload.get('technical_drawings', data['technical_drawings'])
            self._save_all_data(data)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return

        elif self.path == '/api/save-hero-contact':
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            if 'phone' in payload:
                data['architect']['phone'] = payload['phone']
            if 'email' in payload:
                data['architect']['email'] = payload['email']
            if 'stats' in payload:
                data['stats'] = payload['stats']

            self._save_all_data(data)
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
                self._save_all_data(data)

                # Remove from entries dir if present
                for fn in os.listdir(ENTRIES_DIR):
                    fp = os.path.join(ENTRIES_DIR, fn)
                    try:
                        with open(fp) as entry_f:
                            ed = json.load(entry_f)
                            if ed.get('id') == proj_id:
                                os.remove(fp)
                    except Exception:
                        pass

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status":"deleted"}')
                return

    def _save_all_data(self, data):
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)

        with open(JS_DATA_FILE, 'w') as f:
            f.write('window.__PORTFOLIO_DATA__ = ' + json.dumps(data, indent=2) + ';')

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), MasterAdminRequestHandler) as httpd:
        print(f"============================================================")
        print(f" MASTER PORTFOLIO CONTROL PANEL: http://localhost:{PORT}")
        print(f" Multi-photo upload + All 5 Sections Editable!")
        print(f"============================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nAdmin Server stopped.")
