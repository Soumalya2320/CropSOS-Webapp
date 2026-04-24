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

            <!-- Heatmap — click to expand -->
            <div class="heatmap-box" @click="showHeatmap = !showHeatmap">
              <button class="heatmap-btn">{{ showHeatmap ? 'HIDE HEATMAP' : 'VIEW HEATMAP' }}</button>
            </div>

            <!-- Expanded heatmap grid -->
            <div v-if="showHeatmap" class="heatmap-legend-box">
              <div class="heatmap-legend-title">Disease Spread Map — {{ userArea }}</div>
              <div class="heatmap-grid">
                <div
                  v-for="cell in heatmapGrid"
                  :key="cell.id"
                  class="heatmap-cell"
                  :class="cell.cls"
                  :title="cell.label"
                ></div>
              </div>
              <div class="heatmap-legend-row">
                <span class="heatmap-dot heatmap-dot-critical"></span> Critical
                <span class="heatmap-dot heatmap-dot-high" style="margin-left:10px"></span> High
                <span class="heatmap-dot heatmap-dot-medium" style="margin-left:10px"></span> Medium
                <span class="heatmap-dot heatmap-dot-none" style="margin-left:10px"></span> Clear
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
      showHeatmap:   false,
      heatmapGrid:   [],

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
      this.showHeatmap  = false
      this.heatmapGrid  = []
    },

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
        const headers = { Authorization: `Bearer ${token}` }

        // ── FIX: get location from user object properly
        const userLocation = user.state || user.area || user.location || 'Unknown'

        const formData = new FormData()
        formData.append('file',     this.selectedFile)
        formData.append('userId',   user.id || user._id || user.userId || '')
        formData.append('location', userLocation)
        formData.append('cropType', user.crop_type || user.cropType || '')

        // Step 1: Predict
        const res1 = await axios.post('/api/predict', formData, { headers })
        const d    = res1.data
        console.log('[CropSOS] predict response:', d)

        // Step 2: Fetch alerts for user's actual location
        let nearbyAlerts = []
        try {
          const res2 = await axios.get(`/api/alerts/${encodeURIComponent(userLocation)}`, { headers })
          console.log('[CropSOS] alerts response:', res2.data)

          nearbyAlerts = (res2.data.alerts || res2.data.nearbyAlerts || []).map(a => ({
            disease:  a.disease  || 'Unknown disease',
            count:    a.count    ?? 0,
            severity: a.severity || 'unknown',
            location: a.location || userLocation,
          }))
        } catch (alertErr) {
          console.warn('[CropSOS] alerts fetch failed:', alertErr.message)
        }

        // Step 3: Build heatmap grid from alerts
        this.heatmapGrid = this.buildHeatmapGrid(nearbyAlerts)

        // ── Clean disease name
        const cleanDisease = d.disease ? d.disease.replace(/___/g, ' - ').replace(/_/g, ' ') : 'Unknown'

        // Step 4: Map to resultData
        this.resultData = {
          diseaseName:       cleanDisease,
          scientificName:    d.scientific_name  || '',
          confidence:        d.confidence       || null,
          severity:          d.severity         || 'HIGH CONCERN',
          scanReference:     d.scan_reference   || d.scanReference || '#CS-00000-A',
          immediateActions:  d.immediate_actions      || [],
          diagnosticContext: d.diagnostic_context     || '',
          spreadRisk:        d.spread_risk            || '—',
          estimatedImpact:   d.estimated_yield_impact || '—',
          nearbyAlerts,
        }

        // Save to history
        this.saveDiagnosisHistory(this.resultData, user)

      } catch (err) {
        console.error('[CropSOS] analyze error:', err)
        this.uploadError = err.response?.data?.message || 'Analysis failed. Please try again.'
      } finally {
        this.isAnalyzing = false
      }
    },

    buildHeatmapGrid(alerts) {
      const total = 48
      const cells = []
      const clsMap = {
        critical: 'heatmap-cell-critical',
        high:     'heatmap-cell-high',
        medium:   'heatmap-cell-medium',
        low:      'heatmap-cell-low',
      }
      const infected = new Map()
      alerts.forEach(alert => {
        const sev   = (alert.severity || 'low').toLowerCase()
        const spots = Math.min(Math.ceil((alert.count || 1) * 2), 12)
        for (let i = 0; i < spots; i++) {
          const hash  = [...(alert.disease || 'x')].reduce((a, c) => a + c.charCodeAt(0), 0)
          const idx   = (hash * (i + 1) * 7 + i * 13) % total
          infected.set(idx, { sev, label: `${alert.disease} (${sev})` })
        }
      })
      for (let i = 0; i < total; i++) {
        if (infected.has(i)) {
          const info = infected.get(i)
          cells.push({ id: i, cls: clsMap[info.sev] || 'heatmap-cell-low', label: info.label })
        } else {
          cells.push({ id: i, cls: 'heatmap-cell-none', label: 'No disease detected' })
        }
      }
      return cells
    },

    nearbyIcon(severity) {
      const map = {
        critical: 'warning',
        high:     'warning',
        medium:   'bug_report',
        low:      'eco',
      }
      return map[(severity || '').toLowerCase()] || 'warning'
    },

    nearbyIconClass(severity) {
      const map = {
        critical: 'nearby-icon-red',
        high:     'nearby-icon-red',
        medium:   'nearby-icon-orange',
        low:      'nearby-icon-green',
      }
      return map[(severity || '').toLowerCase()] || 'nearby-icon-red'
    },

    saveDiagnosisHistory(result, user) {
      const record = {
        id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
        diseaseName: result.diseaseName || 'Unknown',
        cropType: user.cropType || user.crop_type || 'Crop',
        location: user.state || user.area || user.location || 'Your Region',
        severity: result.severity || 'Medium',
        confidence: result.confidence || null,
        scanReference: result.scanReference || '',
        imageUrl: this.previewDataUrl || this.previewUrl || '',
        date: new Date().toISOString()
      }
      try {
        const previous = JSON.parse(localStorage.getItem('diagnosisHistory') || '[]')
        localStorage.setItem('diagnosisHistory', JSON.stringify([record, ...previous].slice(0, 50)))
      } catch (_) {
        localStorage.setItem('diagnosisHistory', JSON.stringify([record]))
      }
    }
  }
}
</script>

<style scoped>
@import "../assets/DetectView.css";
</style>