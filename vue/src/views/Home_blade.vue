<script setup>
import TimeSlider from '../components/TimeSlider.vue';
import Students from '@/components/Students.vue'
import Attendance from '../components/Attendance.vue';
import Emotion from '../components/Emotion.vue';
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
    }
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

<h1>Current State of the Classroom</h1>
<button class='btn' id="refresh" @click="refresh()">refresh</button>
<TimeSlider />
<h2>Attendance</h2>
<Attendance :key="[update]"/>
<h2>Classroom Vibe</h2>
<Emotion :key="[update]"/>
<h2>Specific Students</h2>
<Students :key="[update]"/>

</template>