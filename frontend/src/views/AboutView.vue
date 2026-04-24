<template>
  <div class="about-container">
    <div class="about-hero">
      <div class="hero-badge">OUR MISSION</div>
      <h1 class="hero-title">Empowering the Future of <span class="highlight">Agriculture</span></h1>
      <p class="hero-subtitle">
        CropSOS bridges the gap between traditional farming and advanced AI diagnostics. 
        We believe that every farmer deserves instant, accurate, and actionable insights to protect their yield.
      </p>
    </div>

    <div class="about-grid">
      <div class="about-card">
        <span class="material-symbols-outlined card-icon">globe_uk</span>
        <h3>Global Impact</h3>
        <p>Trained on millions of data points from around the globe to recognize hyper-local plant diseases and pests.</p>
      </div>
      <div class="about-card">
        <span class="material-symbols-outlined card-icon">bolt</span>
        <h3>Real-time Speed</h3>
        <p>No waiting for lab results. Our ML models run instantly in the browser or on mobile, saving critical time.</p>
      </div>
      <div class="about-card">
        <span class="material-symbols-outlined card-icon">security</span>
        <h3>Yield Protection</h3>
        <p>We provide chemical and biological treatment plans verified by expert agronomists to secure your harvest.</p>
      </div>
    </div>

    <div class="about-cta">
      <h2>Join the agricultural revolution.</h2>
      <p>Start securing your crops today with precision AI diagnostics.</p>
      <button class="cta-button" @click="$router.push('/detect')">
        <span class="material-symbols-outlined">center_focus_strong</span>
        Scan a Crop Now
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutView'
}
</script>

<style scoped>
.about-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 60px 20px;
  font-family: 'Inter', system-ui, sans-serif;
  color: #1C3A1F;
}

.about-hero {
  text-align: center;
  margin-bottom: 80px;
  animation: fadeIn 0.8s ease-out;
}

.hero-badge {
  display: inline-block;
  padding: 6px 16px;
  background: #E8F0E9;
  color: #2D5A32;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1.5px;
  border-radius: 20px;
  margin-bottom: 20px;
}

.hero-title {
  font-family: 'Georgia', serif;
  font-size: 48px;
  margin: 0 0 20px;
  line-height: 1.1;
  color: #1C3A1F;
}

.highlight {
  color: #5C9B6B;
  font-style: italic;
}

.hero-subtitle {
  font-size: 18px;
  color: #5A7060;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.about-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 80px;
}

.about-card {
  background: #F0EBE0;
  padding: 40px 30px;
  border-radius: 20px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid #E4DCCB;
}

.about-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(28, 58, 31, 0.08);
  border-color: #C8D9CA;
}

.card-icon {
  font-size: 42px;
  color: #2D5A32;
  margin-bottom: 20px;
  background: #E8F0E9;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin-left: auto;
  margin-right: auto;
}

.about-card h3 {
  font-size: 22px;
  margin: 0 0 15px;
  color: #1C3A1F;
}

.about-card p {
  font-size: 15px;
  color: #5A7060;
  line-height: 1.6;
  margin: 0;
}

.about-cta {
  background: #1C3A1F;
  color: #FFF;
  border-radius: 24px;
  padding: 60px 40px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.about-cta::before {
  content: '';
  position: absolute;
  top: -50%; left: -10%;
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(92,155,107,0.3) 0%, transparent 70%);
  border-radius: 50%;
}

.about-cta h2 {
  font-family: 'Georgia', serif;
  font-size: 36px;
  margin: 0 0 15px;
  position: relative;
  z-index: 1;
}

.about-cta p {
  font-size: 18px;
  color: #C8D9CA;
  margin: 0 0 30px;
  position: relative;
  z-index: 1;
}

.cta-button {
  background: #5C9B6B;
  color: #FFF;
  border: none;
  padding: 16px 32px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
}

.cta-button:hover {
  background: #4A7C59;
  transform: scale(1.05);
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
  .hero-title { font-size: 36px; }
  .about-cta { padding: 40px 20px; }
  .about-cta h2 { font-size: 28px; }
}
</style>
