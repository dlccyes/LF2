<script setup>
import { globeStore } from '@/stores/globe'
</script>
<script>
export default {
  data() {
    return {
      globe:  globeStore(),
    }
  },
  computed: {
    isHome(){
      return this.$route.name == 'home';
    },
  },
  methods: {
    meditate(){
      if(this.globe.night == 1){
        document.getElementById("night-btn").innerHTML = "🌞";
        document.documentElement.dataset.theme = "day";
        this.globe.night = 0;
      }else{
        document.getElementById("night-btn").innerHTML = "🌝";
        document.documentElement.dataset.theme = "night";
        this.globe.night = 1;
      }
      this.globe.update++;
    },
    nightEnter(){
      if(this.globe.night == 1){
        document.getElementById("night-btn").innerHTML = "🌝";
      }else{
        document.getElementById("night-btn").innerHTML = "🌞";
      }
    },
    nightLeave(){
      if(this.globe.night == 1){
        document.getElementById("night-btn").innerHTML = "🌙";
      }else{
        document.getElementById("night-btn").innerHTML = "⛅";
      }
    }
  },
  mounted() {
    document.getElementById("night-btn").addEventListener("mouseenter", this.nightEnter);
    document.getElementById("night-btn").addEventListener("mouseleave", this.nightLeave);
  },
}
</script>

<template>

<span id="night-btn" @click="meditate()">🌙</span>
<div id="nav">
  <router-link v-if="!isHome" to="/">Dashboard</router-link>
</div>
<router-view/>

</template>