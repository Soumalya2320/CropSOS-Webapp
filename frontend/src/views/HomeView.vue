<template>
  <section class="home-container">
    <section class="home-warpper">
      
      <section class="home-hero">
        <!-- hero section left -->
        <div class="hero-left">
          <div class="hero-left-upper">
            <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">
              energy_savings_leaf
            </span>
            <span class="hero-left-upper-text">Precision Agronomy</span>
          </div>
          <h1 class="hero-left-heading">CropSOS</h1>
          <p class="hero-left-p">Upload crop images to detect diseases and get AI-powered treatment
            advice from the world's most advanced digital agronomist.</p>
          <div class="hero-left-bottom">
            <button class="hero-left-button-button" @click="$router.push('/detect')">
              <span class="material-symbols-outlined">upload_file</span>
              Upload Image
            </button>
            <button class="btn-text" @click="$router.push('/about')">Learn More</button>
          </div>
        </div>
        <div class="hero-right">
          <div class="title-square-img">
            <img class="hero-img"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuD3QA7jqqpMTb_-8CXxh2cU6_gF3lOrNBlPUkrtqS95wQj-TAQZOjd69nX2MDov1PEmLLDXbpHX7TT1NX279FLU8G2B0uo2SxOlDWshrot370EGcnW6f12KoybAutZLAEi9SjmO7Uqv3uOa-vCoZl1rv7bykzDrdwHlhvs20ulyT-7-JhogYoFDPOFyd1vMwMew9Zu7DQCYa6wfESV42SiR_LUC3XT4AVxYMad5J96BNGOcwIGFA3VWz4C32DsVjCzZhYcdFxBp9eg">
          </div>
          <div class="hero-right-bottom">
            <div class="hero-right-icon">
              <span class="material-symbols-outlined check-circle">check_circle</span>
            </div>
            <div class="hero-right-bottom-text">
              <div class="u">
                Real-Time Analysis
              </div>
              <div class="b">99.4% Dignostic Accuracy</div>
            </div>
          </div>

        </div>
      </section>
      <section class="home-middle">
        <div class="home-middle-left">
          <span class="material-symbols-outlined span">biotech</span>
          <h3 class="home-middle-left-h3">Neural Dignostic Engine</h3>
          <p class="home-midlle-left-p">Our AI is trained on 10M+ curated agricultural datasets to
            identify 150+ plant pathogens across 30 major crop species.</p>
          <div class="home-middle-left-bottom">
            10M+ <span>IMAGES ANALYZED</span>
          </div>
        </div>
        <div class="home-middle-middle">
          <span class="material-symbols-outlined">speed</span>
          <h3>Instant Results</h3>
          <p>Diagnosis in under 3 seconds directly in the field, even with limited connectivity.</p>
        </div>
        <div class="home-middle-right">
          <span class="material-symbols-outlined">psychology</span>
          <h3>Expert Logic</h3>
          <p>Treatment protocols developed by certified agronomists and plant pathologists.</p>
        </div>
      </section>
      <section class="home-style">
        <div class="ht-left">
          <div class="ht-img">
            <img class="second-img"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuAYOlqSqukeWruxpLdlpoMq4FObZmgntoKP13hVQe2BrbJAnUdMoifaLCcrjy-WXMspGxiDVkoSAeKPt3Idt6-u3TNQMFDpXuoWBjFtW9q4Tb8rdedaleoH0LG1E6yFi7Hq-J-9FddrbOReE93WFAFyVTBSQaDdXwUfeDLxjNwQZ1QZUrY9w5QYfqbF9m8KBa4FO81DBjUGep5eTYAWtHMdLwdSgx64NRXKCzdw0fuKRmjxobb8dNV0k_AZPHDg0k7iEtI8I_EN_Dw">

          </div>
          <div class="ht-img-upper">
            <span class="material-symbols-outlined">warning</span>
            <span class="t-text">Late Blight Detected</span>
            <div>82% onfidence Score</div>
          </div>
        </div>
        <div class="ht-right">
          <h2>The Modern Path to <span class="h2-s">Yield Resilience</span></h2>
          <p>Traditional scouting takes days. CropSOS gives you answers in seconds.
            Our proprietary Diagnostic Blade overlay allows you to view field conditions through a lens of deep data.
          </p>
          <div class="htr-b">
            <h4>Automated Treatment Plans</h4>
            <p>Receive immediate dosages and chemical recommendations based on local regulations.</p>
          </div>
          <div class="htr-db">
            <h4>Disease Heatmapping</h4>
            <p>Visualize infection spread across your entire field via satellite integration.</p>
          </div>
        </div>
      </section>
      <section class="lb">
        <div class="ht-history">
          <h4>Ready to secure your harvest?</h4>
          <p>Join over 50,000 farmers worldwide who trust CropSOS for precision crop protection.</p>
          <button @click="$router.push('/detect')">Start Your First Scan</button>
        </div>
      </section>
    </section>
  </section>
</template>

<script>

// import { Bell, User } from 'lucide-vue'
// @ is an alias to /src

export default {
  name: 'HomeView'
}
</script>
<style scoped>
@import "../assets/HomeView.css";
</style>
