<script setup>
import TimeSlider from '@/components/TimeSlider.vue';
</script>

<script>
import axios from 'axios';
import { drawLine } from '@/helper.js';
import { globeStore } from '@/stores/globe'

export default {
  data() {
    return {
      studentAttendanceHtml: '',
      attendanceGraphDivHtml: '',
      globe:  globeStore(),
      studentId: this.$route.params.id,
    }
  },
  methods: {
    getStudentAttendance() {
      var self = this; // can't access this in axios
      var url = "/student-attendance"
      var objData = {
        'time_range': this.globe.timeRange,
        'student_id': this.studentId
      };
      axios.post(url, objData)
      .then(function(result){
        console.log(result);
        var studentAttendance = result.data.data.student_attendance;
        var attendanceDataNum = studentAttendance.length;
        // get the most recent attendance data
        var isPresent;
        if(attendanceDataNum == 0){
          isPresent = 0;
        }else{
          isPresent = studentAttendance[attendanceDataNum-1][1];
        }
        self.studentAttendanceHtml = '';
        if(isPresent){
          self.studentAttendanceHtml += 'Present';
        }
        else{
          self.studentAttendanceHtml += 'Absent';
        }
        if(attendanceDataNum < 2){
          self.attendanceGraphDivHtml = 'Not enough data to show graph.';
        }else{
          self.attendanceGraphDivHtml = '';
          var attandanceVsTimeArr = [];
          for(var item of studentAttendance){
            attandanceVsTimeArr.push([new Date(item[0]), item[1]]);
          }
          attandanceVsTimeArr.sort();
          drawLine(attandanceVsTimeArr, 'attendanceGraphDiv', 'log time', 'Is present?');
        }
      });
    },
  },
  mounted() {
    this.getStudentAttendance();
  }
}
</script>

<template>

<h1>{{ studentId }}</h1>
<TimeSlider />
<div id="studentAttendance">{{ studentAttendanceHtml }}</div>
<div id="attendanceGraphDiv">{{ attendanceGraphDivHtml }}</div>

</template>