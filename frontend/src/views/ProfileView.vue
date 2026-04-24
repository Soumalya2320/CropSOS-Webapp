<template>
  <section class="profile-page">
    <div class="profile-shell">
      <section class="profile-hero">
        <div class="profile-avatar">{{ initials }}</div>
        <div class="profile-title">
          <div class="profile-kicker">
            <span class="material-symbols-outlined">energy_savings_leaf</span>
            Farmer Profile
          </div>
          <h1>{{ fullName }}</h1>
          <p>{{ user.email || 'Email not added yet' }}</p>
        </div>
        <button class="profile-logout" type="button" @click="logout">
          <span class="material-symbols-outlined">logout</span>
          Logout
        </button>
      </section>

      <section class="profile-grid">
        <div class="profile-card">
          <div class="card-heading">
            <span class="material-symbols-outlined">badge</span>
            Personal Details
          </div>
          <div class="detail-list">
            <div class="detail-row">
              <span>Name</span>
              <strong>{{ fullName }}</strong>
            </div>
            <div class="detail-row">
              <span>Email</span>
              <strong>{{ user.email || 'Not available' }}</strong>
            </div>
            <div class="detail-row">
              <span>Phone</span>
              <strong>{{ user.phone || 'Not added' }}</strong>
            </div>
            <div class="detail-row">
              <span>Location</span>
              <strong>{{ location }}</strong>
            </div>
          </div>
        </div>

        <div class="profile-card profile-farm-card">
          <div class="card-heading">
            <span class="material-symbols-outlined">psychiatry</span>
            Farm Snapshot
          </div>
          <div class="farm-stats">
            <div>
              <span>{{ user.farmName || user.farm_name || 'My Farm' }}</span>
              <small>Farm name</small>
            </div>
            <div>
              <span>{{ user.cropType || user.crop_type || 'Crop not set' }}</span>
              <small>Primary crop</small>
            </div>
            <div>
              <span>{{ user.farmSize || user.farm_size || '0' }}</span>
              <small>Acres</small>
            </div>
          </div>
        </div>
      </section>

      <section class="history-panel">
        <div class="history-head">
          <div>
            <div class="profile-kicker">
              <span class="material-symbols-outlined">history</span>
              Diagnosis History
            </div>
            <h2>Recent crop scans</h2>
          </div>
          <router-link class="history-link" to="/history">
            View all
            <span class="material-symbols-outlined">arrow_forward</span>
          </router-link>
        </div>

        <div v-if="recentHistory.length === 0" class="empty-history">
          <span class="material-symbols-outlined">image_search</span>
          <p>No diagnosis history yet. Start a scan and your reports will appear here.</p>
          <router-link to="/detect">Start Scan</router-link>
        </div>

        <div v-else class="history-list">
          <article v-for="item in recentHistory" :key="item.id" class="history-item">
            <div class="history-icon">
              <span class="material-symbols-outlined">query_stats</span>
            </div>
            <div>
              <h3>{{ item.diseaseName }}</h3>
              <p>{{ item.cropType }} · {{ formatDate(item.date) }}</p>
            </div>
            <span class="severity-badge" :class="severityClass(item.severity)">
              {{ item.severity }}
            </span>
          </article>
        </div>
      </section>
    </div>
  </section>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ProfileView',
  data() {
    return {
      user: {},
      history: []
    }
  },
  computed: {
    fullName() {
      const first = this.user.firstName || this.user.first_name || ''
      const last = this.user.lastName || this.user.last_name || ''
      const name = this.user.name || `${first} ${last}`.trim()
      return name || 'CropSOS User'
    },
    initials() {
      return this.fullName
        .split(' ')
        .filter(Boolean)
        .slice(0, 2)
        .map(part => part[0])
        .join('')
        .toUpperCase() || 'U'
    },
    location() {
      return this.user.state || this.user.area || this.user.location || 'Your Region'
    },
    recentHistory() {
      return this.history.slice(0, 4)
    }
  },
  mounted() {
    this.fetchUser()
    this.loadHistory()
  },
  methods: {
    async fetchUser() {
      const token = localStorage.getItem('token')
      if (!token) {
        localStorage.removeItem('user')
        this.$router.push('/account/login')
        return
      }

      try {
        const res = await axios.get('/api/auth/me', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.user = res.data?.user || res.data || {}
        localStorage.setItem('user', JSON.stringify(this.user))
      } catch (err) {
        this.user = {}
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        this.$router.push('/account/login')
      }
    },
    loadHistory() {
      try {
        this.history = JSON.parse(localStorage.getItem('diagnosisHistory') || '[]')
      } catch (_) {
        this.history = []
      }
    },
    formatDate(value) {
      if (!value) return 'Today'
      return new Date(value).toLocaleDateString('en-IN', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
      })
    },
    severityClass(severity) {
      return `severity-${String(severity || 'medium').toLowerCase().replace(/\s+/g, '-')}`
    },
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      localStorage.removeItem('diagnosisHistory')
      window.location.href = '/account/login'
    }
  }
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #F5F0E8;
  padding: 98px 24px 56px;
  box-sizing: border-box;
}

.profile-shell {
  max-width: 1100px;
  margin: 0 auto;
}

.profile-hero,
.profile-card,
.history-panel {
  background: #fff;
  border: 1px solid #D6CEBC;
  border-radius: 16px;
  box-shadow: 0 18px 45px rgba(28, 58, 31, 0.08);
}

.profile-hero {
  display: flex;
  align-items: center;
  gap: 22px;
  padding: 30px;
  margin-bottom: 20px;
}

.profile-avatar {
  width: 86px;
  height: 86px;
  border-radius: 50%;
  background: #1C3A1F;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: Georgia, serif;
  font-size: 30px;
  font-weight: 700;
  flex-shrink: 0;
}

.profile-title {
  flex: 1;
}

.profile-kicker {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #2D5A32;
  background: #D4E8D8;
  border-radius: 20px;
  padding: 5px 12px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.profile-kicker span {
  font-size: 15px;
}

.profile-title h1,
.history-head h2 {
  font-family: Georgia, serif;
  color: #1A2B1C;
  margin: 0;
}

.profile-title h1 {
  font-size: 36px;
}

.profile-title p {
  color: #7A8F7C;
  margin: 6px 0 0;
}

.profile-logout,
.history-link,
.empty-history a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  border-radius: 10px;
  font-family: inherit;
  font-weight: 700;
  cursor: pointer;
  text-decoration: none;
}

.profile-logout {
  background: #FEE9E9;
  color: #B94040;
  padding: 11px 16px;
}

.profile-logout span,
.history-link span {
  font-size: 18px;
}

.profile-grid {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 20px;
  margin-bottom: 20px;
}

.profile-card,
.history-panel {
  padding: 24px;
}

.card-heading {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #1A2B1C;
  font-size: 16px;
  font-weight: 800;
  margin-bottom: 18px;
}

.card-heading span {
  color: #2D5A32;
}

.detail-list {
  display: grid;
  gap: 12px;
}

.detail-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  background: #F5F0E8;
  border-radius: 10px;
  padding: 14px 16px;
}

.detail-row span,
.farm-stats small,
.history-item p {
  color: #7A8F7C;
  font-size: 13px;
}

.detail-row strong {
  color: #1A2B1C;
  font-size: 14px;
  text-align: right;
}

.profile-farm-card {
  background: #1C3A1F;
}

.profile-farm-card .card-heading {
  color: #fff;
}

.profile-farm-card .card-heading span {
  color: #a3c9b0;
}

.farm-stats {
  display: grid;
  gap: 12px;
}

.farm-stats div {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  padding: 16px;
}

.farm-stats span {
  display: block;
  color: #fff;
  font-size: 18px;
  font-weight: 800;
  margin-bottom: 4px;
}

.farm-stats small {
  color: rgba(255, 255, 255, 0.55);
}

.history-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 18px;
}

.history-link,
.empty-history a {
  color: #fff;
  background: #1C3A1F;
  padding: 11px 16px;
}

.history-list {
  display: grid;
  gap: 12px;
}

.history-item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 14px;
  background: #F5F0E8;
  border: 1px solid #D6CEBC;
  border-radius: 12px;
  padding: 15px;
}

.history-icon {
  width: 42px;
  height: 42px;
  border-radius: 11px;
  background: #D4E8D8;
  color: #2D5A32;
  display: flex;
  align-items: center;
  justify-content: center;
}

.history-item h3 {
  color: #1A2B1C;
  font-size: 15px;
  margin: 0 0 4px;
}

.history-item p {
  margin: 0;
}

.severity-badge {
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  background: #FFF4CE;
  color: #B98A00;
}

.severity-low { background: #D4E8D8; color: #2D5A32; }
.severity-medium { background: #FFF4CE; color: #B98A00; }
.severity-high,
.severity-high-concern,
.severity-critical { background: #FEE9E9; color: #B94040; }

.empty-history {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 220px;
  text-align: center;
  color: #7A8F7C;
  background: #F5F0E8;
  border-radius: 14px;
  padding: 24px;
}

.empty-history span {
  font-size: 42px;
  color: #2D5A32;
  margin-bottom: 8px;
}

.empty-history p {
  max-width: 360px;
  margin: 0 0 18px;
  line-height: 1.6;
}

@media (max-width: 760px) {
  .profile-hero,
  .history-head {
    flex-direction: column;
  }

  .profile-grid {
    grid-template-columns: 1fr;
  }

  .profile-title h1 {
    font-size: 30px;
  }

  .detail-row,
  .history-item {
    align-items: flex-start;
  }
}
</style>
