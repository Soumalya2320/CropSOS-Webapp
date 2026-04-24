<template>
  <div class="reg-root">

    <!-- ── STEP INDICATOR ── -->
    <div class="reg-steps" v-if="currentStep < 3">
      <div
        v-for="n in 3"
        :key="n"
        class="reg-step-dot"
        :class="{
          'reg-step-done'   : n < currentStep,
          'reg-step-active' : n === currentStep
        }"
      ></div>
      <span class="reg-step-label">
        Step <strong>{{ currentStep }}</strong> of 3
      </span>
    </div>

    <!-- ══════════════════════════════════
         STEP 1 — Personal Details
    ══════════════════════════════════ -->
    <div v-if="currentStep === 1">
      <h2 class="reg-title">Create your account</h2>
      <p class="reg-sub">Start with your personal details. Takes less than 2 minutes.</p>

      <div class="reg-row">
        <div class="reg-field first">
          <label class="reg-label">First Name</label>
          <div class="reg-input-wrap first">
            <span class="material-symbols-outlined reg-icon">person</span>
            <input v-model="form.firstName" class="reg-input" type="text" placeholder="Piyu" />
          </div>
          <span class="reg-err" v-if="errors.firstName">{{ errors.firstName }}</span>
        </div>
        <div class="reg-field first"> 
          <label class="reg-label">Last Name</label>
          <div class="reg-input-wrap first">
            <span class="material-symbols-outlined reg-icon">person</span>
            <input v-model="form.lastName" class="reg-input" type="text" placeholder="Singh" />
          </div>
          <span class="reg-err" v-if="errors.lastName">{{ errors.lastName }}</span>
        </div>
      </div>

      <div class="reg-field">
        <label class="reg-label">Email Address</label>
        <div class="reg-input-wrap second">
          <span class="material-symbols-outlined reg-icon">mail</span>
          <input v-model="form.email" class="reg-input" type="email" placeholder="ravi@example.com" />
        </div>
        <span class="reg-err" v-if="errors.email">{{ errors.email }}</span>
      </div>

      <div class="reg-field">
        <label class="reg-label">
          Phone Number <span class="reg-optional">(optional)</span>
        </label>
        <div class="reg-input-wrap second">
          <span class="material-symbols-outlined reg-icon">call</span>
          <input v-model="form.phone" class="reg-input" type="tel" placeholder="+91 98765 43210" />
        </div>
      </div>

      <div class="reg-field">
        <label class="reg-label">Password</label>
        <div class="reg-input-wrap second">
          <span class="material-symbols-outlined reg-icon">lock</span>
          <input
            v-model="form.password"
            class="reg-input"
            :type="showPass ? 'text' : 'password'"
            placeholder="Min. 8 characters"
            style="padding-right: 44px;"
            @input="updateStrength"
          />
          <button class="reg-eye" type="button" @click="showPass = !showPass" tabindex="-1">
            <span class="material-symbols-outlined">{{ showPass ? 'visibility_off' : 'visibility' }}</span>
          </button>
        </div>
        <div class="str-bar">
          <div
            v-for="i in 4" :key="i"
            class="str-seg second" 
            :style="i <= strength ? { background: strengthColor } : {}"
          ></div>
        </div>
        <span class="str-lbl" :style="{ color: strengthColor }">{{ strengthLabel }}</span>
        <span class="reg-err" v-if="errors.password">{{ errors.password }}</span>
      </div>

      <div class="reg-field">
        <label class="reg-label">Confirm Password</label>
        <div class="reg-input-wrap second">
          <span class="material-symbols-outlined reg-icon">lock</span>
          <input
            v-model="form.confirmPassword"
            class="reg-input"
            :type="showConfirm ? 'text' : 'password'"
            placeholder="Re-enter password"
            style="padding-right: 44px;"
          />
          <button class="reg-eye" type="button" @click="showConfirm = !showConfirm" tabindex="-1">
            <span class="material-symbols-outlined">{{ showConfirm ? 'visibility_off' : 'visibility' }}</span>
          </button>
        </div>
        <span class="reg-err" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</span>
      </div>

      <div class="reg-btn-row">
        <button class="reg-btn-next" @click="step1Next">
          Continue
          <span class="material-symbols-outlined" style="font-size:18px;">arrow_forward</span>
        </button>
      </div>

      <div class="reg-divider">
        <div class="reg-dline"></div>
        <span class="reg-dtxt">or sign up with</span>
        <div class="reg-dline"></div>
      </div>

      <button class="reg-google-btn" type="button">
        <svg width="18" height="18" viewBox="0 0 48 48">
          <path fill="#FFC107" d="M43.6 20.1H42V20H24v8h11.3C33.6 32.7 29.3 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.1 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.6-.4-3.9z"/>
          <path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.6 15.8 19 12 24 12c3.1 0 5.8 1.1 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/>
          <path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.3 35.3 26.8 36 24 36c-5.2 0-9.6-3.3-11.2-8H6.5C9.9 35.6 16.4 44 24 44z"/>
          <path fill="#1976D2" d="M43.6 20.1H42V20H24v8h11.3c-.8 2.2-2.3 4.2-4.2 5.6l6.2 5.2C43.2 35.5 48 28.5 48 24c0-1.3-.1-2.6-.4-3.9z"/>
        </svg>
        Continue with Google
      </button>

      <p class="reg-signin-note">
        Already have an account?
        <a @click="$router.push('/account/login')">Sign in →</a>
      </p>
    </div>

    <!-- ══════════════════════════════════
         STEP 2 — Farm Profile
    ══════════════════════════════════ -->
    <div v-if="currentStep === 2">
      <h2 class="reg-title">Your farm profile</h2>
      <p class="reg-sub">Help us personalize your disease alerts and crop recommendations.</p>

      <div class="reg-field">
        <label class="reg-label">Farm / Field Name</label>
        <div class="reg-input-wrap">
          <span class="material-symbols-outlined reg-icon">home</span>
          <input v-model="form.farmName" class="reg-input" type="text" placeholder="e.g. Green Valley Farm" />
        </div>
        <span class="reg-err" v-if="errors.farmName">{{ errors.farmName }}</span>
      </div>

      <div class="reg-row">
        <div class="reg-field">
          <label class="reg-label">State / Region</label>
          <div class="reg-input-wrap">
            <span class="material-symbols-outlined reg-icon">location_on</span>
            <select v-model="form.state" class="reg-input reg-select">
              <option value="">Select state</option>
              <option>Punjab</option>
              <option>Haryana</option>
              <option>Uttar Pradesh</option>
              <option>Maharashtra</option>
              <option>Karnataka</option>
              <option>Tamil Nadu</option>
              <option>Andhra Pradesh</option>
              <option>Rajasthan</option>
              <option>Gujarat</option>
              <option>Madhya Pradesh</option>
              <option>West Bengal</option>
              <option>Other</option>
            </select>
          </div>
          <span class="reg-err" v-if="errors.state">{{ errors.state }}</span>
        </div>
        <div class="reg-field">
          <label class="reg-label">Farm Size (acres)</label>
          <div class="reg-input-wrap">
            <span class="material-symbols-outlined reg-icon">grid_view</span>
            <input v-model="form.farmSize" class="reg-input" type="number" placeholder="e.g. 5" min="0" />
          </div>
        </div>
      </div>

      <div class="reg-field">
        <label class="reg-label" style="margin-bottom:10px;">Primary Crop Type</label>
        <div class="reg-crop-group">
          <div
            v-for="crop in cropOptions" :key="crop.value"
            class="reg-crop-card"
            :class="{ 'reg-crop-selected': form.cropType === crop.value }"
            @click="form.cropType = crop.value"
          >
            <span class="reg-crop-icon">{{ crop.icon }}</span>
            <div class="reg-crop-lbl">{{ crop.label }}</div>
            <div class="reg-crop-sub">{{ crop.sub }}</div>
          </div>
        </div>
        <span class="reg-err" v-if="errors.cropType">{{ errors.cropType }}</span>
      </div>

      <div class="reg-field">
        <label class="reg-label">Irrigation Method</label>
        <div class="reg-input-wrap">
          <span class="material-symbols-outlined reg-icon">water_drop</span>
          <select v-model="form.irrigation" class="reg-input reg-select">
            <option value="">Select method</option>
            <option>Drip Irrigation</option>
            <option>Sprinkler</option>
            <option>Flood / Surface</option>
            <option>Rainfed only</option>
            <option>Canal / River</option>
          </select>
        </div>
      </div>

      <label class="reg-chk">
        <input type="checkbox" v-model="form.alertsEnabled" />
        Send me regional blight and disease alerts for my crop and location.
      </label>

      <label class="reg-chk">
        <input type="checkbox" v-model="form.termsAccepted" />
        I agree to the <a href="#" class="reg-link">Terms of Service</a> and
        <a href="#" class="reg-link">Privacy Policy</a> of CropSOS.
      </label>
      <span class="reg-err" v-if="errors.terms">{{ errors.terms }}</span>

      <div class="reg-api-err" v-if="apiError">
        <span class="material-symbols-outlined" style="font-size:16px;">error</span>
        {{ apiError }}
      </div>

      <div class="reg-btn-row">
        <button class="reg-btn-back" @click="currentStep = 1">
          <span class="material-symbols-outlined" style="font-size:16px;">arrow_back</span>
          Back
        </button>
        <button class="reg-btn-next" @click="step2Submit" :disabled="isLoading">
          <template v-if="!isLoading">
            Create Account
            <span class="material-symbols-outlined" style="font-size:18px;">edit</span>
          </template>
          <span v-else class="reg-spinner"></span>
        </button>
      </div>
    </div>

    <!-- ══════════════════════════════════
         STEP 3 — Success
    ══════════════════════════════════ -->
    <div v-if="currentStep === 3" class="reg-success">
      <div class="reg-success-icon">
        <span class="material-symbols-outlined" style="font-size:36px; color:#2D5A32;">check_circle</span>
      </div>
      <h2 class="reg-success-title">Welcome to CropSOS!</h2>
      <p class="reg-success-sub">
        Your account is ready, <strong>{{ form.firstName }}</strong>. You can now scan crops,
        track field health, and get AI-powered treatment advice instantly.
      </p>
      <div class="reg-pills">
        <div class="reg-pill"><span class="reg-pill-dot"></span> AI Diagnostics enabled</div>
        <div class="reg-pill"><span class="reg-pill-dot"></span> Disease alerts active</div>
        <div class="reg-pill"><span class="reg-pill-dot"></span> History tracking on</div>
      </div>
      <button class="reg-btn-next reg-btn-center" @click="$router.push('/detect')">
        <span class="material-symbols-outlined" style="font-size:18px;">search</span>
        Start Your First Scan
      </button>
      <p class="reg-signin-note" style="margin-top:14px;">First scan is free · No credit card required</p>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RegisterView',
  data() {
    return {
      currentStep: 1,
      isLoading: false,
      apiError: '',
      showPass: false,
      showConfirm: false,
      strength: 0,
      strengthColor: '#C8D9CA',
      strengthLabel: 'Enter a password',
      cropOptions: [
        { value: 'Cereals',    icon: '🌾', label: 'Cereals',    sub: 'Wheat, rice, maize' },
        { value: 'Vegetables', icon: '🥦', label: 'Vegetables', sub: 'Tomato, potato, onion' },
        { value: 'Fruits',     icon: '🍇', label: 'Fruits',     sub: 'Mango, grapes, citrus' }
      ],
      form: {
        firstName: '', lastName: '', email: '', phone: '',
        password: '', confirmPassword: '',
        farmName: '', state: '', farmSize: '',
        cropType: '', irrigation: '',
        alertsEnabled: true, termsAccepted: false
      },
      errors: {}
    }
  },
  methods: {
    updateStrength() {
      const v = this.form.password
      const colors = ['#C0392B', '#E67E22', '#F1C40F', '#27AE60']
      const labels = ['Weak', 'Fair', 'Good', 'Strong']
      if (!v) {
        this.strength = 0; this.strengthColor = '#C8D9CA'; this.strengthLabel = 'Enter a password'; return
      }
      let score = 0
      if (v.length >= 8)          score++
      if (/[A-Z]/.test(v))        score++
      if (/[0-9]/.test(v))        score++
      if (/[^A-Za-z0-9]/.test(v)) score++
      score = Math.max(1, score)
      this.strength = score
      this.strengthColor = colors[score - 1]
      this.strengthLabel = labels[score - 1]
    },
    step1Next() {
      const e = {}
      if (!this.form.firstName.trim())  e.firstName = 'Please enter your first name.'
      if (!this.form.lastName.trim())   e.lastName  = 'Please enter your last name.'
      if (!this.form.email.trim() || !/\S+@\S+\.\S+/.test(this.form.email)) e.email = 'Enter a valid email address.'
      if (this.form.password.length < 8) e.password = 'Password must be at least 8 characters.'
      if (this.form.password !== this.form.confirmPassword) e.confirmPassword = 'Passwords do not match.'
      this.errors = e
      if (Object.keys(e).length === 0) this.currentStep = 2
    },
    async step2Submit() {
      const e = {}
      if (!this.form.farmName.trim()) e.farmName = 'Please enter your farm name.'
      if (!this.form.state)           e.state    = 'Please select your state.'
      if (!this.form.cropType)        e.cropType = 'Please select a crop type.'
      if (!this.form.termsAccepted)   e.terms    = 'You must accept the terms to continue.'
      this.errors = e
      if (Object.keys(e).length > 0) return

      this.isLoading = true
      this.apiError  = ''
      try {
        const res = await axios.post('/api/auth/register', {
          first_name:     this.form.firstName,
          last_name:      this.form.lastName,
          email:          this.form.email,
          phone:          this.form.phone,
          password:       this.form.password,
          farm_name:      this.form.farmName,
          state:          this.form.state,
          farm_size:      this.form.farmSize,
          crop_type:      this.form.cropType,
          irrigation:     this.form.irrigation,
          alerts_enabled: this.form.alertsEnabled
        })
        if (res.data?.token) {
          localStorage.setItem('token', res.data.token)
        }
        if (res.data?.user) {
          localStorage.setItem('user', JSON.stringify(res.data.user))
        }
        this.currentStep = 3
      } catch (err) {
        this.apiError = err.response?.data?.message || 'Something went wrong. Please try again.'
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>

/* ── ROOT ── */
.reg-root { flex: 1; }

/* ── STEP DOTS ── */
.reg-steps {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 22px;
}

.reg-step-dot {
  width: 32px;
  height: 4px;
  border-radius: 4px;
  background: #D6CEBC;
  transition: background 0.3s;
}

.reg-step-done   { background: #5C9B6B; }
.reg-step-active { background: #1C3A1F; }

.reg-step-label {
  font-size: 11.5px;
  color: #9DAF9F;
  margin-left: 7px;
}

.reg-step-label strong { color: #1C3A1F; }

/* ── TITLE ── */
.reg-title {
  font-family: 'Georgia', serif;
  font-size: 26px;
  font-weight: 400;
  color: #1A2B1C;
  margin-bottom: 5px;
  line-height: 1.2;
  transform: translateX(23px);
}

.reg-sub {
  font-size: 13px;
  color: #8FA490;
  margin-bottom: 20px;
  line-height: 1.55;
  text-align: left;
}

/* ── GRID ROW ── */
.reg-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

/* ── FIELD ── */
.reg-field { margin-bottom: 14px; }

.reg-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #2E4830;
  margin-bottom: 7px;
  letter-spacing: 0.25px;
}

.first {
  transform: translateX(-25px);
}

.second {
  transform: translateX(-25px);
}

.reg-optional {
  font-weight: 400;
  color: #9DAF9F;
}

/* ── INPUT WRAP ── */
.reg-input-wrap { position: relative; }

.reg-icon {
  position: absolute;
  left: 13px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 17px !important;
  color: #9DAF9F;
  pointer-events: none;
  line-height: 1;
}

/* ── INPUT ── */
.reg-input {
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
  appearance: none;
}

.reg-input::placeholder {
  color: #B0BCA8;
}

.reg-input:hover {
  border-color: #B5C9B8;
  background: #EDE8DC;
}

.reg-input:focus {
  border-color: #4A7C59;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(74, 124, 89, 0.12);
}

/* ── SELECT ── */
.reg-select {
  cursor: pointer;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%239DAF9F' stroke-width='2.5'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  padding-right: 36px;
}

/* ── EYE BUTTON ── */
.reg-eye {
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

.reg-eye:hover { color: #4A7C59; }

.reg-eye .material-symbols-outlined { font-size: 18px !important; }

/* ── STRENGTH ── */
.str-bar {
  display: flex;
  gap: 5px;
  margin-top: 8px;
}

.str-seg {
  height: 3px;
  flex: 1;
  border-radius: 2px;
  background: #D6CEBC;
  transition: background 0.3s;
}

.str-lbl {
  font-size: 11px;
  color: #9DAF9F;
  margin-top: 5px;
  display: block;
}

/* ── ERROR ── */
.reg-err {
  font-size: 11px;
  color: #B94040;
  margin-top: 5px;
  display: block;
}

.reg-api-err {
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

/* ── CROP CARDS ── */
.reg-crop-group {
  display: flex;
  gap: 10px;
  margin-bottom: 4px;
}

.reg-crop-card {
  flex: 1;
  border: 1.5px solid #D6CEBC;
  border-radius: 10px;
  padding: 12px 10px;
  cursor: pointer;
  transition: all 0.2s;
  background: #F0EBE0;
  text-align: center;
}

.reg-crop-card:hover {
  border-color: #5C9B6B;
  background: #E8F0E9;
}

.reg-crop-selected {
  border-color: #2D5A32 !important;
  background: rgba(45, 90, 50, 0.07) !important;
}

.reg-crop-icon { font-size: 22px; display: block; margin-bottom: 5px; }

.reg-crop-lbl {
  font-size: 12.5px;
  font-weight: 600;
  color: #2E4830;
}

.reg-crop-selected .reg-crop-lbl { color: #1C3A1F; }

.reg-crop-sub {
  font-size: 10.5px;
  color: #9DAF9F;
  margin-top: 2px;
  line-height: 1.3;
}

/* ── CHECKBOX ── */
.reg-chk {
  display: flex;
  align-items: flex-start;
  gap: 9px;
  font-size: 12.5px;
  color: #8FA490;
  cursor: pointer;
  margin-bottom: 10px;
  line-height: 1.55;
}

.reg-chk input {
  accent-color: #2D5A32;
  width: 15px;
  height: 15px;
  margin-top: 2px;
  flex-shrink: 0;
}

.reg-link { color: #2D5A32; text-decoration: none; }
.reg-link:hover { text-decoration: underline; }

/* ── BUTTONS ── */
.reg-btn-row {
  display: flex;
  gap: 10px;
  margin-top: 8px;
}

.reg-btn-back {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 11px 18px;
  background: transparent;
  border: 1.5px solid #D6CEBC;
  border-radius: 10px;
  font-size: 13px;
  font-family: inherit;
  color: #5A7060;
  cursor: pointer;
  transition: all 0.2s;
}

.reg-btn-back:hover {
  background: #EDE8DC;
  border-color: #B5C9B8;
}

.reg-btn-next {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
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
}

.reg-btn-next:hover:not(:disabled) { background: #2D5A32; }
.reg-btn-next:active:not(:disabled) { transform: scale(0.985); }
.reg-btn-next:disabled { opacity: 0.6; cursor: not-allowed; }

.reg-btn-center {
  flex: unset;
  width: 240px;
  margin: 0 auto;
}

/* ── SPINNER ── */
.reg-spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ── DIVIDER ── */
.reg-divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 16px 0;
}

.reg-dline { flex: 1; height: 1px; background: #D6CEBC; }

.reg-dtxt { font-size: 11.5px; color: #9DAF9F; white-space: nowrap; }

/* ── GOOGLE ── */
.reg-google-btn {
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

.reg-google-btn:hover {
  background: #EDE8DC;
  border-color: #B5C9B8;
}

/* ── SIGN-IN NOTE ── */
.reg-signin-note {
  font-size: 12px;
  color: #9DAF9F;
  text-align: center;
  margin-top: 14px;
}

.reg-signin-note a {
  color: #2D5A32;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
}

.reg-signin-note a:hover { text-decoration: underline; }

/* ── SUCCESS ── */
.reg-success { text-align: center; padding: 20px 0; }

.reg-success-icon {
  width: 72px; height: 72px;
  border-radius: 50%;
  background: #D4E8D8;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 18px;
}

.reg-success-title {
  font-family: 'Georgia', serif;
  font-size: 26px; font-weight: 400;
  color: #1A2B1C; margin-bottom: 10px;
}

.reg-success-sub {
  font-size: 13px; color: #8FA490; line-height: 1.65;
  margin-bottom: 22px; max-width: 300px;
  margin-left: auto; margin-right: auto;
}

.reg-pills {
  display: flex; flex-wrap: wrap; gap: 8px;
  justify-content: center; margin-bottom: 24px;
}

.reg-pill {
  display: flex; align-items: center; gap: 7px;
  background: #F0EBE0;
  border: 1px solid #D6CEBC;
  border-radius: 20px;
  padding: 6px 16px;
  font-size: 12px; color: #3D5440;
}

.reg-pill-dot {
  width: 7px; height: 7px;
  border-radius: 50%; background: #5C9B6B; flex-shrink: 0;
}
</style>