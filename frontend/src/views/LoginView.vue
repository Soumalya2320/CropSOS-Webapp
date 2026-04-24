<template>
  <div class="login-root">

    <h2 class="login-title">Welcome back !!</h2>
    <p class="login-sub">Sign in to your CropSOS dashboard to continue monitoring your crops.</p>

    <!-- EMAIL -->
    <div class="login-field">
      <label class="login-label">Email Address</label>
      <div class="login-input-wrap">
        <span class="material-symbols-outlined login-icon">mail</span>
        <input
          v-model="form.email"
          class="login-input"
          type="email"
          placeholder="ravi@example.com"
        />
      </div>
      <span class="login-err" v-if="errors.email">{{ errors.email }}</span>
    </div>

    <!-- PASSWORD -->
    <div class="login-field">
      <div class="login-label-row">
        <label class="login-label first">Password</label>
        <a class="login-forgot" href="#">Forgot password?</a>
      </div>
      <div class="login-input-wrap"> 
        <span class="material-symbols-outlined login-icon">lock</span>
        <input
          v-model="form.password"
          class="login-input"
          :type="showPass ? 'text' : 'password'"
          placeholder="Your password"
          style="padding-right: 44px;"
          @keyup.enter="handleLogin"
        />
        <button class="login-eye" type="button" @click="showPass = !showPass" tabindex="-1">
          <span class="material-symbols-outlined">{{ showPass ? 'visibility_off' : 'visibility' }}</span>
        </button>
      </div>
      <span class="login-err" v-if="errors.password">{{ errors.password }}</span>
    </div>

    <!-- REMEMBER ME -->
    <label class="login-chk">
      <input type="checkbox" v-model="form.remember" />
      Remember me for 30 days
    </label>

    <!-- API ERROR -->
    <div class="login-api-err" v-if="apiError">
      <span class="material-symbols-outlined" style="font-size:16px;">error</span>
      {{ apiError }}
    </div>

    <!-- SUBMIT -->
    <button class="login-btn" @click="handleLogin" :disabled="isLoading">
      <template v-if="!isLoading">
        <span class="material-symbols-outlined" style="font-size:18px;">login</span>
        Sign In to CropSOS
      </template>
      <span v-else class="login-spinner"></span>
    </button>

    <!-- DIVIDER -->
    <div class="login-divider">
      <div class="login-dline"></div>
      <span class="login-dtxt">or continue with</span>
      <div class="login-dline"></div>
    </div>

    <!-- GOOGLE -->
    <button class="login-google-btn" type="button">
      <svg width="18" height="18" viewBox="0 0 48 48">
        <path fill="#FFC107" d="M43.6 20.1H42V20H24v8h11.3C33.6 32.7 29.3 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.1 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.6-.4-3.9z"/>
        <path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.6 15.8 19 12 24 12c3.1 0 5.8 1.1 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/>
        <path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.3 35.3 26.8 36 24 36c-5.2 0-9.6-3.3-11.2-8H6.5C9.9 35.6 16.4 44 24 44z"/>
        <path fill="#1976D2" d="M43.6 20.1H42V20H24v8h11.3c-.8 2.2-2.3 4.2-4.2 5.6l6.2 5.2C43.2 35.5 48 28.5 48 24c0-1.3-.1-2.6-.4-3.9z"/>
      </svg>
      Continue with Google
    </button>

    <p class="login-register-note">
      Don't have an account?
      <a @click="$router.push('/account/register')">Create one free →</a>
    </p>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginView',
  data() {
    return {
      isLoading: false,
      apiError: '',
      showPass: false,
      form: {
        email:    '',
        password: '',
        remember: false
      },
      errors: {}
    }
  },
  methods: {
    validate() {
      const e = {}
      if (!this.form.email.trim() || !/\S+@\S+\.\S+/.test(this.form.email))
        e.email = 'Enter a valid email address.'
      if (!this.form.password)
        e.password = 'Please enter your password.'
      this.errors = e
      return Object.keys(e).length === 0
    },

    async handleLogin() {
      if (!this.validate()) return

      this.isLoading = true
      this.apiError  = ''

      try {
        const res = await axios.post('/api/auth/login', {
          email:    this.form.email,
          password: this.form.password,
          remember: this.form.remember
        })

        // Save token and user if returned
        if (res.data?.token) {
          localStorage.setItem('token', res.data.token)
        }
        if (res.data?.user) {
          localStorage.setItem('user', JSON.stringify(res.data.user))
        }

        // Redirect to detect page after login
        this.$router.push('/detect')

      } catch (err) {
        this.apiError = err.response?.data?.message || 'Invalid email or password. Please try again.'
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>

/* ── ROOT ── */
.login-root {
  flex: 1;
  width: 100%;
  max-width: 430px;
  margin: 0 auto;
  box-sizing: border-box;
}

/* ── TITLE ── */
.login-title {
  font-family: 'Georgia', serif;
  font-size: 26px;
  font-weight: 400;
  color: #1A2B1C;
  margin-bottom: 5px;
  line-height: 1.2;
}

.login-sub {
  font-size: 13px;
  color: #8FA490;
  margin-bottom: 26px;
  line-height: 1.55;
  text-align: left;
}

/* ── FIELD ── */
.login-field { 
  margin-bottom: 16px;
}

.login-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 7px;
}

.login-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #2E4830;
  margin-bottom: 7px;
  letter-spacing: 0.25px;
}

/* when inside label-row, remove bottom margin */
.login-label-row .login-label { margin-bottom: 0; }

.login-forgot {
  font-size: 12px;
  color: #2D5A32;
  font-weight: 500;
  text-decoration: none;
}

.login-forgot:hover { text-decoration: underline; }

/* ── INPUT WRAP ── */
.login-input-wrap { position: relative; }

.login-icon {
  position: absolute;
  left: 13px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 17px !important;
  color: #9DAF9F;
  pointer-events: none;
  line-height: 1;
}

.first { transform: none; }

/* ── INPUT ── */
.login-input {
  width: 100%;
  padding: 11px 14px 11px 40px;
  background: #F0EBE0;
  border: 1.5px solid #D6CEBC;
  border-radius: 10px;
  font-size: 13.5px;
  font-family: inherit;
  color: #1A2B1C;
  outline: none;
  transition: border-color 0.2s, background 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}

.login-input::placeholder { color: #B0BCA8; }

.login-input:hover {
  border-color: #B5C9B8;
  background: #EDE8DC;
}

.login-input:focus {
  border-color: #4A7C59;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(74, 124, 89, 0.12);
}

/* ── EYE ── */
.login-eye {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #9DAF9F;
  padding: 2px;
  display: flex;
  align-items: center;
  transition: color 0.2s;
}

.login-eye:hover { color: #4A7C59; }
.login-eye .material-symbols-outlined { font-size: 18px !important; }

/* ── CHECKBOX ── */
.login-chk {
  display: flex;
  align-items: center;
  gap: 9px;
  font-size: 12.5px;
  color: #8FA490;
  cursor: pointer;
  margin-bottom: 18px;
  user-select: none;
}

.login-chk input {
  accent-color: #2D5A32;
  width: 15px;
  height: 15px;
  flex-shrink: 0;
}

/* ── ERROR ── */
.login-err {
  font-size: 11px;
  color: #B94040;
  margin-top: 5px;
  display: block;
}

.login-api-err {
  display: flex;
  align-items: center;
  gap: 7px;
  background: #FEE9E9;
  border: 1px solid #F5BABA;
  border-radius: 9px;
  padding: 10px 14px;
  font-size: 12.5px;
  color: #B94040;
  margin-bottom: 14px;
}

/* ── SUBMIT BTN ── */
.login-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 13px;
  background: #1C3A1F;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
  letter-spacing: 0.2px;
  margin-bottom: 0;
}

.login-btn:hover:not(:disabled) { background: #2D5A32; }
.login-btn:active:not(:disabled) { transform: scale(0.985); }
.login-btn:disabled { opacity: 0.6; cursor: not-allowed; }

/* ── SPINNER ── */
.login-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ── DIVIDER ── */
.login-divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 18px 0;
}

.login-dline { flex: 1; height: 1px; background: #D6CEBC; }
.login-dtxt  { font-size: 11.5px; color: #9DAF9F; white-space: nowrap; }

/* ── GOOGLE ── */
.login-google-btn {
  width: 100%;
  padding: 11px;
  background: #F0EBE0;
  border: 1.5px solid #D6CEBC;
  border-radius: 10px;
  font-size: 13.5px;
  font-family: inherit;
  color: #1A2B1C;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.2s;
}

.login-google-btn:hover {
  background: #EDE8DC;
  border-color: #B5C9B8;
}

/* ── REGISTER NOTE ── */
.login-register-note {
  font-size: 12px;
  color: #9DAF9F;
  text-align: center;
  margin-top: 16px;
}

.login-register-note a {
  color: #2D5A32;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
}

.login-register-note a:hover { text-decoration: underline; }
</style>
