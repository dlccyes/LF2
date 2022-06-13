<script>
import axios from 'axios';
import { globeStore } from '@/stores/globe'

export default {
  data() {
    return {
      students: [],
      globe:  globeStore(),
    }
  },
  methods: {
    getAttendanceCount() {
      var self = this; // can't access this in axios
      var objData = {
        'time_range': this.globe.timeRange
      };
      axios.post("/student-attendance-count", objData)
      .then(function(result){
        console.log(result);
        self.students = result.data.data.attendance_count;
      })
      .catch(function(error){
        console.log(error);
        self.students = [];
      });
    },
    refresh(){
      this.getAttendanceCount();
    },
  },
  mounted() {
    this.refresh();
  },
  computed: {
    update(){
      return this.globe.update;
    },
  },
  watch: {
    update(){
      this.refresh();
    },
  }
}
</script>

<template>

<div class="fontMono">
  <ol>
    <li v-for="student in students">
      <router-link :to="{name: 'student', params: {id: student[0]}}"> {{ student[0] }}</router-link>: {{ student[1] }}
    </li>
  </ol>
</div>

</template>