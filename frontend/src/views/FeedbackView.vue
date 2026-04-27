<template>
  <div class="feedback-container">
    <div class="feedback-wrapper">
      
      <!-- Left Side: Illustration & Intro -->
      <div class="feedback-info">
        <div class="info-badge">FEEDBACK</div>
        <h1 class="info-title">Help us protect<br/><span class="highlight">more harvests.</span></h1>
        <p class="info-text">
          CropSOS is built for farmers. Your feedback directly shapes our AI 
          models and features. Tell us what we're doing right, or what we can fix.
        </p>
        
        <div class="feedback-stats">
          <div class="stat-item">
            <span class="material-symbols-outlined stat-icon">group</span>
            <div>
              <div class="stat-num">50k+</div>
              <div class="stat-label">Active Farmers</div>
            </div>
          </div>
          <div class="stat-item">
            <span class="material-symbols-outlined stat-icon">verified</span>
            <div>
              <div class="stat-num">98.4%</div>
              <div class="stat-label">Reported Accuracy</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Side: Form -->
      <div class="feedback-form-card">
        <div v-if="submitted" class="success-msg">
          <span class="material-symbols-outlined success-icon">check_circle</span>
          <h2>Thank You!</h2>
          <p>Your feedback has been received. Our team will review it shortly.</p>
          <button class="back-btn" @click="$router.push('/')">Return Home</button>
        </div>

        <form v-else @submit.prevent="submitFeedback">
          <div class="form-group">
            <label>How was your experience?</label>
            <div class="star-rating">
              <span 
                v-for="star in 5" 
                :key="star" 
                class="material-symbols-outlined star"
                :class="{ 'star-active': star <= rating }"
                @click="rating = star"
              >
                star
              </span>
            </div>
          </div>

          <div class="form-group">
            <label for="category">What is this about?</label>
            <select id="category" v-model="form.category" required>
              <option value="" disabled selected>Select a category</option>
              <option value="Accuracy">Diagnostic Accuracy</option>
              <option value="UIUX">Interface & Design</option>
              <option value="Performance">App Speed/Performance</option>
              <option value="Feature">Feature Request</option>
              <option value="Bug">Report a Bug</option>
            </select>
          </div>

          <div class="form-group">
            <label for="message">Detailed Feedback</label>
            <textarea 
              id="message" 
              v-model="form.message" 
              placeholder="Tell us more about your experience..."
              required
            ></textarea>
          </div>

          <button type="submit" class="submit-btn" :disabled="isSubmitting">
            <template v-if="!isSubmitting">
              Send Feedback
              <span class="material-symbols-outlined">send</span>
            </template>
            <span v-else class="spinner"></span>
          </button>
        </form>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'FeedbackView',
  data() {
    return {
      rating: 0,
      form: {
        category: '',
        message: ''
      },
      isSubmitting: false,
      submitted: false
    }
  },
  methods: {
    async submitFeedback() {
      if (this.rating === 0) {
        alert('Please select a rating before submitting.')
        return
      }

      this.isSubmitting = true

      try {
        const user = JSON.parse(localStorage.getItem("user") || "{}")

        await axios.post("/feedback", {
          reportId: this.reportId || "general-feedback",
          userId: user.id || user._id,
          isCorrect: this.rating >= 3,   // simple logic (3+ = positive)
          rating: this.rating,
          category: this.form.category,
          message: this.form.message
        })

        this.submitted = true

      } catch (err) {
        console.error("Feedback error:", err)
        alert("Failed to submit feedback")
      } finally {
        this.isSubmitting = false
      }
    }
  }
}
</script>

<style scoped>
.feedback-container {
  min-height: 100vh;
  background: #F5F0E8;
  padding: 80px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.feedback-wrapper {
  max-width: 1100px;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 60px;
  align-items: center;
}

/* ── Left Side ── */
.feedback-info {
  animation: slideIn 0.6s ease-out;
}

.info-badge {
  display: inline-block;
  padding: 6px 14px;
  background: #D4E8D8;
  color: #2D5A32;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
  border-radius: 20px;
  margin-bottom: 20px;
}

.info-title {
  font-family: 'Georgia', serif;
  font-size: 44px;
  color: #1A2B1C;
  line-height: 1.1;
  margin-bottom: 24px;
}

.highlight {
  color: #5C9B6B;
}

.info-text {
  font-size: 16px;
  color: #5A7060;
  line-height: 1.6;
  margin-bottom: 40px;
}

.feedback-stats {
  display: flex;
  gap: 40px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-icon {
  font-size: 32px;
  color: #2D5A32;
  background: #fff;
  width: 54px;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
}

.stat-num {
  font-size: 18px;
  font-weight: 700;
  color: #1A2B1C;
}

.stat-label {
  font-size: 12px;
  color: #9DAF9F;
}

/* ── Form Card ── */
.feedback-form-card {
  background: #fff;
  padding: 50px;
  border-radius: 24px;
  border: 1px solid #D6CEBC;
  box-shadow: 0 20px 40px rgba(28, 58, 31, 0.05);
  animation: fadeIn 0.8s ease-out;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #1A2B1C;
  margin-bottom: 10px;
}

/* ── Star Rating ── */
.star-rating {
  display: flex;
  gap: 8px;
}

.star {
  font-size: 32px !important;
  color: #E0E0E0;
  cursor: pointer;
  transition: color 0.2s, transform 0.2s;
}

.star:hover {
  transform: scale(1.1);
  color: #FFD700;
}

.star-active {
  color: #FFD700 !important;
  font-variation-settings: 'FILL' 1;
}

/* ── Inputs ── */
select, textarea {
  width: 100%;
  padding: 14px;
  border: 1px solid #E0E0E0;
  border-radius: 12px;
  font-family: inherit;
  font-size: 15px;
  transition: border-color 0.2s;
}

select:focus, textarea:focus {
  outline: none;
  border-color: #5C9B6B;
}

textarea {
  min-height: 120px;
  resize: vertical;
}

.submit-btn {
  width: 100%;
  padding: 16px;
  background: #1C3A1F;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  transition: all 0.3s;
}

.submit-btn:hover:not(:disabled) {
  background: #2D5A32;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ── Success Message ── */
.success-msg {
  text-align: center;
}

.success-icon {
  font-size: 64px !important;
  color: #5C9B6B;
  margin-bottom: 20px;
}

.back-btn {
  margin-top: 24px;
  background: transparent;
  border: 1px solid #E0E0E0;
  padding: 12px 24px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
}

/* ── Utils ── */
.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
@keyframes slideIn { from { opacity: 0; transform: translateX(-30px); } to { opacity: 1; transform: translateX(0); } }
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

@media (max-width: 900px) {
  .feedback-wrapper {
    grid-template-columns: 1fr;
    gap: 40px;
  }
  .feedback-form-card {
    padding: 30px;
  }
  .info-title {
    font-size: 36px;
  }
}
</style>
