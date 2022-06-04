<script setup>
import TimeSlider from '../components/TimeSlider.vue';
import Home from '@/views/Home_blade.vue'
import Student from '@/views/Student_blade.vue'

import { globeStore } from '@/stores/globe'
</script>

<script>
var adjusting = 0;
var resizing = 0;
export default {
  data() {
    return {
      update: 0,
      globe:  globeStore(),
    }
  },
  methods: {
    refresh() {
      this.update++;
    },
    windResize() {
      // prevent too many calls
      if(resizing){
        return;
      }
      resizing = 1;
      self = this;
      setTimeout(function(){
        self.update++;
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
        self.update++;
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
<Home v-if="isHome" :key="[update]"/>
<Student v-if="isStudent" :key="[update]"/>
</template>