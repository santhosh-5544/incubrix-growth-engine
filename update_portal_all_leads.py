import json
import re

# Read all 1000 leads
with open('all_leads.json', 'r', encoding='utf-8') as f:
    all_leads = json.load(f)

# Read 25 priority A leads
with open('priority_a_full.json', 'r', encoding='utf-8') as f:
    priority_a_full = json.load(f)

print(f"Loaded {len(all_leads)} leads and {len(priority_a_full)} priority A leads.")

# Read build_master_portal.py template
with open('build_master_portal.py', 'r', encoding='utf-8') as f:
    portal_code = f.read()

# Replace sample_leads.json with all_leads.json in the file loader
portal_code = portal_code.replace("with open('sample_leads.json'", "with open('all_leads.json'")

# Now let's inject pagination styling into CSS
pagination_css = """
    /* Pagination Controls */
    .pagination-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 1.25rem;
      flex-wrap: wrap;
      gap: 1rem;
    }
    .pagination-info {
      color: var(--text-dim);
      font-size: 0.85rem;
    }
    .pagination-controls {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .page-btn {
      background: rgba(31, 41, 55, 0.6);
      border: 1px solid var(--card-border-glow);
      color: white;
      padding: 0.4rem 0.85rem;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.8rem;
      font-weight: 600;
      transition: all 0.15s;
    }
    .page-btn:hover:not(:disabled) {
      background: var(--primary);
      border-color: var(--primary);
    }
    .page-btn:disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }
    .page-indicator {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: #A5B4FC;
      padding: 0 0.5rem;
    }
    .page-size-select {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 6px;
      color: #CBD5E1;
      padding: 0.35rem 0.6rem;
      font-size: 0.8rem;
    }
"""

if '/* Pagination Controls */' not in portal_code:
    portal_code = portal_code.replace("/* Table Styles */", pagination_css + "\n    /* Table Styles */")

# Add pagination controls below table in HTML
pagination_html = """    </div>
    
    <div class="pagination-bar">
      <div class="pagination-info" id="pageInfo">Showing 1–25 of 1,000 creators</div>
      <div class="pagination-controls">
        <label style="font-size: 0.8rem; color: var(--text-dim); margin-right: 0.25rem;">Rows:</label>
        <select id="pageSizeSelect" class="page-size-select" onchange="changePageSize(this.value)">
          <option value="25" selected>25</option>
          <option value="50">50</option>
          <option value="100">100</option>
          <option value="250">250</option>
          <option value="1000">All 1,000</option>
        </select>
        <button id="prevBtn" class="page-btn" onclick="prevPage()">◀ Prev</button>
        <span id="pageIndicator" class="page-indicator">Page 1 of 40</span>
        <button id="nextBtn" class="page-btn" onclick="nextPage()">Next ▶</button>
      </div>
    </div>
    <p style="margin-top: 1rem; color: var(--text-dim); font-size: 0.85rem; text-align: center;">
      Full 1,000 qualified dataset with 30 columns is verified in <a href="https://github.com/santhosh-5544/incubrix-growth-engine/blob/main/output/leads.csv" target="_blank" style="color: var(--accent);">output/leads.csv</a>.
    </p>"""

portal_code = re.sub(
    r'\s*</div>\s*<p style="margin-top: 1rem; color: var\(--text-dim\); font-size: 0\.85rem; text-align: center;">\s*Showing interactive preview.*?output/leads\.csv</a>\.\s*</p>',
    "\n" + pagination_html,
    portal_code,
    flags=re.DOTALL
)

# Update JavaScript to handle pagination
old_js = """    function renderLeads(leads) {
      const tbody = document.getElementById('leadsTableBody');
      tbody.innerHTML = '';
      leads.forEach(lead => {
        const tr = document.createElement('tr');
        tr.className = 'lead-row';
        tr.onclick = () => openModal(lead);
        const priBadge = lead.priority === 'A' 
          ? '<span class="badge-pill badge-pri-a">Priority A</span>'
          : '<span class="badge-pill badge-pri-b">Priority B</span>';
        
        tr.innerHTML = `
          <td><strong>${lead.lead_id}</strong></td>
          <td><strong>${lead.name}</strong></td>
          <td style="text-transform: capitalize;">${lead.segment}</td>
          <td>${lead.country}</td>
          <td>${priBadge}</td>
          <td><span class="score-badge">${lead.score.toFixed(1)}</span></td>
          <td><span class="channel-badge">${lead.best_channel}</span></td>
          <td><span style="font-size: 0.775rem; color: #94A3B8;">${lead.monetization}</span></td>
          <td><span style="font-size: 0.775rem; color: #94A3B8;">${lead.need}</span></td>
        `;
        tbody.appendChild(tr);
      });
    }

    function filterLeads() {
      const q = document.getElementById('searchInput').value.toLowerCase();
      const country = document.getElementById('countryFilter').value;
      const segment = document.getElementById('segmentFilter').value.toLowerCase();
      const priority = document.getElementById('priorityFilter').value;

      const filtered = leadsData.filter(l => {
        const matchesQ = !q || l.name.toLowerCase().includes(q) || l.lead_id.toLowerCase().includes(q) || l.need.toLowerCase().includes(q);
        const matchesCountry = !country || l.country === country;
        const matchesSegment = !segment || l.segment.toLowerCase().includes(segment);
        const matchesPriority = !priority || l.priority === priority;
        return matchesQ && matchesCountry && matchesSegment && matchesPriority;
      });
      renderLeads(filtered);
    }"""

new_js = """    let currentPage = 1;
    let pageSize = 25;
    let filteredLeads = leadsData;

    function renderLeadsTable() {
      const total = filteredLeads.length;
      const totalPages = Math.ceil(total / pageSize) || 1;
      if (currentPage > totalPages) currentPage = totalPages;
      if (currentPage < 1) currentPage = 1;

      const start = (currentPage - 1) * pageSize;
      const end = Math.min(start + pageSize, total);
      const paged = filteredLeads.slice(start, end);

      const tbody = document.getElementById('leadsTableBody');
      tbody.innerHTML = '';

      if (paged.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align:center; padding: 2rem; color: var(--text-dim);">No matching creators found</td></tr>';
      } else {
        paged.forEach(lead => {
          const tr = document.createElement('tr');
          tr.className = 'lead-row';
          tr.onclick = () => openModal(lead);
          const priBadge = lead.priority === 'A' 
            ? '<span class="badge-pill badge-pri-a">Priority A</span>'
            : '<span class="badge-pill badge-pri-b">Priority B</span>';
          
          tr.innerHTML = `
            <td><strong>${lead.lead_id}</strong></td>
            <td><strong>${lead.name}</strong></td>
            <td style="text-transform: capitalize;">${lead.segment}</td>
            <td>${lead.country}</td>
            <td>${priBadge}</td>
            <td><span class="score-badge">${lead.score.toFixed(1)}</span></td>
            <td><span class="channel-badge">${lead.best_channel}</span></td>
            <td><span style="font-size: 0.775rem; color: #94A3B8;">${lead.monetization}</span></td>
            <td><span style="font-size: 0.775rem; color: #94A3B8;">${lead.need}</span></td>
          `;
          tbody.appendChild(tr);
        });
      }

      document.getElementById('pageInfo').innerText = `Showing ${total === 0 ? 0 : start + 1}–${end} of ${total.toLocaleString()} creators`;
      document.getElementById('pageIndicator').innerText = `Page ${currentPage} of ${totalPages}`;
      document.getElementById('prevBtn').disabled = currentPage <= 1;
      document.getElementById('nextBtn').disabled = currentPage >= totalPages;
    }

    function filterLeads() {
      const q = document.getElementById('searchInput').value.toLowerCase();
      const country = document.getElementById('countryFilter').value;
      const segment = document.getElementById('segmentFilter').value.toLowerCase();
      const priority = document.getElementById('priorityFilter').value;

      filteredLeads = leadsData.filter(l => {
        const matchesQ = !q || l.name.toLowerCase().includes(q) || l.lead_id.toLowerCase().includes(q) || l.need.toLowerCase().includes(q);
        const matchesCountry = !country || l.country === country;
        const matchesSegment = !segment || l.segment.toLowerCase().includes(segment);
        const matchesPriority = !priority || l.priority === priority;
        return matchesQ && matchesCountry && matchesSegment && matchesPriority;
      });
      currentPage = 1;
      renderLeadsTable();
    }

    function nextPage() {
      currentPage++;
      renderLeadsTable();
    }
    function prevPage() {
      currentPage--;
      renderLeadsTable();
    }
    function changePageSize(size) {
      pageSize = parseInt(size, 10);
      currentPage = 1;
      renderLeadsTable();
    }"""

portal_code = portal_code.replace(old_js, new_js)
portal_code = portal_code.replace("renderLeads(leadsData);", "renderLeadsTable();")

# Save updated build_master_portal.py
with open('build_master_portal.py', 'w', encoding='utf-8') as f:
    f.write(portal_code)

print("Updated build_master_portal.py with all 1,000 leads and pagination controls.")
