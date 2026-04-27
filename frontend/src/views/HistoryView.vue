<template>
  <section class="archive-page">
    <div class="archive-shell">
      <header class="archive-header">
        <div class="archive-title-block">
          <div class="archive-kicker">
            <span></span>
            Diagnostic Archives
          </div>
          <h1>History</h1>
          <p>
            Review past crop scans to monitor health trends and track the effectiveness of
            your interventions across different field zones.
          </p>
        </div>

        <div class="archive-actions">
          <div class="filter-wrap">
            <button
              class="archive-filter"
              :class="{ 'archive-filter-active': showFilters || selectedFilter !== 'all' }"
              type="button"
              @click="showFilters = !showFilters"
            >
              <span class="material-symbols-outlined">filter_list</span>
              {{ selectedFilterLabel }}
            </button>
            <div v-if="showFilters" class="filter-menu">
              <button
                v-for="option in filterOptions"
                :key="option.value"
                type="button"
                :class="{ 'filter-option-active': selectedFilter === option.value }"
                @click="applyFilter(option.value)"
              >
                {{ option.label }}
              </button>
            </div>
          </div>
          <button class="archive-export" type="button" @click="exportData">
            <span class="material-symbols-outlined">download</span>
            Export CSV
          </button>
        </div>
      </header>

      <section class="archive-tools">
        <label class="archive-search">
          <span class="material-symbols-outlined">search</span>
          <input
            v-model="search"
            type="search"
            placeholder="Search by crop, disease, or field..."
          />
        </label>

        <div class="archive-total">
          <small>Total scans analyzed</small>
          <strong>{{ totalScans }}</strong>
        </div>
      </section>

      <section class="archive-list">
        <article v-for="record in filteredRecords" :key="record.id" class="archive-card">
          <div class="scan-thumb" :class="{ 'scan-thumb-empty': !record.imageUrl }">
            <img v-if="record.imageUrl" :src="record.imageUrl" alt="Scanned crop" @error="$event.target.style.display='none'; $event.target.nextElementSibling.style.display='grid'; $event.target.nextElementSibling.nextElementSibling.style.display='grid';" />
            <div class="scan-grid">
              <span v-for="n in 9" :key="n"></span>
            </div>
            <div class="scan-lines">
              <i v-for="n in 5" :key="n"></i>
            </div>
          </div>

          <div class="archive-record-copy">
            <div class="record-meta">
              <span>{{ record.field }}</span>
              <small>· {{ record.date }}</small>
            </div>
            <h2>{{ record.title }}</h2>
            <p>{{ record.summary }}</p>
          </div>

          <div class="record-status-wrap">
            <span class="record-status" :class="record.statusClass">{{ record.status }}</span>
            <button class="record-next" type="button">
              <span class="material-symbols-outlined">chevron_right</span>
            </button>
          </div>
        </article>
      </section>

      <section v-if="history.length === 0" class="archive-empty">
        <span class="material-symbols-outlined">image_search</span>
        <h2>No scan history yet</h2>
        <p>Jab user crop scan karega, wahi actual report aur image yahan history me show hogi.</p>
        <router-link to="/detect">Start Scan</router-link>
      </section>

      <section v-else-if="filteredRecords.length === 0" class="archive-empty">
        <span class="material-symbols-outlined">filter_alt_off</span>
        <h2>No matching scans</h2>
        <p>Is filter ya search me koi scan nahi mila. Filter clear karke dobara try karo.</p>
        <button type="button" @click="clearFilters">Clear Filters</button>
      </section>

      <button v-if="history.length > 0" class="archive-load" type="button">Load More Records</button>

      <router-link class="floating-scan" to="/detect" aria-label="Start new crop scan">
        <span class="material-symbols-outlined">add_a_photo</span>
      </router-link>
    </div>
  </section>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HistoryView',
  data() {
    return {
      search: '',
      selectedFilter: 'all',
      showFilters: false,
      filterOptions: [
        { label: 'All Records', value: 'all' },
        { label: 'Action Required', value: 'action' },
        { label: 'Monitoring', value: 'monitoring' },
        { label: 'Healthy', value: 'healthy' },
        { label: 'Critical', value: 'critical' }
      ],
      history: []
    }
  },
  

  computed: {
    selectedFilterLabel() {
      const option = this.filterOptions.find(item => item.value === this.selectedFilter)
      return option ? option.label : 'Filter'
    },
    records() {
      return this.history.map((item, index) => ({
        id: item.id || `history-${index}`,
        field: item.cropType || item.location || 'Crop Scan',
        date: this.formatDate(item.date),
        title: (item.diseaseName || 'Crop Diagnosis').replace(/___/g, ' - ').replace(/_/g, ' '),
        summary: this.summaryFor(item),
        status: this.statusLabel(item.severity),
        statusClass: this.statusClass(item.severity),
        filterKey: this.filterKey(item.severity),
        imageUrl: item.imageUrl || ''
      }))
    },
    filteredRecords() {
      const query = this.search.trim().toLowerCase()
      return this.records.filter(record => {
        const matchesSearch = !query || (
          record.field.toLowerCase().includes(query) ||
          record.title.toLowerCase().includes(query) ||
          record.summary.toLowerCase().includes(query) ||
          record.status.toLowerCase().includes(query)
        )
        const matchesFilter = this.selectedFilter === 'all' || record.filterKey === this.selectedFilter
        return matchesSearch && matchesFilter
      })
    },
    totalScans() {
      return this.history.length
    }
  },
  mounted() {
    this.loadHistory()
  },
  methods: {
    async loadHistory() {
      let localHistory = []

      // 🟢 local storage (backup)
      try {
        localHistory = JSON.parse(localStorage.getItem('diagnosisHistory') || '[]')
      } catch (_) {
        console.warn('Failed to parse local history', _)
      }

      try {
        const user = JSON.parse(localStorage.getItem("user") || "{}")
        const userId = user.id || user._id

        if (!userId) {
          console.error("User ID missing")
          this.history = localHistory
          return
        }

        // ✅ CORRECT API
        const res = await axios.get(`/reports/${userId}`)

        const serverHistory = res.data?.reports || []

        this.history = serverHistory.map(item => ({
          id: item.id,
          diseaseName: item.disease,
          cropType: item.cropType || item.crop_type,
          location: item.location,
          severity: item.severity,
          date: item.createdAt || item.date,
          imageUrl: item.imageUrl || ''
        }))

      } catch (err) {
        console.error('Failed to load history from server', err)

        // fallback
        this.history = localHistory
      }
    },
    formatDate(value) {
      if (!value) return 'Today · --'
      return new Date(value).toLocaleString('en-IN', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    statusLabel(severity) {
      const value = String(severity || '').toLowerCase()
      if (value.includes('critical')) return 'Critical'
      if (value.includes('high')) return 'Action Required'
      if (value.includes('low')) return 'Healthy'
      return 'Monitoring'
    },
    statusClass(severity) {
      const label = this.statusLabel(severity).toLowerCase()
      if (label.includes('healthy')) return 'status-healthy'
      if (label.includes('monitoring')) return 'status-warning'
      return 'status-danger'
    },
    filterKey(severity) {
      const label = this.statusLabel(severity).toLowerCase()
      if (label.includes('critical')) return 'critical'
      if (label.includes('healthy')) return 'healthy'
      if (label.includes('monitoring')) return 'monitoring'
      return 'action'
    },
    applyFilter(value) {
      this.selectedFilter = value
      this.showFilters = false
    },
    clearFilters() {
      this.search = ''
      this.applyFilter('all')
    },
    summaryFor(item) {
      const severity = this.statusLabel(item.severity)
      if (severity === 'Healthy') return 'No severe issue detected. Keep monitoring irrigation, nutrition, and nearby crop stress.'
      if (severity === 'Monitoring') return 'Early signs found. Monitor the affected area and repeat scanning if symptoms spread.'
      return 'Disease pressure detected. Take recommended action quickly and isolate affected plants when possible.'
    },
    exportData() {
      const headers = ['ID', 'Crop/Field', 'Date', 'Diagnosis', 'Summary', 'Status', 'Image URL']
      const rows = this.records.map(record => [
        record.id,
        record.field,
        record.date,
        record.title,
        record.summary,
        record.status,
        record.imageUrl
      ])
      const csv = [headers, ...rows]
        .map(row => row.map(this.escapeCsvValue).join(','))
        .join('\n')
      const blob = new Blob([`\uFEFF${csv}`], { type: 'text/csv;charset=utf-8;' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = 'cropsos-history.csv'
      link.click()
      URL.revokeObjectURL(url)
    },
    escapeCsvValue(value) {
      const stringValue = String(value ?? '')
      return `"${stringValue.replace(/"/g, '""')}"`
    }
  }
}
</script>

<style scoped>
.archive-page {
  min-height: 100vh;
  background: #FFF8EF;
  padding: 92px 24px 66px;
  box-sizing: border-box;
}

.archive-shell {
  max-width: 1180px;
  margin: 0 auto;
  position: relative;
}

.archive-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 28px;
  margin-bottom: 46px;
}

.archive-kicker {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #48503e;
  font-size: 12px;
  font-weight: 900;
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-bottom: 10px;
}

.archive-kicker span {
  width: 30px;
  height: 2px;
  background: #2E7D32;
}

.archive-title-block h1 {
  color: #201B0C;
  font-size: 48px;
  line-height: 1;
  margin: 0 0 14px;
  font-family: 'Manrope', Arial, sans-serif;
  letter-spacing: 0;
}

.archive-title-block p {
  max-width: 670px;
  color: #40493d;
  font-size: 17px;
  line-height: 1.6;
  margin: 0;
}

.archive-actions {
  display: flex;
  gap: 12px;
  flex-shrink: 0;
}

.archive-actions button,
.archive-load {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  border: none;
  border-radius: 10px;
  font-family: inherit;
  font-weight: 800;
  cursor: pointer;
}

.archive-filter {
  background: #F3EBD8;
  color: #315C35;
  padding: 13px 24px;
}

.filter-wrap {
  position: relative;
}

.archive-filter-active {
  background: #2E7D4E;
  color: #fff;
}

.filter-menu {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 190px;
  background: #fff;
  border: 1px solid #EEE5D7;
  border-radius: 12px;
  padding: 8px;
  box-shadow: 0 18px 38px rgba(83, 71, 48, 0.12);
  z-index: 40;
}

.filter-menu button {
  width: 100%;
  justify-content: flex-start;
  background: transparent;
  color: #40493d;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 13px;
}

.filter-menu button:hover,
.filter-option-active {
  background: #F3EBD8 !important;
  color: #2E7D4E !important;
}

.archive-export {
  background: #2E7D4E;
  color: #fff;
  padding: 13px 24px;
  box-shadow: 0 10px 24px rgba(46, 125, 78, 0.2);
}

.archive-actions span {
  font-size: 19px;
}

.archive-tools {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 370px;
  gap: 22px;
  margin-bottom: 38px;
}

.archive-search,
.archive-total {
  height: 94px;
  background: #FFF4D9;
  border-radius: 7px;
  display: flex;
  align-items: center;
  box-sizing: border-box;
}

.archive-search {
  gap: 20px;
  padding: 0 26px;
}

.archive-search span {
  color: #6F7666;
  font-size: 24px;
}

.archive-search input {
  width: 100%;
  border: 0;
  outline: 0;
  background: transparent;
  color: #1F251F;
  font-size: 16px;
  font-family: inherit;
  font-weight: 700;
}

.archive-search input::placeholder {
  color: #8D927F;
}

.archive-total {
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  padding: 0 24px;
}

.archive-total small {
  color: #303526;
  font-size: 11px;
  font-weight: 900;
  text-transform: uppercase;
  margin-bottom: 3px;
}

.archive-total strong {
  color: #2E7D4E;
  font-size: 30px;
  line-height: 1;
  letter-spacing: 0;
}

.archive-list {
  display: grid;
  gap: 24px;
}

.archive-card {
  min-height: 164px;
  display: grid;
  grid-template-columns: 120px minmax(0, 1fr) auto;
  align-items: center;
  gap: 22px;
  background: #fff;
  border-radius: 7px;
  padding: 22px 24px;
  box-shadow: 0 16px 32px rgba(83, 71, 48, 0.035);
}

.scan-thumb {
  width: 120px;
  height: 120px;
  border-radius: 4px;
  overflow: hidden;
  background:
    linear-gradient(135deg, rgba(100, 138, 108, 0.16), transparent),
    #07130F;
  border: 1px solid #152C24;
  position: relative;
}

.scan-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.scan-thumb:not(.scan-thumb-empty) .scan-grid,
.scan-thumb:not(.scan-thumb-empty) .scan-lines {
  display: none;
}

.scan-grid {
  position: absolute;
  inset: 17px 18px;
  border: 1px solid rgba(157, 201, 175, 0.7);
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
}

.scan-grid span {
  border-right: 1px solid rgba(157, 201, 175, 0.12);
  border-bottom: 1px solid rgba(157, 201, 175, 0.12);
}

.scan-lines {
  position: absolute;
  left: 28px;
  top: 25px;
  width: 42px;
  display: grid;
  gap: 5px;
}

.scan-lines i {
  height: 2px;
  background: rgba(209, 230, 212, 0.38);
  border-radius: 2px;
}

.record-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 7px;
}

.record-meta span {
  background: #EFE7C7;
  color: #51533F;
  padding: 3px 7px;
  border-radius: 2px;
  font-size: 11px;
  font-weight: 900;
  text-transform: uppercase;
}

.record-meta small {
  color: #727767;
  font-size: 12px;
  font-weight: 700;
}

.archive-record-copy h2 {
  color: #171A12;
  font-size: 25px;
  line-height: 1.1;
  margin: 0 0 6px;
  letter-spacing: 0;
}

.archive-record-copy p {
  max-width: 640px;
  color: #3F453B;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
}

.record-status-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-left: 18px;
}

.record-status {
  min-width: 86px;
  text-align: center;
  border-radius: 999px;
  padding: 8px 13px;
  color: #201B0C;
  font-size: 11px;
  font-weight: 900;
  text-transform: uppercase;
}

.status-danger {
  background: #B94245;
  color: #3A1113;
}

.status-healthy {
  background: #B9F49A;
  color: #2D5A32;
}

.status-warning {
  background: #B94245;
  color: #3A1113;
}

.record-next {
  width: 38px;
  height: 38px;
  border: none;
  border-radius: 10px;
  background: #F7EBCB;
  color: #2E7D4E;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.record-next span {
  font-size: 24px;
}

.archive-load {
  margin: 46px auto 0;
  color: #4A4F43;
  background: transparent;
  border: 1px solid #EEE5D7;
  border-radius: 12px;
  padding: 16px 32px;
  font-size: 15px;
}

.archive-empty {
  min-height: 280px;
  margin-top: 24px;
  background: #fff;
  border-radius: 7px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 30px;
}

.archive-empty span {
  font-size: 46px;
  color: #2E7D4E;
}

.archive-empty h2 {
  color: #201B0C;
  margin: 12px 0 8px;
}

.archive-empty p {
  color: #40493d;
  max-width: 420px;
  line-height: 1.6;
  margin: 0 0 18px;
}

.archive-empty a,
.archive-empty button {
  color: #fff;
  background: #2E7D4E;
  border-radius: 10px;
  padding: 12px 20px;
  text-decoration: none;
  font-weight: 800;
  border: none;
  cursor: pointer;
  font-family: inherit;
}

.floating-scan {
  position: fixed;
  right: 46px;
  bottom: 46px;
  width: 62px;
  height: 62px;
  border-radius: 16px;
  background: #2E7D4E;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  box-shadow: 0 18px 34px rgba(46, 125, 78, 0.28);
}

.floating-scan span {
  font-size: 30px;
}

@media (max-width: 820px) {
  .archive-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .archive-tools {
    grid-template-columns: 1fr;
  }

  .archive-card {
    grid-template-columns: 86px minmax(0, 1fr);
    align-items: flex-start;
  }

  .scan-thumb {
    width: 86px;
    height: 86px;
  }

  .record-status-wrap {
    grid-column: 1 / -1;
    justify-content: space-between;
    padding-left: 0;
  }

  .archive-title-block h1 {
    font-size: 42px;
  }
}

@media (max-width: 560px) {
  .archive-page {
    padding-left: 16px;
    padding-right: 16px;
  }

  .archive-actions {
    width: 100%;
  }

  .archive-actions button {
    flex: 1;
    padding-left: 12px;
    padding-right: 12px;
  }

  .archive-card {
    grid-template-columns: 1fr;
  }
}
</style>
