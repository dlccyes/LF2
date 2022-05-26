<script>
console.log(process.env.NODE_ENV)
console.log(import.meta.env.BASE_URL)
</script>

<template>
  <div id="nav">
    <router-link to="/">Home</router-link> | 
    <router-link to="/students">Students</router-link>
  </div>
  <router-view/>
</template>