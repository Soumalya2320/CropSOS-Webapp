<template>
  <section class="detect-container">
    <section class="detect-wrapper">

      <!-- ══════════════════════════════════════════
           VIEW 1 — UPLOAD (before image selected)
      ══════════════════════════════════════════ -->
      <div v-if="!resultData" class="upload-page">

        <!-- LEFT: Upload area -->
        <div class="upload-left">
          <div class="upload-badge">
            <span class="material-symbols-outlined" style="font-size:13px;">psychiatry</span>
            NEW DIAGNOSIS
          </div>
          <h1 class="upload-heading">Identify Crop Stress</h1>
          <p class="upload-sub">
            Upload a high-resolution photo of your crop's leaves or stems for
            immediate AI-powered agronomic analysis.
          </p>
          <div class="upload-accuracy">
            <span class="material-symbols-outlined" style="font-size:16px;color:#2D5A32;">verified</span>
            <span>98.4% Accuracy Rating</span>
          </div>

          <!-- DROP ZONE -->
          <div
            class="drop-zone"
            :class="{ 'drop-zone-active': isDragging, 'drop-zone-preview': previewUrl }"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
            @click="triggerFileInput"
          >
            <!-- Preview image -->
            <img v-if="previewUrl" :src="previewUrl" class="drop-preview-img" alt="Crop preview" />

            <!-- Placeholder -->
            <template v-else>
              <div class="drop-icon-wrap">
                <span class="material-symbols-outlined" style="font-size:32px;color:#5C9B6B;">add_a_photo</span>
              </div>
              <p class="drop-title">Drop your crop photo here</p>
              <p class="drop-hint">Support for JPEG, PNG and RAW formats.<br />For best results, use natural daylight.</p>
              <button class="drop-browse-btn" type="button" @click.stop="triggerFileInput">
                Browse Files
              </button>
            </template>

            <input
              ref="fileInput"
              type="file"
              accept="image/jpeg,image/png,image/webp,image/*"
              style="display:none"
              @change="handleFileSelect"
            />
          </div>

          <!-- Selected file name -->
          <div v-if="selectedFile" class="selected-file-info">
            <span class="material-symbols-outlined" style="font-size:15px;color:#5C9B6B;">image</span>
            {{ selectedFile.name }}
            <button class="remove-file-btn" @click.stop="clearFile" type="button">
              <span class="material-symbols-outlined" style="font-size:15px;">close</span>
            </button>
          </div>

          <!-- ANALYZE BUTTON -->
          <button
            class="analyze-btn"
            :class="{ 'analyze-btn-disabled': !selectedFile || isAnalyzing }"
            :disabled="!selectedFile || isAnalyzing"
            @click="analyzeCrop"
          >
            <template v-if="!isAnalyzing">
              <span class="material-symbols-outlined" style="font-size:18px;">query_stats</span>
              Analyze Crop
            </template>
            <template v-else>
              <span class="detect-spinner"></span>
              Analyzing...
            </template>
          </button>

          <!-- API Error -->
          <div class="detect-api-err" v-if="uploadError">
            <span class="material-symbols-outlined" style="font-size:15px;">error</span>
            {{ uploadError }}
          </div>
        </div>

        <!-- RIGHT: Tips + Insights -->
        <div class="upload-right">

          <!-- Capture Tips -->
          <div class="tips-card">
            <div class="tips-header">
              <span class="material-symbols-outlined" style="font-size:18px;color:#2D5A32;">lightbulb</span>
              <span class="tips-title">Capture Tips</span>
            </div>
            <div class="tip-item" v-for="(tip, i) in captureTips" :key="i">
              <div class="tip-num">{{ i + 1 }}</div>
              <p class="tip-text">{{ tip }}</p>
            </div>
          </div>

          <!-- Agronomist Insights -->
          <div class="insights-card">
            <div class="insights-label">AGRONOMIST INSIGHTS</div>
            <div class="insight-row">
              <span class="insight-dot insight-dot-red"></span>
              <span class="insight-key">Blight Alerts (Region)</span>
              <span class="insight-val insight-val-red">High</span>
            </div>
            <div class="insight-row">
              <span class="insight-dot insight-dot-green"></span>
              <span class="insight-key">Soil Moisture Avg</span>
              <span class="insight-val insight-val-green">64%</span>
            </div>
            <button class="insights-trends-btn">VIEW REGIONAL TRENDS</button>
          </div>

          <!-- Satellite PRO card -->
          <div class="satellite-card">
            <div class="satellite-top">
              <span class="material-symbols-outlined" style="font-size:18px;color:#a3c9b0;">auto_awesome</span>
              <span class="satellite-pro-badge">PRO</span>
            </div>
            <div class="satellite-title">Satellite Monitoring</div>
            <p class="satellite-sub">
              Get 24/7 autonomous field health monitoring with NDVI infrared imaging.
            </p>
            <a href="#" class="satellite-link">Learn More →</a>
          </div>

        </div>
      </div>

      <!-- ══════════════════════════════════════════
           VIEW 2 — RESULTS (after API response)
      ══════════════════════════════════════════ -->
      <div v-if="resultData" class="result-page">

        <!-- HEADER -->
        <div class="result-header">
          <div class="result-header-left">
            <div class="result-badge">
              <span class="material-symbols-outlined" style="font-size:12px;">check_circle</span>
              DIAGNOSTIC COMPLETE
            </div>
            <h1 class="result-heading">
              Diagnostic<br />
              <span class="result-heading-green">Results.</span>
            </h1>
          </div>
          <div class="result-scan-ref">
            <div class="result-scan-label">Scan Reference</div>
            <!-- ── USER AVATAR + AREA ── -->
            <div class="result-user-block">
              <div class="result-avatar">{{ userInitials }}</div>
              <div class="result-user-info">
                <div class="result-user-name">{{ userName }}</div>
                <div class="result-user-area">{{ userArea }}</div>
              </div>
            </div>
            <div class="result-scan-num">{{ resultData.scanReference || '#CS-00000-A' }}</div>
          </div>
        </div>

        <!-- TOP SECTION: Disease card + Action card -->
        <div class="result-top-grid">

          <!-- Disease Info Card -->
          <div class="disease-card">
            <div class="disease-img-wrap">
              <img :src="previewUrl" alt="Uploaded crop" class="disease-img" />
            </div>
            <div class="disease-info">
              <div class="disease-severity">
                <div class="disease-severity-line"></div>
                <span class="disease-severity-txt">{{ resultData.severity || 'HIGH CONCERN' }}</span>
              </div>
              <div class="disease-name">{{ resultData.diseaseName || 'Unknown' }}</div>
              <div class="disease-scientific">{{ resultData.scientificName || '' }}</div>
              <div class="disease-confidence">
                <span class="disease-conf-num">{{ resultData.confidence || '—' }}</span>
                <span class="disease-conf-pct" v-if="resultData.confidence">%</span>
                <span class="disease-conf-label">Confidence Score</span>
              </div>
            </div>
          </div>

          <!-- Immediate Action Card -->
          <div class="action-card">
            <div class="action-header">
              <span class="material-symbols-outlined" style="font-size:18px;">bolt</span>
              Immediate Action
            </div>
            <div class="action-list">
              <div
                class="action-item"
                v-for="(action, i) in (resultData.immediateActions || [])"
                :key="i"
              >
                <div class="action-num">{{ String(i + 1).padStart(2, '0') }}</div>
                <p class="action-text">{{ action }}</p>
              </div>
            </div>

            <!-- NEW SCAN button + Generate Protocol -->
            <button class="new-scan-btn" @click="resetScan">
              <span class="material-symbols-outlined" style="font-size:16px;">add_a_photo</span>
              New Scan
            </button>
            <button class="protocol-btn">
              Generate Full Protocol
              <span class="material-symbols-outlined" style="font-size:16px;">auto_awesome</span>
            </button>
          </div>

        </div>

        <!-- BOTTOM SECTION: Context + Nearby Alerts -->
        <div class="result-bottom-grid">

          <!-- AI Diagnostic Context -->
          <div class="context-card">
            <div class="context-header">
              <span class="context-title">AI Diagnostic Context</span>
              <span class="material-symbols-outlined context-info-icon">info</span>
            </div>
            <p class="context-text">{{ resultData.diagnosticContext || '' }}</p>
            <div class="context-stats">
              <div class="context-stat">
                <div class="context-stat-label">SPREAD RISK</div>
                <div class="context-stat-val context-stat-critical">{{ resultData.spreadRisk || '—' }}</div>
              </div>
              <div class="context-stat">
                <div class="context-stat-label">ESTIMATED IMPACT</div>
                <div class="context-stat-val">{{ resultData.estimatedImpact || '—' }}</div>
              </div>
            </div>
          </div>

          <!-- Nearby Alerts -->
          <div class="nearby-section">
            <div class="nearby-header">
              <span class="nearby-title">Nearby Alerts</span>
              <span class="nearby-live-badge">LIVE MAP</span>
            </div>

            <div class="nearby-list">
              <div
                class="nearby-item"
                v-for="(alert, i) in (resultData.nearbyAlerts || [])"
                :key="i"
              >
                <div
                  class="nearby-icon-wrap"
                  :class="nearbyIconClass(alert.severity)"
                >
                  <span class="material-symbols-outlined">
                    {{ nearbyIcon(alert.severity) }}
                  </span>
                </div>
                <div class="nearby-info">
                  <div class="nearby-name">{{ alert.disease }}</div>
                  <div class="nearby-meta">
                    Cases: {{ alert.count }} · Severity: {{ alert.severity }}
                  </div>
                </div>
                <span class="material-symbols-outlined nearby-arrow">chevron_right</span>
              </div>
            </div>

            <!-- Real Maps Heatmap -->
            <div class="heatmap-toggle-bar" @click="toggleHeatmap">
              <span class="material-symbols-outlined" style="font-size:16px;">map</span>
              <span>{{ showHeatmap ? 'HIDE DISEASE MAP' : 'VIEW DISEASE HEATMAP' }}</span>
              <span class="material-symbols-outlined heatmap-chevron" :class="{ rotated: showHeatmap }">expand_more</span>
            </div>

            <div v-if="showHeatmap" class="heatmap-map-wrap">
              <div class="heatmap-map-header">
                <span class="heatmap-map-title">
                  <span class="material-symbols-outlined" style="font-size:14px;color:#D94040;">location_on</span>
                  Live Disease Spread — {{ userArea }}
                </span>
                <span class="heatmap-cases-badge">{{ nearbyAlertsForMap.length }} active zones</span>
              </div>
              <div class="map-wrapper">
                <div id="cropsos-heatmap"></div>
              </div>
              <div class="heatmap-legend-row">
                <span class="heatmap-dot" style="background:#D94040"></span> Critical &nbsp;
                <span class="heatmap-dot" style="background:#E87B2A"></span> High &nbsp;
                <span class="heatmap-dot" style="background:#D4B84A"></span> Medium &nbsp;
                <span class="heatmap-dot" style="background:#4A7C59"></span> Low
              </div>
            </div>

          </div>

        </div>

        <!-- FOOTER ACTIONS -->
        <div class="result-footer-actions">
          <div class="footer-action-card">
            <span class="footer-action-title">Consult Expert</span>
            <span class="footer-action-sub">Connect with an agronomist</span>
            <span class="material-symbols-outlined footer-action-icon">support_agent</span>
          </div>
          <div class="footer-action-card">
            <span class="footer-action-title">Local Suppliers</span>
            <span class="footer-action-sub">Find fungicides nearby</span>
            <span class="material-symbols-outlined footer-action-icon">storefront</span>
          </div>
          <div class="footer-action-card">
            <span class="footer-action-title">Export Report</span>
            <span class="footer-action-sub">Download PDF summary</span>
            <span class="material-symbols-outlined footer-action-icon">description</span>
          </div>
        </div>

      </div>

    </section>
  </section>
</template>

<script>
import axios from 'axios'

export default {
  name: 'DetectView',

  data() {
    return {
      selectedFile:  null,
      previewUrl:    null,
      previewDataUrl:null,
      isDragging:    false,
      isAnalyzing:   false,
      uploadError:   '',
      resultData:    null,
      userName:      '',
      userInitials:  '',
      userArea:      '',
      showHeatmap:         false,
      heatmapGrid:         [],
      nearbyAlertsForMap:  [],
      userLat:             22.57,
      userLng:             88.36,
 
      captureTips: [
        'Focus on the affected area. If you see spots or discoloration, center it.',
        'Ensure good lighting. Avoid strong shadows or high-noon glare.',
        'Include a scale if possible (like a coin) for size reference.'
      ]
    }
  },

  mounted() {
    try {
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      const first = user.first_name || user.firstName || ''
      const last  = user.last_name  || user.lastName  || ''
      this.userName     = first && last ? `${first} ${last}` : (first || 'Farmer')
      this.userInitials = ((first[0] || '') + (last[0] || '')).toUpperCase() || 'F'
      this.userArea     = user.state || user.area || user.location || 'Your Region'
    } catch (e) {
      this.userInitials = 'F'
      this.userName     = 'Farmer'
      this.userArea     = 'Your Region'
    }
  },

  methods: {

    triggerFileInput() { this.$refs.fileInput.click() },

    handleFileSelect(e) {
      const file = e.target.files[0]
      if (file) this.setFile(file)
    },

    handleDrop(e) {
      this.isDragging = false
      const file = e.dataTransfer.files[0]
      if (file) this.setFile(file)
    },

    setFile(file) {
      this.selectedFile = file
      this.uploadError  = ''
      this.previewUrl   = URL.createObjectURL(file)
      
      const reader = new FileReader()
      reader.onload = (e) => {
        this.previewDataUrl = e.target.result
      }
      reader.readAsDataURL(file)
    },

    clearFile() {
      this.selectedFile = null
      this.previewUrl   = null
      this.previewDataUrl = null
      this.uploadError  = ''
      this.$refs.fileInput.value = ''
    },

    resetScan() {
      this.resultData   = null
      this.selectedFile = null
      this.previewUrl   = null
      this.previewDataUrl = null
      this.uploadError  = ''
      this.showHeatmap        = false
      this.heatmapGrid        = []
      this.nearbyAlertsForMap = []
    },
 
    // ════════════════════════════════════════
    async analyzeCrop() {
      if (!this.selectedFile) return

      const token = localStorage.getItem('token')
      if (!token) {
        this.$router.push('/account/login')
        return
      }

      this.isAnalyzing = true
      this.uploadError = ''

      try {
        const user    = JSON.parse(localStorage.getItem('user') || '{}')
        const token   = localStorage.getItem('token')
        const headers = token ? { Authorization: `Bearer ${token}` } : {}
        const userLocation = user.state || user.area || user.location || 'Unknown'

        // Step 0: Get GPS coordinates
        const getLocation = () => new Promise((resolve) => {
          if (!navigator.geolocation) return resolve({ lat: 22.57, lng: 88.36 })
          navigator.geolocation.getCurrentPosition(
            (pos) => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
            ()    => resolve({ lat: 22.57, lng: 88.36 })  // fallback: Kolkata
          )
        })
        const { lat, lng } = await getLocation()
        this.userLat = lat
        this.userLng = lng

        // Step 1: Predict — send GPS coords too
        const formData = new FormData()
        formData.append('file',     this.selectedFile)
        formData.append('userId',   user.id || user._id || '')
        formData.append('location', userLocation)
        formData.append('cropType', user.crop_type || user.cropType || '')
        formData.append('lat',      lat)
        formData.append('lng',      lng)

        const res1 = await axios.post('/predict', formData, { headers })
        const d    = res1.data
        console.log('[CropSOS] predict response:', d)

        // Step 2: Fetch ALL geo-alerts for heatmap
        let nearbyAlerts = []
        try {
          const res2 = await axios.get('/alerts/geo', { headers })
          nearbyAlerts = (res2.data.alerts || []).map(a => ({
            disease:  a.disease  || 'Unknown',
            count:    a.count    ?? 1,
            severity: a.severity || 'medium',
            lat:      a.lat      || lat,
            lng:      a.lng      || lng,
            location: a.location || userLocation,
          }))
        } catch (alertErr) {
          console.warn('[CropSOS] geo-alerts fetch failed:', alertErr.message)
        }

        this.nearbyAlertsForMap = nearbyAlerts

        // Step 3: Map to resultData
        this.resultData = {
          diseaseName:       d.disease          || d.disease_name || 'Unknown',
          scientificName:    d.scientific_name  || '',
          confidence:        d.confidence       || null,
          severity:          (d.severity || 'medium').toUpperCase(),
          scanReference:     d.reportId ? `#CS-${d.reportId.slice(0,5).toUpperCase()}-A` : '#CS-00000-A',
          immediateActions:  d.advice?.immediate_actions      || [],
          diagnosticContext: d.advice?.diagnostic_context     || '',
          spreadRisk:        d.advice?.spread_risk            || '—',
          estimatedImpact:   d.advice?.estimated_yield_impact || '—',
          nearbyAlerts: nearbyAlerts.slice(0, 5),
        }

      } catch (err) {
        console.error('[CropSOS] analyze error:', err)
        this.uploadError = err.response?.data?.message || 'Analysis failed. Please try again.'
      } finally {
        this.isAnalyzing = false
      }
    },
 
    // ════════════════════════════════════════
    // BUILD HEATMAP: generates 8×6 grid from alerts
    // ════════════════════════════════════════
    // ── Toggle heatmap + init Google Maps ──
    async toggleHeatmap() {
      this.showHeatmap = !this.showHeatmap
      if (this.showHeatmap) {
        await this.$nextTick()
        this.initLeafletMap()
      } else {
        // Destroy map instance to avoid duplicate map on re-open
        if (this._leafletMap) {
          this._leafletMap.remove()
          this._leafletMap = null
        }
      }
    },

    initLeafletMap() {
      // Destroy previous instance if exists
      if (this._leafletMap) {
        this._leafletMap.remove()
        this._leafletMap = null
      }

      const L = window.L
      if (!L) { console.warn('Leaflet not loaded'); return }

      const center = [this.userLat, this.userLng]

      // Init map with dark CartoDB tiles (no API key needed)
      const map = L.map('cropsos-heatmap', { zoomControl: true, scrollWheelZoom: true })
        .setView(center, 12)
      this._leafletMap = map

      // Ensure map renders properly after container changes
      setTimeout(() => {
        map.invalidateSize()
      }, 300)

      L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap & CARTO'
      }).addTo(map)

      // Severity → circle color + radius
      const sevStyle = {
        critical: { color: '#D94040', radius: 600 },
        high:     { color: '#E87B2A', radius: 450 },
        medium:   { color: '#D4B84A', radius: 300 },
        low:      { color: '#4A7C59', radius: 200 },
      }

      // Draw heatmap circles for each alert
      this.nearbyAlertsForMap.forEach(alert => {
        const sev = (alert.severity || 'medium').toLowerCase()
        const s   = sevStyle[sev] || sevStyle.medium

        // Outer glow circle
        L.circle([alert.lat, alert.lng], {
          color:       'transparent',
          fillColor:   s.color,
          fillOpacity: 0.18,
          radius:      s.radius * 2,
        }).addTo(map)

        // Inner solid circle
        const circle = L.circle([alert.lat, alert.lng], {
          color:       s.color,
          fillColor:   s.color,
          fillOpacity: 0.55,
          weight:      1.5,
          radius:      s.radius,
        }).addTo(map)

        // Popup on click
        circle.bindPopup(`
          <div style="font-family:sans-serif;min-width:140px;">
            <div style="font-weight:700;font-size:14px;margin-bottom:4px;">${alert.disease}</div>
            <div style="font-size:12px;color:#555;">
              Severity: <strong style="color:${s.color}">${alert.severity}</strong><br/>
              Cases: <strong>${alert.count}</strong><br/>
              Zone: ${alert.location}
            </div>
          </div>
        `)
      })

      // User location pulse marker (green)
      const pulseIcon = L.divIcon({
        className: '',
        html: `<div style="
          width:16px;height:16px;
          background:#5C9B6B;
          border:2.5px solid #fff;
          border-radius:50%;
          box-shadow:0 0 0 6px rgba(92,155,107,0.25);
        "></div>`,
        iconSize: [16, 16],
        iconAnchor: [8, 8],
      })
      L.marker(center, { icon: pulseIcon })
        .addTo(map)
        .bindPopup('<strong>📍 Your Location</strong>')

      // If no alerts, show a placeholder circle at user location
      if (this.nearbyAlertsForMap.length === 0) {
        L.circle(center, {
          color: '#5C9B6B', fillColor: '#5C9B6B',
          fillOpacity: 0.2, radius: 500
        }).addTo(map).bindPopup('No disease alerts in your area yet')
      }
    },

    nearbyIcon(severity) {
      const m = { critical: 'warning', high: 'warning', medium: 'bug_report', low: 'eco' }
      return m[(severity || '').toLowerCase()] || 'warning'
    },

    nearbyIconClass(severity) {
      const m = { critical: 'nearby-icon-red', high: 'nearby-icon-red', medium: 'nearby-icon-orange', low: 'nearby-icon-green' }
      return m[(severity || '').toLowerCase()] || 'nearby-icon-red'
    }
  }
}
</script>


<style scoped>

/* ══════════════════════════════════════
   ROOT
══════════════════════════════════════ */
.detect-container {
  min-height: 100vh;
  background: #F5F0E8;
  padding-top: 60px;
}

.detect-wrapper {
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 40px 60px;
}

/* ══════════════════════════════════════
   UPLOAD PAGE
══════════════════════════════════════ */
.upload-page {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 40px;
  align-items: start;
}

/* ── Badge ── */
.upload-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 600;
  color: #2D5A32;
  background: #D4E8D8;
  border-radius: 20px;
  padding: 5px 14px;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  margin-bottom: 16px;
}

.upload-heading {
  font-family: 'Georgia', serif;
  font-size: 36px;
  font-weight: 700;
  color: #1A2B1C;
  margin-bottom: 10px;
  line-height: 1.15;
}

.upload-sub {
  font-size: 14px;
  color: #7A8F7C;
  line-height: 1.65;
  margin-bottom: 10px;
  max-width: 460px;
}

.upload-accuracy {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #2D5A32;
  margin-bottom: 24px;
}

/* ── Drop Zone ── */
.drop-zone {
  border: 2px dashed #C8D9CA;
  border-radius: 16px;
  background: #fff;
  min-height: 260px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
  padding: 32px 24px;
  margin-bottom: 14px;
  position: relative;
  overflow: hidden;
}

.drop-zone:hover,
.drop-zone-active {
  border-color: #4A7C59;
  background: #F0F7F1;
}

.drop-zone-preview {
  border-style: solid;
  border-color: #4A7C59;
  padding: 0;
  min-height: 280px;
}

.drop-preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 14px;
  display: block;
}

.drop-icon-wrap {
  width: 68px;
  height: 68px;
  background: #F0EBE0;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.drop-title {
  font-size: 15px;
  font-weight: 600;
  color: #1A2B1C;
  margin: 0;
}

.drop-hint {
  font-size: 12.5px;
  color: #9DAF9F;
  text-align: center;
  line-height: 1.55;
  margin: 0;
}

.drop-browse-btn {
  padding: 10px 28px;
  background: #1C3A1F;
  color: #fff;
  border: none;
  border-radius: 9px;
  font-size: 13.5px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  margin-top: 6px;
  transition: background 0.2s;
}

.drop-browse-btn:hover { background: #2D5A32; }

/* ── Selected file info ── */
.selected-file-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  color: #3D5440;
  background: #E8F0E9;
  border: 1px solid #B5D4BB;
  border-radius: 8px;
  padding: 8px 14px;
  margin-bottom: 14px;
}

.remove-file-btn {
  margin-left: auto;
  background: none;
  border: none;
  cursor: pointer;
  color: #7A8F7C;
  display: flex;
  align-items: center;
  padding: 0;
  transition: color 0.2s;
}

.remove-file-btn:hover { color: #B94040; }

/* ── Analyze button ── */
.analyze-btn {
  width: 100%;
  padding: 15px;
  background: #1C3A1F;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: background 0.2s, transform 0.1s;
  letter-spacing: 0.2px;
}

.analyze-btn:hover:not(.analyze-btn-disabled) { background: #2D5A32; }
.analyze-btn:active:not(.analyze-btn-disabled) { transform: scale(0.985); }

.analyze-btn-disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

/* ── API error ── */
.detect-api-err {
  display: flex;
  align-items: center;
  gap: 7px;
  background: #FEE9E9;
  border: 1px solid #F5BABA;
  border-radius: 9px;
  padding: 10px 14px;
  font-size: 12.5px;
  color: #B94040;
  margin-top: 12px;
}

/* ── Spinner ── */
.detect-spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(255,255,255,0.35);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ══════════════════════════════════════
   UPLOAD RIGHT SIDEBAR
══════════════════════════════════════ */
.upload-right {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ── Tips Card ── */
.tips-card {
  background: #fff;
  border: 1px solid #D6CEBC;
  border-radius: 14px;
  padding: 18px 20px;
}

.tips-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 14px;
}

.tips-title {
  font-size: 14px;
  font-weight: 600;
  color: #1A2B1C;
}

.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 12px;
}

.tip-num {
  width: 22px; height: 22px;
  border-radius: 50%;
  background: #F0EBE0;
  color: #5A7060;
  font-size: 11.5px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 1px;
}

.tip-text {
  font-size: 12.5px;
  color: #5A7060;
  line-height: 1.55;
  margin: 0;
}

.tip-item:last-child .tip-text {
  background: #F5F0E8;
  border-radius: 8px;
  padding: 8px 10px;
  margin-left: -10px;
}

/* ── Insights Card ── */
.insights-card {
  background: #fff;
  border: 1px solid #D6CEBC;
  border-radius: 14px;
  padding: 18px 20px;
}

.insights-label {
  font-size: 10.5px;
  font-weight: 700;
  color: #9DAF9F;
  letter-spacing: 1px;
  margin-bottom: 14px;
}

.insight-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.insight-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.insight-dot-red   { background: #D94040; }
.insight-dot-green { background: #2D5A32; }

.insight-key {
  font-size: 13px;
  color: #3D5440;
  flex: 1;
}

.insight-val {
  font-size: 13px;
  font-weight: 700;
}

.insight-val-red   { color: #D94040; }
.insight-val-green { color: #2D5A32; }

.insights-trends-btn {
  width: 100%;
  margin-top: 12px;
  padding: 9px;
  background: transparent;
  border: 1px solid #D6CEBC;
  border-radius: 8px;
  font-size: 11.5px;
  font-weight: 600;
  font-family: inherit;
  color: #5A7060;
  letter-spacing: 0.8px;
  cursor: pointer;
  transition: all 0.2s;
}

.insights-trends-btn:hover {
  background: #F0EBE0;
  border-color: #B5C9B8;
}

/* ── Satellite PRO Card ── */
.satellite-card {
  background: #1C3A1F;
  border-radius: 14px;
  padding: 20px;
}

.satellite-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.satellite-pro-badge {
  font-size: 10px;
  font-weight: 700;
  color: #a3c9b0;
  background: rgba(163,201,176,0.18);
  border: 1px solid rgba(163,201,176,0.3);
  border-radius: 5px;
  padding: 2px 8px;
  letter-spacing: 1px;
}

.satellite-title {
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 6px;
}

.satellite-sub {
  font-size: 12px;
  color: rgba(255,255,255,0.5);
  line-height: 1.6;
  margin-bottom: 14px;
}

.satellite-link {
  font-size: 12.5px;
  color: #5C9B6B;
  font-weight: 600;
  text-decoration: none;
}

.satellite-link:hover { text-decoration: underline; }

/* ══════════════════════════════════════
   RESULT PAGE
══════════════════════════════════════ */
.result-page { display: flex; flex-direction: column; gap: 20px; }

/* ── Result Header ── */
.result-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 6px;
}

.result-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 600;
  color: #2D5A32;
  background: #D4E8D8;
  border-radius: 20px;
  padding: 4px 12px;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  margin-bottom: 10px;
}

.result-heading {
  font-family: 'Georgia', serif;
  font-size: 48px;
  font-weight: 900;
  color: #1A2B1C;
  line-height: 1.05;
  margin: 0;
}

.result-heading-green { color: #2D5A32; }

.result-scan-ref {
  text-align: right;
}

.result-scan-label {
  font-size: 11px;
  color: #9DAF9F;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  margin-bottom: 8px;
}

/* ── User block (avatar + name + area) ── */
.result-user-block {
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: flex-end;
  margin-bottom: 8px;
}

.result-avatar {
  width: 40px; height: 40px;
  border-radius: 50%;
  background: #1C3A1F;
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: 0.5px;
  flex-shrink: 0;
}

.result-user-name {
  font-size: 13.5px;
  font-weight: 600;
  color: #1A2B1C;
  text-align: right;
}

.result-user-area {
  font-size: 11.5px;
  color: #9DAF9F;
  text-align: right;
}

.result-scan-num {
  font-size: 15px;
  font-weight: 700;
  color: #1A2B1C;
  letter-spacing: 0.5px;
}

/* ── Top Grid ── */
.result-top-grid {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 16px;
}

/* ── Disease Card ── */
.disease-card {
  background: #fff;
  border-radius: 16px;
  border: 1px solid #D6CEBC;
  display: flex;
  gap: 24px;
  padding: 24px;
  align-items: center;
}

.disease-img-wrap {
  width: 240px;
  height: 200px;
  flex-shrink: 0;
  border-radius: 12px;
  overflow: hidden;
}

.disease-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.disease-info { flex: 1; }

.disease-severity {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.disease-severity-line {
  width: 20px; height: 2px;
  background: #D94040;
  border-radius: 2px;
}

.disease-severity-txt {
  font-size: 11px;
  font-weight: 700;
  color: #D94040;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.disease-name {
  font-family: 'Georgia', serif;
  font-size: 28px;
  font-weight: 700;
  color: #1A2B1C;
  margin-bottom: 5px;
}

.disease-scientific {
  font-size: 13px;
  color: #7A8F7C;
  font-style: italic;
  margin-bottom: 18px;
}

.disease-confidence {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.disease-conf-num {
  font-family: 'Georgia', serif;
  font-size: 42px;
  font-weight: 700;
  color: #2D5A32;
  line-height: 1;
}

.disease-conf-pct {
  font-size: 18px;
  font-weight: 700;
  color: #2D5A32;
}

.disease-conf-label {
  font-size: 13px;
  color: #7A8F7C;
  margin-left: 6px;
}

/* ── Action Card ── */
.action-card {
  background: #1C3A1F;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.action-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 18px;
}

.action-list { flex: 1; margin-bottom: 20px; }

.action-item {
  display: flex;
  gap: 12px;
  margin-bottom: 14px;
  align-items: flex-start;
}

.action-num {
  font-size: 11.5px;
  font-weight: 700;
  color: rgba(255,255,255,0.4);
  flex-shrink: 0;
  margin-top: 2px;
  width: 20px;
}

.action-text {
  font-size: 12.5px;
  color: rgba(255,255,255,0.85);
  line-height: 1.6;
  margin: 0;
}

/* ── New Scan btn (above protocol btn) ── */
.new-scan-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
  font-family: inherit;
  color: rgba(255,255,255,0.75);
  cursor: pointer;
  transition: background 0.2s;
  margin-bottom: 10px;
}

.new-scan-btn:hover { background: rgba(255,255,255,0.14); }

.protocol-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 13px;
  background: #fff;
  border: none;
  border-radius: 10px;
  font-size: 13.5px;
  font-weight: 600;
  font-family: inherit;
  color: #1C3A1F;
  cursor: pointer;
  transition: background 0.2s;
}

.protocol-btn:hover { background: #F0EBE0; }

/* ── Bottom Grid ── */
.result-bottom-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* ── Context Card ── */
.context-card {
  background: #F5F0E8;
  border: 1px solid #D6CEBC;
  border-radius: 16px;
  padding: 24px;
}

.context-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.context-title {
  font-size: 15px;
  font-weight: 700;
  color: #1A2B1C;
}

.context-info-icon {
  font-size: 18px !important;
  color: #9DAF9F;
  cursor: pointer;
}

.context-text {
  font-size: 13px;
  color: #3D5440;
  line-height: 1.7;
  margin-bottom: 20px;
}

.context-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.context-stat {
  background: #EDE8DC;
  border-radius: 10px;
  padding: 14px 16px;
}

.context-stat-label {
  font-size: 10.5px;
  font-weight: 700;
  color: #9DAF9F;
  letter-spacing: 0.8px;
  margin-bottom: 6px;
}

.context-stat-val {
  font-size: 15px;
  font-weight: 700;
  color: #1A2B1C;
}

.context-stat-critical { color: #D94040; }

/* ── Nearby ── */
.nearby-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.nearby-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nearby-title {
  font-size: 16px;
  font-weight: 700;
  color: #1A2B1C;
}

.nearby-live-badge {
  font-size: 10px;
  font-weight: 700;
  color: #2D5A32;
  background: #D4E8D8;
  border-radius: 20px;
  padding: 3px 10px;
  letter-spacing: 0.8px;
}

.nearby-list { display: flex; flex-direction: column; gap: 8px; }

.nearby-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #fff;
  border: 1px solid #D6CEBC;
  border-radius: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: background 0.15s;
}

.nearby-item:hover { background: #F5F0E8; }

.nearby-icon-wrap {
  width: 36px; height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.nearby-icon-red    { background: #FEE9E9; color: #D94040; }
.nearby-icon-green  { background: #D4E8D8; color: #2D5A32; }
.nearby-icon-orange { background: #FDEFD4; color: #C47A1E; }
.nearby-icon-yellow { background: #FEF9D4; color: #A08C10; }

.nearby-info { flex: 1; }

.nearby-name {
  font-size: 13.5px;
  font-weight: 600;
  color: #1A2B1C;
  margin-bottom: 2px;
}

.nearby-meta {
  font-size: 11.5px;
  color: #9DAF9F;
}

.nearby-arrow {
  font-size: 20px !important;
  color: #C8D9CA;
}

/* ── Real Heatmap ── */
.heatmap-toggle-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #1A2B1C;
  border-radius: 10px;
  padding: 12px 16px;
  cursor: pointer;
  font-size: 11.5px;
  font-weight: 700;
  color: rgba(255,255,255,0.8);
  letter-spacing: 0.8px;
  transition: background 0.2s;
  user-select: none;
}
.heatmap-toggle-bar:hover { background: #243D26; }
.heatmap-chevron { margin-left: auto; font-size: 18px !important; transition: transform 0.25s; }
.heatmap-chevron.rotated { transform: rotate(180deg); }

.heatmap-map-wrap {
  background: #1A2B1C;
  border-radius: 12px;
  padding: 0;
  margin-top: 6px;
  overflow: hidden;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}
.heatmap-map-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 14px 10px 14px;
  width: 100%;
  box-sizing: border-box;
}
.heatmap-map-title {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  font-weight: 600;
  color: rgba(255,255,255,0.75);
}
.heatmap-cases-badge {
  font-size: 10.5px;
  font-weight: 700;
  color: #5C9B6B;
  background: rgba(92,155,107,0.15);
  border: 1px solid rgba(92,155,107,0.3);
  border-radius: 99px;
  padding: 2px 10px;
}
.heatmap-legend-row {
  display: flex;
  align-items: center;
  font-size: 11px;
  color: rgba(255,255,255,0.5);
  gap: 4px;
  flex-wrap: wrap;
}
.heatmap-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  display: inline-block;
  flex-shrink: 0;
}

/* ── Footer Actions ── */
.result-footer-actions {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px;
}

.footer-action-card {
  background: #F5F0E8;
  border: 1px solid #D6CEBC;
  border-radius: 14px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 3px;
  cursor: pointer;
  position: relative;
  transition: background 0.2s, border-color 0.2s;
}

.footer-action-card:hover {
  background: #EDE8DC;
  border-color: #B5C9B8;
}

.footer-action-title {
  font-size: 14px;
  font-weight: 600;
  color: #1A2B1C;
}

.footer-action-sub {
  font-size: 12px;
  color: #9DAF9F;
}

.footer-action-icon {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 22px !important;
  color: #C8D9CA;
}

/* Heatmap expanded panel */
.heatmap-legend-box {
  background: #1A2B1C;
  border-radius: 12px;
  padding: 16px;
  margin-top: 8px;
}
 
.heatmap-legend-title {
  font-size: 12px;
  font-weight: 600;
  color: rgba(255,255,255,0.6);
  letter-spacing: 0.5px;
  margin-bottom: 12px;
  text-transform: uppercase;
}
 
.heatmap-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 4px;
  margin-bottom: 12px;
}
 
.heatmap-cell {
  height: 22px;
  border-radius: 4px;
  transition: transform 0.15s;
  cursor: default;
}
 
.heatmap-cell:hover { transform: scale(1.15); }
 
.heatmap-cell-critical { background: #D94040; }
.heatmap-cell-high     { background: #E87B2A; }
.heatmap-cell-medium   { background: #D4B84A; }
.heatmap-cell-low      { background: #4A7C59; opacity: 0.7; }
.heatmap-cell-none     { background: rgba(255,255,255,0.08); }
 
.heatmap-legend-row {
  display: flex;
  align-items: center;
  font-size: 11px;
  color: rgba(255,255,255,0.5);
  gap: 4px;
  padding: 10px 14px 14px 14px;
  width: 100%;
  box-sizing: border-box;
}
 
.heatmap-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  display: inline-block;
}
 
.heatmap-dot-critical { background: #D94040; }
.heatmap-dot-high     { background: #E87B2A; }
.heatmap-dot-medium   { background: #D4B84A; }
.heatmap-dot-none     { background: rgba(255,255,255,0.15); }

/* ── Map Container Styles ── */
.map-wrapper {
  width: 100%;
  height: 350px;
  border-radius: 0;
  overflow: hidden;
  position: relative;
  box-sizing: border-box;
  flex-shrink: 0;
}

#cropsos-heatmap {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}

.map-container {
  padding: 0;
  margin: 0;
}

.leaflet-container {
  width: 100% !important;
  height: 100% !important;
  box-sizing: border-box !important;
  display: block !important;
}

/* ══════════════════════════════════════
   RESPONSIVE
══════════════════════════════════════ */
@media (max-width: 900px) {
  .upload-page { grid-template-columns: 1fr; }
  .upload-right { display: none; }
  .result-top-grid    { grid-template-columns: 1fr; }
  .result-bottom-grid { grid-template-columns: 1fr; }
  .result-footer-actions { grid-template-columns: 1fr; }
  .disease-card { flex-direction: column; }
  .disease-img-wrap { width: 100%; height: 200px; }
  .detect-wrapper { padding: 24px 20px 40px; }
}
</style>