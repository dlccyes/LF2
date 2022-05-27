<script>
import axios from 'axios';
import { drawLine } from '@/helper.js';
import { globeStore } from '@/stores/globe'

export default {
  data() {
    return {
      numStudent: '?',
      numAttendance: '?',
      attendanceGraphHtml: '',
      globe:  globeStore(),
    }
  },
  methods: {
    getAttendance() {
      var self = this; // can't access this in axios
      var url = "/overall-attendance";
      var objData = {
        'time_range': this.globe.timeRange
      };
      axios.post(url, objData)
      .then(function(result){
        console.log(result);
        self.numStudent = result.data.data.num_student;
        var overallAttendance = result.data.data.overall_attendance;
        var attendanceDataNum = overallAttendance.length;
        if(attendanceDataNum == 0){
          self.numAttendance = 0;
        }else{
          self.numAttendance = overallAttendance[attendanceDataNum-1]['student_id'].length;
        }
        if(attendanceDataNum < 2){
          self.attendanceGraphHtml = "Not enough data to show attendance vs. time graph.";
        }else{
          self.attendanceGraphHtml = "";
          var attandanceVsTimeArr = [];
          for(var item of overallAttendance){
            attandanceVsTimeArr.push([new Date(item['log_time']), item['student_id'].length]);
          }
          var yAx;
          drawLine(attandanceVsTimeArr, 'attendanceGraphDiv', 'log time', 'num of students', yAx=[0, self.numStudent, 1]);
        }
      })
      .catch(function(error){
        console.log(error);
      });
    },
  },
  mounted() {
    this.getAttendance();
  }
}
</script>

<template>

<div>Students</div>
<button class='btn' @click="getAttendance()">show attendance</button>
<div id="currentAttendanceDiv">
  <p>Current attendance: {{ numAttendance }}/{{ numStudent }} </p>
</div>
<div id="attendanceGraphDiv"> {{ attendanceGraphHtml }}</div>

</template>