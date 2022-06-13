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
      attendanceCountHtml: '',
      maskGraphDivHtml: '',
      globe:  globeStore(),
      studentId: this.$route.params.id,
      studentName: '',
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
        var isMasked;
        if(attendanceDataNum == 0){
          isPresent = 0;
        }else{
          isPresent = studentAttendance[attendanceDataNum-1][1];
          isMasked = studentAttendance[attendanceDataNum-1][2];
        }
        self.studentAttendanceHtml = '';
        var attendanceCount = 0;
        if(isPresent){
          self.studentAttendanceHtml += 'Present';
          attendanceCount = 1;
          if(isMasked){
            self.studentAttendanceHtml += ' (masked)';
          }else{
            self.studentAttendanceHtml += ' (unmasked)';
          }
        }
        else{
          self.studentAttendanceHtml += 'Absent';
          attendanceCount = 0;
        }
        if(attendanceDataNum < 2){
          self.attendanceGraphDivHtml = 'Not enough data to show graph.';
        }else{
          self.attendanceGraphDivHtml = '';
          self.maskGraphDivHtml = '';
          attendanceCount = 0;
          var attandanceVsTimeArr = [];
          var maskVsTimeArr = [];
          for(var item of studentAttendance){
            attandanceVsTimeArr.push([new Date(item[0]), item[1]]);
            console.log(attandanceVsTimeArr)
            maskVsTimeArr.push([new Date(item[0]), item[2]]);
            console.log(maskVsTimeArr)
            attendanceCount += item[1];
          }
          attandanceVsTimeArr.sort();
          var yAx = [0, 1, 1];
          drawLine(attandanceVsTimeArr, 'attendanceGraphDiv', 'log time', 'Is present?', yAx);
          drawLine(maskVsTimeArr, 'maskGraphDiv', 'log time', 'Is masked?', yAx);
        }
        self.attendanceCountHtml = "Attendance count: " + attendanceCount + " / " + attendanceDataNum;
      });
    },
    getStudentName(){
      var self = this; // can't access this in axios
      var url = "/student-name";
      var objData = {
        'student_id': this.studentId
      };
      axios.post(url, objData)
      .then(function(result){
        console.log(result);
        self.studentName = result.data.data.student_name;
      });
    },
    refresh() {
      this.getStudentAttendance();
    },
  },
  mounted() {
    this.getStudentName();
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

<h1>{{ studentId }} {{ studentName }}</h1>
<TimeSlider />
<div id="studentAttendance">{{ studentAttendanceHtml }}</div>
<div id="attendanceCountDiv">{{ attendanceCountHtml }}</div>
<div id="attendanceGraphDiv">{{ attendanceGraphDivHtml }}</div>
<div id="maskGraphDiv">{{ maskGraphDivHtml }}</div>

</template>