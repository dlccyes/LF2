<script>
import axios from 'axios';

export default {
  data() {
    return {
      students: [],
    }
  },
  methods: {
    getStudents() {
      var self = this; // can't access this in axios
      // var url = "//flask-env.eba-ts5yjdi9.us-east-2.elasticbeanstalk.com/students";
      // var url = 'http://localhost:5000/students';
      // var url = "https://classroom-helper-lf2.herokuapp.com/students"
      var url = "/students"
      axios.post(url, {
        time_range: 30,
      })
      .then(function(result){
        console.log(result);
        self.students = result.data.data;
      })
      .catch(function(error){
        console.log(error);
        self.students = "error";
      });
    },
  }
}
</script>

<template>
  <div>Students</div>
  <button @click="getStudents()">show students</button>
  <div>
    <ul>
      <li v-for="student in students">
        {{ student['student_id'] }} {{ student['student_name'] }}
      </li>
    </ul>
  </div>

</template>