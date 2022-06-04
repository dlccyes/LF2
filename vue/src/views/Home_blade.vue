<script setup>
import Students from '@/components/Students.vue'
import Attendance from '@/components/Attendance.vue';
import Emotion from '@/components/Emotion.vue';
import TimeSlider from '@/components/TimeSlider.vue';
</script>

<template>

<h1>Current State of the Classroom</h1>
<TimeSlider />
<h2>Attendance</h2>
<Attendance/>
<h2>Classroom Vibe</h2>
<Emotion/>
<h2>Specific Students</h2>
<Students/>

</template>