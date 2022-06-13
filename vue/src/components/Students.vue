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
    getStudents() {
      var self = this; // can't access this in axios
      var objData = {
        'time_range': this.globe.timeRange
      };
      axios.post("/students", objData)
      .then(function(result){
        console.log(result);
        self.students = result.data.data.students;
        for(var i = 0; i < self.students.length; i++){
          var student = self.students[i];
          if(student['is_present']){
            self.students[i]['is_present'] = 'Present';
          }else{
            self.students[i]['is_present'] = 'Absent';
          }
        }
      })
      .catch(function(error){
        console.log(error);
        self.students = [];
      });
    },
    refresh(){
      this.getStudents();
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
  <ul>
    <li v-for="student in students">
      <router-link :to="{name: 'student', params: {id: student.student_id}}"> {{ student.student_id }}</router-link>: {{ student.is_present }}
    </li>
  </ul>
</div>

</template>