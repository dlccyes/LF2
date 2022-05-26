<script setup>
import Students from '@/components/Students.vue'
import Attendance from '../components/Attendance.vue';
import TimeSlider from '../components/TimeSlider.vue';
</script>

<script>
export default {
  data() {
    return {
      update: 0,
    }
  },
  methods: {
    refresh() {
      this.update++;
    }
  }
}
</script>

<template>

<h1>Current State of the Classroom</h1>
<button class='btn' id="refresh" @click="refresh()">refresh</button>
<TimeSlider />
<h2>Attendance</h2>
<Attendance :key="update"/>
<h2>Classroom Vibe</h2>
<div id="currentEmotionDiv"></div>
<div id="emotionGraphDiv"></div>
<div id="emotionCloudDiv"></div>
<h2>Specific Students</h2>
<Students :key="update"/>

</template>