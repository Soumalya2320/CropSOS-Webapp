<template>
  <section class="account-container">
    <section class="account-wrapper">

      <!-- LEFT PANEL -->
      <div class="account-left">
        <div class="account-left-brand">CropSOS</div>
        <div class="account-left-content">
          <div class="account-left-tag">
            <span class="material-symbols-outlined" style="font-size:14px;">energy_savings_leaf</span>
            Precision Agronomy
          </div>
          <h2 class="account-left-headline">
            Protect your crops,<br />
            <span class="account-left-accent">secure your harvest.</span>
          </h2>
          <p class="account-left-sub">
            Join 50,000+ farmers using AI-powered diagnostics to detect disease early and act fast.
          </p>
          <div class="account-left-stats">
            <div class="account-stat">
              <div class="account-stat-num">10M+</div>
              <div class="account-stat-lbl">Images analyzed</div>
            </div>
            <div class="account-stat">
              <div class="account-stat-num">98.4%</div>
              <div class="account-stat-lbl">Accuracy rating</div>
            </div>
            <div class="account-stat">
              <div class="account-stat-num">3 sec</div>
              <div class="account-stat-lbl">Avg. diagnosis</div>
            </div>
          </div>
        </div>
        <div class="account-left-footer">© 2024 CropSOS · The Resilient Harvest System</div>
      </div>

      <!-- RIGHT PANEL -->
      <div class="account-right">

        <!-- TABS -->
        <div class="account-tabs">
          <button
            class="account-tab"
            :class="{ 'account-tab-active': activeTap === 'login' }"
            @click="switchTab('login')"
          >
            Sign In
          </button>
          <button
            class="account-tab"
            :class="{ 'account-tab-active': activeTap === 'register' }"
            @click="switchTab('register')"
          >
            Create Account
          </button>
        </div>

        <!-- CHILD VIEWS RENDER HERE -->
        <div class="account-right-content">
          <router-view />
        </div>

      </div>

    </section>
  </section>
</template>

<script>
export default {
  name: 'AccountView',
  data() {
    return {
      activeTap: 'login'
    }
  },
  methods: {
    switchTab(tab) {
      this.activeTap = tab
      this.$router.push(`/account/${tab}`)
    }
  },
  mounted() {
    const path = this.$route.path
    if (path.includes('register')) {
      this.activeTap = 'register'
    } else {
      this.activeTap = 'login'
    }
  },
  watch: {
    '$route.path'(newPath) {
      if (newPath.includes('register')) {
        this.activeTap = 'register'
      } else {
        this.activeTap = 'login'
      }
    }
  }
}
</script>

<style scoped>
.account-container {
  height: 100vh;
  background: #F5F0E8;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 85px 20px 20px;
  overflow: hidden;
  box-sizing: border-box;
}

.account-wrapper {
  display: flex;
  width: 100%;
  max-width: 1100px;
  height: calc(100vh - 105px);
  min-height: 550px;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(28, 58, 31, 0.12);
}

/* ── LEFT ── */
.account-left {
  width: 40%;
  background: #1C3A1F;
  padding: 40px 44px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

.account-left::before {
  content: '';
  position: absolute;
  bottom: -80px;
  left: -80px;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.04);
}

.account-left::after {
  content: '';
  position: absolute;
  top: -60px;
  right: -60px;
  width: 220px;
  height: 220px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.03);
}

.account-left-brand {
  font-family: 'Georgia', serif;
  font-size: 22px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.3px;
  position: relative;
  z-index: 1;
}

.account-left-content {
  position: relative;
  z-index: 1;
}

.account-left-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-weight: 500;
  color: #5C9B6B;
  background: rgba(92, 155, 107, 0.18);
  border: 1px solid rgba(92, 155, 107, 0.3);
  border-radius: 20px;
  padding: 5px 12px;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 20px;
}

.account-left-headline {
  font-family: 'Georgia', serif;
  font-size: 30px;
  font-weight: 400;
  color: #fff;
  line-height: 1.3;
  margin-bottom: 14px;
  font-style: italic;
}

.account-left-accent {
  color: #5C9B6B;
}

.account-left-sub {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.7;
  margin-bottom: 32px;
}

.account-left-stats {
  display: flex;
  gap: 10px;
}

.account-stat {
  border-left: 2px solid rgba(92, 155, 107, 0.4);
  padding-left: 8px;
}

.account-stat-num {
  font-family: 'Georgia', serif;
  font-size: 20px;
  font-weight: 700;
  color: #fff;
}

.account-stat-lbl {
  font-size: 10.5px;
  color: rgba(255, 255, 255, 0.4);
  margin-top: 3px;
}

.account-left-footer {
  font-size: 10.5px;
  color: rgba(255, 255, 255, 0.25);
  position: relative;
  z-index: 1;
}

/* ── RIGHT ── */
.account-right {
  flex: 1;
  background: #F5F0E8;
  padding: 36px 38px 32px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* ── TABS ── */
.account-tabs {
  display: flex;
  background: #EDE8DC;
  border: 1px solid #C8D9CA;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 30px;
  flex-shrink: 0;
  width: 430px;
  max-width: calc(100% - 56px);
  align-self: center;
}

.account-right-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0 24px 10px 0;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  scrollbar-gutter: stable;
}

.account-tab {
  flex: 1;
  padding: 11px;
  font-size: 13px;
  font-weight: 500;
  color: #7A8F7C;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  letter-spacing: 0.2px;
  font-family: inherit;
}

.account-tab-active {
  background: #1C3A1F;
  color: #fff;
  border-radius: 9px;
}

/* ── FORM ── */
.account-form {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.account-form-title {
  font-family: 'Georgia', serif;
  font-size: 24px;
  font-weight: 700;
  color: #1C3A1F;
  margin-bottom: 6px;
}

.account-form-sub {
  font-size: 13px;
  color: #7A8F7C;
  margin-bottom: 28px;
}

.account-field {
  margin-bottom: 18px;
}

.account-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #1C3A1F;
  margin-bottom: 6px;
  letter-spacing: 0.3px;
}

.account-input {
  width: 100%;
  padding: 12px 14px;
  font-size: 14px;
  color: #1C3A1F;
  background: #fff;
  border: 1px solid #C8D9CA;
  border-radius: 10px;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  font-family: inherit;
  box-sizing: border-box;
}

.account-input:focus {
  border-color: #5C9B6B;
  box-shadow: 0 0 0 3px rgba(92, 155, 107, 0.15);
}

.account-input::placeholder {
  color: #B0BFB2;
}

.account-btn {
  width: 100%;
  padding: 13px;
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  background: #1C3A1F;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.1s ease;
  font-family: inherit;
  margin-top: 8px;
  letter-spacing: 0.3px;
}

.account-btn:hover {
  background: #2A5530;
}

.account-btn:active {
  transform: scale(0.98);
}

/* ── RESPONSIVE ── */
@media (max-width: 720px) {
  .account-wrapper {
    flex-direction: column;
    border-radius: 16px;
  }

  .account-left {
    width: 100%;
    padding: 28px 28px;
    min-height: unset;
  }

  .account-left-headline {
    font-size: 22px;
  }

  .account-left-stats {
    gap: 14px;
  }

  .account-right {
    padding: 28px 24px;
  }
}
</style>
