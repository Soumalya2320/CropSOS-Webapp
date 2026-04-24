<template>
  <div id="app">
    <nav class="navbar-home">
      <div class="nav-main">
        <div class="nav-logo">CropSOS</div>
        <ul class="home-nav-links">
          <li :class="{ bottomLine: activeTap === 'home' }">
            <router-link to="/" @click.native="activeTap = 'home'">Home</router-link>
          </li>
          <li :class="{ bottomLine: activeTap === 'detect' }">
            <router-link to="/detect" @click.native="activeTap = 'detect'">Detect</router-link>
          </li>
          <li :class="{ bottomLine: activeTap === 'history' }">
            <router-link to="/history" @click.native="activeTap = 'history'">History</router-link>
          </li>
        </ul>
        <div class="nav-icons">
          <router-link class="nav-icon-link" to="/notifications" @click.native="activeTap = 'notifications'" aria-label="Notifications">
            <span class="material-symbols-outlined">notifications</span>
          </router-link>
          <router-link class="nav-icon-link" :to="accountIconTarget" @click.native="activeTap = accountIconActiveTab" aria-label="Account">
            <span class="material-symbols-outlined">account_circle</span>
          </router-link>
        </div>
      </div>
    </nav>
    <keep-alive include="DetectView">
      <router-view />
    </keep-alive>
  </div>
</template>

<script>


export default {
  data() {
    return {
      activeTap: 'home'
    }
  },
  computed: {
    isLoggedIn() {
      return Boolean(localStorage.getItem('token'))
    },
    accountIconTarget() {
      return this.isLoggedIn ? '/profile' : '/account/login'
    },
    accountIconActiveTab() {
      return this.isLoggedIn ? 'profile' : 'account'
    }
  },
  mounted() {
    this.syncActiveTab(this.$route.path)
  },
  watch: {
    '$route.path'(path) {
      this.syncActiveTab(path)
    }
  },
  methods: {
    syncActiveTab(path) {
      if (path === '/') this.activeTap = 'home'
      else if (path.startsWith('/detect')) this.activeTap = 'detect'
      else if (path.startsWith('/history')) this.activeTap = 'history'
      else if (path.startsWith('/profile')) this.activeTap = 'profile'
      else if (path.startsWith('/account')) this.activeTap = 'account'
    }
  }
}
</script>
<style>
@import "./assets/HomeView.css";
</style>
