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
        self.students = result.data.data;
      })
      .catch(function(error){
        console.log(error);
        self.students = "error";
      });
    },
  },
  mounted() {
    this.getStudents();
  },
}
</script>

<template>
  <div>Students</div>
  <button class='btn' @click="getStudents()">show students</button>
  <div>
    <ul>
      <li v-for="student in students">
        <router-link :to="{name: 'student', params: {id: student.student_id}}"> {{ student.student_id }} {{ student.student_name }}</router-link>
      </li>
    </ul>
  </div>

</template>