<script setup>
import Todo from './components/Todo.vue'
import Students from './components/Students.vue'
console.log(process.env.NODE_ENV)
console.log(import.meta.env.BASE_URL)
</script>

<template>
  <header>
    <!-- <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" /> -->
    <div id="nav">
      <router-link to="/">Home</router-link> | 
      <router-link to="/students">Students</router-link>
    </div>
    <div>
      <!-- <HelloWorld msg="You did it!" /> -->
      <!-- fuck you -->
      <!-- <router-link to="/students">About</router-link> -->
      <!-- <Todo /> -->
    </div>
    <!-- <Students /> -->
  </header>
  <router-view />

  <!-- <main> -->
    <!-- <TheWelcome /> -->
  <!-- </main> -->
</template>
<script>
// $(document).ready(function(){
//   $('#bruh').html("from jquery haha");
// });
</script>