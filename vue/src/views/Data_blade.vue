<script setup>
// import TimeSlider from '../components/TimeSlider.vue';
import Dashboard from '@/views/Dashboard_blade.vue'
import Student from '@/views/Student_blade.vue'

import { globeStore } from '@/stores/globe'
</script>

<script>
var adjusting = 0;
var resizing = 0;
export default {
  data() {
    return {
      reload: 0,
      globe:  globeStore(),
    }
  },
  methods: {
    refresh() {
      this.reload++;
    },
    windResize() {
      // prevent too many calls
      if(resizing){
        return;
      }
      resizing = 1;
      self = this;
      setTimeout(function(){
        self.globe.update++;
        resizing = 0;
      }, 500);
    },
  },
  computed: {
    timeRange(){
      return this.globe.timeRange;
    },
    isHome() {
      return this.$route.name == 'home'
    },
    isStudent() {
      return this.$route.name == 'student'
    },
    update() {
      return this.globe.update;
    },
  },
  watch: {
    timeRange(newVal, oldVal) {
      // prevent too many calls
      if(adjusting){
        return;
      }
      adjusting = 1;
      self = this;
      setTimeout(function(){
        self.globe.update++;
        adjusting = 0;
      }, 500);
    },
  },
  created() {
    window.addEventListener("resize", this.windResize);
  },
  destroyed() {
    window.removeEventListener("resize", this.windResize);
  },
}
</script>

<template>

<button class='btn' id="refresh" @click="refresh()">refresh</button>
<!-- <TimeSlider /> -->
<Dashboard v-if="isHome" :key="[reload]"/>
<Student v-if="isStudent" :key="[reload]"/>
</template>