<script>
export default {
  computed: {
    isHome(){
      return this.$route.name == 'home';
    }
  }
}
</script>
<template>
  <div id="nav">
    <router-link v-if="!isHome" to="/">Dashboard</router-link>
  </div>
  <router-view/>
</template>