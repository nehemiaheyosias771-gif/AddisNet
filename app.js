/* =============================================
   ADDISNET — Core Application JavaScript
   ============================================= */

'use strict';

// ── APP STATE ──
const AppState = {
  currentPage: 'dashboard',
  darkMode: true,
  sidebarCollapsed: false,
  language: 'en',
  fontSize: 'normal',
  highContrast: false,
  emergencyActive: true,
  liveUpdateInterval: null,
  activityInterval: null,
  iotInterval: null,
  chartInstances: {},
  votes: {},
  upvotes: {}
};

// ── TRANSLATIONS ──
const translations = {
  en: {
    dashboard: 'Dashboard',
    report: 'Report Issue',
    map: 'City Map',
    community: 'Community',
    analytics: 'Analytics',
    budget: 'Budgeting',
    settings: 'Settings',
    emergency: 'Emergency',
    greeting: 'Good morning',
    totalIssues: 'Total Issues',
    activeReports: 'Active Reports',
    volunteers: 'Volunteers',
    resolved: 'Resolved Today',
    liveActivity: 'Live Activity',
    quickActions: 'Quick Actions',
    reportIssue: 'Report Issue',
    viewMap: 'View Map',
    joinCommunity: 'Join Community',
    viewAnalytics: 'View Analytics',
  },
  am: {
    dashboard: 'ዳሽቦርድ',
    report: 'ጉዳይ ሪፖርት',
    map: 'ካርታ',
    community: 'ማህበረሰብ',
    analytics: 'ትንተና',
    budget: 'በጀት',
    settings: 'ቅንብሮች',
    emergency: 'አደጋ',
    greeting: 'እንደምን አደሩ',
    totalIssues: 'ጠቅላላ ጉዳዮች',
    activeReports: 'ንቁ ሪፖርቶች',
    volunteers: 'በጎ ፈቃደኞች',
    resolved: 'ዛሬ የተፈቱ',
    liveActivity: 'ቀጥታ እንቅስቃሴ',
    quickActions: 'ፈጣን ድርጊቶች',
    reportIssue: 'ጉዳይ ሪፖርት አድርግ',
    viewMap: 'ካርታ ይመልከቱ',
    joinCommunity: 'ማህበረሰቡን ይቀላቀሉ',
    viewAnalytics: 'ትንተና ይመልከቱ',
  }
};

// ── MOCK DATA ──
const MockData = {
  activities: [
    { type: 'red', title: 'Road damage reported on Bole Road', meta: 'Reported by Tigist M. • Severity: High', time: '2m ago' },
    { type: 'green', title: 'Waste collection completed in Piassa', meta: 'Resolved by City Sanitation Team', time: '8m ago' },
    { type: 'yellow', title: 'Street light outage in Kazanchis', meta: 'Pending review • 3 upvotes', time: '15m ago' },
    { type: 'blue', title: 'New volunteer joined in Megenagna', meta: 'Abebe K. joined the cleanup drive', time: '23m ago' },
    { type: 'green', title: 'Water supply restored in Merkato', meta: 'Issue #4421 closed successfully', time: '31m ago' },
    { type: 'red', title: 'Flooding reported near Mexico Square', meta: 'Emergency team dispatched', time: '45m ago' },
    { type: 'yellow', title: 'Noise complaint in Bole Michael', meta: 'Under investigation by authorities', time: '1h ago' },
    { type: 'blue', title: 'Community meeting scheduled in CMC', meta: '47 residents RSVP\'d', time: '2h ago' },
  ],
  newActivities: [
    { type: 'red', title: 'Pothole spotted near Meskel Square', meta: 'Just reported by a resident', time: 'just now' },
    { type: 'blue', title: 'New community post about park renovation', meta: '12 people interested', time: 'just now' },
    { type: 'green', title: 'Issue #5103 marked as resolved', meta: 'Street cleaning completed', time: 'just now' },
    { type: 'yellow', title: 'Traffic congestion alert on Ring Road', meta: 'Expected to clear in 30 min', time: 'just now' },
    { type: 'red', title: 'Power outage in Lideta sub-city', meta: 'EEP team en route', time: 'just now' },
  ],
  posts: [
    {
      id: 1,
      author: 'Abebe Kebede',
      avatar: '#078930',
      initials: 'AK',
      date: '2 hours ago',
      title: 'Proposal: Convert Megenagna Roundabout into a Green Space',
      body: 'The Megenagna roundabout is currently underutilized and contributes to traffic congestion. I propose we work with the city to convert it into a pedestrian-friendly green space with local plants and seating. This would improve air quality and give residents a place to gather.',
      tags: ['Environment', 'Urban Planning', 'Traffic'],
      upvotes: 124,
    },
    {
      id: 2,
      author: 'Meron Tadesse',
      avatar: '#FCDD09',
      initials: 'MT',
      date: '5 hours ago',
      title: 'Request for Improved Lighting on Bole Road at Night',
      body: 'Walking home after evening hours on Bole Road is unsafe due to inadequate street lighting. Several residents have raised concerns. Can we escalate this to the city infrastructure team?',
      tags: ['Safety', 'Infrastructure', 'Lighting'],
      upvotes: 89,
    },
    {
      id: 3,
      author: 'Dawit Haile',
      avatar: '#DA121A',
      initials: 'DH',
      date: '1 day ago',
      title: 'Community Cleanup Drive This Saturday in Piassa',
      body: 'Organizing a community cleanup in Piassa market area this Saturday at 8AM. We have 30+ volunteers ready. Looking for partnerships with local businesses for supplies and disposal.',
      tags: ['Community', 'Environment', 'Volunteering'],
      upvotes: 203,
    },
    {
      id: 4,
      author: 'Selamawit Girma',
      avatar: '#3b8dff',
      initials: 'SG',
      date: '2 days ago',
      title: 'Air Quality in Akaki Kaliti Needs Urgent Attention',
      body: 'Factory emissions in Akaki Kaliti are affecting air quality for thousands of residents. The EPA sensors show PM2.5 levels above safe thresholds on 12 of the last 30 days. We need enforcement action.',
      tags: ['Health', 'Environment', 'Policy'],
      upvotes: 167,
    }
  ],
  budgetProjects: [
    { id: 1, name: 'Entoto Park Expansion', amount: '₿ 4.2M Birr', desc: 'Expand the green area and add recreational facilities for families in northern Addis Ababa.', votes: 1247, target: 2000, category: 'Environment' },
    { id: 2, name: 'Bole Road Smart Traffic System', amount: '₿ 7.8M Birr', desc: 'Install AI-powered traffic lights and sensors along Bole Road to reduce congestion by 40%.', votes: 983, target: 2000, category: 'Infrastructure' },
    { id: 3, name: 'Merkato Market Digital Registry', amount: '₿ 2.1M Birr', desc: 'Digitize vendor registration and tax records for Merkato, Africa\'s largest open market.', votes: 756, target: 2000, category: 'Economy' },
    { id: 4, name: 'Addis Ababa Flood Early Warning System', amount: '₿ 5.5M Birr', desc: 'Deploy sensor networks in flood-prone areas to give 72h advance warning to residents.', votes: 1891, target: 2000, category: 'Safety' },
  ],
  iotData: {
    airQuality: 72,
    traffic: 64,
    waterPressure: 88,
    noise: 45
  }
};

// ── INITIALIZATION ──
document.addEventListener('DOMContentLoaded', () => {
  initApp();
});

function initApp() {
  setupNavigation();
  setupSidebar();
  setupTopbar();
  setupEmergencyAlert();
  setupToasts();
  startLiveUpdates();
  initPage('dashboard');
  loadThemePreference();
  updateTranslations();
}

// ── NAVIGATION ──
function setupNavigation() {
  document.querySelectorAll('[data-page]').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const page = link.dataset.page;
      navigateTo(page);
    });
  });
}

function navigateTo(page) {
  AppState.currentPage = page;

  // Update nav links
  document.querySelectorAll('[data-page]').forEach(link => {
    link.classList.toggle('active', link.dataset.page === page);
  });

  // Switch pages
  document.querySelectorAll('.page').forEach(p => {
    p.classList.remove('active');
  });

  const target = document.getElementById(`page-${page}`);
  if (target) {
    target.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Update topbar title
  const pageNames = {
    dashboard: 'Dashboard',
    report: 'Report Issue',
    map: 'City Map',
    community: 'Community Board',
    analytics: 'Analytics',
    budget: 'Participatory Budgeting',
    settings: 'Settings',
    emergency: 'Emergency Management'
  };
  const titleEl = document.querySelector('.topbar-title');
  if (titleEl) titleEl.textContent = pageNames[page] || page;

  initPage(page);

  // Close mobile sidebar
  document.querySelector('.sidebar')?.classList.remove('mobile-open');
}

function initPage(page) {
  switch (page) {
    case 'dashboard': initDashboard(); break;
    case 'map': initMap(); break;
    case 'analytics': initAnalytics(); break;
    case 'community': initCommunity(); break;
    case 'budget': initBudget(); break;
    case 'report': initReport(); break;
    case 'settings': initSettings(); break;
  }
}

// ── SIDEBAR ──
function setupSidebar() {
  const toggleBtn = document.getElementById('sidebarToggle');
  const mobileToggle = document.getElementById('mobileSidebarToggle');
  const sidebar = document.querySelector('.sidebar');
  const mainContent = document.querySelector('.main-content');
  const topbar = document.querySelector('.topbar');

  // On small screens, show the mobile sidebar toggle button
  if (mobileToggle && window.innerWidth <= 768) {
    mobileToggle.style.display = 'flex';
  }

  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      AppState.sidebarCollapsed = !AppState.sidebarCollapsed;
      sidebar?.classList.toggle('collapsed', AppState.sidebarCollapsed);
      mainContent?.classList.toggle('sidebar-collapsed', AppState.sidebarCollapsed);
      topbar?.classList.toggle('sidebar-collapsed', AppState.sidebarCollapsed);
    });
  }

  if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
      sidebar?.classList.toggle('mobile-open');
    });
  }
}

// ── TOPBAR ──
function setupTopbar() {
  const searchInput = document.querySelector('.search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const val = e.target.value;
      if (val.length > 2) {
        // Simulate AI search suggestions
        showToast('info', 'Smart Search', `Found results for "${val}"`, 2000);
      }
    });
  }
}

// ── EMERGENCY ALERT ──
function setupEmergencyAlert() {
  const banner = document.getElementById('emergencyBanner');
  const closeBtn = document.getElementById('emergencyClose');
  const triggerBtn = document.getElementById('triggerEmergency');

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      banner?.classList.add('hidden');
      AppState.emergencyActive = false;
    });
  }

  if (triggerBtn) {
    triggerBtn.addEventListener('click', () => {
      banner?.classList.remove('hidden');
      AppState.emergencyActive = true;
      showToast('error', 'Emergency Alert', 'New emergency alert has been broadcast!');
    });
  }
}

// ── TOAST SYSTEM ──
function setupToasts() {
  // Ensure container exists
  if (!document.querySelector('.toast-container')) {
    const tc = document.createElement('div');
    tc.className = 'toast-container';
    document.body.appendChild(tc);
  }
}

function showToast(type, title, message, duration = 4500) {
  const container = document.querySelector('.toast-container');
  if (!container) return;

  const icons = { success: 'OK', error: 'ERR', warning: 'WARN', info: 'INFO' };
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${icons[type] || 'MSG'}</span>
    <div class="toast-content">
      <div class="toast-title">${title}</div>
      <div class="toast-message">${message}</div>
    </div>
    <button class="toast-close" onclick="removeToast(this.parentElement)">✕</button>
  `;

  container.appendChild(toast);

  if (duration > 0) {
    setTimeout(() => removeToast(toast), duration);
  }
}

function removeToast(toast) {
  if (!toast || !toast.parentElement) return;
  toast.classList.add('removing');
  setTimeout(() => toast.remove(), 250);
}

// ── LIVE UPDATES ──
function startLiveUpdates() {
  // Activity feed updates
  AppState.activityInterval = setInterval(() => {
    const feed = document.getElementById('activityFeed');
    if (!feed) return;
    const randomActivity = MockData.newActivities[Math.floor(Math.random() * MockData.newActivities.length)];
    const item = createActivityItem(randomActivity);
    feed.insertBefore(item, feed.firstChild);
    // Remove old items
    const items = feed.querySelectorAll('.activity-item');
    if (items.length > 8) items[items.length - 1].remove();
    // Update counter
    updateStatCounter();
  }, 7000);

  // IoT data updates
  AppState.iotInterval = setInterval(() => {
    updateIoTWidgets();
  }, 3500);

  // Random toast notifications
  const toastMessages = [
    ['success', 'Issue Resolved', 'Pothole on Bole Road has been fixed!'],
    ['info', 'New Volunteer', 'Tigist Alemu joined the community!'],
    ['warning', 'High Traffic', 'Congestion detected on Ring Road'],
    ['success', 'Project Funded', 'Entoto Park expansion reached 80% funding!'],
    ['info', 'Report Update', '23 new issues reported this hour'],
  ];

  setInterval(() => {
    const msg = toastMessages[Math.floor(Math.random() * toastMessages.length)];
    showToast(msg[0], msg[1], msg[2]);
  }, 18000);
}

function createActivityItem(data) {
  const div = document.createElement('div');
  div.className = 'activity-item';
  div.innerHTML = `
    <div class="activity-dot ${data.type}"></div>
    <div class="activity-content">
      <div class="activity-title">${data.title}</div>
      <div class="activity-meta">${data.meta}</div>
    </div>
    <div class="activity-time">${data.time}</div>
  `;
  return div;
}

function updateStatCounter() {
  const el = document.getElementById('totalIssuesCounter');
  if (!el) return;
  const val = parseInt(el.textContent.replace(/,/g, '')) + Math.floor(Math.random() * 3) + 1;
  animateCounter(el, parseInt(el.textContent.replace(/,/g, '')), val, 600);
}

function animateCounter(el, from, to, duration) {
  const start = performance.now();
  function update(time) {
    const progress = Math.min((time - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(from + (to - from) * eased).toLocaleString();
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

function updateIoTWidgets() {
  const iotData = {
    airQuality: Math.max(30, Math.min(100, MockData.iotData.airQuality + (Math.random() - 0.5) * 10)),
    traffic: Math.max(20, Math.min(100, MockData.iotData.traffic + (Math.random() - 0.5) * 15)),
    waterPressure: Math.max(60, Math.min(100, MockData.iotData.waterPressure + (Math.random() - 0.5) * 5)),
    noise: Math.max(20, Math.min(80, MockData.iotData.noise + (Math.random() - 0.5) * 8)),
  };

  Object.assign(MockData.iotData, iotData);

  const ids = ['iotAir', 'iotTraffic', 'iotWater', 'iotNoise'];
  const vals = [iotData.airQuality, iotData.traffic, iotData.waterPressure, iotData.noise];
  const fills = ['iotAirFill', 'iotTrafficFill', 'iotWaterFill', 'iotNoiseFill'];

  ids.forEach((id, i) => {
    const el = document.getElementById(id);
    if (el) el.textContent = Math.round(vals[i]);
    const fill = document.getElementById(fills[i]);
    if (fill) fill.style.width = `${vals[i]}%`;
  });
}

// ── DASHBOARD ──
function initDashboard() {
  // Set dashboard date (used in the "liveDate" placeholder)
  const dateEl = document.getElementById('liveDate');
  if (dateEl) {
    const now = new Date();
    dateEl.textContent = now.toLocaleDateString('en-ET', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }

  // Animate counters on load
  setTimeout(() => {
    const counters = [
      { id: 'totalIssuesCounter', to: 3847 },
      { id: 'activeReportsCounter', to: 421 },
      { id: 'volunteersCounter', to: 1209 },
      { id: 'resolvedCounter', to: 87 },
    ];

    counters.forEach(c => {
      const el = document.getElementById(c.id);
      if (el) animateCounter(el, 0, c.to, 1400);
    });
  }, 300);

  // Populate activity feed
  const feed = document.getElementById('activityFeed');
  if (feed) {
    feed.innerHTML = '';
    MockData.activities.forEach(a => {
      feed.appendChild(createActivityItem(a));
    });
  }

  // Init dashboard mini chart
  const ctx = document.getElementById('dashMiniChart');
  if (ctx && !AppState.chartInstances.dashMini) {
    AppState.chartInstances.dashMini = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
          data: [45, 62, 38, 78, 55, 91, 67],
          borderColor: '#078930',
          backgroundColor: 'rgba(7,137,48,0.1)',
          borderWidth: 2.5,
          fill: true,
          tension: 0.4,
          pointRadius: 0,
          pointHoverRadius: 5,
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { display: false },
          y: { display: false }
        },
        interaction: { mode: 'index', intersect: false }
      }
    });
  }

  // Progress bars animation
  setTimeout(() => {
    document.querySelectorAll('.progress-bar-fill[data-width]').forEach(bar => {
      bar.style.width = bar.dataset.width;
    });
  }, 500);
}

// ── MAP ──
let mapInstance = null;

function initMap() {
  const mapContainer = document.getElementById('cityMap');
  if (!mapContainer) return;

  if (mapInstance) return; // Already initialized

  // Use Leaflet (OpenStreetMap)
  if (typeof L === 'undefined') return;

  mapInstance = L.map('cityMap', {
    center: [9.0054, 38.7636], // Addis Ababa
    zoom: 13,
    zoomControl: false
  });

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
  attribution: 'OpenStreetMap contributors',
    subdomains: 'abcd',
    maxZoom: 20
  }).addTo(mapInstance);

  L.control.zoom({ position: 'bottomright' }).addTo(mapInstance);

  // Add markers
  const markers = [
    { lat: 9.0054, lng: 38.7636, title: 'Road Damage', category: 'Infrastructure', severity: 'High', color: '#DA121A' },
    { lat: 9.0120, lng: 38.7580, title: 'Water Leakage', category: 'Utilities', severity: 'Medium', color: '#FCDD09' },
    { lat: 8.9980, lng: 38.7700, title: 'Garbage Pile', category: 'Sanitation', severity: 'Low', color: '#078930' },
    { lat: 9.0200, lng: 38.7650, title: 'Street Light Out', category: 'Infrastructure', severity: 'Medium', color: '#FCDD09' },
    { lat: 9.0080, lng: 38.7750, title: 'Flooding Risk', category: 'Safety', severity: 'High', color: '#DA121A' },
    { lat: 9.0150, lng: 38.7500, title: 'Noise Complaint', category: 'Community', severity: 'Low', color: '#078930' },
    { lat: 8.9900, lng: 38.7620, title: 'Air Quality Alert', category: 'Environment', severity: 'High', color: '#DA121A' },
    { lat: 9.0300, lng: 38.7780, title: 'Traffic Congestion', category: 'Traffic', severity: 'Medium', color: '#FCDD09' },
    { lat: 9.0070, lng: 38.7450, title: 'Park Damage', category: 'Parks', severity: 'Low', color: '#078930' },
    { lat: 9.0250, lng: 38.7560, title: 'Sewer Overflow', category: 'Utilities', severity: 'High', color: '#DA121A' },
  ];

  markers.forEach(m => {
    const icon = L.divIcon({
      className: '',
      html: `<div style="
        width:14px;height:14px;border-radius:50%;
        background:${m.color};border:2.5px solid white;
        box-shadow:0 0 12px ${m.color}80;
        animation: pulse 2s infinite;
      "></div>`,
      iconSize: [14, 14],
      iconAnchor: [7, 7]
    });

    const marker = L.marker([m.lat, m.lng], { icon }).addTo(mapInstance);
    marker.bindPopup(`
      <div class="map-popup-title">${m.title}</div>
      <div class="map-popup-meta">${m.category}</div>
      <div class="map-popup-badge" style="margin-top:8px;">
        <span style="
          display:inline-block;padding:2px 10px;border-radius:20px;
          font-size:11px;font-weight:700;
          background:${m.color}22;color:${m.color};
          border:1px solid ${m.color}44;
        ">${m.severity} Severity</span>
      </div>
    `, { maxWidth: 200 });
  });

  // Filter buttons
  document.querySelectorAll('.map-filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.map-filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      showToast('info', 'Filter Applied', `Showing: ${btn.textContent.trim()}`);
    });
  });
}

// ── ANALYTICS ──
function initAnalytics() {
  initPieChart();
  initLineChart();
  initBarChart();
}

function initPieChart() {
  const ctx = document.getElementById('pieChart');
  if (!ctx) return;
  if (AppState.chartInstances.pie) { AppState.chartInstances.pie.destroy(); }

  AppState.chartInstances.pie = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Infrastructure', 'Sanitation', 'Safety', 'Utilities', 'Environment', 'Community'],
      datasets: [{
        data: [32, 18, 15, 14, 12, 9],
        backgroundColor: ['#078930', '#FCDD09', '#DA121A', '#3b8dff', '#a855f7', '#f97316'],
        borderColor: 'transparent',
        borderWidth: 0,
        hoverOffset: 8,
      }]
    },
    options: {
      responsive: true,
      cutout: '65%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#8a93b0', padding: 16, font: { size: 12, family: 'Plus Jakarta Sans' }, boxWidth: 10 }
        },
        tooltip: {
          backgroundColor: 'rgba(13,20,34,0.9)',
          titleColor: '#f0f4ff',
          bodyColor: '#8a93b0',
          callbacks: { label: (c) => ` ${c.label}: ${c.parsed}%` }
        }
      },
      animation: { animateRotate: true, duration: 1200 }
    }
  });
}

function initLineChart(period = 'weekly') {
  const ctx = document.getElementById('lineChart');
  if (!ctx) return;
  if (AppState.chartInstances.line) { AppState.chartInstances.line.destroy(); }

  const datasets = {
    daily: { labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], data: [34,52,41,67,48,78,55], data2: [22,31,27,45,33,56,41] },
    weekly: { labels: ['Wk1','Wk2','Wk3','Wk4','Wk5','Wk6','Wk7','Wk8'], data: [234,312,278,445,389,521,467,398], data2: [154,221,198,312,267,387,334,289] },
    monthly: { labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], data: [1234,1567,1398,1789,1543,1987,1765,2012,1890,2234,2012,2345], data2: [987,1234,1098,1456,1234,1678,1543,1789,1654,1987,1765,2012] }
  };

  const d = datasets[period];
  AppState.chartInstances.line = new Chart(ctx, {
    type: 'line',
    data: {
      labels: d.labels,
      datasets: [
        {
          label: 'Issues Reported',
          data: d.data,
          borderColor: '#078930',
          backgroundColor: 'rgba(7,137,48,0.1)',
          borderWidth: 2.5,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#078930',
          pointRadius: 4,
          pointHoverRadius: 7,
        },
        {
          label: 'Issues Resolved',
          data: d.data2,
          borderColor: '#3b8dff',
          backgroundColor: 'rgba(59,141,255,0.1)',
          borderWidth: 2.5,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#3b8dff',
          pointRadius: 4,
          pointHoverRadius: 7,
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { labels: { color: '#8a93b0', font: { family: 'Plus Jakarta Sans' } } },
        tooltip: { backgroundColor: 'rgba(13,20,34,0.9)', titleColor: '#f0f4ff', bodyColor: '#8a93b0', mode: 'index', intersect: false }
      },
      scales: {
        x: { ticks: { color: '#4a5168' }, grid: { color: 'rgba(255,255,255,0.04)' } },
        y: { ticks: { color: '#4a5168' }, grid: { color: 'rgba(255,255,255,0.04)' } }
      },
      animation: { duration: 800 }
    }
  });
}

function initBarChart() {
  const ctx = document.getElementById('barChart');
  if (!ctx) return;
  if (AppState.chartInstances.bar) { AppState.chartInstances.bar.destroy(); }

  AppState.chartInstances.bar = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Bole', 'Megenagna', 'Piassa', 'Merkato', 'CMC', 'Kazanchis', 'Mexico Sq', 'Lideta'],
      datasets: [{
        label: 'Issues',
        data: [89, 67, 123, 98, 45, 78, 112, 56],
        backgroundColor: [
          'rgba(7,137,48,0.7)', 'rgba(7,137,48,0.5)', 'rgba(218,18,26,0.7)',
          'rgba(252,221,9,0.7)', 'rgba(59,141,255,0.7)', 'rgba(7,137,48,0.6)',
          'rgba(218,18,26,0.6)', 'rgba(252,221,9,0.5)'
        ],
        borderRadius: 6,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: { backgroundColor: 'rgba(13,20,34,0.9)', titleColor: '#f0f4ff', bodyColor: '#8a93b0' }
      },
      scales: {
        x: { ticks: { color: '#4a5168', font: { size: 11 } }, grid: { display: false } },
        y: { ticks: { color: '#4a5168' }, grid: { color: 'rgba(255,255,255,0.04)' } }
      },
      animation: { duration: 1000, easing: 'easeOutBounce' }
    }
  });
}

// ── TIME FILTER TABS ──
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('time-tab')) {
    const group = e.target.closest('.time-filter-tabs');
    group?.querySelectorAll('.time-tab').forEach(t => t.classList.remove('active'));
    e.target.classList.add('active');
    const period = e.target.dataset.period;
    if (period) initLineChart(period);
  }
});

// ── COMMUNITY ──
function initCommunity() {
  const board = document.getElementById('communityBoard');
  if (!board || board.hasChildNodes()) return;

  MockData.posts.forEach(post => {
    board.appendChild(createPostCard(post));
  });
}

function createPostCard(post) {
  const card = document.createElement('div');
  card.className = 'glass-card post-card';

  card.innerHTML = `
    <div class="post-header">
      <div class="post-avatar" style="background:${post.avatar}">${post.initials}</div>
      <div>
        <div class="post-author">${post.author}</div>
        <div class="post-date">${post.date}</div>
      </div>
      <div style="margin-left:auto">
        <span class="badge badge-green">Resident</span>
      </div>
    </div>
    <div class="post-title">${post.title}</div>
    <div class="post-body">${post.body}</div>
    <div class="post-tags">
      ${post.tags.map(t => `<span class="post-tag">${t}</span>`).join('')}
    </div>
    <div class="post-actions">
      <button class="upvote-btn" data-post-id="${post.id}">
        <span class="upvote-icon">▲</span>
        <span class="upvote-count">${post.upvotes.toLocaleString()}</span>
      </button>
      <button class="btn-secondary" style="padding:6px 14px;font-size:13px;">Comment</button>
      <button class="btn-secondary" style="padding:6px 14px;font-size:13px;margin-left:auto;">Collaborate</button>
    </div>
  `;

  const upvoteBtn = card.querySelector('.upvote-btn');
  upvoteBtn.addEventListener('click', () => {
    const postId = upvoteBtn.dataset.postId;
    if (AppState.upvotes[postId]) return;
    AppState.upvotes[postId] = true;
    upvoteBtn.classList.add('voted');
    const countEl = upvoteBtn.querySelector('.upvote-count');
    const current = parseInt(countEl.textContent.replace(/,/g, ''));
    animateCounter(countEl, current, current + 1, 400);
    showToast('success', '▲ Upvoted!', `You supported: "${post.title.substring(0, 40)}..."`);
  });

  return card;
}

// ── BUDGET ──
function initBudget() {
  const list = document.getElementById('budgetList');
  if (!list || list.hasChildNodes()) return;

  MockData.budgetProjects.forEach(project => {
    list.appendChild(createBudgetCard(project));
  });

  initBudgetPieChart();
}

function initBudgetPieChart() {
  const canvas = document.getElementById('budgetPieChart');
  if (!canvas) return;

  // If the user navigates between pages, re-init cleanly
  if (AppState.chartInstances.budgetPie) {
    AppState.chartInstances.budgetPie.destroy();
  }

  const ctx = canvas;
  AppState.chartInstances.budgetPie = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Entoto Park Expansion', 'Bole Road Smart Traffic', 'Merkato Market Digital Registry', 'Flood Warning System'],
      datasets: [{
        data: [1247, 983, 756, 1891],
        backgroundColor: ['#078930', '#3b8dff', '#FCDD09', '#DA121A'],
        borderColor: 'transparent',
      }]
    },
    options: {
      responsive: true,
      cutout: '60%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#8a93b0',
            font: { size: 11 },
            padding: 10,
            boxWidth: 8
          }
        }
      }
    }
  });
}

function createBudgetCard(project) {
  const card = document.createElement('div');
  card.className = 'glass-card budget-project';
  const pct = Math.round((project.votes / project.target) * 100);

  const categoryColors = { Environment: 'green', Infrastructure: 'blue', Economy: 'yellow', Safety: 'red' };
  const badgeClass = `badge-${categoryColors[project.category] || 'green'}`;

  card.innerHTML = `
    <div class="budget-project-header">
      <div>
        <div class="budget-project-name">${project.name}</div>
        <span class="badge ${badgeClass}" style="margin-top:4px">${project.category}</span>
      </div>
      <div class="budget-project-amount">${project.amount}</div>
    </div>
    <div class="budget-project-desc">${project.desc}</div>
    <div style="margin-bottom:10px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
        <span class="fs-12 text-muted">Community Support</span>
        <span class="fs-12 fw-bold text-green">${pct}% funded</span>
      </div>
      <div class="progress-bar-wrap">
        <div class="progress-bar-fill" style="width:0;background:linear-gradient(90deg,var(--eth-green),var(--eth-green-light))" data-width="${pct}%"></div>
      </div>
      <div class="vote-bar-wrap" style="margin-top:10px">
        <span class="vote-count">${project.votes.toLocaleString()} / ${project.target.toLocaleString()} votes</span>
      </div>
    </div>
    <button class="vote-btn vote-btn-support" data-project-id="${project.id}">
      Vote to Support
    </button>
  `;

  // Animate progress bar
  setTimeout(() => {
    const bar = card.querySelector('.progress-bar-fill[data-width]');
    if (bar) bar.style.width = bar.dataset.width;
  }, 400);

  const voteBtn = card.querySelector('.vote-btn-support');
  voteBtn.addEventListener('click', () => {
    const pid = voteBtn.dataset.projectId;
    if (AppState.votes[pid]) {
      showToast('warning', 'Already Voted', 'You have already voted for this project.');
      return;
    }
    AppState.votes[pid] = true;
    voteBtn.classList.add('voted');
    voteBtn.textContent = 'Voted!';
    voteBtn.disabled = true;
    showToast('success', 'Vote Cast!', `You supported: "${project.name}"`);

    // Update vote count
    const countEl = card.querySelector('.vote-count');
    const newVotes = project.votes + 1;
    countEl.textContent = `${newVotes.toLocaleString()} / ${project.target.toLocaleString()} votes`;

    // Update progress bar
    const newPct = Math.round((newVotes / project.target) * 100);
    const bar = card.querySelector('.progress-bar-fill');
    if (bar) bar.style.width = `${newPct}%`;
  });

  return card;
}

// ── REPORT PAGE ──
function initReport() {
  setupCategorySelector();
  setupUploadZone();
  setupSeveritySlider();
  setupReportForm();
  setupAutoSuggest();
}

function setupCategorySelector() {
  document.querySelectorAll('.category-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
    });
  });
}

function setupUploadZone() {
  const zone = document.getElementById('uploadZone');
  if (!zone) return;

  zone.addEventListener('dragover', (e) => { e.preventDefault(); zone.classList.add('dragover'); });
  zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
  zone.addEventListener('drop', (e) => {
    e.preventDefault();
    zone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length) handleFileUpload(files);
  });

  zone.addEventListener('click', () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.multiple = true;
    input.onchange = (e) => handleFileUpload(e.target.files);
    input.click();
  });
}

function handleFileUpload(files) {
  const preview = document.getElementById('uploadPreview');
  if (!preview) return;
  preview.innerHTML = '';

  Array.from(files).forEach(file => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const item = document.createElement('div');
      item.style.cssText = `
        width:80px;height:80px;border-radius:8px;overflow:hidden;
        border:2px solid var(--eth-green);position:relative;display:inline-block;margin:4px;
      `;
      item.innerHTML = `<img src="${e.target.result}" style="width:100%;height:100%;object-fit:cover">`;
      preview.appendChild(item);
    };
    reader.readAsDataURL(file);
  });

  showToast('success', 'Photos Added', `${files.length} image(s) attached to your report`);
}

function setupSeveritySlider() {
  const slider = document.getElementById('severitySlider');
  const label = document.getElementById('severityLabel');
  if (!slider || !label) return;

  const levels = ['Low', 'Low-Medium', 'Medium', 'Medium-High', 'High', 'Critical'];
  const colors = ['#078930', '#5da830', '#FCDD09', '#f97316', '#DA121A', '#8b0000'];

  slider.addEventListener('input', () => {
    const val = parseInt(slider.value);
    const idx = Math.round((val / 100) * (levels.length - 1));
    label.textContent = levels[idx];
    label.style.color = colors[idx];
  });
}

function setupReportForm() {
  const form = document.getElementById('reportForm');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    btn.textContent = 'Submitting...';
    btn.disabled = true;

    setTimeout(() => {
      btn.textContent = 'Report Submitted!';
      showToast('success', 'Report Submitted!', 'Your issue has been logged and assigned to the city team.');
      setTimeout(() => {
        btn.textContent = 'Submit Report';
        btn.disabled = false;
        form.reset();
        document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('selected'));
        navigateTo('dashboard');
      }, 2000);
    }, 2000);
  });
}

function setupAutoSuggest() {
  const titleInput = document.getElementById('reportTitle');
  const suggestEl = document.getElementById('autoSuggest');
  if (!titleInput || !suggestEl) return;

  const suggestions = {
    'road': 'Infrastructure - Road Damage',
    'water': 'Utilities - Water Supply Issue',
    'trash': 'Sanitation - Garbage Collection',
    'light': 'Infrastructure - Street Lighting',
    'flood': 'Safety - Flooding Risk',
    'noise': 'Community - Noise Complaint',
    'air': 'Environment - Air Quality',
    'tree': 'Environment - Tree/Park Issue',
    'traffic': 'Traffic - Congestion / Signal',
  };

  titleInput.addEventListener('input', () => {
    const val = titleInput.value.toLowerCase();
    let suggestion = null;
    for (const [key, cat] of Object.entries(suggestions)) {
      if (val.includes(key)) { suggestion = cat; break; }
    }
    if (suggestion) {
      suggestEl.textContent = `AI suggests: ${suggestion}`;
      suggestEl.style.display = 'block';
    } else {
      suggestEl.style.display = 'none';
    }
  });
}

// ── SETTINGS ──
function initSettings() {
  const darkModeToggle = document.getElementById('darkModeToggle');
  const langToggle = document.getElementById('langToggle');
  const contrastToggle = document.getElementById('contrastToggle');
  const fontSelect = document.getElementById('fontSizeSelect');

  if (darkModeToggle) {
    darkModeToggle.checked = AppState.darkMode;
    darkModeToggle.addEventListener('change', () => {
      AppState.darkMode = darkModeToggle.checked;
      document.documentElement.setAttribute('data-theme', AppState.darkMode ? 'dark' : 'light');
      showToast('info', 'Theme Changed', AppState.darkMode ? 'Dark mode enabled' : 'Light mode enabled');
    });
  }

  if (langToggle) {
    langToggle.checked = AppState.language === 'am';
    langToggle.addEventListener('change', () => {
      AppState.language = langToggle.checked ? 'am' : 'en';
      updateTranslations();
      showToast('info', 'Language Changed', langToggle.checked ? 'Switched to Amharic (አማርኛ)' : 'Switched to English');
    });
  }

  if (contrastToggle) {
    contrastToggle.checked = AppState.highContrast;
    contrastToggle.addEventListener('change', () => {
      AppState.highContrast = contrastToggle.checked;
      document.documentElement.setAttribute('data-contrast', AppState.highContrast ? 'high' : 'normal');
      showToast('info', 'Contrast Changed', 'Accessibility setting updated');
    });
  }

  if (fontSelect) {
    fontSelect.value = AppState.fontSize;
    fontSelect.addEventListener('change', () => {
      AppState.fontSize = fontSelect.value;
      document.documentElement.setAttribute('data-fontsize', AppState.fontSize);
    });
  }
}

function updateTranslations() {
  const t = translations[AppState.language];
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (t[key]) el.textContent = t[key];
  });
}

function loadThemePreference() {
  document.documentElement.setAttribute('data-theme', 'dark');
}

// ── QUICK ACTIONS ──
function setupQuickActions() {
  document.querySelectorAll('[data-nav]').forEach(btn => {
    btn.addEventListener('click', () => navigateTo(btn.dataset.nav));
  });
}

document.addEventListener('DOMContentLoaded', setupQuickActions);
